const { defineConfig } = require("@playwright/test");
const port = Number(process.env.TEST_PORT || 4173);
module.exports = defineConfig({
  testDir: "./tests/browser",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: [
    ["list"],
    ["junit", { outputFile: "test-results/browser.xml" }],
    ["html", { open: "never" }],
  ],
  use: {
    baseURL: `http://127.0.0.1:${port}`,
    browserName: "chromium",
    viewport: { width: 1440, height: 900 },
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "node tests/browser/server.js",
    url: `http://127.0.0.1:${port}`,
    reuseExistingServer: false,
    timeout: 10000,
  },
});
