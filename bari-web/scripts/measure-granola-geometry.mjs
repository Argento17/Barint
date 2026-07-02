/**
 * TASK-384A: Verify granola page is unaffected by the prop-gated changes.
 * Checks: no clamp on verdict text, normal divider height.
 */
import { chromium } from "playwright";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.setViewportSize({ width: 390, height: 812 });
await page.goto("http://localhost:3000/hashvaot/granola", { waitUntil: "networkidle" });

const scroll = await page.$(".bari-cmp-scroll");
if (!scroll) { console.error("No .bari-cmp-scroll found"); await browser.close(); process.exit(1); }

const items = await page.evaluate(() => {
  const scroll = document.querySelector(".bari-cmp-scroll");
  const results = [];
  for (const child of scroll.children) {
    const r = child.getBoundingClientRect();
    const isRow = child.tagName === "ARTICLE";
    const isDivider = child.classList.contains("bari-cmp-divider");
    if (!isRow && !isDivider) continue;
    // For rows, check verdict paragraph line count
    let verdictLines = null;
    let verdictOverflow = null;
    if (isRow) {
      const p = child.querySelector(".bari-cmp-namecell p");
      if (p) {
        const style = window.getComputedStyle(p);
        verdictOverflow = style.overflow;
        verdictLines = style.webkitLineClamp;
      }
    }
    results.push({
      type: isRow ? "ROW" : "DIVIDER",
      height: Math.round(r.height),
      verdictOverflow,
      verdictLines,
    });
  }
  return results.slice(0, 10);
});

console.log("=== GRANOLA PAGE — PROP ISOLATION CHECK ===");
for (const item of items) {
  if (item.type === "DIVIDER") {
    const expected = item.height >= 28 ? "✓ normal" : "✗ COMPACT (should not be)";
    console.log(`DIVIDER h=${item.height}px  ${expected}`);
  } else {
    const clamped = item.verdictLines && item.verdictLines !== "none" && item.verdictLines !== "0";
    const clampStatus = clamped ? `✗ CLAMPED (${item.verdictLines}) — should NOT be` : "✓ unclamped";
    console.log(`ROW     h=${item.height}px  verdict overflow=${item.verdictOverflow} clamp=${item.verdictLines}  ${clampStatus}`);
  }
}

await browser.close();
