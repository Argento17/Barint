const { chromium } = require('@playwright/test');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, locale: 'he-IL' });
  const page = await ctx.newPage();
  await page.goto('http://localhost:3000/hashvaot/supplements', { waitUntil: 'load' });
  await page.waitForTimeout(500);
  const magCard = await page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('a[href*="magnesium"]'));
    if (links.length === 0) return { found: false };
    const mc = links[0];
    const img = mc.querySelector('img');
    const r = mc.getBoundingClientRect();
    return {
      found: true,
      href: mc.getAttribute('href'),
      w: Math.round(r.width), h: Math.round(r.height),
      hasImg: !!img,
      imgSrc: img ? img.getAttribute('src').slice(0, 120) : null,
      imgComplete: img ? img.complete : null,
      imgNaturalW: img ? img.naturalWidth : null,
      imgNaturalH: img ? img.naturalHeight : null
    };
  });
  console.log('SUPPLEMENTS MAG CARD:', JSON.stringify(magCard, null, 2));
  await page.screenshot({ path: 'tmp_shots/supplements_index.png', fullPage: false });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
