"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  DAIRY_PROTEIN_METRIC,
  SUGAR_METRIC,
} from "@/components/shared/comparison-metric-column";
import type { BariProductVM } from "@/lib/view-models";

export interface YogurtDrinksComparisonPageProps {
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
// "ל-100 גרם" (verified across all 20 products), unlike milk/juices which are measured
// per 100ml. Reuse DAIRY_PROTEIN_METRIC's numeric thresholds (scaleMax 8 / good 5 / poor 2
// — a close match to this shelf's real 1.9–8.4g protein range) and SUGAR_METRIC's
// (scaleMax 15 / good 5 / poor 10 — matches this shelf's real 2.7–12g sugar range), but
// override the per-100ml unit strings to the correct per-100g basis. Protein + sugar are
// the headline pair the page_copy prologue and caveat both discuss (protein-via-additives
// vs. sugar-via-fruit tradeoff).
const YOGURT_DRINKS_METRIC_SPECS = [
  { ...DAIRY_PROTEIN_METRIC, perLabel: "ל-100 ג׳", ariaUnit: "גרם חלבון ל-100 גרם" },
  { ...SUGAR_METRIC, perLabel: "ל-100 ג׳", ariaUnit: "גרם סוכר ל-100 גרם" },
] as const;

const yogurtDrinksShelfFilters = {
  lensOptions: [],
  filterProducts: (products: BariProductVM[]) => products,
};

export function YogurtDrinksComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: YogurtDrinksComparisonPageProps) {
  return (
    <ComparisonPage
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={yogurtDrinksShelfFilters}
      metricSpecs={YOGURT_DRINKS_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="yogurt-drinks"
    />
  );
}
