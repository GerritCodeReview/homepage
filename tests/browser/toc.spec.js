const { test, expect, expectHeadingVisible } = require("./support");
const article = "/fixtures/nested/page.html";

test("TOC contains only article headings in document order and nesting", async ({
  page,
}) => {
  await page.goto(article);
  const links = page.locator("#toc a");
  await expect(links).toHaveText([
    "First section",
    "Nested section",
    "Detail section",
    "Final section",
  ]);
  await expect(page.locator("#toc > ul > li > a")).toHaveText([
    "First section",
    "Final section",
  ]);
  await expect(page.locator("#toc > ul > li > ul > li > a")).toHaveText([
    "Nested section",
  ]);
  await expect(
    page.locator("#toc > ul > li > ul > li > ul > li > a"),
  ).toHaveText(["Detail section"]);
  for (const href of await links.evaluateAll((items) =>
    items.map((a) => a.getAttribute("href")),
  )) {
    await expect(page.locator(href)).toHaveCount(1);
  }
});

for (const width of [1440, 769, 768, 375]) {
  for (const input of ["mouse", "keyboard"]) {
    test(`TOC ${input} navigation keeps target below header at ${width}px`, async ({
      page,
    }) => {
      await page.setViewportSize({ width, height: 900 });
      await page.goto("/fixtures/long.html");
      const link = page.locator("#toc a").filter({ hasText: /^Section 12 / });
      if (input === "mouse") await link.click();
      else {
        await link.focus();
        await page.keyboard.press("Enter");
      }
      await expectHeadingVisible(
        page,
        "#section-12-long-heading-for-the-navigation-regression-fixture",
      );
    });
  }
  test(`direct fragment and heading-anchor navigation at ${width}px`, async ({
    page,
  }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto(
      "/fixtures/long.html#section-12-long-heading-for-the-navigation-regression-fixture",
    );
    const heading =
      "#section-12-long-heading-for-the-navigation-regression-fixture";
    await expectHeadingVisible(page, heading);
    const anchor = page.locator(`${heading} .heading-anchor`);
    await expect(anchor).toHaveCount(1);
    await expect(anchor).toHaveAttribute(
      "aria-label",
      "Link to section: Section 12 Long heading for the navigation regression fixture",
    );
    await expect(anchor).toHaveAttribute("href", heading);
    // Activate from elsewhere without focus itself scrolling to the target.
    await page.evaluate(() => {
      history.replaceState(null, "", location.pathname);
      window.scrollTo({ top: 0, behavior: "instant" });
    });
    await anchor.evaluate((a) => a.focus({ preventScroll: true }));
    await expect(anchor).toBeFocused();
    await expect
      .poll(() => anchor.evaluate((a) => Number(getComputedStyle(a).opacity)))
      .toBe(1);
    await page.keyboard.press("Enter");
    await expect(page).toHaveURL(
      /#section-12-long-heading-for-the-navigation-regression-fixture$/,
    );
    await expectHeadingVisible(page, heading);
  });
  test(`long TOC and wide content remain reachable without page overflow at ${width}px`, async ({
    page,
  }) => {
    await page.setViewportSize({ width, height: 600 });
    await page.goto("/fixtures/long.html");
    await expect
      .poll(() =>
        page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
      )
      .toBe(true);
    for (const selector of [".post-content table", ".post-content pre"]) {
      const scroller = page.locator(selector);
      await expect
        .poll(() =>
          scroller.evaluate((element) => {
            element.scrollLeft = element.scrollWidth;
            return (
              element.scrollLeft > 0 &&
              getComputedStyle(element).overflowX === "auto"
            );
          }),
        )
        .toBe(true);
    }
    const last = page.locator("#toc a").last();
    await last.scrollIntoViewIfNeeded();
    await last.click();
    await expectHeadingVisible(
      page,
      "#section-18-long-heading-for-the-navigation-regression-fixture",
    );
  });
}

for (const url of ["/fixtures/excluded.html", "/fixtures/no-headings.html"]) {
  test(`optional TOC stays absent or hidden on ${url}`, async ({ page }) => {
    await page.goto(url);
    await expect(page.locator("#toc")).toBeHidden();
    await expect(page.locator(".post-content")).toBeVisible();
  });
}

test("repeated anchor initialization does not duplicate links", async ({
  page,
}) => {
  await page.goto(article);
  await page.evaluate(() =>
    document.dispatchEvent(new Event("DOMContentLoaded")),
  );
  await expect(page.locator(".post-content .heading-anchor")).toHaveCount(4);
});

test("TOC scopes headings to the article and preserves literal label text", async ({
  page,
}) => {
  await page.goto("/fixtures/special.html");
  await expect(page.locator("#toc a")).toHaveText([
    "Text <literal> and “quotes”",
  ]);
});

test("TOC links follow keyboard order with visible focus", async ({ page }) => {
  await page.goto(article);
  await page.locator("#toc a").first().focus();
  await page.keyboard.press("Tab");
  const next = page.locator("#toc a").nth(1);
  await expect(next).toBeFocused();
  await expect
    .poll(() =>
      next.evaluate((link) => {
        const style = getComputedStyle(link);
        return style.outlineStyle !== "none" || style.boxShadow !== "none";
      }),
    )
    .toBe(true);
});
