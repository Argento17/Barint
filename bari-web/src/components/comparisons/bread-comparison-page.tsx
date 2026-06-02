"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { FIBER_METRIC } from "@/components/shared/comparison-metric-column";
import {
  filterBreadProducts,
  BREAD_SHELF_LENS_OPTIONS,
  type BreadShelfFilterId,
} from "@/lib/comparisons/bread-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface BreadComparisonPageProps {
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

const breadShelfFilters = {
  lensOptions: BREAD_SHELF_LENS_OPTIONS,
  filterProducts: filterBreadProducts,
} as const;

// Fiber is the bread row metric (TASK-162): Nutrition decided fiber is the more meaningful
// headline number for bread. The real per-100g fiber value is now plumbed into the metrics
// view-model (fiber_g) and populated by the bread data builder — display-only, no score change.
const BREAD_METRIC_SPECS = [FIBER_METRIC] as const;

export function BreadComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: BreadComparisonPageProps) {
  return (
    <ComparisonPage<BreadShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={breadShelfFilters}
      metricSpecs={BREAD_METRIC_SPECS}
      categoryNote={categoryNote}
      blogLink={{
        href: "/research/bread-transparency-shufersal",
        label: "קראו את הניתוח בבלוג ←",
      }}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
