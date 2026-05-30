import { chromium } from "playwright";

const url = process.env.ROUTE_URL ?? "http://localhost:3000/hashvaot/maadanim";
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
await page.goto(url, { waitUntil: "networkidle" });
await page.waitForSelector("text=מעדנים", { timeout: 30000 });
await page.waitForTimeout(800);
await page.screenshot({
  path: "public/qa/maadanim-v2/production-hashvaot-maadanim.png",
  fullPage: true,
});
await browser.close();
console.log("saved public/qa/maadanim-v2/production-hashvaot-maadanim.png");
