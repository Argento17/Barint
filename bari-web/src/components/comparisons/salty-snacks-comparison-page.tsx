"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  FIBER_METRIC,
  SODIUM_METRIC,
} from "@/components/shared/comparison-metric-column";
import {
  filterSaltySnacksProducts,
  SALTY_SNACKS_SHELF_LENS_OPTIONS,
  type SaltySnacksShelfFilterId,
} from "@/lib/comparisons/salty-snacks-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface SaltySnacksComparisonPageProps {
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

const saltySnacksShelfFilters = {
  lensOptions: SALTY_SNACKS_SHELF_LENS_OPTIONS,
  filterProducts: filterSaltySnacksProducts,
} as const;

// Two headline numbers for the salty-snacks shelf, shown column-aligned:
//  • Fiber separates baked-legume snacks (12g) from extruded puffs/plain chips (0–2g).
//    Scale 0–15 fits the real shelf range; ≥6g good / <2g poor.
//  • Sodium is what separates a clean snack from a salt-loaded one — real per-100g range
//    is ~10–920mg (median 560). Lower is better; ≤300mg good / ≥600mg a visible limit.
const SALTY_SNACKS_METRIC_SPECS = [
  {
    ...FIBER_METRIC,
    scaleMax: 15,
    good: 6,
    poor: 2,
  },
  SODIUM_METRIC,
] as const;

export function SaltySnacksComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: SaltySnacksComparisonPageProps) {
  return (
    <ComparisonPage<SaltySnacksShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={saltySnacksShelfFilters}
      metricSpecs={SALTY_SNACKS_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="salty-snacks"
    />
  );
}
