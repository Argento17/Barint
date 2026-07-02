// Targeted visual check for magnesium page post-publish safety audit
const { chromium } = require('@playwright/test');

(async () => {
  const browser = await chromium.launch();

  // ── MOBILE (390px) ──────────────────────────────────────────────────────────
  const mobileCtx = await browser.newContext({ viewport: { width: 390, height: 844 }, locale: 'he-IL' });
  const mobilePage = await mobileCtx.newPage();
  await mobilePage.goto('http://localhost:3000/hashvaot/magnesium', { waitUntil: 'load' });
  // Freeze animations
  await mobilePage.evaluate(() => {
    const s = document.createElement('style');
    s.textContent = '*, *::before, *::after { animation: none !important; transition: none !important; }';
    document.head.appendChild(s);
  });
  await mobilePage.waitForTimeout(500);

  // 1. Hero height = first product row top
  const heroMetrics = await mobilePage.evaluate(() => {
    const articles = Array.from(document.querySelectorAll('article'));
    const firstArticle = articles.find(a => a.getBoundingClientRect().height > 50);
    if (!firstArticle) return { found: false };
    const r = firstArticle.getBoundingClientRect();
    return {
      firstRowTop: Math.round(r.top),
      firstRowH: Math.round(r.height),
      firstRowText: firstArticle.textContent?.trim().slice(0, 40)
    };
  });
  console.log('\n=== HERO HEIGHT (pre-table) ===');
  console.log(JSON.stringify(heroMetrics));
  console.log('PASS:', heroMetrics.firstRowTop <= 480 ? `YES (${heroMetrics.firstRowTop}px < 480px limit)` : `FAIL (${heroMetrics.firstRowTop}px > 480px)`);

  // 2. Rows visible at 0px scroll
  const rowsAtLoad = await mobilePage.evaluate(() => {
    const articles = Array.from(document.querySelectorAll('article'));
    const vh = 844; // mobile viewport height
    const visible = articles.filter(a => {
      const r = a.getBoundingClientRect();
      return r.top < vh && r.bottom > 0 && r.height > 50;
    });
    return {
      total: articles.length,
      visibleCount: visible.length,
      visibleTitles: visible.map(a => a.textContent?.trim().slice(0, 40))
    };
  });
  console.log('\n=== ROWS VISIBLE AT 0px SCROLL ===');
  console.log(JSON.stringify(rowsAtLoad, null, 2));
  console.log('PASS (need ≥3):', rowsAtLoad.visibleCount >= 3 ? `YES (${rowsAtLoad.visibleCount})` : `FAIL (${rowsAtLoad.visibleCount})`);

  // 3. First product score chip visible at 0px scroll
  const scoreChipVisible = await mobilePage.evaluate(() => {
    // Grade chips are text like "73" or "B" in score chip elements
    const allText = Array.from(document.querySelectorAll('*'));
    const chips = allText.filter(el => {
      const txt = el.textContent?.trim();
      return txt && /^\d{2}$/.test(txt) && el.children.length === 0;
    });
    if (chips.length === 0) return { found: false };
    const firstChip = chips[0];
    const r = firstChip.getBoundingClientRect();
    return {
      found: true,
      text: firstChip.textContent?.trim(),
      visible: r.top < 844 && r.bottom > 0 && r.height > 0,
      y: Math.round(r.top)
    };
  });
  console.log('\n=== FIRST SCORE CHIP VISIBLE AT 0px ===');
  console.log(JSON.stringify(scoreChipVisible));

  // 4. Safety / over-UL blocks for D products (oxide 520mg etc)
  const safetyBlocks = await mobilePage.evaluate(() => {
    const allEls = Array.from(document.querySelectorAll('*'));
    const results = [];
    allEls.forEach(el => {
      const txt = (el.textContent || '').trim();
      if (el.children.length === 0 && txt.length > 0 && txt.length < 200) {
        if (txt.includes('⚠') || txt.includes('מינון') && txt.includes('גבול')) {
          const r = el.getBoundingClientRect();
          const cs = window.getComputedStyle(el);
          results.push({
            text: txt.slice(0, 100),
            visible: r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden',
            w: Math.round(r.width), h: Math.round(r.height),
            color: cs.color, bg: cs.backgroundColor
          });
        }
      }
    });
    return results;
  });
  console.log('\n=== SAFETY/OVER-UL BLOCKS ===');
  console.log(JSON.stringify(safetyBlocks, null, 2));

  // 5. Full-Mag product (Bari label — null image)
  const fullMag = await mobilePage.evaluate(() => {
    const articles = Array.from(document.querySelectorAll('article'));
    const fm = articles.find(a => a.textContent && a.textContent.includes('פול-מג'));
    if (!fm) return { found: false };
    const img = fm.querySelector('img');
    const svgPlaceholder = fm.querySelector('svg');
    const divPlaceholder = fm.querySelector('[class*="placeholder"], [class*="fallback"], [class*="no-image"]');
    return {
      found: true,
      text: fm.textContent?.trim().slice(0, 60),
      hasImg: !!img,
      imgSrc: img ? img.getAttribute('src')?.slice(0, 100) : null,
      imgW: img ? Math.round(img.getBoundingClientRect().width) : null,
      imgH: img ? Math.round(img.getBoundingClientRect().height) : null,
      imgNaturalW: img ? img.naturalWidth : null,
      imgNaturalH: img ? img.naturalHeight : null,
      imgComplete: img ? img.complete : null,
      hasSvgPlaceholder: !!svgPlaceholder,
      hasDivPlaceholder: !!divPlaceholder
    };
  });
  console.log('\n=== FULL-MAG (null image product) ===');
  console.log(JSON.stringify(fullMag, null, 2));

  // 6. RTL check
  const rtl = await mobilePage.evaluate(() => ({
    dir: document.documentElement.dir,
    lang: document.documentElement.lang
  }));
  console.log('\n=== RTL / LANG ===');
  console.log(JSON.stringify(rtl));

  // 7. No "undefined" visible in page text
  const undefinedCheck = await mobilePage.evaluate(() => {
    const bodyText = document.body.innerText;
    const hasBadText = bodyText.includes('undefined') || bodyText.includes('NaN') || bodyText.includes('[object Object]');
    const matches = [];
    if (bodyText.includes('undefined')) matches.push('undefined');
    if (bodyText.includes('NaN')) matches.push('NaN');
    if (bodyText.includes('[object Object]')) matches.push('[object Object]');
    return { clean: !hasBadText, badStrings: matches };
  });
  console.log('\n=== UNDEFINED/NaN CHECK ===');
  console.log(JSON.stringify(undefinedCheck));

  await mobilePage.screenshot({ path: 'tmp_shots/mag_mobile_0scroll.png', fullPage: false });
  console.log('\nMobile viewport screenshot saved: tmp_shots/mag_mobile_0scroll.png');
  await mobileCtx.close();

  // ── HASHVAOT INDEX — magnesium card ─────────────────────────────────────────
  const indexCtx = await browser.newContext({ viewport: { width: 390, height: 844 }, locale: 'he-IL' });
  const indexPage = await indexCtx.newPage();
  await indexPage.goto('http://localhost:3000/hashvaot', { waitUntil: 'load' });
  await indexPage.waitForTimeout(500);

  const magCard = await indexPage.evaluate(() => {
    // Find all links/cards containing מגנזיום
    const allLinks = Array.from(document.querySelectorAll('a'));
    const mc = allLinks.find(a => a.textContent && a.textContent.includes('מגנזיום'));
    if (!mc) return { found: false, availableLinks: Array.from(document.querySelectorAll('a')).map(a => a.href?.slice(-30) + '|' + a.textContent?.trim().slice(0, 30)).slice(0, 20) };
    const img = mc.querySelector('img');
    const r = mc.getBoundingClientRect();
    return {
      found: true,
      href: mc.getAttribute('href'),
      text: mc.textContent?.trim().slice(0, 80),
      w: Math.round(r.width), h: Math.round(r.height),
      hasImg: !!img,
      imgSrc: img ? img.getAttribute('src')?.slice(0, 120) : null,
      imgComplete: img ? img.complete : null,
      imgNaturalW: img ? img.naturalWidth : null,
      imgNaturalH: img ? img.naturalHeight : null
    };
  });
  console.log('\n=== HASHVAOT INDEX — MAG CARD ===');
  console.log(JSON.stringify(magCard, null, 2));
  await indexPage.screenshot({ path: 'tmp_shots/hashvaot_index_mobile.png', fullPage: false });

  await indexCtx.close();
  await browser.close();

  console.log('\n=== DONE ===');
})().catch(e => { console.error('SCRIPT ERROR:', e); process.exit(1); });
