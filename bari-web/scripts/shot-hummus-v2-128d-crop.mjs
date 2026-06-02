import { chromium } from "playwright";

const OUT = "C:/Bari/02_products/hummus/reports/128d_screenshots";
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.setViewportSize({ width: 375, height: 900 });
await page.goto("http://localhost:3100/hashvaot/hummus", { waitUntil: "networkidle" });
await page.waitForLoadState("domcontentloaded");
await page.waitForTimeout(1500);

const target = "סלט חומוס";
const row = page.locator(`[aria-label="${target}"]`).first();
await row.scrollIntoViewIfNeeded();
await row.click();
if ((await row.getAttribute("aria-expanded")) !== "true") await row.click();
await page.waitForSelector(`[aria-label="${target}"][aria-expanded="true"]`, { timeout: 8000 });
await page.waitForTimeout(500);
await page.screenshot({ path: `${OUT}/mobile-expanded-top.png`, clip: { x: 0, y: 0, width: 375, height: 900 } });

await browser.close();
console.log("CROP_DONE");
