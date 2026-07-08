"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  SPOONABLE_PROTEIN_METRIC,
  SUGAR_METRIC,
} from "@/components/shared/comparison-metric-column";
import type { BariProductVM } from "@/lib/view-models";

export interface YogurtSpoonableComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

// This corpus's nutrition is per-100g — every product's expansion.servingNote reads
// "ל-100 גרם" (same basis as yogurt-drinks), NOT per-100ml like milk/juices.
// SPOONABLE_PROTEIN_METRIC (comparison-metric-column.tsx) is a dedicated scale — the
// shelf's real 2.5–13.1g protein range would clip badly under the drinkable-tuned
// 0–8g DAIRY_PROTEIN_METRIC (23/78 products exceed 8g). SUGAR_METRIC's numeric
// thresholds (scaleMax 15 / good 5 / poor 10) fit this shelf's real 1.0–14.8g sugar
// range without adjustment; only its per-100ml unit strings are overridden to the
// correct per-100g basis. Protein + sugar are the headline pair the page_copy prologue
// and caveat both discuss.
const YOGURT_SPOONABLE_METRIC_SPECS = [
  SPOONABLE_PROTEIN_METRIC,
  { ...SUGAR_METRIC, perLabel: "ל-100 ג׳", ariaUnit: "גרם סוכר ל-100 גרם" },
] as const;

const yogurtSpoonableShelfFilters = {
  lensOptions: [],
  filterProducts: (products: BariProductVM[]) => products,
};

export function YogurtSpoonableComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: YogurtSpoonableComparisonPageProps) {
  return (
    <ComparisonPage
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={yogurtSpoonableShelfFilters}
      metricSpecs={YOGURT_SPOONABLE_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="yogurt-spoonable"
    />
  );
}
