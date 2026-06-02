"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  DAIRY_PROTEIN_METRIC,
  SUGAR_METRIC,
} from "@/components/shared/comparison-metric-column";
import { milkShelfFilters } from "@/lib/comparisons/milk-comparison-page-data";
import type { MilkShelfFilterId } from "@/lib/comparisons/milk-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface MilkComparisonPageProps {
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
  blogLink?: { href: string; label: string };
  initialExpandedProductId?: string | null;
}

// Milk's headline metrics are protein + sugar — both real per-100ml label data. Sugar is
// a genuine dairy signal (unlike hummus, where it is suppressed). additive_count is NOT a
// numeric field in the milk data (only a textual additivesLabel) → not fabricated.
const MILK_METRIC_SPECS = [DAIRY_PROTEIN_METRIC, SUGAR_METRIC] as const;

export function MilkComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  blogLink,
  initialExpandedProductId = null,
}: MilkComparisonPageProps) {
  return (
    <ComparisonPage<MilkShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={milkShelfFilters}
      metricSpecs={MILK_METRIC_SPECS}
      categoryNote={categoryNote}
      blogLink={blogLink}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
