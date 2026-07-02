/**
 * verify-magnesium-clamp.js
 * Playwright verification for line-clamp-3 fix on /hashvaot/magnesium
 *
 * Run: cd C:\Bari\bari-web && node verify-magnesium-clamp.js
 */

const { chromium } = require('@playwright/test');

async function getVerdictInfo(page) {
  return page.evaluate(() => {
    // Strategy 1: p.line-clamp-3 anywhere
    let paras = Array.from(document.querySelectorAll('p.line-clamp-3'));

    // Strategy 2: paragraphs with mt-[5px] inside .bari-cmp-namecell
    if (paras.length === 0) {
      const namecells = document.querySelectorAll('.bari-cmp-namecell');
      namecells.forEach(cell => {
        const ps = cell.querySelectorAll('p');
        ps.forEach(p => {
          const style = window.getComputedStyle(p);
          const mt = style.marginTop;
          if (mt === '5px' || p.className.includes('mt-')) {
            paras.push(p);
          }
        });
      });
    }

    // Strategy 3: any paragraph inside .bari-cmp-namecell
    if (paras.length === 0) {
      paras = Array.from(document.querySelectorAll('.bari-cmp-namecell p'));
    }

    // Strategy 4: any paragraph inside article rows
    if (paras.length === 0) {
      paras = Array.from(document.querySelectorAll('.bari-cmp-row p, article p'));
    }

    return paras.map(p => {
      const style = window.getComputedStyle(p);
      const clampVal = style.webkitLineClamp || style['-webkit-line-clamp'] || '';
      const overflowVal = style.overflow;
      const displayVal = style.display;
      const scrollH = p.scrollHeight;
      const clientH = p.clientHeight;
      const text = p.textContent.trim();
      const classes = p.className;
      const rect = p.getBoundingClientRect();
      return {
        text,
        classes,
        clampVal,
        overflowVal,
        displayVal,
        scrollH,
        clientH,
        isClipped: scrollH > clientH + 2,
        endsWithEllipsis: text.endsWith('…'),
        top: rect.top,
        bottom: rect.bottom,
      };
    });
  });
}

async function checkCerealsPage(page) {
  return page.evaluate(() => {
    // Check verdict paragraphs - look for any with line-clamp-3
    const paras = Array.from(document.querySelectorAll('p'));
    const verdictParas = paras.filter(p => {
      const classes = p.className || '';
      return classes.includes('line-clamp');
    });

    return verdictParas.map(p => ({
      classes: p.className,
      text: p.textContent.trim().substring(0, 60),
      hasLineClamp3: (p.className || '').includes('line-clamp-3'),
      hasLineClamp2: (p.className || '').includes('line-clamp-2'),
    }));
  });
}

async function countAboveFoldRows(page, viewportHeight) {
  return page.evaluate((vh) => {
    const rows = document.querySelectorAll('.bari-cmp-row');
    let count = 0;
    rows.forEach(row => {
      const rect = row.getBoundingClientRect();
      if (rect.bottom <= vh) count++;
    });
    return { total: rows.length, aboveFold: count };
  }, viewportHeight);
}

async function main() {
  console.log('='.repeat(60));
  console.log('MAGNESIUM LINE-CLAMP VERIFICATION');
  console.log('='.repeat(60));

  const browser = await chromium.launch({ headless: true });

  try {
    // ──────────────────────────────────────────────
    // CHECK 1 & 2: TRUNCATION + ALTMAN ROWS @ 390px
    // ──────────────────────────────────────────────
    console.log('\n[1] Viewport 390x844 — Magnesium page');
    const page390 = await browser.newPage();
    await page390.setViewportSize({ width: 390, height: 844 });
    await page390.goto('http://localhost:3000/hashvaot/magnesium', { waitUntil: 'networkidle' });

    // Give React time to hydrate / paint
    await page390.waitForTimeout(1500);

    const verdicts390 = await getVerdictInfo(page390);

    console.log(`  Verdict paragraphs found: ${verdicts390.length}`);

    if (verdicts390.length === 0) {
      console.log('  WARNING: No verdict paragraphs detected. Dumping page structure for debug...');
      const structure = await page390.evaluate(() => {
        const rows = document.querySelectorAll('.bari-cmp-row, article');
        return Array.from(rows).slice(0, 3).map(r => ({
          tag: r.tagName,
          classes: r.className.substring(0, 80),
          children: Array.from(r.querySelectorAll('p')).slice(0, 5).map(p => ({
            classes: p.className,
            text: p.textContent.trim().substring(0, 60),
          })),
        }));
      });
      console.log('  Page structure sample:', JSON.stringify(structure, null, 2));
    } else {
      const clipped390 = verdicts390.filter(v => v.isClipped);
      const ellipsis390 = verdicts390.filter(v => v.endsWithEllipsis);

      console.log(`  Clipped (scrollH > clientH+2): ${clipped390.length}`);
      console.log(`  End with ellipsis U+2026: ${ellipsis390.length}`);

      if (clipped390.length > 0) {
        console.log('  CLIPPED rows:');
        clipped390.forEach(v => {
          console.log(`    text="${v.text.substring(0, 60)}..." scrollH=${v.scrollH} clientH=${v.clientH} clamp="${v.clampVal}"`);
        });
      } else {
        console.log('  PASS: No verdict paragraphs are clipped at 390px');
      }

      // CSS properties sample
      const sample = verdicts390[0];
      if (sample) {
        console.log(`  Sample CSS: overflow="${sample.overflowVal}" -webkit-line-clamp="${sample.clampVal}" display="${sample.displayVal}"`);
        console.log(`  Sample classes: "${sample.classes}"`);
      }

      // Check specific Altman rows
      console.log('\n[2] Altman Bisglycinate + Altman UP specific check');
      const altmanRows = verdicts390.filter(v =>
        v.text.toLowerCase().includes('bisglycinate') ||
        v.text.toLowerCase().includes('altman up') ||
        v.text.toLowerCase().includes('altman')
      );

      // Also search by page text for those product names
      const altmanFound = await page390.evaluate(() => {
        // Find rows that contain "Altman" in their name cell
        const rows = document.querySelectorAll('.bari-cmp-row, article');
        const results = [];
        rows.forEach(row => {
          const text = row.textContent;
          if (text.includes('Altman') || text.includes('bisglycinate') || text.includes('Bisglycinate')) {
            const ps = row.querySelectorAll('p');
            ps.forEach(p => {
              if (p.scrollHeight > 0) {
                results.push({
                  rowText: text.substring(0, 80),
                  pText: p.textContent.trim().substring(0, 80),
                  scrollH: p.scrollHeight,
                  clientH: p.clientHeight,
                  isClipped: p.scrollHeight > p.clientHeight + 2,
                  classes: p.className,
                });
              }
            });
          }
        });
        return results;
      });

      if (altmanFound.length === 0) {
        console.log('  NOTE: No Altman rows found on page (product names may differ)');
        // List first 5 row texts to help debug
        const rowTexts = await page390.evaluate(() => {
          const rows = document.querySelectorAll('.bari-cmp-row, article');
          return Array.from(rows).slice(0, 5).map(r => r.textContent.substring(0, 100));
        });
        console.log('  First 5 row texts:');
        rowTexts.forEach((t, i) => console.log(`    [${i+1}] ${t}`));
      } else {
        altmanFound.forEach(a => {
          const status = a.isClipped ? 'CLIPPED' : 'OK';
          console.log(`  ${status}: "${a.pText.substring(0, 60)}" scrollH=${a.scrollH} clientH=${a.clientH}`);
        });
      }
    }

    // ──────────────────────────────────────────────
    // CHECK 3: ABOVE-FOLD COUNT @ 390x844
    // ──────────────────────────────────────────────
    console.log('\n[3] Above-fold rows @ 390x844');
    const foldData390 = await countAboveFoldRows(page390, 844);
    console.log(`  Total .bari-cmp-row elements: ${foldData390.total}`);
    console.log(`  Rows fully above fold (bottom <= 844): ${foldData390.aboveFold}`);

    await page390.close();

    // ──────────────────────────────────────────────
    // CHECK 4: TRUNCATION @ 375px
    // ──────────────────────────────────────────────
    console.log('\n[4] Viewport 375x812 — Magnesium page');
    const page375 = await browser.newPage();
    await page375.setViewportSize({ width: 375, height: 812 });
    await page375.goto('http://localhost:3000/hashvaot/magnesium', { waitUntil: 'networkidle' });
    await page375.waitForTimeout(1500);

    const verdicts375 = await getVerdictInfo(page375);
    const clipped375 = verdicts375.filter(v => v.isClipped);

    console.log(`  Verdict paragraphs found: ${verdicts375.length}`);
    console.log(`  Clipped: ${clipped375.length}`);
    if (clipped375.length > 0) {
      console.log('  CLIPPED rows:');
      clipped375.forEach(v => {
        console.log(`    text="${v.text.substring(0, 60)}..." scrollH=${v.scrollH} clientH=${v.clientH}`);
      });
    } else {
      console.log('  PASS: No verdict paragraphs clipped at 375px');
    }

    await page375.close();

    // ──────────────────────────────────────────────
    // CHECK 5: CEREALS REGRESSION
    // ──────────────────────────────────────────────
    console.log('\n[5] Cereals regression — /hashvaot/dganey-boker');
    const pageCereals = await browser.newPage();
    await pageCereals.setViewportSize({ width: 390, height: 844 });
    await pageCereals.goto('http://localhost:3000/hashvaot/dganey-boker', { waitUntil: 'networkidle' });
    await pageCereals.waitForTimeout(1500);

    const cerealsParas = await checkCerealsPage(pageCereals);

    console.log(`  Paragraphs with any line-clamp class: ${cerealsParas.length}`);
    const withClamp3 = cerealsParas.filter(p => p.hasLineClamp3);
    const withClamp2 = cerealsParas.filter(p => p.hasLineClamp2);
    console.log(`  line-clamp-3 found: ${withClamp3.length}`);
    console.log(`  line-clamp-2 found: ${withClamp2.length}`);

    if (withClamp3.length === 0) {
      console.log('  PASS: No line-clamp-3 on cereals page (not affected by magnesium change)');
    } else {
      console.log('  FAIL: line-clamp-3 unexpectedly found on cereals page:');
      withClamp3.forEach(p => console.log(`    classes="${p.classes}" text="${p.text}"`));
    }

    await pageCereals.close();

  } finally {
    await browser.close();
  }

  console.log('\n' + '='.repeat(60));
  console.log('VERIFICATION COMPLETE');
  console.log('='.repeat(60));
}

main().catch(err => {
  console.error('Script failed:', err);
  process.exit(1);
});
