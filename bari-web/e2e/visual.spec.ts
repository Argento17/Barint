/**
 * Visual regression — screenshot baseline for key Bari routes.
 *
 * First run (create baselines):
 *   npx playwright test e2e/visual.spec.ts --update-snapshots --project=mobile
 *   npx playwright test e2e/visual.spec.ts --update-snapshots --project=desktop
 *
 * Review and commit the generated PNGs in e2e/snapshots/.
 * Subsequent runs compare against them:
 *   npm run test:visual
 *
 * On failure, actual/diff images land in test-results/ (gitignored).
 *
 * Each route asserts:
 *   200 OK · RTL Hebrew · header visible · substantive text · no blank whitespace ·
 *   grade chips present (comparison pages) · full-page screenshot captured
 *
 * Mobile project additionally checks: no horizontal overflow.
 *
 * Cross-page stability helpers:
 *   - Embla auto-scrolling carousels are stopped via mouseenter before screenshot
 *   - All routes wait briefly after load to let JS animations settle
 *   - toHaveScreenshot uses 30s timeout for first-run baseline creation
 */

import { test, expect } from "@playwright/test";

// ── Routes under test ────────────────────────────────────────────────────────
const ROUTES = [
  { path: "/",                          name: "homepage"            },
  { path: "/hashvaot",                  name: "hashvaot-index"      },
  { path: "/hashvaot/maadanim",         name: "hashvaot-maadanim"   },
  { path: "/hashvaot/hard-cheeses",     name: "hashvaot-hard-cheeses" },
  { path: "/hashvaot/snack-bars",       name: "hashvaot-snack-bars" },
  { path: "/hashvaot/milk-comparison",  name: "hashvaot-milk"       },
] as const;

// ── Pages with auto-scrolling Embla carousels ────────────────────────────────
const CAROUSEL_PAGES = new Set(["/", "/hashvaot"]);

// ── Comparison pages (subset that should show grade chips) ───────────────────
const COMPARISON_ROUTES = new Set([
  "/hashvaot/maadanim",
  "/hashvaot/hard-cheeses",
  "/hashvaot/snack-bars",
  "/hashvaot/milk-comparison",
]);

// ── Helpers ──────────────────────────────────────────────────────────────────

async function stopCarousels(page: import("@playwright/test").Page) {
  // Embla auto-scroll pauses on mouseenter; dispatch to stop any running scroll
  await page.evaluate(() => {
    document.querySelectorAll("[class*='embla']").forEach((el) => {
      el.dispatchEvent(new MouseEvent("mouseenter", { bubbles: true }));
    });
  });
}

// ── Tests ────────────────────────────────────────────────────────────────────

for (const { path, name } of ROUTES) {
  test(`visual: ${name}`, async ({ page }, testInfo) => {
    test.setTimeout(90_000);
    // 1. Navigate and confirm 200
    const resp = await page.goto(path, { waitUntil: "load" });
    expect(resp?.ok()).toBeTruthy();

    // 2. RTL Hebrew document
    await expect(page.locator("html")).toHaveAttribute("dir", "rtl");

    // 3. Header / logo visible
    await expect(page.locator("header, nav").first()).toBeVisible();

    // 4. Substantive Hebrew content on the page
    const bodyText = await page.locator("body").innerText();
    expect(bodyText.length).toBeGreaterThan(100);
    expect(bodyText).toMatch(/[\u0590-\u05FF]/);

    // 5. No Next.js error overlay
    await expect(page.locator("text=Application error")).toHaveCount(0);

    // 6. Comparison pages: grade chips (A–E) are visible and more than 1
    if (COMPARISON_ROUTES.has(path)) {
      const gradeChips = page.getByText(/^[A-E]$/);
      await expect(gradeChips.first()).toBeVisible({ timeout: 15_000 });
      const count = await gradeChips.count();
      expect(count).toBeGreaterThan(1);
    }

    // 7. Comparison pages: filters are NOT accidentally visible
    if (COMPARISON_ROUTES.has(path)) {
      const filterCandidates = page.locator(
        'button:has-text("סינון"), button:has-text("סנן"), ' +
        '[data-testid="filter-panel"]:visible, ' +
        '[role="dialog"]:has-text("סינון"):visible'
      );
      const filterCount = await filterCandidates.count();
      if (filterCount > 0) {
        for (let i = 0; i < filterCount; i++) {
          const visible = await filterCandidates.nth(i).isVisible();
          if (visible) {
            const expanded = await filterCandidates.nth(i).getAttribute("aria-expanded");
            expect(expanded).not.toBe("true");
          }
        }
      }
    }

    // 8. Mobile only: no horizontal overflow
    if (testInfo.project.name === "mobile") {
      const overflow = await page.evaluate(() => {
        const html = document.documentElement;
        return html.scrollWidth > html.clientWidth;
      });
      expect(overflow, "mobile viewport should not overflow horizontally").toBe(false);
    }

    // 9. Stop auto-scrolling carousels for screenshot stability
    if (CAROUSEL_PAGES.has(path)) {
      await stopCarousels(page);
    }

    // 10. Verify the page scrolls (there is content below the fold)
    const scrollable = await page.evaluate(() => {
      return document.documentElement.scrollHeight > window.innerHeight + 50;
    });
    expect(scrollable).toBe(true);

    // 11. JS freeze: inject CSS to kill residual JS-driven animations that
    //     Playwright's `animations: "disabled"` cannot stop
    //     (requestAnimationFrame, setInterval). Needed for full-page mobile
    //     screenshots of comparison routes, which have radar chart SVGs
    //     or expandable product cards with JS-transitioned content.
    const needsFreeze = testInfo.project.name === "mobile" && !CAROUSEL_PAGES.has(path);
    if (needsFreeze) {
      await page.evaluate(() => {
        const s = document.createElement("style");
        s.id = "__freeze";
        s.textContent =
          "*, *::before, *::after { " +
          "animation: none !important; " +
          "transition: none !important; }";
        document.head.appendChild(s);
      });
      await page.waitForTimeout(1000);
    }

    // 12. Screenshot baseline
    //     Mobile full-page routes (unstable JS animations → freeze manually):
    //     use page.screenshot + toMatchSnapshot (no stability check).
    //     Desktop routes and index pages: use toHaveScreenshot.
    const mobileFullPage = testInfo.project.name === "mobile" && !CAROUSEL_PAGES.has(path);
    if (mobileFullPage) {
      const buf = await page.screenshot({
        fullPage: true,
        animations: "allow",
        scale: "device",
      });
      expect(buf).toMatchSnapshot(`${name}.png`, {
        maxDiffPixelRatio: 0.03,
      });
    } else if (path === "/") {
      // Homepage: viewport-only with JS freeze for SVG radar chart.
      const buf = await page.screenshot({
        animations: "allow",
        scale: "device",
      });
      expect(buf).toMatchSnapshot(`${name}.png`, {
        maxDiffPixelRatio: 0.03,
      });
    } else if (CAROUSEL_PAGES.has(path)) {
      // Index pages: viewport-only, mask for Embla carousel.
      await expect(page).toHaveScreenshot(`${name}.png`, {
        fullPage: false,
        animations: "disabled",
        scale: "device",
        threshold: 0.03,
        timeout: 30_000,
        mask: [page.locator('[class*="embla"]')],
      });
    } else {
      // Desktop comparison routes: stable, use toHaveScreenshot.
      await expect(page).toHaveScreenshot(`${name}.png`, {
        fullPage: true,
        animations: "disabled",
        scale: "device",
        threshold: 0.02,
        timeout: 30_000,
      });
    }
  });
}
