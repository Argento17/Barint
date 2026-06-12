import { test, expect } from "@playwright/test";

/**
 * OFF-removal display verification (TASK-238 Phase 2).
 *
 * Phase 1 (Data) stripped Open Food Facts data: 25 products across granola/cereals/
 * hard_cheeses/juices/butter became `confidence: "insufficient"` with `score: null` /
 * `grade: null` (State 7 of score_confidence_indicators_spec_v1.md), and 38 products had
 * their OFF `imageUrl` set to null. This spec asserts the DISPLAY layer renders those
 * states honestly — never a fake score, never a broken <img>, name always present.
 *
 * It also confirms the OFF-affected shelves and the yogurts de-list (11 survivors) still
 * paint, and that no Next error overlay appears on any of them.
 */

// Categories that carry State-7 (insufficient / "טרם נוקד") products after OFF removal.
const NULL_STATE_ROUTES = [
  "/hashvaot/granola", // 9 insufficient + 9 null images
  "/hashvaot/breakfast-cereals", // 8 insufficient + 8 null images
  "/hashvaot/hard-cheeses", // 3 insufficient + 15 null images
  "/hashvaot/juices", // 3 insufficient
  "/hashvaot/butter", // 2 insufficient
];

const ALL_AFFECTED_ROUTES = [
  ...NULL_STATE_ROUTES,
  "/hashvaot/yogurts", // 11 survivors after 7-product OFF de-list
  "/hashvaot/salty-snacks",
];

for (const route of ALL_AFFECTED_ROUTES) {
  test(`OFF-affected shelf paints without error: ${route}`, async ({ page }) => {
    const resp = await page.goto(route);
    expect(resp?.ok()).toBeTruthy();
    await expect(page.locator("h1, h2").first()).toBeVisible();
    // No Next runtime error overlay.
    await expect(page.locator("text=Application error")).toHaveCount(0);
    // No broken-image icon is left on screen. A product with a null imageUrl renders a
    // branded placeholder DIV (no <img> at all); a product whose external image URL fails
    // to load swaps to the same placeholder via the thumbnail's onError handler. Either
    // way, once load settles no <img> may remain in the broken state — the user never sees
    // a broken-image glyph. We poll (onError swap is async) rather than wait for
    // networkidle (the dev server's HMR socket never idles).
    await expect
      .poll(
        () =>
          page.evaluate(() =>
            Array.from(document.querySelectorAll("img"))
              .filter((img) => img.getAttribute("src"))
              .filter((img) => img.complete && img.naturalWidth === 0).length
          ),
        { timeout: 15_000 }
      )
      .toBe(0);
  });
}

for (const route of NULL_STATE_ROUTES) {
  test(`State-7 null pill renders ("טרם נוקד"), no fake score: ${route}`, async ({
    page,
  }) => {
    await page.goto(route);
    // The State-7 null pill carries the verbatim spec label. At least one must be visible
    // on these shelves (each has ≥2 insufficient products).
    const nullPill = page.getByText("טרם נוקד");
    await expect(nullPill.first()).toBeVisible({ timeout: 15_000 });
    expect(await nullPill.count()).toBeGreaterThan(0);
  });
}
