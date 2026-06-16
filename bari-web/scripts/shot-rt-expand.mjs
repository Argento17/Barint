import { chromium } from "playwright";
import fs from "fs";

const base = process.env.BASE ?? "http://localhost:3100";
const outDir = "public/qa/rt-gate";
fs.mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ headless: true });

async function expandShot(url, outName) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 1300 }, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
  await page.waitForTimeout(1200);
  // first VISIBLE collapsed row toggle
  const btn = page.locator('button[aria-expanded="false"]:visible').first();
  await btn.scrollIntoViewIfNeeded();
  await btn.click();
  await page.waitForTimeout(1000);
  // try to also open the additives section if it is a nested disclosure
  const addBtn = page.getByText(/תוספי מזון|תוספים/).first();
  try {
    if (await addBtn.isVisible()) { await addBtn.scrollIntoViewIfNeeded(); await addBtn.click({ timeout: 2000 }); await page.waitForTimeout(700); }
  } catch {}
  await page.screenshot({ path: `${outDir}/${outName}`, fullPage: true });
  await page.close();
  console.log("saved " + outName);
}

await expandShot(`${base}/hashvaot/cakes`, "cakes-row-expanded.png");
await expandShot(`${base}/hashvaot/cookies-coffee`, "biscuits-row-expanded.png");
await browser.close();
console.log("DONE");
