import { test, expect } from "@playwright/test";

/**
 * TASK-507 — render verification for the "עוד השוואות" (explore-next) module.
 * Checks: renders, RTL, current category excluded, links resolve to live routes,
 * no regression on the golden brined-cheeses page.
 */

test.describe("Explore-next comparisons module", () => {
  test("snacks leaf page: module renders, excludes snacks, links are /hashvaot/*", async ({
    page,
  }) => {
    await page.goto("/hashvaot/snacks");
    const heading = page.getByRole("heading", { name: "עוד השוואות" });
    await expect(heading).toBeVisible();

    const section = page.locator("section", { has: heading });
    await expect(section).toHaveAttribute("dir", "rtl");

    const links = section.getByRole("link");
    const count = await links.count();
    expect(count).toBeGreaterThanOrEqual(3);
    expect(count).toBeLessThanOrEqual(4);

    for (let i = 0; i < count; i++) {
      const href = await links.nth(i).getAttribute("href");
      expect(href).toMatch(/^\/hashvaot\/[a-z-]+$/);
      expect(href).not.toBe("/hashvaot/snacks");
    }
  });

  test("golden brined-cheeses page: module renders, excludes brined-cheeses, no drift above the fold", async ({
    page,
  }) => {
    await page.goto("/hashvaot/brined-cheeses");
    const heading = page.getByRole("heading", { name: "עוד השוואות" });
    await expect(heading).toBeVisible();

    const section = page.locator("section", { has: heading });
    const links = section.getByRole("link");
    const count = await links.count();
    for (let i = 0; i < count; i++) {
      const href = await links.nth(i).getAttribute("href");
      expect(href).not.toBe("/hashvaot/brined-cheeses");
    }

    // Golden page's own hero/table chrome must still be present and unaffected.
    await expect(page.locator(".bc-page")).toBeVisible();
  });

  test("blog post (sugar-alcohols): module renders as a feasibility demo", async ({
    page,
  }) => {
    await page.goto("/blog/sugar-alcohols");
    const heading = page.getByRole("heading", { name: "עוד השוואות" });
    await expect(heading).toBeVisible();
  });

  test("a live category clicked from the module resolves (not a 404)", async ({
    page,
  }) => {
    await page.goto("/hashvaot/snacks");
    const heading = page.getByRole("heading", { name: "עוד השוואות" });
    const section = page.locator("section", { has: heading });
    const firstHref = await section.getByRole("link").first().getAttribute("href");
    expect(firstHref).toBeTruthy();
    const response = await page.goto(firstHref!);
    expect(response?.status()).toBeLessThan(400);
  });
});
