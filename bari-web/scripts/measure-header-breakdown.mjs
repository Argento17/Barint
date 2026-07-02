/**
 * TASK-384A: Measure header breakdown — what's consuming the 439px above the first row.
 */
import { chromium } from "playwright";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.setViewportSize({ width: 390, height: 812 });
await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle" });

const breakdown = await page.evaluate(() => {
  const getBox = (sel) => {
    const el = document.querySelector(sel);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { top: r.top, bottom: r.bottom, height: r.height };
  };

  return {
    // Nav/header bar
    nav: getBox("nav, header"),
    // Category hero
    hero: getBox(".bari-cat-hero, [class*='category-hero'], [class*='CategoryHero']"),
    // Prologue
    prologue: getBox("[class*='prologue'], [class*='Prologue']"),
    // Category note box
    noteBox: getBox(".bari-cat-note, [class*='note'], [dir='rtl'] > div > div:nth-child(4)"),
    // Safety box (headerSlot)
    safetyBox: getBox("[class*='safety'], [class*='Safety'], [class*='magnesium']"),
    // Band divider above first row
    firstDivider: getBox(".bari-cmp-divider"),
    // First row
    firstRow: getBox("article.bari-cmp-row"),
    // Workspace
    workspace: getBox(".bari-cmp-workspace"),
  };
});

console.log("=== HEADER BREAKDOWN ===");
for (const [name, box] of Object.entries(breakdown)) {
  if (box) {
    console.log(`${name.padEnd(15)}: top=${box.top.toFixed(0)}px  bottom=${box.bottom.toFixed(0)}px  height=${box.height.toFixed(0)}px`);
  } else {
    console.log(`${name.padEnd(15)}: NOT FOUND`);
  }
}

// Also measure the band-divider height
const dividerHeight = await page.evaluate(() => {
  const d = document.querySelector(".bari-cmp-divider");
  return d ? d.getBoundingClientRect().height : null;
});
console.log(`\nBand divider height: ${dividerHeight?.toFixed(0) ?? "N/A"}px`);

// Measure all visible sections between page top and first row
const sections = await page.evaluate(() => {
  const container = document.querySelector("[dir='rtl']");
  if (!container) return [];
  const children = Array.from(container.querySelectorAll(":scope > * > *, :scope > *"));
  return children.slice(0, 20).map(el => ({
    tag: el.tagName,
    className: el.className?.toString?.()?.slice(0, 60) ?? "",
    top: el.getBoundingClientRect().top,
    height: el.getBoundingClientRect().height,
  })).filter(el => el.top < 450);
});

console.log("\n=== SECTIONS ABOVE FIRST ROW ===");
for (const s of sections) {
  console.log(`<${s.tag}> top=${s.top.toFixed(0)} h=${s.height.toFixed(0)}  class="${s.className}"`);
}

await browser.close();
