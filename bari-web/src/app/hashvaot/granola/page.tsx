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
  granolaComparisonMetadata,
} from "@/lib/comparisons/granola-page-data";

export const metadata: Metadata = granolaComparisonMetadata;

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
