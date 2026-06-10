"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { FIBER_METRIC } from "@/components/shared/comparison-metric-column";
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

// Fiber is the key differentiator in the salty-snacks category — it separates
// baked-legume snacks (12g fiber) from extruded puffs and plain chips (0–2g).
// Scale 0–15 fits the real shelf range; thresholds ≥6g good / <2g poor.
const SALTY_SNACKS_METRIC_SPECS = [
  {
    ...FIBER_METRIC,
    scaleMax: 15,
    good: 6,
    poor: 2,
  },
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
