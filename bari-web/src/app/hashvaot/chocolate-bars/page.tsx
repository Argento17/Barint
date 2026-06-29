import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { ChocolateBarsComparisonPage } from "@/components/comparisons/chocolate-bars-comparison-page";
import {
  chocolateBarsComparisonMetadata,
  chocolateBarsHero,
  chocolateBarsMetadataLine,
  chocolateBarsMethodologyLines,
  chocolateBarsPrologueSentences,
  chocolateBarsProducts,
  chocolateBarsCategoryNote,
} from "@/lib/comparisons/chocolate-bars-comparison-page-data";

export const metadata: Metadata = chocolateBarsComparisonMetadata;

export default async function ChocolateBarsComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/chocolate-bars" products={chocolateBarsProducts} />
    <ChocolateBarsComparisonPage
      products={chocolateBarsProducts}
      metadataLine={chocolateBarsMetadataLine}
      hero={chocolateBarsHero}
      prologueSentences={chocolateBarsPrologueSentences}
      methodologyLines={chocolateBarsMethodologyLines}
      categoryNote={chocolateBarsCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

    />
    </>
  );
}
