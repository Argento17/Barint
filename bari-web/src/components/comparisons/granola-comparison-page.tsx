"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { FIBER_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterGranolaProducts,
  GRANOLA_SHELF_LENS_OPTIONS,
  type GranolaShelfFilterId,
} from "@/lib/comparisons/granola-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface GranolaComparisonPageProps {
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

const granolaShelfFilters = {
  lensOptions: GRANOLA_SHELF_LENS_OPTIONS,
  filterProducts: filterGranolaProducts,
} as const;

// Fiber is granola's headline differentiator — it separates real whole-grain products
// from sugared clusters. Scale 0–20g matches the bread fiber range; thresholds ≥7g good
// / <4g poor are calibrated to the real shelf range (~4–12g for granola).
const GRANOLA_METRIC_SPECS = [FIBER_METRIC] as const;

export function GranolaComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: GranolaComparisonPageProps) {
  return (
    <ComparisonPage<GranolaShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={granolaShelfFilters}
      metricSpecs={GRANOLA_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="granola"
    />
  );
}
