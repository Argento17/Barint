const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 812 });
  await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle", timeout: 20000 });
  await page.waitForTimeout(1500);

  // Check what insightLine vs rowVerdict the rows show in collapsed state
  // Look at the actual text content of rows and compare against page-data.ts
  const firstRowExpanded = await page.evaluate(() => {
    const btn = document.querySelector(".bari-cmp-rowhead");
    if (!btn) return { error: "no rowhead" };
    // Is there an expandable section?
    const article = btn.closest("article");
    if (!article) return { error: "no article" };
    
    // Get the bari-cmp-expansion or similar
    const expansion = article.querySelector("[class*=expansion], [class*=detail], [id*=expand]");
    const isExpanded = expansion ? true : false;
    
    // Get the rowVerdict/insightLine specifically — look for the insight line element
    const insightEls = article.querySelectorAll("[class*=insight], [class*=verdict]");
    const insights = [...insightEls].map(el => ({ cls: el.className.slice(0, 60), text: el.textContent.trim().slice(0, 120) }));

    return { isExpanded, insights, articleHTML: article.innerHTML.slice(0, 500) };
  });

  // Count rows with visible expansion panel
  const expandedRows = await page.$$eval(".bari-cmp-row", els => {
    return els.filter(el => {
      const h = el.getBoundingClientRect().height;
      return h > 300; // expanded rows are typically >300px
    }).length;
  });

  console.log(JSON.stringify({ firstRowExpanded, expandedRows }, null, 2));
  await browser.close();
})();
