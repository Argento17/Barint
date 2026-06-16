import { chromium } from "playwright";
import fs from "fs";

const base = process.env.BASE ?? "http://localhost:3100";
const outDir = "public/qa/rt-gate";
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });

async function cardShot(matchText, outName) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 2 });
  await page.goto(`${base}/hashvaot`, { waitUntil: "networkidle", timeout: 90000 });
  await page.waitForTimeout(1000);
  const el = page.getByText(matchText, { exact: false }).first();
  await el.scrollIntoViewIfNeeded();
  await el.evaluate((node) => node.scrollIntoView({ block: "center" }));
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${outDir}/${outName}`, fullPage: false });
  await page.close();
  console.log("saved " + outName);
}

await cardShot("עוגות גבינה", "card-cakes.png");
await cardShot("ביסקוויטים", "card-biscuits.png");
await browser.close();
console.log("DONE");
