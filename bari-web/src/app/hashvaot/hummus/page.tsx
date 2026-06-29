import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { HummusComparisonPage } from "@/components/comparisons/hummus-comparison-page";
import {
  hummusHero,
  hummusMetadataLine,
  hummusMethodologyLines,
  hummusPrologueSentences,
  hummusProducts,
  hummusCategoryNote,
  hummusComparisonMetadata,
} from "@/lib/comparisons/hummus-comparison-page-data";

export const metadata: Metadata = hummusComparisonMetadata;

export default async function HummusComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/hummus" products={hummusProducts} faqKey="hummus" />
      <HummusComparisonPage
      products={hummusProducts}
      metadataLine={hummusMetadataLine}
      hero={hummusHero}
      prologueSentences={hummusPrologueSentences}
      methodologyLines={hummusMethodologyLines}
      categoryNote={hummusCategoryNote}
      glassBoxMethodologyLink
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
