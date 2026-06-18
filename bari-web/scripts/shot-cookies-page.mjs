import { chromium } from "playwright";
import fs from "fs";

const base = process.env.BASE ?? "http://localhost:3100";
const url = `${base}/hashvaot/cookies-coffee`;
fs.mkdirSync("public/qa/cookies", { recursive: true });
const browser = await chromium.launch({ headless: true });

async function shot(width, outName, fullPage) {
  const page = await browser.newPage({ viewport: { width, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `public/qa/cookies/${outName}`, fullPage });
  await page.close();
  console.log("saved public/qa/cookies/" + outName);
}

// desktop full page, desktop above-fold, mobile above-fold
await shot(1280, "cookies-desktop-full.png", true);
await shot(1280, "cookies-desktop-fold.png", false);
await shot(390, "cookies-mobile-fold.png", false);
await browser.close();
