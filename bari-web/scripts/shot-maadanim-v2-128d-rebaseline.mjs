// TASK-128D — Maadanim v2 activation QA re-baseline (mobile + lg).
// Captures the LIVE v2 row surface (MAADANIM_V2_SLICE=true) at the two
// breakpoints named in comparison_ui_reference_v2 §12: mobile (375) and lg (1024).
// Collapsed + expanded at each. Also a hummus regression shot (must stay v1).
import { chromium } from "playwright";
import { mkdirSync } from "node:fs";

const BASE = process.env.BARI_BASE ?? "http://localhost:3100";
const URL = `${BASE}/hashvaot/maadanim`;
const HUMMUS = `${BASE}/hashvaot/hummus`;
const OUT = "C:/Bari/02_products/maadanim/reports/128d_screenshots";
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

async function ready(url) {
  await page.goto(url, { waitUntil: "networkidle" });
  await page.waitForLoadState("domcontentloaded");
  await page.waitForTimeout(1200);
}

const target = "יופלה GO מועשר בחלבון";

// The mobile and desktop render paths both live in the DOM; only one is visible
// per breakpoint and they expand differently:
//   - mobile: the row div (aria-label) is itself the toggle.
//   - lg/desktop: expansion is driven by the "למה קיבל את הציון?" button.
async function setExpandedMobile(want) {
  const row = page.locator(`[aria-label="${target}"]:visible`).first();
  await row.scrollIntoViewIfNeeded();
  if (((await row.getAttribute("aria-expanded")) === "true") !== want) {
    await row.click();
    await page.waitForTimeout(500);
  }
}

async function expandDesktopFirstRow() {
  const btn = page.getByRole("button", { name: "למה קיבל את הציון?" }).first();
  await btn.scrollIntoViewIfNeeded();
  await btn.click();
  await page.waitForTimeout(600);
}

async function shoot(label, kind) {
  await ready(URL);
  if (kind === "mobile") {
    await setExpandedMobile(false);
    await page.screenshot({ path: `${OUT}/${label}-collapsed.png`, fullPage: true });
    await setExpandedMobile(true);
    await page.screenshot({ path: `${OUT}/${label}-expanded.png`, fullPage: true });
  } else {
    // desktop/lg: collapsed is the natural load state
    await page.screenshot({ path: `${OUT}/${label}-collapsed.png`, fullPage: true });
    await expandDesktopFirstRow();
    await page.screenshot({ path: `${OUT}/${label}-expanded.png`, fullPage: true });
  }
}

// ── Mobile (375) ─────────────────────────────────────────────────────────────
await page.setViewportSize({ width: 375, height: 900 });
await shoot("mobile", "mobile");

// ── lg (1024) ────────────────────────────────────────────────────────────────
await page.setViewportSize({ width: 1024, height: 1000 });
await shoot("lg", "desktop");

// ── Regression: hummus must remain v1 (no protein metric / no promoted conf) ──
await page.setViewportSize({ width: 1024, height: 1000 });
await ready(HUMMUS);
await page.screenshot({ path: `${OUT}/regression-hummus-lg.png`, fullPage: false });

await browser.close();
console.log("SHOTS_DONE", OUT);
