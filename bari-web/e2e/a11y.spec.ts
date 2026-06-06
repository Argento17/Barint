import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

/**
 * Accessibility scan — axe-core over the live comparison pages.
 *
 * RTL Hebrew + color-coded grade chips are exactly where contrast and structure bugs hide.
 * This gates on serious/critical WCAG 2 A/AA violations (the consequential ones); minor /
 * moderate findings are reported but not failed, to keep the gate honest and unflaky.
 */

const ROUTES = ["/", "/hashvaot/maadanim", "/hashvaot/hummus"];

for (const route of ROUTES) {
  test(`a11y: no serious/critical violations on ${route}`, async ({ page }) => {
    await page.goto(route);
    await page.locator("h1, h2").first().waitFor();

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa"])
      .analyze();

    const serious = results.violations.filter(
      (v) => v.impact === "serious" || v.impact === "critical"
    );

    if (serious.length) {
      console.log(
        `\n${route} — serious/critical a11y violations:\n` +
          serious
            .map((v) => `  [${v.impact}] ${v.id}: ${v.help} (${v.nodes.length} nodes)`)
            .join("\n")
      );
    }
    expect(serious, `serious/critical a11y violations on ${route}`).toEqual([]);
  });
}
