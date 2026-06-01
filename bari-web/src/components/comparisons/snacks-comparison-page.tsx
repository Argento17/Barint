"use client";

import {
  BariComparisonDesktopPage,
  productInsightLines,
} from "@/components/comparisons/bari-comparison-desktop-page";
import { ComparisonShelfPage } from "@/components/comparisons/comparison-shelf-page";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import { SNACK_REPORT_STATS } from "@/lib/comparisons/snack-page-data";
import { snacksCorpusMeta } from "@/lib/comparisons/snacks-comparison-page-data";
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
  initialExpandedProductId?: string | null;
}

const snacksShelfFilters = {
  lensOptions: SNACKS_SHELF_LENS_OPTIONS,
  filterProducts: filterSnacksProducts,
} as const;

const SNACKS_INSIGHT_LINES = [
  "הציון הגבוה ביותר בקטגוריה — 70/B — לא הלך לאף אחד מהשמות המוכרים",
  "חטיפי תמרים עם 3–4 מרכיבים מובילים את המדף בפשטות מבנית",
  "תווית אדומה על סוכר לא אומרת תמיד ציון נמוך — מקור הסוכר נכנס לחישוב",
  "חטיפי חלבון מעובדים לעיתים מקבלים ציון נמוך יותר מחטיפי תמרים פשוטים",
] as const;

export function SnacksComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  initialExpandedProductId = null,
}: SnacksComparisonPageProps) {
  const insightLines =
    productInsightLines(products).length > 0
      ? productInsightLines(products)
      : SNACKS_INSIGHT_LINES;

  const desktopHero = {
    badge: "דוח חדש",
    categoryTags: "חטיפים · מדף יוחננוף",
    title: hero.title,
    description:
      prologueSentences[0] ??
      `דוח השוואה לחטיפי המדף: ${SNACK_REPORT_STATS.scraped} נסרקו, ${products.length} מוצרים בדף.`,
    insightLines,
    stats: [
      { value: SNACK_REPORT_STATS.scraped, label: "מוצרים נסרקו" },
      { value: SNACK_REPORT_STATS.scored, label: "קיבלו ציון" },
      { value: products.length, label: "בדף ההשוואה" },
    ],
    updatedLabel: formatComparisonUpdatedLine(snacksCorpusMeta.generated),
  };

  return (
    <>
      <div className="max-lg:block lg:hidden">
        <ComparisonShelfPage<SnacksShelfFilterId>
          products={products}
          metadataLine={metadataLine}
          hero={hero}
          prologueSentences={prologueSentences}
          methodologyLines={methodologyLines}
          shelfFilters={snacksShelfFilters}
          initialExpandedProductId={initialExpandedProductId}
        />
      </div>
      <div className="hidden lg:block">
        <BariComparisonDesktopPage<SnacksShelfFilterId>
          products={products}
          hero={desktopHero}
          prologueSentences={prologueSentences.slice(1)}
          methodologyLines={methodologyLines}
          lensOptions={SNACKS_SHELF_LENS_OPTIONS}
          filterProducts={filterSnacksProducts}
          blogLink={{
            href: "/blog/snack-bars-flagship",
            label: "קראו את הניתוח העיתונאי בבלוג ←",
          }}
        />
      </div>
    </>
  );
}
