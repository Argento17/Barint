// TASK-082 — Capture Hummus explanation-layer preview screenshots.
// Usage: BASE_URL=http://localhost:3000 VARIANT=insight node scripts/capture-hummus-explanation-preview.mjs
//   VARIANT controls the output filename prefix ("insight" for v2, "fallback" for v1).
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const base = process.env.BASE_URL ?? "http://localhost:3000";
const variant = process.env.VARIANT ?? "insight";
const url = `${base}/hashvaot/hummus`;
const outDir = "screenshots/explanation_preview";
mkdirSync(outDir, { recursive: true });

const EXPAND_LABEL = "למה קיבל את הציון?";

// Products to expand, keyed by visible name. Picked one per grade + matbucha.
const EXPAND_TARGETS = {
  a_grade: "הקיסר חומוס ענק",
  b_grade: "חומוס מסעדות",
  c_grade: "מלך החומוס סמיר הגדול",
  matbucha: "סלט מטבוחה",
};

const browser = await chromium.launch({ headless: true });

async function settle(page) {
  await page.waitForSelector(`text=${EXPAND_LABEL}`, { timeout: 30000 });
  await page.waitForTimeout(700);
}

// Expand a single product row (desktop) and screenshot just that article.
async function captureExpanded(page, key, name) {
  // Collapse any previously expanded row first by reloading for a clean state.
  await page.goto(url, { waitUntil: "networkidle" });
  await settle(page);
  // Scope to the visible desktop grid; the mobile shelf renders the same
  // article markup but is display:none at >=lg widths.
  const article = page.locator("#comparison-grid article", { hasText: name }).first();
  await article.scrollIntoViewIfNeeded();
  const btn = article.getByRole("button", { name: EXPAND_LABEL });
  await btn.click();
  await page.waitForTimeout(600); // expansion animation
  await article.scrollIntoViewIfNeeded();
  await page.waitForTimeout(300);
  const path = `${outDir}/${variant}_${key}_expanded.png`;
  await article.screenshot({ path });
  console.log("saved", path);
}

// ---- Desktop ----
const desktop = await browser.newPage({ viewport: { width: 1280, height: 1600 } });
await desktop.goto(url, { waitUntil: "networkidle" });
await settle(desktop);

// Top 10 products: screenshot the comparison grid region (first rows).
const grid = desktop.locator("#comparison-grid");
await grid.scrollIntoViewIfNeeded();
await desktop.waitForTimeout(400);
await desktop.screenshot({
  path: `${outDir}/${variant}_top10_desktop.png`,
  clip: { x: 0, y: 0, width: 1280, height: 1600 },
});
// Also a focused grid shot from the grid's top.
const gridBox = await grid.boundingBox();
if (gridBox) {
  await desktop.screenshot({
    path: `${outDir}/${variant}_product_list_desktop.png`,
    clip: { x: gridBox.x, y: gridBox.y, width: gridBox.width, height: Math.min(1500, gridBox.height) },
  });
  console.log("saved product_list_desktop");
}

for (const [key, name] of Object.entries(EXPAND_TARGETS)) {
  await captureExpanded(desktop, key, name);
}
await desktop.close();

// ---- Mobile ----
const mobile = await browser.newPage({ viewport: { width: 390, height: 1500 } });
await mobile.goto(url, { waitUntil: "networkidle" });
await mobile.waitForLoadState("networkidle");
await mobile.locator("text=בקצרה").first().waitFor({ state: "attached", timeout: 30000 });
await mobile.waitForTimeout(1200);
await mobile.screenshot({ path: `${outDir}/${variant}_mobile.png`, fullPage: false });
console.log("saved mobile");

await browser.close();
console.log(`DONE variant=${variant}`);
