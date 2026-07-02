/**
 * TASK-384 geometry verification.
 * Measures pre-table height and visible product rows at 390px on magnesium.
 * Also spot-checks protein-bars + hard-cheeses for no-regression.
 *
 * Product rows use className "bari-cmp-row" (comparison-row.tsx:162).
 * "Visible" = any part of the row overlaps the 844px viewport (top < 844 AND bottom > 0).
 */
import { test, expect } from "@playwright/test";

const BASE = "http://localhost:3000";

test("magnesium — mobile 390px: pre-table height ≤480px and ≥3 product rows partially visible at first paint", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`${BASE}/hashvaot/magnesium`, { waitUntil: "networkidle" });

  const geometry = await page.evaluate(() => {
    const rows = Array.from(document.querySelectorAll(".bari-cmp-row"));
    return rows.map((el, i) => {
      const rect = el.getBoundingClientRect();
      return { index: i, top: rect.top, bottom: rect.bottom, height: rect.height };
    });
  });

  console.log(`Total .bari-cmp-row elements: ${geometry.length}`);
  expect(geometry.length, "Should have product rows").toBeGreaterThan(0);

  const tableTopY = geometry[0]?.top ?? 9999;
  console.log(`Pre-table height (first row top): ${tableTopY.toFixed(1)}px`);

  // A row is "visible" if any portion overlaps the viewport (top < 844 AND bottom > 0)
  const viewportH = 844;
  const visibleRows = geometry.filter((r) => r.top < viewportH && r.bottom > 0);
  console.log(`Rows partially visible at 0px scroll: ${visibleRows.length}`);
  console.log(`First 6 rows:`, geometry.slice(0, 6).map(
    r => `top=${r.top.toFixed(0)} bottom=${r.bottom.toFixed(0)} h=${r.height.toFixed(0)}`
  ).join(" | "));

  expect(tableTopY, `Pre-table height must be ≤480px; got ${tableTopY.toFixed(0)}px`).toBeLessThanOrEqual(480);
  expect(visibleRows.length, `At least 3 product rows must be (partially) visible at 0px scroll`).toBeGreaterThanOrEqual(3);
});

test("magnesium — desktop 1280px: full content visible, no 'קרא עוד' button visible", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto(`${BASE}/hashvaot/magnesium`, { waitUntil: "networkidle" });

  const expandBtns = page.locator('button:has-text("קרא עוד")');
  const count = await expandBtns.count();
  console.log(`Desktop: total "קרא עוד" buttons in DOM: ${count}`);
  for (let i = 0; i < count; i++) {
    const visible = await expandBtns.nth(i).isVisible();
    console.log(`  button[${i}] visible=${visible}`);
    expect(visible, `"קרא עוד" button ${i} must be hidden at desktop (md:hidden)`).toBe(false);
  }

  const rows = page.locator(".bari-cmp-row");
  const total = await rows.count();
  console.log(`Desktop: .bari-cmp-row count=${total}`);
  expect(total).toBeGreaterThan(0);
});

test("protein-bars — mobile 390px: no regression (no expand buttons, rows render)", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`${BASE}/hashvaot/protein-bars`, { waitUntil: "networkidle" });

  await expect(page.locator("h1")).toBeVisible();

  const expandBtns = page.locator('button:has-text("קרא עוד")');
  const count = await expandBtns.count();
  console.log(`protein-bars mobile: "קרא עוד" button count=${count}`);
  expect(count, "protein-bars must have 0 expand buttons").toBe(0);

  const rows = page.locator(".bari-cmp-row");
  const total = await rows.count();
  console.log(`protein-bars mobile: .bari-cmp-row count=${total}`);
  expect(total).toBeGreaterThan(0);
});

test("hard-cheeses — desktop 1280px: no regression (no expand buttons, rows render)", async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto(`${BASE}/hashvaot/hard-cheeses`, { waitUntil: "networkidle" });

  await expect(page.locator("h1")).toBeVisible();

  const expandBtns = page.locator('button:has-text("קרא עוד")');
  const count = await expandBtns.count();
  console.log(`hard-cheeses desktop: "קרא עוד" button count=${count}`);
  expect(count, "hard-cheeses desktop must have 0 expand buttons").toBe(0);

  const rows = page.locator(".bari-cmp-row");
  const total = await rows.count();
  console.log(`hard-cheeses desktop: .bari-cmp-row count=${total}`);
  expect(total).toBeGreaterThan(0);
});
