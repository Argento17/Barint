import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { ProteinBarsComparisonPage } from "@/components/comparisons/protein-bars-comparison-page";
import {
  proteinBarsComparisonMetadata,
  proteinBarsHero,
  proteinBarsMetadataLine,
  proteinBarsMethodologyLines,
  proteinBarsPrologueSentences,
  proteinBarsProducts,
  proteinBarsCategoryNote,
} from "@/lib/comparisons/protein-bars-comparison-page-data";

export const metadata: Metadata = proteinBarsComparisonMetadata;

export default async function ProteinBarsComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/protein-bars" products={proteinBarsProducts} />
      <ProteinBarsComparisonPage
      products={proteinBarsProducts}
      metadataLine={proteinBarsMetadataLine}
      hero={proteinBarsHero}
      prologueSentences={proteinBarsPrologueSentences}
      methodologyLines={proteinBarsMethodologyLines}
      categoryNote={proteinBarsCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
