"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  filterProteinBarsProducts,
  PROTEIN_BARS_SHELF_LENS_OPTIONS,
  type ProteinBarsShelfFilterId,
} from "@/lib/comparisons/protein-bars-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

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
      metricSpecs={[]}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="protein-bars"
    />
  );
}
