"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { DAIRY_PROTEIN_METRIC } from "@/components/shared/comparison-metric-column";
import type { BariProductVM } from "@/lib/view-models";

export interface YogurtsComparisonPageProps {
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

const yogurtsShelfFilters = {
  lensOptions: [] as Array<{ id: string; label: string }>,
  filterProducts: (products: BariProductVM[]) => products,
};

// Protein is the yogurt row metric.
const YOGURTS_METRIC_SPECS = [DAIRY_PROTEIN_METRIC] as const;

export function YogurtsComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: YogurtsComparisonPageProps) {
  return (
    <ComparisonPage
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={yogurtsShelfFilters}
      metricSpecs={YOGURTS_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
