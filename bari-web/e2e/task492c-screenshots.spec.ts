import { test } from "@playwright/test";

/**
 * TASK-492C screenshot capture — not a standing suite member. One-off script to produce
 * the deliverable screenshots for the creatine comparison page build (desktop + mobile,
 * including product tables + safety/dairy sections).
 */

const OUT_DIR = "C:/Bari/tasks/returns/TASK-492C_screenshots";

test("capture creatine page screenshots", async ({ page }, testInfo) => {
  const isMobile = testInfo.project.name === "mobile";
  const tag = isMobile ? "mobile-390" : "desktop-1440";

  if (!isMobile) {
    await page.setViewportSize({ width: 1440, height: 900 });
  }

  await page.goto("/hashvaot/creatine");
  await page.waitForSelector("text=מותגי ייחוס עולמיים", { timeout: 15_000 });

  // Dismiss cookie consent if present.
  const consentAccept = page.getByRole("button", { name: /מסכים|אישור|קבל/ });
  if (await consentAccept.first().isVisible({ timeout: 2_000 }).catch(() => false)) {
    await consentAccept.first().click();
  }

  // 1. Hero + prologue + category note (top of page).
  await page.screenshot({ path: `${OUT_DIR}/${tag}-01-hero.png` });

  // 2. Scroll to Israeli shelf section and expand first row (shows badge grid + dose-honesty).
  const israeliHeading = page.getByText("המדף הישראלי", { exact: false }).first();
  await israeliHeading.scrollIntoViewIfNeeded();
  await page.screenshot({ path: `${OUT_DIR}/${tag}-02-israeli-section.png` });

  const firstRow = page.locator("article button[aria-expanded]").first();
  await firstRow.click({ force: true });
  await page.waitForTimeout(300);
  await page.screenshot({ path: `${OUT_DIR}/${tag}-03-israeli-row-expanded.png` });

  // 3. Scroll to worldwide benchmark section, expand a directory-verified row (Thorne).
  const worldwideHeading = page.getByText("מותגי ייחוס עולמיים", { exact: false }).first();
  await worldwideHeading.scrollIntoViewIfNeeded();
  await page.screenshot({ path: `${OUT_DIR}/${tag}-04-worldwide-section.png` });

  const worldwideRows = page.locator("article button[aria-expanded]");
  const worldwideCount = await worldwideRows.count();
  const thorneButton = page.locator('article button[aria-label*="Thorne"]').first();
  if (await thorneButton.count()) {
    await thorneButton.scrollIntoViewIfNeeded();
    await thorneButton.click({ force: true });
    await page.waitForTimeout(300);
    await page.screenshot({ path: `${OUT_DIR}/${tag}-05-worldwide-directory-verified-row.png` });
  }

  // 4. Full page screenshot (captures everything incl. safety/dairy category-note content
  //    which lives in the categoryNote box near the top, and methodology footer at bottom).
  await page.screenshot({ path: `${OUT_DIR}/${tag}-06-fullpage.png`, fullPage: true });

  void worldwideCount;
});
