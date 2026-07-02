import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { JuicesComparisonPage } from "@/components/comparisons/juices-comparison-page";
import {
  juicesCategoryNote,
  juicesHero,
  juicesMetadataLine,
  juicesMethodologyLines,
  juicesPrologueSentences,
  juicesProducts,
} from "@/lib/comparisons/juices-page-data";

export const metadata: Metadata = {
  title: "השוואת מיצים ומשקאות פירות | Bari",
  description:
    'השוואת 17 מיצים ומשקאות פירות מהמדף הישראלי — ציון Bari, סוכר ל-100 מ"ל, ריכוז פרי ורמת עיבוד. מידע, לא המלצה.',
};

export default async function JuicesComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/juices" products={juicesProducts} faqKey="juices" />
      <JuicesComparisonPage
      products={juicesProducts}
      metadataLine={juicesMetadataLine}
      hero={juicesHero}
      prologueSentences={juicesPrologueSentences}
      methodologyLines={juicesMethodologyLines}
      categoryNote={juicesCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
