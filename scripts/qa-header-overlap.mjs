import { chromium } from "playwright";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
await page.goto("http://localhost:3000/hashvaot/maadanim", {
  waitUntil: "networkidle",
});

const result = await page.evaluate(() => {
  const header = document.querySelector("header");
  const hRect = header?.getBoundingClientRect();
  const row = document.querySelector('[aria-label="יופלה GO דובדבן 0.7%"]');
  row?.scrollIntoView({ block: "start" });
  const rRect = row?.getBoundingClientRect();
  const headerBottom = hRect ? hRect.bottom : 0;
  const underHeader = rRect ? rRect.top < headerBottom : false;
  const el = document.elementFromPoint(
    rRect ? rRect.left + 20 : 0,
    rRect ? rRect.top + 10 : 0
  );
  return {
    underHeader,
    hitTag: el?.tagName,
    hitClass: el?.className?.slice?.(0, 80),
    rowTop: rRect?.top,
    headerBottom,
  };
});

console.log(JSON.stringify(result));
await browser.close();
