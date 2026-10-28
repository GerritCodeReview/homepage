const { test: base, expect } = require("@playwright/test");
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "../..");

// Mirror the production CDN versions with lockfile-pinned local packages.
// Application scripts, templates and CSS are not mocked.
const assets = {
  "https://code.jquery.com/jquery-3.3.1.slim.min.js":
    "jquery/dist/jquery.slim.min.js",
  "https://cdn.jsdelivr.net/npm/popper.js@1.14.3/dist/umd/popper.min.js":
    "popper.js/dist/umd/popper.min.js",
  "https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js":
    "bootstrap/dist/js/bootstrap.min.js",
  "https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css":
    "bootstrap/dist/css/bootstrap.min.css",
  "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css":
    "@fortawesome/fontawesome-free/css/all.min.css",
};
const test = base.extend({
  page: async ({ page, baseURL }, use) => {
    const origin = new URL(baseURL).origin;
    const errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.route("**/*", async (route) => {
      const url = new URL(route.request().url());
      if (url.origin === origin) return route.continue();
      const asset = assets[url.href];
      if (asset)
        return route.fulfill({
          path: path.join(root, "node_modules", asset),
          contentType: asset.endsWith(".css") ? "text/css" : "text/javascript",
        });
      if (
        url.hostname === "cdnjs.cloudflare.com" &&
        url.pathname.includes("/webfonts/")
      ) {
        return route.fulfill({
          path: path.join(
            root,
            "node_modules/@fortawesome/fontawesome-free/webfonts",
            path.basename(url.pathname),
          ),
          contentType: "font/woff2",
        });
      }
      // Fonts and analytics do not influence the navigation contract. Use stable
      // system fonts and prevent analytics traffic, including on the homepage.
      if (url.hostname === "fonts.googleapis.com")
        return route.fulfill({ body: "", contentType: "text/css" });
      if (url.hostname === "www.googletagmanager.com")
        return route.fulfill({ body: "", contentType: "text/javascript" });
      errors.push(`Unexpected external request: ${url.href}`);
      return route.abort();
    });
    await use(page);
    expect(
      errors,
      "No runtime errors or unhandled external dependencies",
    ).toEqual([]);
  },
});

async function expectHeadingVisible(page, selector) {
  // Do not accept a transient position halfway through smooth scrolling.
  await page.evaluate(
    () =>
      new Promise((resolve) => {
        let previous = -1;
        let stable = 0;
        function sample() {
          stable = window.scrollY === previous ? stable + 1 : 0;
          previous = window.scrollY;
          if (stable >= 6) resolve();
          else requestAnimationFrame(sample);
        }
        requestAnimationFrame(sample);
      }),
  );
  await expect
    .poll(
      async () => {
        const heading = await page.locator(selector).boundingBox();
        const header = await page.locator(".site-header").boundingBox();
        return (
          heading.y >= Math.max(0, header.y + header.height) - 1 &&
          heading.y + heading.height <= page.viewportSize().height
        );
      },
      { message: "Target heading must be visible below the fixed header" },
    )
    .toBe(true);
}

module.exports = { test, expect, expectHeadingVisible, root, fs };
