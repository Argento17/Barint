import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const URL = "http://localhost:3100/hashvaot/maadanim";
const OUT = "C:/Bari/02_products/maadanim/reports/128b_screenshots";
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

// Mobile — top rows only (viewport crop), then expanded top row
await page.setViewportSize({ width: 390, height: 740 });
await page.goto(URL, { waitUntil: "networkidle" });
await page.waitForTimeout(1200);
await page.screenshot({ path: `${OUT}/mobile-crop-collapsed.png` });

const target = "יופלה GO מועשר בחלבון";
const row = page.locator(`[aria-label="${target}"]`).first();
await row.scrollIntoViewIfNeeded();
if ((await row.getAttribute("aria-expanded")) !== "true") await row.click();
await page.waitForSelector(`[aria-label="${target}"][aria-expanded="true"]`, { timeout: 8000 });
await page.waitForTimeout(500);
await page.evaluate(() => window.scrollTo(0, 0));
await page.screenshot({ path: `${OUT}/mobile-crop-expanded.png` });

// Desktop — top rows only (viewport crop)
await page.setViewportSize({ width: 1280, height: 820 });
await page.goto(URL, { waitUntil: "networkidle" });
await page.waitForTimeout(1200);
await page.evaluate(() => {
  document.querySelector("#comparison-grid")?.scrollIntoView();
});
await page.waitForTimeout(400);
await page.screenshot({ path: `${OUT}/desktop-crop-collapsed.png` });

await browser.close();
console.log("CROPS_DONE");
