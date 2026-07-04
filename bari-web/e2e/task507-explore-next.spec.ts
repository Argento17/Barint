import { test, expect } from "@playwright/test";
import {
  getExploreNextCategories,
  EXPLORE_NEXT_CATEGORIES,
} from "../src/lib/hashvaot/explore-next-categories";

/**
 * TASK-507 — render verification for the "עוד השוואות" (explore-next) module.
 * Checks: renders, RTL, current category excluded, links resolve to live routes,
 * no regression on the golden brined-cheeses page, shelf scoping (Product D1),
 * family de-dup cap (Product D2), and the CTA copy fix (Content gate-1).
 */

test.describe("Explore-next: pure manifest logic (no browser needed)", () => {
  test("shelf scoping: magnesium (only supplements entry) has an empty pool once excluded", () => {
    const result = getExploreNextCategories("magnesium", 4);
    expect(result).toEqual([]);
  });

  test("shelf scoping: a supermarket page never surfaces the supplements-shelf magnesium card", () => {
    for (const c of EXPLORE_NEXT_CATEGORIES) {
      if (c.shelf !== "supermarket") continue;
      const result = getExploreNextCategories(c.id, 17); // ask for everything
      expect(result.some((r) => r.id === "magnesium")).toBe(false);
      expect(result.every((r) => r.shelf === "supermarket")).toBe(true);
    }
  });

  test("family de-dup cap: brined-cheeses' rotation would naturally hit both cheese-family duplicates; the cap must skip one and backfill", () => {
    // Rotation from brined-cheeses at count=8 reaches, in order: cakes, cheese
    // (family "cheese"), chocolate-bars, chocolate-tablets, cookies-coffee,
    // crackers, granola, hard-cheeses (family "cheese" — the duplicate). Without
    // the cap this 8th slot would be hard-cheeses; with the cap it must be
    // skipped and backfilled by the next candidate (hummus).
    const result = getExploreNextCategories("brined-cheeses", 8);
    expect(result).toHaveLength(8);
    const cheeseFamilyMembers = result.filter((r) => r.family === "cheese");
    expect(cheeseFamilyMembers).toHaveLength(1);
    expect(result.some((r) => r.id === "hard-cheeses")).toBe(false);
    expect(result.some((r) => r.id === "hummus")).toBe(true); // backfilled in
  });

  test("family de-dup cap does not apply to untagged categories (no false-positive capping)", () => {
    const result = getExploreNextCategories("bread", 17);
    // bread, breakfast-cereals, cakes, chocolate-bars, etc. are all untagged —
    // every one of them must still appear (only cheese-family and self/shelf are filtered).
    const untaggedIds = EXPLORE_NEXT_CATEGORIES.filter(
      (c) => c.shelf === "supermarket" && !c.family && c.id !== "bread"
    ).map((c) => c.id);
    for (const id of untaggedIds) {
      expect(result.some((r) => r.id === id)).toBe(true);
    }
  });
});

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

  test("card CTA uses the Content-approved copy 'להשוואה', not the old 'לכל ההשוואות'", async ({
    page,
  }) => {
    await page.goto("/hashvaot/snacks");
    const heading = page.getByRole("heading", { name: "עוד השוואות" });
    const section = page.locator("section", { has: heading });
    await expect(section.getByText("להשוואה", { exact: true }).first()).toBeVisible();
    await expect(section.getByText("לכל ההשוואות")).toHaveCount(0);
  });

  test("magnesium page (only supplements-shelf category): module renders NOTHING, no fallback to the supermarket pool", async ({
    page,
  }) => {
    await page.goto("/hashvaot/magnesium");
    await expect(page.getByRole("heading", { name: "עוד השוואות" })).toHaveCount(0);
  });
});
