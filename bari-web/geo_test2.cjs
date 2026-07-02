const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 812 });
  await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle", timeout: 20000 });
  await page.waitForTimeout(1500);

  // Find what data attributes exist
  const dataAttrs = await page.evaluate(() => {
    const all = document.querySelectorAll("*");
    const attrs = new Set();
    all.forEach(el => {
      el.getAttributeNames().forEach(a => { if (a.startsWith("data-")) attrs.add(a); });
    });
    return [...attrs];
  });
  console.log("Data attrs found:", JSON.stringify(dataAttrs));

  // Get page title and hero text
  const title = await page.title();
  const heroText = await page.evaluate(() => {
    const h1 = document.querySelector("h1");
    return h1 ? h1.textContent : "no h1";
  });
  console.log("Title:", title, "Hero:", heroText);

  await browser.close();
})();
