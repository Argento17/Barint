import { chromium } from "playwright";
import fs from "fs";

const base = "http://localhost:3106";
const url = `${base}/hashvaot/cookies-coffee`;
fs.mkdirSync("public/qa/cookies", { recursive: true });
const browser = await chromium.launch({ headless: true });

// Full mobile chart section
const page = await browser.newPage({ viewport: { width: 390, height: 900 }, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
await page.waitForTimeout(2000);
const viz = await page.$('[data-testid="cookies-viz"]');
if (viz) {
  const box = await viz.boundingBox();
  console.log("mobile viz bounds:", JSON.stringify(box));
  // Full chart height - might be tall, take in chunks
  await page.screenshot({ path: "public/qa/cookies/charts-mobile-full.png", clip: { x: 0, y: box.y - 5, width: 390, height: Math.min(box.height + 10, 3000) } });
  console.log("saved charts-mobile-full.png");
}
await browser.close();
