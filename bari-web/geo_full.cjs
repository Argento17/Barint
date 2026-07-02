const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 812 });
  await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle", timeout: 20000 });
  await page.waitForTimeout(1500);

  // Get all bari-cmp-row elements
  const rows = await page.$$eval(".bari-cmp-row", els => els.map((el, i) => {
    const rect = el.getBoundingClientRect();
    const scoreText = el.querySelector(".bari-score-chip, [class*=score]");
    const insightEl = el.querySelector(".bari-insight, [class*=insight]");
    return {
      index: i,
      top: Math.round(rect.top),
      bottom: Math.round(rect.bottom),
      height: Math.round(rect.height),
      scoreText: scoreText ? scoreText.textContent.trim().slice(0, 30) : null,
      insight: insightEl ? insightEl.textContent.trim().slice(0, 60) : null,
      productName: el.querySelector("h2,h3,[class*=name],[class*=title]")?.textContent?.trim()?.slice(0, 50) ?? null
    };
  }));
  
  const firstRowTop = rows.length > 0 ? rows[0].top : null;
  const rowsAboveFold = rows.filter(r => r.top < 812).length;
  const rowsFullyVisible = rows.filter(r => r.bottom <= 812).length;

  // Hero element
  const hero = await page.evaluate(() => {
    const h1 = document.querySelector("h1");
    if (!h1) return null;
    const rect = h1.getBoundingClientRect();
    // Get parent section
    const sect = h1.closest("section, [class*=hero]");
    if (!sect) return { h1Top: Math.round(rect.top), h1Bottom: Math.round(rect.bottom) };
    const sr = sect.getBoundingClientRect();
    return { sectionTop: Math.round(sr.top), sectionBottom: Math.round(sr.bottom), sectionHeight: Math.round(sr.height) };
  });

  // Prologue
  const prologue = await page.evaluate(() => {
    const el = document.querySelector("[class*=prologue], .bari-prologue");
    if (!el) return null;
    const rect = el.getBoundingClientRect();
    return { top: Math.round(rect.top), bottom: Math.round(rect.bottom), height: Math.round(rect.height) };
  });

  // Safety box
  const safetyBoxes = await page.$$eval("[class*=FBF8EE]", els => els.map(el => {
    const rect = el.getBoundingClientRect();
    return { top: Math.round(rect.top), bottom: Math.round(rect.bottom), height: Math.round(rect.height), cls: el.className.slice(0, 60) };
  }));

  console.log(JSON.stringify({ 
    firstRowTop, rowsAboveFold, rowsFullyVisible, totalRows: rows.length,
    rows: rows.slice(0, 8),
    hero, prologue, safetyBoxes 
  }, null, 2));

  await page.screenshot({ path: "mag_mobile_390.png", fullPage: false });
  await browser.close();
})();
