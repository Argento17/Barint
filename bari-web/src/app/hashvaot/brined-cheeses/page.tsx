import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { BrinedCheesesComparisonPage } from "@/components/comparisons/brined-cheeses-comparison-page";
import {
  brinedCheesesCategoryNote,
  brinedCheesesHero,
  brinedCheesesMetadataLine,
  brinedCheesesMethodologyLines,
  brinedCheesesPrologueSentences,
  brinedCheesesProducts,
} from "@/lib/comparisons/brined-cheeses-page-data";

export const metadata: Metadata = {
  title: "השוואת גבינות מלוחות | Bari",
  description:
    "השוואת 36 גבינות מלוחות מהמדף הישראלי — ציון Bari, נתרן, חלבון ושומן ל-100 גרם. מידע, לא המלצה.",
};

export default async function BrinedCheesesComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/brined-cheeses" products={brinedCheesesProducts} faqKey="brined_cheeses" />
      <BrinedCheesesComparisonPage
      products={brinedCheesesProducts}
      metadataLine={brinedCheesesMetadataLine}
      hero={brinedCheesesHero}
      prologueSentences={brinedCheesesPrologueSentences}
      methodologyLines={brinedCheesesMethodologyLines}
      categoryNote={brinedCheesesCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
