/**
 * TASK-534 — codified rule for `BariProductThumbnail`'s `blendWhite` prop.
 *
 * Owner finding (2026-07-08, reviewing live yogurt pages): "I see white backgrounds
 * here guys, we discussed about it. Codify it please." Some categories' product photos
 * are retail/e-commerce shots with a baked-in solid white background (supplement bottles,
 * yogurt tubs/cartons). Rendered inside the standard cream (#F7F7F2) thumbnail tile, that
 * baked-in white reads as a mismatched "white box inside a cream tile." `blendWhite` swaps
 * the tile fill to pure white so the photo's background dissolves into the tile instead
 * (border + shadow are unchanged — see bari-product-thumbnail.tsx).
 *
 * Before this file existed, `blendWhite` was a manual boolean set per call site
 * (`category === "magnesium"` hardcoded inline in comparison-row.tsx). Yogurt shipped
 * with the mismatch because nobody flipped that inline check for the new category — a
 * failure mode of omission, not a one-off bug.
 *
 * This file is now the ONLY place that decides which categories get the treatment. Every
 * surface that renders a category's product photos — comparison table rows
 * (comparison-row.tsx), the GLP-1 guide shortlist (yogurt-glp1-guide-page.tsx), and any
 * future surface — MUST resolve `blendWhite` through `shouldBlendWhiteForCategory()`
 * rather than re-deriving it locally. Register a new retail-photo category by adding its
 * slug to the set below; every current and future call site picks it up automatically.
 *
 * Do not add a second `category === "..."` check anywhere in the codebase — grep for
 * `shouldBlendWhiteForCategory` to find every consumer before changing this contract.
 */

/**
 * Category slugs whose product photography has a baked-in white background. Slugs match
 * the `category` string each comparison page passes into `<ComparisonPage category="...">`
 * (see e.g. magnesium-comparison-page.tsx, yogurt-spoonable-comparison-page.tsx,
 * yogurt-drinks-comparison-page.tsx).
 */
const BLEND_WHITE_CATEGORIES: ReadonlySet<string> = new Set([
  "magnesium",
  "yogurt-spoonable",
  "yogurt-drinks",
]);

/**
 * Resolves whether a category's product thumbnails should blend a white photo background
 * into a white tile fill (`blendWhite=true`) instead of the default cream tile. Categories
 * not in `BLEND_WHITE_CATEGORIES` — and any call site that omits `category` — resolve to
 * `false`, which renders byte-identical to pre-TASK-534 behavior.
 */
export function shouldBlendWhiteForCategory(category: string | undefined | null): boolean {
  if (!category) return false;
  return BLEND_WHITE_CATEGORIES.has(category);
}
