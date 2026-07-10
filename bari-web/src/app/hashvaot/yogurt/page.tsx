import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { YogurtSpoonableComparisonPage } from "@/components/comparisons/yogurt-spoonable-comparison-page";
import {
  yogurtSpoonableCategoryNote,
  yogurtSpoonableHero,
  yogurtSpoonableMetadataLine,
  yogurtSpoonableMethodologyLines,
  yogurtSpoonablePrologueSentences,
  yogurtSpoonableProducts,
} from "@/lib/comparisons/yogurt-spoonable-page-data";

export const metadata: Metadata = {
  title: "השוואת יוגורטים לאכילה בכפית | Bari",
  description:
    'השוואת 50 יוגורטים לאכילה בכפית מהמדף הישראלי — ציון Bari, חלבון וסוכר ל-100 גרם, רכיבים ותוספים. מידע, לא המלצה.',
};

export default async function YogurtSpoonableComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo
        pagePath="/hashvaot/yogurt"
        products={yogurtSpoonableProducts}
        faqKey="yogurt_spoonable"
      />
      <YogurtSpoonableComparisonPage
        products={yogurtSpoonableProducts}
        metadataLine={yogurtSpoonableMetadataLine}
        hero={yogurtSpoonableHero}
        prologueSentences={yogurtSpoonablePrologueSentences}
        methodologyLines={yogurtSpoonableMethodologyLines}
        categoryNote={yogurtSpoonableCategoryNote}
        initialExpandedProductId={initialExpandedProductId}
      />
    </>
  );
}
