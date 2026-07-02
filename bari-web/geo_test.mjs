const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 812 });
  await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle", timeout: 20000 });
  await page.waitForTimeout(1500);

  // Take screenshot
  await page.screenshot({ path: "mag_mobile_390.png", fullPage: false });

  // Measure product rows
  const rows = await page.$$eval('[data-product-id]', els => els.map((el, i) => {
    const rect = el.getBoundingClientRect();
    return { index: i, id: el.getAttribute('data-product-id'), top: rect.top, bottom: rect.bottom, height: rect.height };
  }));

  // Measure safety box
  const safetyBox = await page.$eval('.rounded-\\[9px\\].border.border-\\[\\#ECE3C8\\].bg-\\[\\#FBF8EE\\]', el => {
    const rect = el.getBoundingClientRect();
    return { top: rect.top, bottom: rect.bottom, height: rect.height };
  }).catch(() => null);

  // First product row top
  const firstRowTop = rows.length > 0 ? rows[0].top : null;
  // Rows above fold (bottom < 812)
  const rowsAboveFold = rows.filter(r => r.top < 812).length;

  console.log(JSON.stringify({ rows: rows.slice(0, 5), safetyBox, firstRowTop, rowsAboveFold, totalRows: rows.length }, null, 2));
  await browser.close();
})();
