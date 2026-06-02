"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  filterSnacksProducts,
  SNACKS_SHELF_LENS_OPTIONS,
  type SnacksShelfFilterId,
} from "@/lib/comparisons/snacks-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface SnacksComparisonPageProps {
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

const snacksShelfFilters = {
  lensOptions: SNACKS_SHELF_LENS_OPTIONS,
  filterProducts: filterSnacksProducts,
} as const;

export function SnacksComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: SnacksComparisonPageProps) {
  return (
    <ComparisonPage<SnacksShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={snacksShelfFilters}
      metricSpecs={[]}
      categoryNote={categoryNote}
      blogLink={{
        href: "/blog/snack-bars-flagship",
        label: "קראו את הניתוח העיתונאי בבלוג ←",
      }}
      initialExpandedProductId={initialExpandedProductId}
    />
  );
}
