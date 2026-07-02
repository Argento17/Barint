import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { HardCheesesComparisonPage } from "@/components/comparisons/hard-cheeses-comparison-page";
import {
  hardCheesesCategoryNote,
  hardCheesesHero,
  hardCheesesMetadataLine,
  hardCheesesMethodologyLines,
  hardCheesesPrologueSentences,
  hardCheesesProducts,
  hardCheesesComparisonMetadata,
} from "@/lib/comparisons/hard-cheeses-page-data";

export const metadata: Metadata = hardCheesesComparisonMetadata;

export default async function HardCheesesComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/hard-cheeses" products={hardCheesesProducts} faqKey="hard_cheeses" />
      <HardCheesesComparisonPage
      products={hardCheesesProducts}
      metadataLine={hardCheesesMetadataLine}
      hero={hardCheesesHero}
      prologueSentences={hardCheesesPrologueSentences}
      methodologyLines={hardCheesesMethodologyLines}
      categoryNote={hardCheesesCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
