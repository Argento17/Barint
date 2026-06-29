import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { BreadComparisonPage } from "@/components/comparisons/bread-comparison-page";
import {
  breadHero,
  breadMetadataLine,
  breadMethodologyLines,
  breadPrologueSentences,
  breadProducts,
  breadCategoryNote,
  breadComparisonMetadata,
} from "@/lib/comparisons/bread-comparison-page-data";

export const metadata: Metadata = breadComparisonMetadata;

export default async function BreadComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/bread" products={breadProducts} faqKey="bread" />
      <BreadComparisonPage
      products={breadProducts}
      metadataLine={breadMetadataLine}
      hero={breadHero}
      prologueSentences={breadPrologueSentences}
      methodologyLines={breadMethodologyLines}
      categoryNote={breadCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
