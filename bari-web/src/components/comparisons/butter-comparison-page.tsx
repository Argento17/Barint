"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  filterButterProducts,
  BUTTER_SHELF_LENS_OPTIONS,
  type ButterShelfFilterId,
} from "@/lib/comparisons/butter-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface ButterComparisonPageProps {
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

const butterShelfFilters = {
  lensOptions: BUTTER_SHELF_LENS_OPTIONS,
  filterProducts: filterButterProducts,
} as const;

// No single dominant numeric headline metric for butter — purity of ingredients
// is the signal, not a scalar nutrient. metricSpecs=[] keeps the row compact.
const BUTTER_METRIC_SPECS = [] as const;

export function ButterComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: ButterComparisonPageProps) {
  return (
    <ComparisonPage<ButterShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={butterShelfFilters}
      metricSpecs={BUTTER_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="butter"
    />
  );
}
