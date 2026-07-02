"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { FIBER_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterCrackersProducts,
  CRACKERS_SHELF_LENS_OPTIONS,
  type CrackersShelfFilterId,
} from "@/lib/comparisons/crackers-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface CrackersComparisonPageProps {
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

const crackersShelfFilters = {
  lensOptions: CRACKERS_SHELF_LENS_OPTIONS,
  filterProducts: filterCrackersProducts,
} as const;

// Fiber is the crackers row metric, same rationale as bread (TASK-162): grain-based
// category, fiber is the meaningful headline number, mirrors the whole/mixed/refined-grain
// shelf clusters. Display-only, no score change.
const CRACKERS_METRIC_SPECS = [FIBER_METRIC] as const;

export function CrackersComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: CrackersComparisonPageProps) {
  return (
    <ComparisonPage<CrackersShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={crackersShelfFilters}
      metricSpecs={CRACKERS_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
