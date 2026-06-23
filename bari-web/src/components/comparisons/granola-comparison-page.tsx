"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  GRANOLA_SUGAR_METRIC,
  PROTEIN_METRIC,
} from "@/components/shared/comparison-metric-column";
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

// TASK-385: sugar + protein replace fiber as the headline pair.
// Fiber was gameable via added chicory/inulin and caused fiber-vs-grade inversions
// (high-fiber products did not reliably land at higher grades on this shelf).
//
// SUGAR (GRANOLA_SUGAR_METRIC): lowerIsBetter; shelf range 4.8–25g/100g; scaleMax 28
//   so the 25g outlier reads near-full without false-clipping. ≤8g = good; ≥18g = amber
//   (the Israeli MoH 17.5g red-label threshold as the "poor" anchor). Per §4.3: amber
//   only — limits are information, not alarms.
//
// PROTEIN: shelf range 8.7–23.7g/100g. The shared PROTEIN_METRIC has scaleMax=20 which
//   clips the 23.7g top product. Override with a granola-tuned scale: scaleMax 25,
//   good ≥15g (genuinely high-protein for a granola), poor ≤10g (below the shelf median).
const GRANOLA_PROTEIN_METRIC = {
  ...PROTEIN_METRIC,
  scaleMax: 25,
  good: 15,
  poor: 10,
  // Match the sugar bar: mid-band (10–15g) protein values otherwise render as a faint
  // neutral bar (#B5BBB6 on #ECECE7). Darker neutral fill keeps both bars visible
  // for the glancing reader (owner live-review note, TASK-385). Granola-scoped only —
  // the shared PROTEIN_METRIC is untouched so other categories don't change.
  neutralBarFill: "#7A817C",
} as const;

const GRANOLA_METRIC_SPECS = [GRANOLA_SUGAR_METRIC, GRANOLA_PROTEIN_METRIC] as const;

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
