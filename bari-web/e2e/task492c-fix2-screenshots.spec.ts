import { test } from "@playwright/test";

/**
 * TASK-492C FIX verification screenshots — /hashvaot/creatine + /hashvaot/magnesium
 * (regression check). Not a standing suite member.
 */

const OUT_DIR = "C:/Bari/tasks/returns/TASK-492C_screenshots";

test("fix2 desktop 1440 — first viewport shows product rows", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "desktop", "desktop-only capture");
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/hashvaot/creatine");
  await page.waitForSelector("text=המדף הישראלי", { timeout: 15_000 });

  const consentAccept = page.getByRole("button", { name: /מסכים|אישור|קבל/ });
  if (await consentAccept.first().isVisible({ timeout: 2_000 }).catch(() => false)) {
    await consentAccept.first().click();
  }

  // No scroll — capture exactly what's in the first 900px viewport.
  await page.screenshot({ path: `${OUT_DIR}/fix2-desktop-1440-first-viewport.png` });
});

test("fix2 desktop 1440 — full page shows evidence section below tables", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "desktop", "desktop-only capture");
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/hashvaot/creatine");
  await page.waitForSelector("text=מותגי ייחוס עולמיים", { timeout: 15_000 });

  const consentAccept = page.getByRole("button", { name: /מסכים|אישור|קבל/ });
  if (await consentAccept.first().isVisible({ timeout: 2_000 }).catch(() => false)) {
    await consentAccept.first().click();
  }

  await page.screenshot({ path: `${OUT_DIR}/fix2-desktop-1440-fullpage.png`, fullPage: true });
});

test("fix2 mobile 390 — no horizontal scroll, categoryNote collapsed", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "mobile", "mobile-only capture");
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/hashvaot/creatine");
  await page.waitForSelector("text=המדף הישראלי", { timeout: 15_000 });

  const consentAccept = page.getByRole("button", { name: /מסכים|אישור|קבל/ });
  if (await consentAccept.first().isVisible({ timeout: 2_000 }).catch(() => false)) {
    await consentAccept.first().click();
  }

  await page.screenshot({ path: `${OUT_DIR}/fix2-mobile-390-top.png` });

  const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
  const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
  console.log(`mobile scrollWidth=${scrollWidth} clientWidth=${clientWidth}`);
});

test("fix2 badge grid contrast — expanded row screenshot", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "desktop", "desktop-only capture");
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/hashvaot/creatine");
  await page.waitForSelector("text=המדף הישראלי", { timeout: 15_000 });

  const consentAccept = page.getByRole("button", { name: /מסכים|אישור|קבל/ });
  if (await consentAccept.first().isVisible({ timeout: 2_000 }).catch(() => false)) {
    await consentAccept.first().click();
  }

  const firstRow = page.locator("article button[aria-expanded]").first();
  await firstRow.click();
  await page.waitForTimeout(300);
  await page.screenshot({ path: `${OUT_DIR}/fix2-badge-grid-expanded.png` });
});

test("fix2 magnesium regression — desktop names render correctly", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "desktop", "desktop-only capture");
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/hashvaot/magnesium");
  await page.waitForSelector("h1, h2", { timeout: 15_000 });

  const consentAccept = page.getByRole("button", { name: /מסכים|אישור|קבל/ });
  if (await consentAccept.first().isVisible({ timeout: 2_000 }).catch(() => false)) {
    await consentAccept.first().click();
  }

  await page.screenshot({ path: `${OUT_DIR}/fix2-magnesium-regression-check.png` });
});
