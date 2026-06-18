"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { DAIRY_PROTEIN_METRIC } from "@/components/shared/comparison-metric-column";
import type { BariProductVM } from "@/lib/view-models";

export interface CheeseComparisonPageProps {
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

const cheeseShelfFilters = {
  lensOptions: [] as Array<{ id: string; label: string }>,
  filterProducts: (products: BariProductVM[]) => products,
};

const CHEESE_METRIC_SPECS = [DAIRY_PROTEIN_METRIC] as const;

export function CheeseComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: CheeseComparisonPageProps) {
  return (
    <ComparisonPage
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={cheeseShelfFilters}
      metricSpecs={CHEESE_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
