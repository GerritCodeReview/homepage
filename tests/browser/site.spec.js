const { test, expect, root, fs } = require("./support");
const path = require("node:path");

test("search results preserve nested URLs and navigate to the article", async ({
  page,
  baseURL,
}) => {
  const searchURL = new URL("/search.json", baseURL).href;
  await page.route(searchURL, (route) =>
    route.fulfill({
      body: fs.readFileSync(path.join(root, "_test/site/search.json"), "utf8"),
      contentType: "application/json",
    }),
  );
  const loaded = page.waitForResponse(
    (response) => response.url() === searchURL,
  );
  await page.goto("/");
  const response = await loaded;
  await response.finished();
  expect(response.url()).toBe(searchURL);
  await page.locator("#search-input").pressSequentially("Quoted");
  const result = page
    .locator("#results-container a")
    .filter({ hasText: "Quoted" });
  await expect(result).toHaveAttribute("href", "/fixtures/nested/page.html");
  await result.click();
  await expect(page).toHaveURL(/\/fixtures\/nested\/page\.html$/);
  await expect(page.locator(".post-title-main")).toHaveText(
    'Quoted "title" and backslash \\',
  );
});

test("desktop dropdown navigation reaches a published page", async ({
  page,
}) => {
  await page.goto("/");
  await page.locator(".dropdown-toggle").filter({ hasText: "Code" }).hover();
  await page
    .locator(".dropdown-menu a")
    .filter({ hasText: /^Releases$/ })
    .click();
  await expect(page).toHaveURL(/\/releases-readme\.html$/);
  await expect(page.locator(".post-title-main")).toHaveText(
    "Gerrit Code Review Releases",
  );
});

for (const width of [768, 375]) {
  test(`documentation dropdown links stay within the viewport at ${width}px`, async ({
    page,
  }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto("/fixtures/nested/page.html");
    for (const title of ["Community", "Docs", "Code"]) {
      const dropdown = page
        .locator(".dropdown")
        .filter({ has: page.locator(".dropdown-toggle", { hasText: title }) });
      await dropdown.locator(".dropdown-toggle").hover();
      await expect(dropdown.locator(".dropdown-menu")).toBeVisible();
      await expect
        .poll(async () => {
          const box = await dropdown.locator(".dropdown-menu").boundingBox();
          return box.x >= 0 && box.x + box.width <= width;
        })
        .toBe(true);
    }
    await page
      .locator(".dropdown-menu a")
      .filter({ hasText: /^Releases$/ })
      .click();
    await expect(page).toHaveURL(/\/releases-readme\.html$/);
  });
}
