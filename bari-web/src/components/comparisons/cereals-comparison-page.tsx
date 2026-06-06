"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  filterCerealsProducts,
  CEREALS_SHELF_LENS_OPTIONS,
  type CerealsShelfFilterId,
} from "@/lib/comparisons/cereals-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface CerealsComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  /** Single category-wide caveat, shown once in the header (standard format). */
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

const cerealsShelfFilters = {
  lensOptions: CEREALS_SHELF_LENS_OPTIONS,
  filterProducts: filterCerealsProducts,
} as const;

// No headline metric: cereals don't have a single dominant numeric signal
// (fiber and protein both matter, sugar is inconsistently available).
// metricSpecs=[] keeps the row compact — same posture as snack bars.
const CEREALS_METRIC_SPECS = [] as const;

export function CerealsComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: CerealsComparisonPageProps) {
  return (
    <ComparisonPage<CerealsShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={cerealsShelfFilters}
      metricSpecs={CEREALS_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="breakfast-cereals"
    />
  );
}
