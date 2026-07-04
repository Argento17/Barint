"use client";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  filterChocolateTabletsProducts,
  CHOCOLATE_TABLETS_SHELF_LENS_OPTIONS,
  type ChocolateTabletsShelfFilterId,
} from "@/lib/comparisons/chocolate-tablets-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface ChocolateTabletsComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: { eyebrow: string; title: string };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

const chocolateTabletsShelfFilters = {
  lensOptions: CHOCOLATE_TABLETS_SHELF_LENS_OPTIONS,
  filterProducts: filterChocolateTabletsProducts,
} as const;

export function ChocolateTabletsComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: ChocolateTabletsComparisonPageProps) {
  return (
    <ComparisonPage<ChocolateTabletsShelfFilterId>
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={chocolateTabletsShelfFilters}
      metricSpecs={[]}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="chocolate-tablets"
      exploreNextCategoryId="chocolate-tablets"
    />
  );
}
