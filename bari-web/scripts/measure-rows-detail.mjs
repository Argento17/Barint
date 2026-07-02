/**
 * TASK-384A: Detailed per-row measurement including band dividers.
 */
import { chromium } from "playwright";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.setViewportSize({ width: 390, height: 812 });
await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle" });

// Get all elements in the scroll container in DOM order
const items = await page.evaluate(() => {
  const scroll = document.querySelector(".bari-cmp-scroll");
  if (!scroll) return [];
  const results = [];
  for (const child of scroll.children) {
    const r = child.getBoundingClientRect();
    const isRow = child.tagName === "ARTICLE";
    const isDivider = child.classList.contains("bari-cmp-divider");
    // For rows, also get the verdict text
    let verdictText = "";
    if (isRow) {
      const p = child.querySelector(".bari-cmp-namecell p");
      verdictText = p ? (p.textContent || "").trim().slice(0, 50) : "";
    }
    results.push({
      type: isRow ? "ROW" : isDivider ? "DIVIDER" : "OTHER",
      top: Math.round(r.top),
      bottom: Math.round(r.bottom),
      height: Math.round(r.height),
      verdict: verdictText,
    });
  }
  return results;
});

const VIEWPORT_HEIGHT = 812;
console.log("=== DETAILED ROW + DIVIDER LAYOUT ===");
console.log(`Viewport: 390×${VIEWPORT_HEIGHT}px\n`);

let rowNum = 0;
for (const item of items) {
  if (item.type === "ROW") rowNum++;
  const aboveFold = item.bottom <= VIEWPORT_HEIGHT ? "✓ ABOVE FOLD" : item.top < VIEWPORT_HEIGHT ? "~ PARTIAL" : "✗ BELOW";
  const label = item.type === "ROW" ? `Row #${rowNum}` : item.type;
  console.log(`${label.padEnd(12)} top=${String(item.top).padStart(4)}  bottom=${String(item.bottom).padStart(4)}  h=${String(item.height).padStart(3)}  ${aboveFold}  "${item.verdict}"`);
}

const rowsFullyAbove = items.filter(i => i.type === "ROW" && i.bottom <= VIEWPORT_HEIGHT).length;
const rowsPartial = items.filter(i => i.type === "ROW" && i.top < VIEWPORT_HEIGHT && i.bottom > VIEWPORT_HEIGHT).length;
console.log(`\nRows fully above fold: ${rowsFullyAbove}`);
console.log(`Rows partially above fold: ${rowsPartial}`);
console.log(`Gate (≥3 fully above fold): ${rowsFullyAbove >= 3 ? "PASS ✓" : "FAIL ✗"}`);

await browser.close();
