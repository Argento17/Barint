import { chromium } from "playwright";
import fs from "fs";

const base = process.env.BASE ?? "http://localhost:3100";
const outDir = "public/qa/rt-gate";
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });

async function additiveShot(url, outName) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
  await page.waitForTimeout(1000);
  const btn = page.locator('button[aria-expanded="false"]:visible').first();
  await btn.scrollIntoViewIfNeeded();
  await btn.click();
  await page.waitForTimeout(900);
  // open additives disclosure if present
  const addBtn = page.getByText(/תוספי מזון|תוספים/).first();
  try { if (await addBtn.isVisible()) { await addBtn.click({ timeout: 2000 }); await page.waitForTimeout(600); } } catch {}
  // pin the expanded button near the top, then grab the viewport
  await btn.evaluate((el) => el.scrollIntoView({ block: "start" }));
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${outDir}/${outName}`, fullPage: false });
  await page.close();
  console.log("saved " + outName);
}

await additiveShot(`${base}/hashvaot/cakes`, "cakes-additive-crop.png");
await additiveShot(`${base}/hashvaot/cookies-coffee`, "biscuits-additive-crop.png");
await browser.close();
console.log("DONE");
