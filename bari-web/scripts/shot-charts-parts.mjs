import { chromium } from "playwright";
import fs from "fs";

const base = "http://localhost:3106";
const url = `${base}/hashvaot/cookies-coffee`;
const browser = await chromium.launch({ headless: true });

// Use a tall viewport to capture everything in one page
const page = await browser.newPage({ viewport: { width: 390, height: 3000 }, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
await page.waitForTimeout(2000);
const viz = await page.$('[data-testid="cookies-viz"]');
const box = await viz.boundingBox();
console.log("bounds:", box);
// Chart A only (first chart)
await page.screenshot({ path: "public/qa/cookies/chart-a-mobile.png", clip: { x: 0, y: box.y, width: 390, height: 600 } });
// Charts B+C
await page.screenshot({ path: "public/qa/cookies/chart-bc-mobile.png", clip: { x: 0, y: box.y + 580, width: 390, height: 800 } });
console.log("saved chart-a-mobile.png chart-bc-mobile.png");
await browser.close();
