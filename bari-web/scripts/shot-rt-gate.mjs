import { chromium } from "playwright";
import fs from "fs";

const base = process.env.BASE ?? "http://localhost:3100";
const outDir = "public/qa/rt-gate";
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });

async function shot(url, width, outName, { fullPage = false, expandFirst = false } = {}) {
  const page = await browser.newPage({ viewport: { width, height: 1300 }, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
  await page.waitForTimeout(1200);
  if (expandFirst) {
    const btn = page.locator("button[aria-expanded]").first();
    await btn.scrollIntoViewIfNeeded();
    await btn.click();
    await page.waitForTimeout(900);
    await btn.scrollIntoViewIfNeeded();
  }
  await page.screenshot({ path: `${outDir}/${outName}`, fullPage });
  await page.close();
  console.log("saved " + outName);
}

await shot(`${base}/hashvaot`, 1280, "index-fold.png", { fullPage: false });
await shot(`${base}/hashvaot/cakes`, 1280, "cakes-desktop-full.png", { fullPage: true });
await shot(`${base}/hashvaot/cakes`, 390, "cakes-mobile-fold.png", { fullPage: false });
await shot(`${base}/hashvaot/cakes`, 1280, "cakes-row-expanded.png", { fullPage: true, expandFirst: true });
await shot(`${base}/hashvaot/cookies-coffee`, 1280, "biscuits-desktop-full.png", { fullPage: true });
await shot(`${base}/hashvaot/cookies-coffee`, 1280, "biscuits-row-expanded.png", { fullPage: true, expandFirst: true });

await browser.close();
console.log("DONE");
