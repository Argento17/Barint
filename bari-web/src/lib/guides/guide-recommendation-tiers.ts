// Recommendation-tier derivation (TASK-504 follow-on).
//
// Rule source (governed, dual-keyed Nutrition + Product):
//   01_framework/nutrition/supplement_guides_bar_rubric_v1.yaml
//   `recommendation_tier_mapping` / `passes_with_flag_split_rule_v2` (id: dose_adequacy_sole_caveat)

import type { GuideBarKey, GuideProductVM, GuideRecommendationTier } from "@/lib/view-models";

/** Bars that participate in the tier-gating predicate (displayed minus band-excluded). */
export function gatingBarsForTier(
  displayedBars: readonly GuideBarKey[],
  bandExcludedBars: readonly GuideBarKey[]
): GuideBarKey[] {
  if (bandExcludedBars.length === 0) return [...displayedBars];
  const excluded = new Set(bandExcludedBars);
  return displayedBars.filter((bar) => !excluded.has(bar));
}

/** Non-PASS bar keys among gating bars — the v2 split predicate operates only here. */
export function nonPassGatingBars(
  product: Pick<GuideProductVM, "bars">,
  gatingBars: readonly GuideBarKey[]
): GuideBarKey[] {
  const barByKey = new Map(product.bars.map((b) => [b.bar, b] as const));
  return gatingBars.filter((bar) => barByKey.get(bar)?.state !== "pass");
}

/**
 * v2 subset test: `recommended` (band B) when nonPassDisplayed ⊆ {doseAdequacy}.
 * Implemented as `.every(b => b === "doseAdequacy")` — empty set OR {dose} only.
 */
export function isPassesWithFlagRecommendedBand(nonPassDisplayed: readonly GuideBarKey[]): boolean {
  return nonPassDisplayed.every((bar) => bar === "doseAdequacy");
}

/**
 * Returns the ranked tier for a product, or `null` when the product belongs to the
 * `cannot_assess` bucket — those products render in a separate, out-of-tier section.
 */
export function computeRecommendationTier(
  product: Pick<GuideProductVM, "bucket" | "bars">,
  displayedBars: readonly GuideBarKey[],
  bandExcludedBars: readonly GuideBarKey[] = []
): GuideRecommendationTier | null {
  switch (product.bucket) {
    case "clears_all":
      return "very_recommended";
    case "fails":
      return "not_recommended";
    case "cannot_assess":
      return null;
    case "passes_with_flag": {
      const gating = gatingBarsForTier(displayedBars, bandExcludedBars);
      const nonPassDisplayed = nonPassGatingBars(product, gating);
      return isPassesWithFlagRecommendedBand(nonPassDisplayed) ? "recommended" : "good";
    }
  }
}
