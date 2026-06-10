"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { PROTEIN_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterHardCheesesProducts,
  HARD_CHEESES_SHELF_LENS_OPTIONS,
  type HardCheesesShelfFilterId,
} from "@/lib/comparisons/hard-cheeses-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface HardCheesesComparisonPageProps {
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

const hardCheesesShelfFilters = {
  lensOptions: HARD_CHEESES_SHELF_LENS_OPTIONS,
  filterProducts: filterHardCheesesProducts,
} as const;

// Protein per 100g is the headline metric for hard cheeses — a genuine differentiator
// (20–28g/100g for solid yellows vs 12–16g for processed/light).
// Scale 0–32 covers the full shelf range including grating cheeses (30–36g).
// ≥22g = good (typical solid cheese); <15g = poor (processed/stabiliser-heavy).
const HARD_CHEESES_METRIC_SPECS = [
  {
    ...PROTEIN_METRIC,
    scaleMax: 32,
    good: 22,
    poor: 15,
  },
] as const;

export function HardCheesesComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: HardCheesesComparisonPageProps) {
  return (
    <ComparisonPage<HardCheesesShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={hardCheesesShelfFilters}
      metricSpecs={HARD_CHEESES_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="hard-cheeses"
    />
  );
}
