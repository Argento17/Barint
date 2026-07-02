import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { CerealsComparisonPage } from "@/components/comparisons/cereals-comparison-page";
import {
  cerealsHero,
  cerealsMetadataLine,
  cerealsMethodologyLines,
  cerealsPrologueSentences,
  cerealsProducts,
  cerealsCategoryNote,
  cerealsComparisonMetadata,
} from "@/lib/comparisons/cereals-page-data";

export const metadata: Metadata = cerealsComparisonMetadata;

export default async function BreakfastCerealsComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/breakfast-cereals" products={cerealsProducts} faqKey="breakfast_cereals" />
      <CerealsComparisonPage
      products={cerealsProducts}
      metadataLine={cerealsMetadataLine}
      hero={cerealsHero}
      prologueSentences={cerealsPrologueSentences}
      methodologyLines={cerealsMethodologyLines}
      categoryNote={cerealsCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
