"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  PROTEIN_BAR_PROTEIN_METRIC,
  PROTEIN_BAR_SUGAR_METRIC,
} from "@/components/shared/comparison-metric-column";
import {
  filterProteinBarsProducts,
  PROTEIN_BARS_SHELF_LENS_OPTIONS,
  type ProteinBarsShelfFilterId,
} from "@/lib/comparisons/protein-bars-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

// TASK-365: protein-bar metric specs — tuned to the 23–36g protein / 1.7–35g sugar
// shelf range. scaleMax=40 for both so bars differentiate instead of pegging at 100%.
const PROTEIN_BAR_METRIC_SPECS = [
  PROTEIN_BAR_PROTEIN_METRIC,
  PROTEIN_BAR_SUGAR_METRIC,
] as const;

export interface ProteinBarsComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: { eyebrow: string; title: string };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

const proteinBarsShelfFilters = {
  lensOptions: PROTEIN_BARS_SHELF_LENS_OPTIONS,
  filterProducts: filterProteinBarsProducts,
} as const;

export function ProteinBarsComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: ProteinBarsComparisonPageProps) {
  return (
    <ComparisonPage<ProteinBarsShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={proteinBarsShelfFilters}
      metricSpecs={PROTEIN_BAR_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="protein-bars"
      exploreNextCategoryId="protein-bars"
    />
  );
}
