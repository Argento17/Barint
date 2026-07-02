const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
  });

  // Collect console messages
  const consoleMessages = [];
  const pageErrors = [];

  const page = await context.newPage();

  page.on('console', msg => {
    consoleMessages.push({ type: msg.type(), text: msg.text() });
  });

  page.on('pageerror', err => {
    pageErrors.push({ message: err.message, stack: err.stack });
  });

  // Load with cache-bust
  await page.goto('https://bari.digital/?cb=diag', { waitUntil: 'networkidle', timeout: 30000 });

  // Wait for hydration
  await page.waitForTimeout(3000);

  // Take full-page screenshot
  await page.screenshot({ path: 'C:\\bari\\bari-diag-before.png', fullPage: true });

  // Check footer
  const footerInfo = await page.evaluate(() => {
    const footer = document.querySelector('footer');
    if (!footer) return { found: false };
    const rect = footer.getBoundingClientRect();
    const style = window.getComputedStyle(footer);
    return {
      found: true,
      innerHTML_length: footer.innerHTML.length,
      offsetHeight: footer.offsetHeight,
      boundingRect: { top: rect.top, bottom: rect.bottom, height: rect.height, width: rect.width },
      computedDisplay: style.display,
      computedVisibility: style.visibility,
      computedOpacity: style.opacity,
      computedOverflow: style.overflow,
    };
  });

  // Check consent manager
  const consentInfo = await page.evaluate(() => {
    // Look for any consent-related elements
    const allDivs = Array.from(document.querySelectorAll('[class*="consent"], [id*="consent"], [data-testid*="consent"]'));

    // Check localStorage
    const storedConsent = localStorage.getItem('bari-cookie-consent');

    // Look for ConsentManager by checking for a fixed/sticky element near bottom
    const fixedElements = Array.from(document.querySelectorAll('*')).filter(el => {
      const style = window.getComputedStyle(el);
      return style.position === 'fixed' && el.offsetHeight > 10;
    }).map(el => ({
      tag: el.tagName,
      id: el.id,
      class: el.className,
      height: el.offsetHeight
    }));

    return {
      consentElements: allDivs.map(el => ({ tag: el.tagName, id: el.id, class: el.className })),
      storedConsent,
      fixedElements: fixedElements.slice(0, 10)
    };
  });

  // Check the body structure
  const domStructure = await page.evaluate(() => {
    const body = document.body;
    return {
      childCount: body.children.length,
      childTags: Array.from(body.children).map(c => ({ tag: c.tagName, id: c.id, class: c.className.substring(0, 100) })),
      // Check for Next.js root
      nextRoot: !!document.getElementById('__next'),
      // Check for hydration markers
      hasReactRoot: !!document.querySelector('[data-reactroot]'),
    };
  });

  // Check HTML end of body
  const bodyEnd = await page.evaluate(() => {
    return document.body.innerHTML.slice(-3000);
  });

  // Now clear localStorage and reload to check if consent banner appears
  await page.evaluate(() => localStorage.clear());
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);

  const afterClearConsent = await page.evaluate(() => {
    const storedConsent = localStorage.getItem('bari-cookie-consent');
    const allFixed = Array.from(document.querySelectorAll('*')).filter(el => {
      const style = window.getComputedStyle(el);
      return style.position === 'fixed' && el.offsetHeight > 10;
    }).map(el => ({
      tag: el.tagName,
      id: el.id,
      class: el.className.substring(0, 80),
      height: el.offsetHeight
    }));
    return { storedConsent, fixedElements: allFixed.slice(0, 10) };
  });

  // Screenshot after clear
  await page.screenshot({ path: 'C:\\bari\\bari-diag-after-clear.png', fullPage: true });

  // Scroll to bottom and screenshot
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'C:\\bari\\bari-diag-bottom.png' });

  const results = {
    consoleMessages: consoleMessages.filter(m => m.type === 'error' || m.type === 'warning' || m.text.toLowerCase().includes('hydrat') || m.text.toLowerCase().includes('footer') || m.text.toLowerCase().includes('consent')),
    allConsoleErrors: consoleMessages.filter(m => m.type === 'error'),
    pageErrors,
    footerInfo,
    consentInfo,
    domStructure,
    bodyEnd,
    afterClearConsent
  };

  fs.writeFileSync('C:\\bari\\bari-diag-results.json', JSON.stringify(results, null, 2));
  console.log(JSON.stringify(results, null, 2));

  await browser.close();
})().catch(err => {
  console.error('SCRIPT ERROR:', err.message);
  console.error(err.stack);
  process.exit(1);
});
