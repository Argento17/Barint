import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { CrackersComparisonPage } from "@/components/comparisons/crackers-comparison-page";
import {
  crackersHero,
  crackersMetadataLine,
  crackersMethodologyLines,
  crackersPrologueSentences,
  crackersProducts,
  crackersCategoryNote,
  crackersComparisonMetadata,
} from "@/lib/comparisons/crackers-page-data";

export const metadata: Metadata = crackersComparisonMetadata;

export default async function CrackersComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/crackers" products={crackersProducts} />
      <CrackersComparisonPage
        products={crackersProducts}
        metadataLine={crackersMetadataLine}
        hero={crackersHero}
        prologueSentences={crackersPrologueSentences}
        methodologyLines={crackersMethodologyLines}
        categoryNote={crackersCategoryNote}
        initialExpandedProductId={initialExpandedProductId}
      />
    </>
  );
}
