/**
 * TASK-384A: DOM structure probe — find what's between 65px and 439px.
 */
import { chromium } from "playwright";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.setViewportSize({ width: 390, height: 812 });
await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle" });

// Walk the main content area and find all elements with height > 20px between y=65 and y=440
const elements = await page.evaluate(() => {
  const all = document.querySelectorAll("*");
  const results = [];
  for (const el of all) {
    const r = el.getBoundingClientRect();
    if (r.height > 20 && r.top >= 60 && r.top < 450 && r.width > 100) {
      const depth = (() => {
        let d = 0, p = el;
        while (p.parentElement) { d++; p = p.parentElement; }
        return d;
      })();
      if (depth < 15) { // Only shallow elements to avoid noise
        results.push({
          tag: el.tagName,
          id: el.id || "",
          className: (el.className?.toString?.() || "").slice(0, 80),
          top: Math.round(r.top),
          bottom: Math.round(r.bottom),
          height: Math.round(r.height),
          depth,
        });
      }
    }
  }
  // Sort by depth then top
  results.sort((a, b) => a.depth - b.depth || a.top - b.top);
  return results.slice(0, 40);
});

console.log("=== DOM ELEMENTS between y=65 and y=440 (depth < 15) ===");
for (const e of elements) {
  const indent = "  ".repeat(Math.max(0, e.depth - 3));
  console.log(`${indent}[d${e.depth}] <${e.tag}> top=${e.top} h=${e.height}  class="${e.className}"`);
}

await browser.close();
