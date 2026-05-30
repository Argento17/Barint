"use client";

import {
  BariComparisonDesktopPage,
  productInsightLines,
} from "@/components/comparisons/bari-comparison-desktop-page";
import { ComparisonShelfPage } from "@/components/comparisons/comparison-shelf-page";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import { yogurtsCorpusMeta } from "@/lib/comparisons/yogurts-comparison-page-data";
import {
  filterYogurtsProducts,
  YOGURTS_SHELF_LENS_OPTIONS,
  type YogurtsShelfFilterId,
} from "@/lib/comparisons/yogurts-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface YogurtsComparisonPageProps {
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

const yogurtsShelfFilters = {
  lensOptions: YOGURTS_SHELF_LENS_OPTIONS,
  filterProducts: filterYogurtsProducts,
} as const;

const YOGURTS_INSIGHT_LINES = [
  "2 מרכיבים מול 8+ — הפער הכי גדול בקטגוריה הוא רשימת הרכיבים, לא המותג",
  "יווני/מסוי מוביל בחלבון — אבל לא תמיד בציון אם יש תוספים",
  "יוגורט 0% טבעי מקבל ציון גבוה ממוצר בטעמים עם אותו 0%",
  "מילקי ויוגורט שתיה — קצה תחתון: מוצרי הנאה, לא בסיס",
] as const;

export function YogurtsComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  initialExpandedProductId = null,
}: YogurtsComparisonPageProps) {
  const insightLines =
    productInsightLines(products).length > 0
      ? productInsightLines(products)
      : YOGURTS_INSIGHT_LINES;

  const desktopHero = {
    badge: "דוח חדש",
    categoryTags: "יוגורטים · מדף ישראלי",
    title: hero.title,
    description:
      prologueSentences[0] ??
      `דוח השוואה ליוגורטים: ${products.length} מוצרים בדף.`,
    insightLines,
    stats: [
      { value: yogurtsCorpusMeta.product_count, label: "מוצרים נבדקו" },
      { value: yogurtsCorpusMeta.scored_count ?? products.length, label: "קיבלו ציון" },
      { value: products.length, label: "בדף ההשוואה" },
    ],
    updatedLabel: formatComparisonUpdatedLine(yogurtsCorpusMeta.generated),
  };

  return (
    <>
      <div className="max-lg:block lg:hidden">
        <ComparisonShelfPage<YogurtsShelfFilterId>
          products={products}
          metadataLine={metadataLine}
          hero={hero}
          prologueSentences={prologueSentences}
          methodologyLines={methodologyLines}
          shelfFilters={yogurtsShelfFilters}
          initialExpandedProductId={initialExpandedProductId}
        />
      </div>
      <div className="hidden lg:block">
        <BariComparisonDesktopPage<YogurtsShelfFilterId>
          products={products}
          hero={desktopHero}
          prologueSentences={prologueSentences.slice(1)}
          methodologyLines={methodologyLines}
          lensOptions={YOGURTS_SHELF_LENS_OPTIONS}
          filterProducts={filterYogurtsProducts}
        />
      </div>
    </>
  );
}
