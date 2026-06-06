// Reference implementation for Bari Gen 1 comparison categories.
// New categories: copy this file, rename, update data import.
"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { PROTEIN_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterHummusProducts,
  HUMMUS_SHELF_LENS_OPTIONS,
  type HummusShelfFilterId,
} from "@/lib/comparisons/hummus-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface HummusComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  /** IMP-6: single category-wide caveat (the fat-data note), shown once in the header. */
  categoryNote?: string;
  initialExpandedProductId?: string | null;
  /** TASK-181Q: when true + NEXT_PUBLIC_GLASSBOX_W5=on, appends the Glass Box methodology link. */
  glassBoxMethodologyLink?: boolean;
}

const hummusShelfFilters = {
  lensOptions: HUMMUS_SHELF_LENS_OPTIONS,
  filterProducts: filterHummusProducts,
} as const;

// Hummus features protein as its single headline metric — the prologue is explicit
// that protein is the chosen front-of-row signal for this category. additive_count /
// base_pct are not in the source data yet (Data Agent dependency); we do not fabricate.
const HUMMUS_METRIC_SPECS = [PROTEIN_METRIC] as const;

export function HummusComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
  glassBoxMethodologyLink = false,
}: HummusComparisonPageProps) {
  return (
    <ComparisonPage<HummusShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={hummusShelfFilters}
      metricSpecs={HUMMUS_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="hummus"
      glassBoxMethodologyLink={glassBoxMethodologyLink}
    />
  );
}
