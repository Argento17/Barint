import { defineConfig, devices } from "@playwright/test";

/**
 * Bari E2E + accessibility harness.
 *
 * The project's one measurable user metric is "a first-time mobile user understands the
 * shelf in 15-20 seconds" — so the default project is mobile (Pixel 5 viewport), and the
 * suite leans on real comparison routes under /hashvaot.
 *
 * Runs against a local dev server it starts itself (reused if one is already up). No CI
 * assumptions baked in; set PLAYWRIGHT_BASE_URL to point at a deployed preview instead.
 */
const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? "http://localhost:3000";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  expect: { timeout: 10_000 },
  fullyParallel: true,
  reporter: process.env.CI ? "github" : "list",
  snapshotDir: "./e2e/snapshots",
  use: {
    baseURL,
    trace: "on-first-retry",
    locale: "he-IL",
  },
  projects: [
    { name: "mobile", use: { ...devices["Pixel 5"] } },
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
  ],
  // Only manage a server when pointing at localhost; skip when a base URL is supplied.
  webServer: process.env.PLAYWRIGHT_BASE_URL
    ? undefined
    : {
        command: "npm run dev",
        url: baseURL,
        timeout: 120_000,
        reuseExistingServer: !process.env.CI,
      },
});
