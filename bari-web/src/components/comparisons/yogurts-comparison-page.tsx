"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { DAIRY_PROTEIN_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterYogurtsProducts,
  YOGURTS_SHELF_LENS_OPTIONS,
  type YogurtsShelfFilterId,
} from "@/lib/comparisons/yogurts-shelf-filters";
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
  /** Single category-wide caveat, shown once in the header (cheese gold-standard format). */
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

const yogurtsShelfFilters = {
  lensOptions: YOGURTS_SHELF_LENS_OPTIONS,
  filterProducts: filterYogurtsProducts,
} as const;

// Protein is the yogurt row metric (TASK-161A). Dairy-tuned scale (scaleMax 8) rather than
// hummus's 0–20 — dairy protein tops ~12g, so the hummus scale would flatten bars
// (Nutrition note 161A #1).
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
    <ComparisonPage<YogurtsShelfFilterId>
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
