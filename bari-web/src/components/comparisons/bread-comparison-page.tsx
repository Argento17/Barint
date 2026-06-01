"use client";

import {
  BariComparisonDesktopPage,
  productInsightLines,
} from "@/components/comparisons/bari-comparison-desktop-page";
import { ComparisonShelfPage } from "@/components/comparisons/comparison-shelf-page";
import { BREAD_REPORT_STATS } from "@/lib/comparisons/bread-page-data";
import { breadCorpusMeta } from "@/lib/comparisons/bread-comparison-page-data";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
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
  initialExpandedProductId?: string | null;
}

const breadShelfFilters = {
  lensOptions: BREAD_SHELF_LENS_OPTIONS,
  filterProducts: filterBreadProducts,
} as const;

export function BreadComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  initialExpandedProductId = null,
}: BreadComparisonPageProps) {
  const desktopHero = {
    badge: "דוח חדש",
    categoryTags: "מנוע השוואה · לחמים",
    title: hero.title,
    description: prologueSentences[0] ?? "השוואת לחם, פיתות וקרקרים ממדף שופרסל.",
    insightLines: productInsightLines(products),
    stats: [
      { value: BREAD_REPORT_STATS.scanned, label: "מוצרים נסרקו" },
      { value: BREAD_REPORT_STATS.sufficient, label: "עם נתונים מספיקים" },
      { value: products.length, label: "בדף ההשוואה" },
    ],
    updatedLabel: formatComparisonUpdatedLine(breadCorpusMeta.generated),
  };

  return (
    <>
      <div className="max-lg:block lg:hidden">
        <ComparisonShelfPage<BreadShelfFilterId>
          products={products}
          metadataLine={metadataLine}
          hero={hero}
          prologueSentences={prologueSentences}
          methodologyLines={methodologyLines}
          shelfFilters={breadShelfFilters}
          initialExpandedProductId={initialExpandedProductId}
        />
      </div>
      <div className="hidden lg:block">
        <BariComparisonDesktopPage<BreadShelfFilterId>
          products={products}
          hero={desktopHero}
          prologueSentences={prologueSentences.slice(1)}
          methodologyLines={methodologyLines}
          lensOptions={BREAD_SHELF_LENS_OPTIONS}
          filterProducts={filterBreadProducts}
          blogLink={{
            href: "/research/bread-transparency-shufersal",
            label: "קראו את הניתוח בבלוג ←",
          }}
        />
      </div>
    </>
  );
}
