const { chromium } = require("playwright");
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 812 });
  await page.goto("http://localhost:3000/hashvaot/magnesium", { waitUntil: "networkidle", timeout: 20000 });
  await page.waitForTimeout(1500);

  // Check for leakage terms in rendered DOM text
  const leakageTerms = ["NOVA", "BSIP", "cap_1", "floor", "structural_class", "matrix_integrity", 
    "pillar", "dimension", "routing", "adjusted_dose", "bav_tier", "binding_constraint",
    "ul_exceed_grade", "blend_dominant", "opacity_signal", "cap_3_honesty", "68.7", "72.8", "66.0",
    "62.2", "63.9", "60.6", "59.3", "46.2", "48.9", "34.0", "49.0"];
  
  const bodyText = await page.evaluate(() => document.body.innerText);
  const leakageFound = leakageTerms.filter(t => bodyText.includes(t));

  // Check score chip values — find chips by looking for product score numbers
  const scoreInfo = await page.evaluate(() => {
    const allText = document.body.innerText;
    // Look for score numbers expected on page
    const scoreNums = ["73", "69", "66", "64", "62", "61", "59", "49", "46", "34"];
    const found = scoreNums.filter(s => {
      // Must appear as standalone number (not part of a larger number)
      const regex = new RegExp("\\b" + s + "\\b");
      return regex.test(allText);
    });
    return found;
  });

  // Check for framework vocab in visible text
  const frameworkTerms = ["ספיגה גבוהה יחסית", "ספיגה בינונית", "ספיגה נמוכה יחסית", "ביסגליצינט", "ציטראט", "אוקסיד"];
  const frameworkVisible = await page.evaluate((terms) => {
    const text = document.body.innerText;
    return terms.filter(t => text.includes(t));
  }, frameworkTerms);
  
  // Row heights check — are they short (condensed verdict ~90px)?
  const rowHeights = await page.$$eval(".bari-cmp-row", els => els.map(el => Math.round(el.getBoundingClientRect().height)));
  const avgHeight = rowHeights.length > 0 ? Math.round(rowHeights.reduce((a,b) => a+b, 0) / rowHeights.length) : 0;

  console.log(JSON.stringify({ 
    leakageFound, 
    scoresVisible: scoreInfo,
    frameworkVisible,
    rowHeights: rowHeights.slice(0, 10),
    avgRowHeight: avgHeight
  }, null, 2));

  await browser.close();
})();
