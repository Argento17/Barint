const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 812 });
  await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle", timeout: 20000 });
  await page.waitForTimeout(1500);

  // Check row content — is "rowVerdict" (1-line) rendering or is it something longer?
  const rowContent = await page.$$eval(".bari-cmp-row", (els) => els.slice(0, 4).map(el => {
    const btn = el.querySelector("button, [class*=rowhead]");
    return btn ? btn.textContent.trim().slice(0, 200) : el.textContent.trim().slice(0, 200);
  }));

  // Check what text is in the first row at the collapsed state
  const firstRowBtn = await page.$eval(".bari-cmp-rowhead", el => ({
    text: el.textContent.trim().slice(0, 300),
    height: Math.round(el.getBoundingClientRect().height),
    classes: el.className.slice(0, 80)
  })).catch(() => null);

  // Check the category note height
  const catNote = await page.evaluate(() => {
    const box = document.querySelector(".rounded-\\[9px\\].border.border-\\[\\#ECE3C8\\].bg-\\[\\#FBF8EE\\].px-3.py-2");
    if (!box) return null;
    const rect = box.getBoundingClientRect();
    return { top: Math.round(rect.top), bottom: Math.round(rect.bottom), height: Math.round(rect.height) };
  });

  // What is above first product row? (everything between y=0 and firstRow.top)
  const preTableHeight = await page.evaluate(() => {
    const firstRow = document.querySelector(".bari-cmp-row");
    return firstRow ? Math.round(firstRow.getBoundingClientRect().top) : null;
  });

  console.log(JSON.stringify({ rowContent, firstRowBtn, catNote, preTableHeight }, null, 2));
  await browser.close();
})();
