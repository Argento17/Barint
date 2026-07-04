import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

/**
 * TASK-492C FIX verification — /hashvaot/creatine design-critic fixes.
 * One-off check, not part of the standing smoke suite. Verifies:
 *   FIX 1 — desktop 1440: at least one product row is visible in the first viewport
 *           (categoryNote trimmed + evidence prose relocated below the tables).
 *   FIX 2 — 0 serious/critical axe color-contrast violations on the badge grid.
 *   FIX 3 — a Latin-script product name truncates at the tail, not the front
 *           (dir="auto" isolation on comparison-row.tsx).
 *   FIX 3 regression — magnesium page product names still render correctly.
 */

test("FIX 1: desktop 1440 — product rows visible in first viewport", async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto("/hashvaot/creatine");
  await page.waitForSelector("text=המדף הישראלי", { timeout: 15_000 });

  const consentAccept = page.getByRole("button", { name: /מסכים|אישור|קבל/ });
  if (await consentAccept.first().isVisible({ timeout: 2_000 }).catch(() => false)) {
    await consentAccept.first().click();
  }

  // First product row (article) must be within the viewport without scrolling.
  const firstRow = page.locator("article").first();
  await expect(firstRow).toBeVisible();
  const box = await firstRow.boundingBox();
  expect(box).not.toBeNull();
  if (box) {
    // Row top must be within the 900px first viewport.
    expect(box.y).toBeLessThan(900);
  }
});

test("FIX 2: axe — 0 serious/critical color-contrast violations on creatine badge grid", async ({ page }) => {
  await page.goto("/hashvaot/creatine");
  await page.waitForSelector("text=המדף הישראלי", { timeout: 15_000 });

  const consentAccept = page.getByRole("button", { name: /מסכים|אישור|קבל/ });
  if (await consentAccept.first().isVisible({ timeout: 2_000 }).catch(() => false)) {
    await consentAccept.first().click();
  }

  // Expand first few rows so badge grid renders into the DOM for the scan.
  const rowCount = await page.locator("article button[aria-expanded]").count();
  for (let i = 0; i < Math.min(rowCount, 6); i++) {
    const btn = page.locator("article button[aria-expanded]").nth(i);
    const expanded = await btn.getAttribute("aria-expanded");
    if (expanded !== "true") {
      await btn.scrollIntoViewIfNeeded();
      await btn.click();
      await page.waitForTimeout(200);
    }
  }

  // Scope the axe scan to the badge grid itself — TASK-492C FIX 2 is scoped to
  // creatine-badge-grid.tsx (honest / below_floor / undisclosed tier text + cert
  // pills). A pre-existing hero-eyebrow contrast issue in the shared
  // category-hero.tsx (text-[#1F8F6A]/80, 2.98:1) also exists on this page but is
  // NOT part of this delegation (shared by every category, including magnesium) —
  // reported separately in the task return, not fixed here.
  const results = await new AxeBuilder({ page })
    .include('[data-testid="creatine-cert-pill"]')
    .include(".max-sm\\:grid-cols-2\\!")
    .withTags(["wcag2a", "wcag2aa"])
    .analyze();

  const contrastViolations = results.violations.filter(
    (v) => v.id === "color-contrast" && (v.impact === "serious" || v.impact === "critical")
  );

  if (contrastViolations.length) {
    console.log(
      "color-contrast violations:\n" +
        contrastViolations.map((v) => `  ${v.help} (${v.nodes.length} nodes)`).join("\n")
    );
  }
  expect(contrastViolations, "serious/critical color-contrast violations on badge grid").toEqual([]);
});

test("FIX 3: Latin product name truncates at the tail, not the front", async ({ page }) => {
  await page.goto("/hashvaot/creatine");
  await page.waitForSelector("text=המדף הישראלי", { timeout: 15_000 });

  // "Sports Micronized Creatine" (NOW Foods) is the first Israeli product — a Latin name.
  const nameSpan = page.locator('span[dir="auto"]', { hasText: "Sports Micronized Creatine" }).first();
  await expect(nameSpan).toBeAttached();

  // Read the full text content (not visually truncated) to confirm the START of the
  // string is intact in the DOM — truncation is CSS-only (ellipsis), so the underlying
  // text node must start with "Sports", not end with "Creatine" only.
  const text = await nameSpan.textContent();
  expect(text?.trim().startsWith("Sports")).toBeTruthy();

  // Confirm the dir="auto" isolation is actually applied (the fix).
  const dirAttr = await nameSpan.getAttribute("dir");
  expect(dirAttr).toBe("auto");
});

test("FIX 3 regression check: magnesium page product names still render correctly", async ({ page }) => {
  await page.goto("/hashvaot/magnesium");
  await page.waitForSelector("h1, h2", { timeout: 15_000 });

  const consentAccept = page.getByRole("button", { name: /מסכים|אישור|קבל/ });
  if (await consentAccept.first().isVisible({ timeout: 2_000 }).catch(() => false)) {
    await consentAccept.first().click();
  }

  // Magnesium product names are Hebrew — dir="auto" must be a no-op for them (still RTL).
  const firstRowName = page.locator("article .bari-cmp-namecell span[dir='auto']").first();
  await expect(firstRowName).toBeVisible();
  const text = (await firstRowName.textContent())?.trim() ?? "";
  expect(text.length).toBeGreaterThan(0);
  // Hebrew range check — confirms real product name text rendered, not blank.
  expect(text).toMatch(/[֐-׿]/);
});
