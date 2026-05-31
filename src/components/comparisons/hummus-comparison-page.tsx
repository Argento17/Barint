// Reference implementation for Bari Gen 1 comparison categories.
// New categories: copy this file, rename, update data import.
"use client";

import { BariComparisonDesktopPage } from "@/components/comparisons/bari-comparison-desktop-page";
import { ComparisonShelfPage } from "@/components/comparisons/comparison-shelf-page";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import { hummusCorpusMeta } from "@/lib/comparisons/hummus-comparison-page-data";
import {
  filterHummusProducts,
  HUMMUS_SHELF_LENS_OPTIONS,
  type HummusShelfFilterId,
} from "@/lib/comparisons/hummus-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export interface HummusComparisonPageProps {
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

const hummusShelfFilters = {
  lensOptions: HUMMUS_SHELF_LENS_OPTIONS,
  filterProducts: filterHummusProducts,
} as const;

// Category-level insight lines. Product-specific lines pending content integration.
const HUMMUS_INSIGHT_LINES = [
  "63 מוצרים בדירוג — ממרחי חומוס, מטבוחה, חצילים, פלפלים ומסבחה",
  "2 מוצרים בציון A: הרכב חזק עם תוספים מוגבלים",
  "פער ציון של 37 נקודות בין הממרח המוביל לתחתית הרשימה",
  "ערכי שומן אינם מוצגים — מגבלת נתוני מקור, מפורטת בתחתית הדף",
] as const;

export function HummusComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  initialExpandedProductId = null,
}: HummusComparisonPageProps) {
  // Product-specific insight lines are pending content integration from hummus_insights_v1.md.
  // Using category-level fallback until that integration is complete.
  const insightLines = HUMMUS_INSIGHT_LINES;

  const desktopHero = {
    badge: "השוואה חדשה",
    categoryTags: "חומוס וממרחים · שופרסל",
    title: hero.title,
    description:
      prologueSentences[0] ??
      `דוח השוואה לחומוס וממרחים: ${products.length} מוצרים בדף.`,
    insightLines,
    stats: [
      { value: hummusCorpusMeta.product_count, label: "מוצרים נבדקו" },
      { value: hummusCorpusMeta.scored_count ?? products.length, label: "קיבלו ציון" },
      { value: products.length, label: "בדף ההשוואה" },
    ],
    updatedLabel: formatComparisonUpdatedLine(hummusCorpusMeta.generated),
  };

  return (
    <>
      <div className="max-lg:block lg:hidden">
        <ComparisonShelfPage<HummusShelfFilterId>
          products={products}
          metadataLine={metadataLine}
          hero={hero}
          prologueSentences={prologueSentences}
          methodologyLines={methodologyLines}
          shelfFilters={hummusShelfFilters}
          initialExpandedProductId={initialExpandedProductId}
        />
      </div>
      <div className="hidden lg:block">
        <BariComparisonDesktopPage<HummusShelfFilterId>
          products={products}
          hero={desktopHero}
          prologueSentences={prologueSentences.slice(1)}
          methodologyLines={methodologyLines}
          lensOptions={HUMMUS_SHELF_LENS_OPTIONS}
          filterProducts={filterHummusProducts}
        />
      </div>
    </>
  );
}
