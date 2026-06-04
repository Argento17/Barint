import { chromium } from "playwright";
import { mkdirSync } from "fs";

const BASE = "http://localhost:3987/dev/glass-box-preview";
const OUT = "C:/Bari/03_operations/bsip2/proto_v0/reports/glass_box/preview_shots";
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch();

async function shot(name, width, expandNames = []) {
  const page = await browser.newPage({ viewport: { width, height: 900 } });
  await page.goto(BASE, { waitUntil: "networkidle" });
  await page.waitForTimeout(300);
  for (const n of expandNames) {
    const btn = page.locator(`button[aria-label="${n}"]`).first();
    if (await btn.count()) {
      await btn.click();
      await page.waitForTimeout(250);
    }
  }
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: true });
  console.log(`wrote ${name}.png (${width}px)`);
  await page.close();
}

// default open rows show the first row expanded; explicitly open the demoted ג'לי
// and the withheld rows so the disclosure note + withhold reason are visible.
await shot("glassbox_on_mobile_375", 375, [
  "חומוס",
  "ג'לי בטעם ענבים",
  "בולגרית מעודנת 24%",
]);
await shot("glassbox_on_desktop_1180", 1180, [
  "ג'לי בטעם ענבים",
  "בולגרית מעודנת 24%",
]);

await browser.close();
console.log("done");
