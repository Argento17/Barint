import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { SnacksComparisonPage } from "@/components/comparisons/snacks-comparison-page";
import {
  snacksComparisonMetadata,
  snacksHero,
  snacksMetadataLine,
  snacksMethodologyLines,
  snacksPrologueSentences,
  snacksProducts,
  snacksCategoryNote,
} from "@/lib/comparisons/snacks-comparison-page-data";

export const metadata: Metadata = snacksComparisonMetadata;

export default async function SnacksComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/snacks" products={snacksProducts} />
      <SnacksComparisonPage
      products={snacksProducts}
      metadataLine={snacksMetadataLine}
      hero={snacksHero}
      prologueSentences={snacksPrologueSentences}
      methodologyLines={snacksMethodologyLines}
      categoryNote={snacksCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
