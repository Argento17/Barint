"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { FIBER_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterFrozenVegetablesProducts,
  FROZEN_VEGETABLES_SHELF_LENS_OPTIONS,
  type FrozenVegetablesShelfFilterId,
} from "@/lib/comparisons/frozen-vegetables-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface FrozenVegetablesComparisonPageProps {
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

const frozenVegetablesShelfFilters = {
  lensOptions: FROZEN_VEGETABLES_SHELF_LENS_OPTIONS,
  filterProducts: filterFrozenVegetablesProducts,
} as const;

const FROZEN_VEGETABLES_METRIC_SPECS = [FIBER_METRIC] as const;

export function FrozenVegetablesComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: FrozenVegetablesComparisonPageProps) {
  return (
    <ComparisonPage<FrozenVegetablesShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={frozenVegetablesShelfFilters}
      metricSpecs={FROZEN_VEGETABLES_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
