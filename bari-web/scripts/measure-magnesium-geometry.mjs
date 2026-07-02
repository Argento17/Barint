/**
 * TASK-384A: Playwright geometry measurement for magnesium comparison page.
 * Measures at 390×812px (standard mobile viewport).
 * Reports: px-to-first-row, collapsed row height, rows-above-fold, screenshot path.
 */
import { chromium } from "playwright";
import { fileURLToPath } from "url";
import path from "path";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SCREENSHOT_PATH = path.join(__dirname, "..", "magnesium-geometry.png");
const URL = "http://localhost:3000/hashvaot/magnesium";
const VIEWPORT = { width: 390, height: 812 };

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.setViewportSize(VIEWPORT);
await page.goto(URL, { waitUntil: "networkidle" });

// Ensure all rows are collapsed (noAutoExpand is set, but verify).
// rows are <article class="bari-cmp-row">
const rowHandles = await page.$$("article.bari-cmp-row");
console.log(`Total rows found: ${rowHandles.length}`);

// Measure bounding boxes
const measurements = [];
for (const handle of rowHandles) {
  const box = await handle.boundingBox();
  if (box) measurements.push(box);
}

if (measurements.length === 0) {
  console.error("No rows found — selector may be wrong.");
  await browser.close();
  process.exit(1);
}

// px-to-first-row: top of first row relative to viewport
const pxToFirstRow = measurements[0].y;

// collapsed row height: use the median of all row heights (first might include extra margin)
const heights = measurements.map((b) => b.height);
const sortedHeights = [...heights].sort((a, b) => a - b);
const medianHeight = sortedHeights[Math.floor(sortedHeights.length / 2)];

// rows-above-fold: count rows whose bottom edge is within the viewport height
const rowsAboveFold = measurements.filter(
  (b) => b.y + b.height <= VIEWPORT.height
).length;

// Also count rows that START above the fold (partially visible)
const rowsStartingAboveFold = measurements.filter(
  (b) => b.y < VIEWPORT.height
).length;

console.log("=== MAGNESIUM GEOMETRY REPORT ===");
console.log(`Viewport: ${VIEWPORT.width}×${VIEWPORT.height}px`);
console.log(`px-to-first-row (top of row 1): ${pxToFirstRow.toFixed(1)}px`);
console.log(`Row heights: ${heights.map((h) => h.toFixed(0)).join(", ")}px`);
console.log(`Median collapsed row height: ${medianHeight.toFixed(1)}px`);
console.log(`Rows fully above fold (bottom ≤ ${VIEWPORT.height}px): ${rowsAboveFold}`);
console.log(`Rows starting above fold (top < ${VIEWPORT.height}px): ${rowsStartingAboveFold}`);
console.log(`PASS (≥3 rows above fold): ${rowsAboveFold >= 3 ? "YES ✓" : "NO ✗"}`);

// Check if expanded row is open (should be none — noAutoExpand)
const openRows = await page.$$("article.bari-cmp-row button[aria-expanded='true']");
console.log(`Open rows (should be 0): ${openRows.length}`);

// Screenshot
await page.screenshot({ path: SCREENSHOT_PATH, fullPage: false });
console.log(`Screenshot saved: ${SCREENSHOT_PATH}`);

await browser.close();
