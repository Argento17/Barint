import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const URL = "http://localhost:3100/hashvaot/hummus";
const OUT = "C:/Bari/02_products/hummus/reports/128d_screenshots";
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

async function ready() {
  await page.goto(URL, { waitUntil: "networkidle" });
  await page.waitForLoadState("domcontentloaded");
  await page.waitForTimeout(1200);
}

// ── Mobile (375) — collapsed + expanded ──────────────────────────────────────
await page.setViewportSize({ width: 375, height: 900 });
await ready();
await page.screenshot({ path: `${OUT}/mobile-collapsed.png`, fullPage: true });

const target = "סלט חומוס";
const row = page.locator(`[aria-label="${target}"]`).first();
await row.scrollIntoViewIfNeeded();
if ((await row.getAttribute("aria-expanded")) !== "true") await row.click();
await page.waitForSelector(`[aria-label="${target}"][aria-expanded="true"]`, { timeout: 8000 });
await page.waitForTimeout(400);
await page.screenshot({ path: `${OUT}/mobile-expanded.png`, fullPage: true });

// ── Desktop (1280) — collapsed + expanded ────────────────────────────────────
await page.setViewportSize({ width: 1280, height: 1000 });
await ready();
await page.screenshot({ path: `${OUT}/desktop-collapsed.png`, fullPage: false });

const expandBtn = page.getByRole("button", { name: "למה קיבל את הציון?" }).first();
await expandBtn.scrollIntoViewIfNeeded();
await expandBtn.click();
await page.waitForTimeout(500);
await page.screenshot({ path: `${OUT}/desktop-expanded.png`, fullPage: false });

await browser.close();
console.log("SHOTS_DONE", OUT);
