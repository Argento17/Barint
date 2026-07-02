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
  juicesComparisonMetadata,
} from "@/lib/comparisons/juices-page-data";

export const metadata: Metadata = juicesComparisonMetadata;

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
