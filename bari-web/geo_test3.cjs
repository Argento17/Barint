const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 812 });
  await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle", timeout: 20000 });
  await page.waitForTimeout(1500);

  // Get all elements with data-state (likely product rows/accordions)
  const stateEls = await page.$$eval("[data-state]", els => els.slice(0, 20).map(el => ({
    tag: el.tagName, state: el.getAttribute("data-state"), classes: el.className.slice(0, 80),
    rect: { top: Math.round(el.getBoundingClientRect().top), height: Math.round(el.getBoundingClientRect().height) }
  })));
  console.log("data-state elements:", JSON.stringify(stateEls, null, 2));

  // Find product rows by looking for score chips or insight lines
  const productRows = await page.evaluate(() => {
    // Look for elements containing Hebrew score text like "ציון B" or "ציון C"
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
    const results = [];
    while (walker.nextNode()) {
      const el = walker.currentNode;
      if (el.children.length > 0 && el.children.length < 20) {
        const text = el.textContent;
        if (text && (text.includes("ציון B") || text.includes("ציון C") || text.includes("ציון D"))) {
          const rect = el.getBoundingClientRect();
          if (rect.height > 50 && rect.height < 200 && rect.width > 300) {
            results.push({ 
              tag: el.tagName, classes: el.className.slice(0, 60),
              top: Math.round(rect.top), height: Math.round(rect.height)
            });
            if (results.length >= 6) break;
          }
        }
      }
    }
    return results;
  });
  console.log("Product row candidates:", JSON.stringify(productRows, null, 2));

  await browser.close();
})();
