import { chromium } from "playwright";

const base = process.env.BASE ?? "http://localhost:3007";
const url = `${base}/hashvaot/brined-cheeses`;
const browser = await chromium.launch({ headless: true });

async function shot(width, outName) {
  const page = await browser.newPage({ viewport: { width, height: 1000 }, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: "networkidle", timeout: 90000 });
  await page.waitForSelector('[data-testid="brined-viz"]', { timeout: 60000 });
  await page.waitForTimeout(1500); // let recharts settle
  const el = page.locator('[data-testid="brined-viz"]');
  await el.screenshot({ path: `public/qa/brined/${outName}` });
  await page.close();
  console.log("saved public/qa/brined/" + outName);
}

await shot(900, "viz-desktop.png");
await shot(390, "viz-mobile.png");
await browser.close();
