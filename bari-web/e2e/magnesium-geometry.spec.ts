/**
 * TASK-384A mobile geometry verification for /hashvaot/magnesium
 * Viewport: 390px width × 812px height (iPhone 12 Pro)
 *
 * Measures:
 * 1. Pixels from top of viewport to first product row (via .bari-cmp-row)
 * 2. How many product rows START above the fold (812px height)
 * 3. That safety box secondary content is collapsed by default on mobile
 * 4. That badge grid is NOT visible in collapsed state (expansion-only)
 */

import { test, expect } from "@playwright/test";
import * as fs from "fs";

test("magnesium page mobile geometry @390px", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 812 });
  await page.goto("http://localhost:3000/hashvaot/magnesium", {
    waitUntil: "networkidle",
  });

  // Ensure screenshots dir exists
  fs.mkdirSync("e2e/screenshots", { recursive: true });

  // Take a screenshot of above-the-fold area
  await page.screenshot({
    path: "e2e/screenshots/magnesium-mobile-390.png",
    fullPage: false,
    clip: { x: 0, y: 0, width: 390, height: 812 },
  });

  // ── 1. First product row top position ────────────────────────────────────
  // Use .bari-cmp-row class — the canonical row element in the comparison table.
  // Each product renders as one article.bari-cmp-row.
  const rows = await page.locator(".bari-cmp-row").all();
  let firstRowTop = -1;
  const rowTops: number[] = [];

  for (const row of rows) {
    const box = await row.boundingBox();
    if (box) {
      rowTops.push(Math.round(box.y));
      if (firstRowTop === -1 || box.y < firstRowTop) {
        firstRowTop = Math.round(box.y);
      }
    }
  }

  const rowsAboveFold = rowTops.filter((y) => y < 812).length;

  console.log(`[GEOMETRY] First product row top: ${firstRowTop}px`);
  console.log(`[GEOMETRY] Rows starting above fold (812px): ${rowsAboveFold}`);
  console.log(`[GEOMETRY] All row tops (first 6): ${rowTops.slice(0, 6).join(", ")}`);

  // ── 2. Safety box secondary content collapsed on mobile ──────────────────
  // The safety banner uses "פרטי בטיחות נוספים ▼" as the collapsed toggle text.
  const safetyBoxExpandBtn = page.locator('button[aria-expanded="false"]').filter({
    hasText: /פרטי בטיחות נוספים/,
  }).first();
  const safetyBoxBtnVisible = await safetyBoxExpandBtn.isVisible();
  console.log(`[SAFETY] Safety expand button visible: ${safetyBoxBtnVisible}`);

  // Drug interaction section should NOT be visible (hidden behind expand)
  const drugInteractionHeader = page.locator('text=אינטרקציות עם תרופות').first();
  const drugInteractionVisible = await drugInteractionHeader.isVisible();
  console.log(`[SAFETY] Drug interaction section visible before expand: ${drugInteractionVisible}`);

  // ── 3. Badge grid NOT visible in collapsed row ───────────────────────────
  // Badge grid title "מגנזיום יסודי למנה יומית" should NOT be visible before any expansion
  const badgeTitleEl = page.locator('text=מגנזיום יסודי למנה יומית').first();
  const badgeTitleVisible = await badgeTitleEl.isVisible();
  console.log(`[BADGES] Badge grid title visible before expansion: ${badgeTitleVisible}`);

  // ── Assertions ────────────────────────────────────────────────────────────
  // First row should appear (any positive value means we found it)
  expect(firstRowTop, "Should find at least one .bari-cmp-row on the page").toBeGreaterThan(0);

  // Safety box collapse behavior
  expect(safetyBoxBtnVisible, "Safety box expand button should be visible on mobile").toBe(true);
  expect(drugInteractionVisible, "Drug interaction section should be collapsed by default").toBe(false);
  expect(badgeTitleVisible, "Badge grid should not be visible in collapsed row").toBe(false);

  // Log geometry summary for the return contract
  console.log(`[SUMMARY] pixels-to-first-row: ${firstRowTop}px | rows-above-fold: ${rowsAboveFold} | screenshot: e2e/screenshots/magnesium-mobile-390.png`);
});
