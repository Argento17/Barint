import { chromium } from "playwright";
import fs from "fs";

const base = "http://localhost:3106";
const url = `${base}/hashvaot/cookies-coffee`;
fs.mkdirSync("public/qa/cookies", { recursive: true });
const browser = await chromium.launch({ headless: true });

// Zoom in on chart area only
const page = await browser.newPage({ viewport: { width: 1280, height: 1800 }, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
await page.waitForTimeout(2000);

// Get the viz container bounds
const viz = await page.$('[data-testid="cookies-viz"]');
if (viz) {
  const box = await viz.boundingBox();
  console.log("viz bounds:", JSON.stringify(box));
  await page.screenshot({ path: "public/qa/cookies/charts-zoom-desktop.png", clip: { x: box.x, y: box.y - 10, width: box.width, height: box.height + 20 } });
  console.log("saved charts-zoom-desktop.png");
}

const page2 = await browser.newPage({ viewport: { width: 390, height: 900 }, deviceScaleFactor: 2 });
await page2.goto(url, { waitUntil: "networkidle", timeout: 90000 });
await page2.waitForTimeout(2000);
const viz2 = await page2.$('[data-testid="cookies-viz"]');
if (viz2) {
  const box2 = await viz2.boundingBox();
  await page2.screenshot({ path: "public/qa/cookies/charts-zoom-mobile.png", clip: { x: box2.x, y: box2.y - 10, width: box2.width, height: Math.min(box2.height + 20, 2400) } });
  console.log("saved charts-zoom-mobile.png");
}

await browser.close();
