import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { YogurtDrinksComparisonPage } from "@/components/comparisons/yogurt-drinks-comparison-page";
import {
  yogurtDrinksCategoryNote,
  yogurtDrinksHero,
  yogurtDrinksMetadataLine,
  yogurtDrinksMethodologyLines,
  yogurtDrinksPrologueSentences,
  yogurtDrinksProducts,
} from "@/lib/comparisons/yogurt-drinks-page-data";

export const metadata: Metadata = {
  title: "השוואת משקאות יוגורט | Bari",
  description:
    'השוואת 20 משקאות יוגורט מהמדף הישראלי — ציון Bari, חלבון וסוכר ל-100 גרם, רכיבים ותוספים. מידע, לא המלצה.',
};

export default async function YogurtDrinksComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo
        pagePath="/hashvaot/yogurt-drinks"
        products={yogurtDrinksProducts}
        faqKey="yogurt_drinks"
      />
      <YogurtDrinksComparisonPage
      products={yogurtDrinksProducts}
      metadataLine={yogurtDrinksMetadataLine}
      hero={yogurtDrinksHero}
      prologueSentences={yogurtDrinksPrologueSentences}
      methodologyLines={yogurtDrinksMethodologyLines}
      categoryNote={yogurtDrinksCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
