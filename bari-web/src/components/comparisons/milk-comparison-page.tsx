"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  DAIRY_PROTEIN_METRIC,
  SUGAR_METRIC,
} from "@/components/shared/comparison-metric-column";
import { milkShelfFilters } from "@/lib/comparisons/milk-page-data";
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
  categoryNote?: string;
  blogLink?: { href: string; label: string };
  initialExpandedProductId?: string | null;
}

// Milk's headline metrics are protein + sugar — both real per-100ml label data.
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
    <ComparisonPage
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={milkShelfFilters}
      metricSpecs={MILK_METRIC_SPECS}
      categoryNote={categoryNote}
      exploreNextCategoryId="milk-comparison"
      blogLink={blogLink}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
