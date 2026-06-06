import { test, expect } from "@playwright/test";

/**
 * Smoke E2E — the comparison pages render and carry their structural invariants.
 *
 * This is a real route check, not a unit test: it boots the app and asserts the things a
 * first-time mobile user depends on — the document is RTL Hebrew, the page has a heading,
 * and the canonical reference page (maadanim) actually paints product rows. If a data or
 * routing regression blanks a comparison page, this fails before a human notices.
 */

const COMPARISON_ROUTES = [
  "/hashvaot/maadanim", // canonical reference page
  "/hashvaot/hummus",
  "/hashvaot/cheese",
];

test("home page loads and is RTL Hebrew", async ({ page }) => {
  const resp = await page.goto("/");
  expect(resp?.ok()).toBeTruthy();
  await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
  await expect(page.locator("html")).toHaveAttribute("lang", /he/);
});

for (const route of COMPARISON_ROUTES) {
  test(`comparison page renders: ${route}`, async ({ page }) => {
    const resp = await page.goto(route);
    expect(resp?.ok()).toBeTruthy();

    // a visible heading exists
    await expect(page.locator("h1, h2").first()).toBeVisible();

    // the page is not an error/blank shell — it has substantive Hebrew text
    const bodyText = (await page.locator("body").innerText()).trim();
    expect(bodyText.length).toBeGreaterThan(200);
    expect(bodyText).toMatch(/[֐-׿]/); // contains Hebrew

    // no Next error overlay
    await expect(page.locator("text=Application error")).toHaveCount(0);
  });
}

test("maadanim page paints multiple product rows", async ({ page }) => {
  await page.goto("/hashvaot/maadanim");
  // grade chips (A-E) are the per-product anchor; expect several on a populated shelf.
  const gradeChips = page.getByText(/^[A-E]$/);
  await expect(gradeChips.first()).toBeVisible({ timeout: 15_000 });
  expect(await gradeChips.count()).toBeGreaterThan(2);
});
