import { chromium } from "playwright";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await page.goto("http://localhost:3000/hashvaot/maadanim", {
  waitUntil: "networkidle",
});

const name = "יופלה GO דובדבן 0.7%";
await page.evaluate((label) => {
  const row = document.querySelector(`[aria-label="${label}"]`);
  row?.scrollIntoView({ block: "start" });
}, name);

const row = page.locator(`[aria-label="${name}"]`);
let clickFailed = false;
try {
  await row.click({ timeout: 3000, force: false });
} catch {
  clickFailed = true;
}
const expanded = await row.getAttribute("aria-expanded");

console.log(
  JSON.stringify({
    clickFailed,
    expandedAfterClick: expanded,
  })
);
await browser.close();
