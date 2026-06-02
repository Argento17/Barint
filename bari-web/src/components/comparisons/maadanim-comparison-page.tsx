"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { PROTEIN_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterMaadanimProducts,
  MAADANIM_SHELF_LENS_OPTIONS,
  type MaadanimShelfFilterId,
} from "@/lib/comparisons/maadanim-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface MaadanimComparisonPageProps {
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

const maadanimShelfFilters = {
  lensOptions: MAADANIM_SHELF_LENS_OPTIONS,
  filterProducts: filterMaadanimProducts,
} as const;

// Protein is the maadanim headline metric (prologue is explicit) — same single-metric
// front-of-row as hummus. Sugar is not consistently available here (source-data gap).
const MAADANIM_METRIC_SPECS = [PROTEIN_METRIC] as const;

export function MaadanimComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: MaadanimComparisonPageProps) {
  return (
    <ComparisonPage<MaadanimShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={maadanimShelfFilters}
      metricSpecs={MAADANIM_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
