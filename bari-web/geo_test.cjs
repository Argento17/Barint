const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 812 });
  await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle", timeout: 20000 });
  await page.waitForTimeout(1500);

  await page.screenshot({ path: "mag_mobile_390.png", fullPage: false });

  const rows = await page.$$eval("[data-product-id]", els => els.map((el, i) => {
    const rect = el.getBoundingClientRect();
    return { index: i, id: el.getAttribute("data-product-id"), top: Math.round(rect.top), bottom: Math.round(rect.bottom), height: Math.round(rect.height) };
  }));

  const safetyBox = await page.evaluate(() => {
    const els = document.querySelectorAll(".bg-\\[\\#FBF8EE\\]");
    if (!els.length) return null;
    const rect = els[0].getBoundingClientRect();
    return { top: Math.round(rect.top), bottom: Math.round(rect.bottom), height: Math.round(rect.height) };
  });

  const firstRowTop = rows.length > 0 ? rows[0].top : null;
  const rowsAboveFold = rows.filter(r => r.top < 812).length;
  const rowsFullyAboveFold = rows.filter(r => r.bottom < 812).length;

  console.log(JSON.stringify({ rows: rows.slice(0, 6), safetyBox, firstRowTop, rowsAboveFold, rowsFullyAboveFold, totalRows: rows.length }, null, 2));
  await browser.close();
})();
