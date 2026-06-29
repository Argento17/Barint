import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { CheeseComparisonPage } from "@/components/comparisons/cheese-comparison-page";
import {
  cheeseHero,
  cheeseMetadataLine,
  cheeseMethodologyLines,
  cheesePrologueSentences,
  cheeseProducts,
  cheeseCategoryNote,
  cheeseComparisonMetadata,
} from "@/lib/comparisons/cheese-page-data";

export const metadata: Metadata = cheeseComparisonMetadata;

export default async function CheeseComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/cheese" products={cheeseProducts} />
      <CheeseComparisonPage
      products={cheeseProducts}
      metadataLine={cheeseMetadataLine}
      hero={cheeseHero}
      prologueSentences={cheesePrologueSentences}
      methodologyLines={cheeseMethodologyLines}
      categoryNote={cheeseCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
