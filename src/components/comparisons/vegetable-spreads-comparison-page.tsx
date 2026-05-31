"use client";

import { BariComparisonDesktopPage } from "@/components/comparisons/bari-comparison-desktop-page";
import { ComparisonShelfPage } from "@/components/comparisons/comparison-shelf-page";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import { vegetableSpreadsCorpusMeta } from "@/lib/comparisons/vegetable-spreads-comparison-page-data";
import {
  filterVegetableSpreadsProducts,
  VEGETABLE_SPREADS_SHELF_LENS_OPTIONS,
  type VegetableSpreadsShelfFilterId,
} from "@/lib/comparisons/vegetable-spreads-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface VegetableSpreadsComparisonPageProps {
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

const vegetableSpreadsShelfFilters = {
  lensOptions: VEGETABLE_SPREADS_SHELF_LENS_OPTIONS,
  filterProducts: filterVegetableSpreadsProducts,
} as const;

const VEGETABLE_SPREADS_INSIGHT_LINES = [
  "מטבוחה, ממרח חצילים וממרח פלפלים — ממרחי ירקות בלבד",
  "ממרחי חומוס ומסבחה מוצגים בדף נפרד",
  "הציון מחושב לפי מדד עיבוד, תוספים וערכים תזונתיים",
  "ניתן לסנן לפי סוג ממרח בעזרת הכפתורים למעלה",
] as const;

export function VegetableSpreadsComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  initialExpandedProductId = null,
}: VegetableSpreadsComparisonPageProps) {
  const insightLines = VEGETABLE_SPREADS_INSIGHT_LINES;

  const displayedCount = products.length;
  const scoredCount = products.filter((product) => product.score != null).length;
  const aGradeCount = products.filter((product) => product.grade === "A").length;

  const desktopHero = {
    badge: "השוואה חדשה",
    categoryTags: "ממרחי ירקות · שופרסל",
    title: hero.title,
    description:
      prologueSentences[0] ??
      `דוח השוואה לממרחי ירקות: ${products.length} מוצרים בדף.`,
    insightLines,
    stats: [
      { value: displayedCount, label: "מוצרים בהשוואה" },
      { value: scoredCount, label: "קיבלו ציון" },
      { value: aGradeCount, label: "בציון A" },
    ],
    updatedLabel: formatComparisonUpdatedLine(vegetableSpreadsCorpusMeta.generated),
  };

  return (
    <>
      <div className="max-lg:block lg:hidden">
        <ComparisonShelfPage<VegetableSpreadsShelfFilterId>
          products={products}
          metadataLine={metadataLine}
          hero={hero}
          prologueSentences={prologueSentences}
          methodologyLines={methodologyLines}
          shelfFilters={vegetableSpreadsShelfFilters}
          initialExpandedProductId={initialExpandedProductId}
        />
      </div>
      <div className="hidden lg:block">
        <BariComparisonDesktopPage<VegetableSpreadsShelfFilterId>
          products={products}
          hero={desktopHero}
          prologueSentences={prologueSentences.slice(1)}
          methodologyLines={methodologyLines}
          lensOptions={VEGETABLE_SPREADS_SHELF_LENS_OPTIONS}
          filterProducts={filterVegetableSpreadsProducts}
        />
      </div>
    </>
  );
}
