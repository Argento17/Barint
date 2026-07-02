const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 812 });
  await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle", timeout: 20000 });
  await page.waitForTimeout(1500);

  // Examine full bari-cmp-rowhead structure
  const rowheadInfo = await page.$$eval(".bari-cmp-rowhead", (els) => els.slice(0, 3).map(el => {
    const rect = el.getBoundingClientRect();
    return {
      height: Math.round(rect.height),
      ariaExpanded: el.getAttribute("aria-expanded"),
      text: el.innerText.trim().slice(0, 300),
      childCount: el.children.length,
      childClasses: [...el.children].map(c => c.className.slice(0, 50))
    };
  }));

  // Check what class bari-cmp-verdict or similar has
  const verdictEls = await page.evaluate(() => {
    const all = document.querySelectorAll("[class*=verdict], [class*=insight]");
    return [...all].slice(0, 6).map(el => ({
      cls: el.className.slice(0,80),
      text: el.textContent.trim().slice(0, 100)
    }));
  });

  console.log(JSON.stringify({ rowheadInfo, verdictEls }, null, 2));
  await browser.close();
})();
