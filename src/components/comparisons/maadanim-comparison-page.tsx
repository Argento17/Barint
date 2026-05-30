"use client";

import {
  BariComparisonDesktopPage,
  productInsightLines,
} from "@/components/comparisons/bari-comparison-desktop-page";
import { ComparisonShelfPage } from "@/components/comparisons/comparison-shelf-page";
import { maadanimCorpusMeta } from "@/lib/comparisons/maadanim-page-data";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  filterMaadanimProducts,
  MAADANIM_SHELF_LENS_OPTIONS,
  type MaadanimShelfFilterId,
} from "@/lib/comparisons/maadanim-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface MaadanimComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  initialExpandedProductId?: string | null;
}

const maadanimShelfFilters = {
  lensOptions: MAADANIM_SHELF_LENS_OPTIONS,
  filterProducts: filterMaadanimProducts,
} as const;

export function MaadanimComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  initialExpandedProductId = null,
}: MaadanimComparisonPageProps) {
  const desktopHero = {
    badge: "דוח חדש",
    categoryTags: "מעדנים · קינוחי חלב",
    title: hero.title,
    description: prologueSentences[0] ?? "השוואת מעדנים וקינוחי חלב מהמדף הישראלי.",
    insightLines: productInsightLines(products),
    stats: [
      { value: products.length, label: "מוצרים בדף" },
      { value: maadanimCorpusMeta.scored_count ?? products.length, label: "קיבלו ציון" },
    ],
    updatedLabel: formatComparisonUpdatedLine(maadanimCorpusMeta.generated),
  };

  return (
    <>
      <div className="max-lg:block lg:hidden">
        <ComparisonShelfPage<MaadanimShelfFilterId>
          products={products}
          metadataLine={metadataLine}
          hero={hero}
          prologueSentences={prologueSentences}
          methodologyLines={methodologyLines}
          shelfFilters={maadanimShelfFilters}
          initialExpandedProductId={initialExpandedProductId}
        />
      </div>
      <div className="hidden lg:block">
        <BariComparisonDesktopPage<MaadanimShelfFilterId>
          products={products}
          hero={desktopHero}
          prologueSentences={prologueSentences.slice(1)}
          methodologyLines={methodologyLines}
          lensOptions={MAADANIM_SHELF_LENS_OPTIONS}
          filterProducts={filterMaadanimProducts}
        />
      </div>
    </>
  );
}
