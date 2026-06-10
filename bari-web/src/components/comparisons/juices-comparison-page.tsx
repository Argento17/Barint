"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { SUGAR_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterJuicesProducts,
  JUICES_SHELF_LENS_OPTIONS,
  type JuicesShelfFilterId,
} from "@/lib/comparisons/juices-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface JuicesComparisonPageProps {
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

const juicesShelfFilters = {
  lensOptions: JUICES_SHELF_LENS_OPTIONS,
  filterProducts: filterJuicesProducts,
} as const;

// Sugar per 100ml is the core consumer insight for juices. The shelf range is
// 1.75–16.8g/100ml — the scale 0–18 keeps the top end from clipping.
// Lower sugar is better: ≤5g is green (low-sugar citrus), ≥12g is amber.
// ariaUnit says "ל-100 מ"ל" because juice is measured by volume (unique in Bari).
const JUICES_METRIC_SPECS = [
  {
    ...SUGAR_METRIC,
    perLabel: "ל-100 מ״ל",
    scaleMax: 18,
    good: 5,
    poor: 12,
    lowerIsBetter: true as const,
    ariaUnit: "גרם סוכר ל-100 מ״ל",
  },
] as const;

export function JuicesComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: JuicesComparisonPageProps) {
  return (
    <ComparisonPage<JuicesShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={juicesShelfFilters}
      metricSpecs={JUICES_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="juices"
    />
  );
}
