import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { GranolaComparisonPage } from "@/components/comparisons/granola-comparison-page";
import {
  granolaHero,
  granolaMetadataLine,
  granolaMethodologyLines,
  granolaPrologueSentences,
  granolaProducts,
  granolaCategoryNote,
} from "@/lib/comparisons/granola-page-data";

export const metadata: Metadata = {
  title: "השוואת גרנולה ומוזלי | Bari",
  description:
    "השוואת 22 מוצרי גרנולה ומוזלי מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

export default async function GranolaComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/granola" products={granolaProducts} faqKey="granola" />
      <GranolaComparisonPage
      products={granolaProducts}
      metadataLine={granolaMetadataLine}
      hero={granolaHero}
      prologueSentences={granolaPrologueSentences}
      methodologyLines={granolaMethodologyLines}
      categoryNote={granolaCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
