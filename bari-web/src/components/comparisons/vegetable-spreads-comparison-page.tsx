"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { VEG_PROTEIN_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterVegetableSpreadsProducts,
  VEGETABLE_SPREADS_SHELF_LENS_OPTIONS,
  type VegetableSpreadsShelfFilterId,
} from "@/lib/comparisons/vegetable-spreads-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface VegetableSpreadsComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  /** Single category-wide caveat, shown once in the header (cheese gold-standard format). */
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

const vegetableSpreadsShelfFilters = {
  lensOptions: VEGETABLE_SPREADS_SHELF_LENS_OPTIONS,
  filterProducts: filterVegetableSpreadsProducts,
} as const;

// Protein is the vegetable-spread row metric (TASK-161A). Uses VEG_PROTEIN_METRIC (TASK-165),
// NOT the hummus PROTEIN_METRIC nor the dairy preset: these spreads draw from the hummus corpus
// (protein is per 100 GRAMS) but run only 0.7–6.3g, so the 0–20g hummus scale flattened every bar.
// VEG_PROTEIN_METRIC drops scaleMax to 7 so the bars discriminate, while keeping the per-100g
// aria unit (these are solids — DAIRY_PROTEIN_METRIC's "ל-100 מ״ל" would be factually wrong).
const VEGETABLE_SPREADS_METRIC_SPECS = [VEG_PROTEIN_METRIC] as const;

export function VegetableSpreadsComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: VegetableSpreadsComparisonPageProps) {
  return (
    <ComparisonPage<VegetableSpreadsShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={vegetableSpreadsShelfFilters}
      metricSpecs={VEGETABLE_SPREADS_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
