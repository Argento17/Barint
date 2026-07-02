// Check safety blocks on oxide D products at mobile viewport
const { chromium } = require('@playwright/test');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, locale: 'he-IL' });
  const page = await ctx.newPage();
  await page.goto('http://localhost:3000/hashvaot/magnesium', { waitUntil: 'load' });
  await page.waitForTimeout(500);

  // Find the 4 oxide D products — all have "⚠" in their button text from the geometry data
  const oxideDProducts = await page.evaluate(() => {
    const articles = Array.from(document.querySelectorAll('article'));
    return articles
      .filter(a => a.textContent && a.textContent.includes('⚠'))
      .map(a => {
        // Find the safety block inside this article
        const safetyEl = Array.from(a.querySelectorAll('*')).find(el => {
          const txt = (el.textContent || '').trim();
          return el.children.length > 0 && txt.includes('⚠') && txt.includes('מ"ג') && txt.length < 300;
        });
        const allTextEls = Array.from(a.querySelectorAll('*')).filter(el => {
          const txt = (el.textContent || '').trim();
          return el.children.length === 0 && txt.includes('⚠');
        });
        const warningTextEl = Array.from(a.querySelectorAll('*')).find(el => {
          const txt = (el.textContent || '').trim();
          return el.children.length === 0 && txt.length > 20 && (txt.includes('מינון') || txt.includes('גבול') || txt.includes('ספיגה'));
        });

        const r = a.getBoundingClientRect();
        const safetyR = safetyEl ? safetyEl.getBoundingClientRect() : null;
        return {
          productName: a.textContent?.trim().slice(0, 50),
          articleH: Math.round(r.height),
          safetyBlockText: safetyEl ? safetyEl.textContent?.trim().slice(0, 120) : null,
          safetyBlockH: safetyR ? Math.round(safetyR.height) : null,
          safetyBlockVisible: safetyEl ? (safetyR && safetyR.width > 0 && safetyR.height > 0) : false,
          warningText: warningTextEl ? warningTextEl.textContent?.trim().slice(0, 120) : null
        };
      });
  });
  console.log('OXIDE D PRODUCTS SAFETY BLOCKS:');
  console.log(JSON.stringify(oxideDProducts, null, 2));

  // Scroll to first oxide product and take a screenshot
  await page.evaluate(() => {
    const articles = Array.from(document.querySelectorAll('article'));
    const firstOxide = articles.find(a => a.textContent && a.textContent.includes('⚠'));
    if (firstOxide) firstOxide.scrollIntoView();
  });
  await page.waitForTimeout(300);
  await page.screenshot({ path: 'tmp_shots/oxide_safety_visible.png' });
  console.log('Screenshot: tmp_shots/oxide_safety_visible.png');

  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
