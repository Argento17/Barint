"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
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

// No metric bar for vegetable spreads (Design ruling, TASK-168 follow-up). Protein (0.7–2.2g
// here) is the category's least-relevant signal and a protein bar mis-signals that these
// spreads are protein-driven (grounding §2 forbids that). The real differentiator — sodium —
// is already stated, with the number, in each row's verdict, so a bar would only duplicate it.
// "No bar" matches the snacks precedent. The hummus page keeps its protein bar; only this
// (filtered) view drops it.
const VEGETABLE_SPREADS_METRIC_SPECS = [] as const;

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
