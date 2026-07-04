"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  filterChocolateBarsProducts,
  CHOCOLATE_BARS_SHELF_LENS_OPTIONS,
  type ChocolateBarsShelfFilterId,
} from "@/lib/comparisons/chocolate-bars-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface ChocolateBarsComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: { eyebrow: string; title: string };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

const chocolateBarsShelfFilters = {
  lensOptions: CHOCOLATE_BARS_SHELF_LENS_OPTIONS,
  filterProducts: filterChocolateBarsProducts,
} as const;

export function ChocolateBarsComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: ChocolateBarsComparisonPageProps) {
  return (
    <ComparisonPage<ChocolateBarsShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={chocolateBarsShelfFilters}
      metricSpecs={[]}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="chocolate-bars"
      exploreNextCategoryId="chocolate-bars"
    />
  );
}
