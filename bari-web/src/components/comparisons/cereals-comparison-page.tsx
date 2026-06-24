"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  CEREALS_SUGAR_METRIC,
  PROTEIN_METRIC,
} from "@/components/shared/comparison-metric-column";
import {
  filterCerealsProducts,
  CEREALS_SHELF_LENS_OPTIONS,
  type CerealsShelfFilterId,
} from "@/lib/comparisons/cereals-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface CerealsComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  /** Single category-wide caveat, shown once in the header (standard format). */
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

const cerealsShelfFilters = {
  lensOptions: CEREALS_SHELF_LENS_OPTIONS,
  filterProducts: filterCerealsProducts,
} as const;

// TASK-387: sugar + protein added as headline metric pair (mirrors the granola pattern).
//
// SUGAR (CEREALS_SUGAR_METRIC): shelf range 3.8–29.9g/100g. Most products cluster at
//   16–29g; only 2 products fall below 8g. scaleMax=32 gives the 29.9g top product room
//   without clipping. Thresholds match the Israeli MoH anchor (≤8g good, ≥18g amber).
//   1 product (barcode 7297488098688) has sugar=null → bar shows "—" (correct).
//
// PROTEIN (CEREALS_PROTEIN_METRIC): cereals protein range is 5.0–12.0g/100g — much
//   narrower and lower than granola (8.7–23.7g). The shared PROTEIN_METRIC (scaleMax=20)
//   would compress every cereals bar into the bottom 60% of the track, losing all
//   discrimination. Cereals-tuned override:
//     scaleMax=14 — 12.0g top reads at ~86%, leaving headroom without clipping.
//     good ≥10g   — only 1 product clears this (Weetabix at 12g); marks genuine outlier.
//     poor ≤7g    — below the shelf median (8.3g); marks the lower cluster (5 products).
//   neutralBarFill: "#7A817C" — mid-band (7–10g) bars otherwise near-invisible on track.
//   All 20 products have protein values (0 null).
const CEREALS_PROTEIN_METRIC = {
  ...PROTEIN_METRIC,
  perLabel: "ל-100 ג׳",
  scaleMax: 14,
  good: 10,
  poor: 7,
  neutralBarFill: "#7A817C",
} as const;

const CEREALS_METRIC_SPECS = [CEREALS_SUGAR_METRIC, CEREALS_PROTEIN_METRIC] as const;

export function CerealsComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: CerealsComparisonPageProps) {
  return (
    <ComparisonPage<CerealsShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={cerealsShelfFilters}
      metricSpecs={CEREALS_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="breakfast-cereals"
    />
  );
}
