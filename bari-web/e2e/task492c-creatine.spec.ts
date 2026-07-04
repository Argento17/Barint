import { test, expect } from "@playwright/test";

/**
 * TASK-492C verification spec — /hashvaot/creatine.
 * One-off check for the creatine comparison page build. Not part of the standing
 * smoke suite; verifies the hard requirements from the delegation spec:
 *   - route renders, RTL Hebrew
 *   - no A–E grade shown anywhere
 *   - exactly 6 "אומת מול מאגר" badges in the worldwide table
 *   - both product tables render all rows (18 Israeli + 13 worldwide = 31)
 *   - zero horizontal scroll
 */

test("creatine page renders, RTL, no error overlay", async ({ page }) => {
  const resp = await page.goto("/hashvaot/creatine");
  expect(resp?.ok()).toBeTruthy();
  await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
  await expect(page.locator("html")).toHaveAttribute("lang", /he/);
  await expect(page.locator("h1, h2").first()).toBeVisible();
  const bodyText = (await page.locator("body").innerText()).trim();
  expect(bodyText.length).toBeGreaterThan(200);
  expect(bodyText).toMatch(/[֐-׿]/);
  await expect(page.locator("text=Application error")).toHaveCount(0);
});

test("creatine page shows zero A-E grade chips", async ({ page }) => {
  await page.goto("/hashvaot/creatine");
  await expect(page.getByText("המדף הישראלי", { exact: false }).first()).toBeVisible({ timeout: 15_000 });
  // ScoreChip renders "—" for null score/grade; A-E letter chips must not appear as
  // standalone grade text (ARIA label check is the strong assertion below).
  const gradeAriaLabels = page.locator('[aria-label^="ציון "]');
  expect(await gradeAriaLabels.count()).toBe(0);
  const nullScoreLabels = page.getByText("ללא ציון", { exact: true });
  expect(await nullScoreLabels.count()).toBeGreaterThan(0);
});

test("creatine page: exactly 6 directory-verified badges, all rows present, no horizontal scroll", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/hashvaot/creatine");
  await expect(page.getByText("מותגי ייחוס עולמיים", { exact: false }).first()).toBeVisible({ timeout: 15_000 });

  // Dismiss the cookie-consent dialog if present — it intercepts pointer events on rows.
  const consentAccept = page.getByRole("button", { name: /מסכים|אישור|קבל/ });
  if (await consentAccept.first().isVisible({ timeout: 2_000 }).catch(() => false)) {
    await consentAccept.first().click();
  }

  // Expand every row to force cert-tier badges into the DOM (badges render only in
  // the expansion panel). Multiple rows can be open at once (spec §6), so expanding
  // does not collapse earlier rows — re-query by index each iteration since the DOM
  // grows as expansion panels open.
  const rows = page.locator("article button[aria-expanded]");
  const rowCount = await rows.count();
  for (let i = 0; i < rowCount; i++) {
    const btn = page.locator("article button[aria-expanded]").nth(i);
    const expanded = await btn.getAttribute("aria-expanded");
    if (expanded !== "true") {
      await btn.scrollIntoViewIfNeeded();
      await btn.click({ force: true });
      await expect(btn).toHaveAttribute("aria-expanded", "true", { timeout: 5_000 });
    }
  }

  const directoryVerifiedBadges = page.locator('[data-testid="creatine-cert-pill"][data-cert-tier="directory_verified"]');
  expect(await directoryVerifiedBadges.count()).toBe(6);

  // Row count: 18 Israeli + 13 worldwide = 31 article rows.
  expect(rowCount).toBe(31);

  // No horizontal scroll at 390px.
  const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
  const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
  expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 1);
});
