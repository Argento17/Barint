import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { MilkComparisonPage } from "@/components/comparisons/milk-comparison-page";
import {
  milkBlogLink,
  milkCategoryNote,
  milkComparisonMetadata,
  milkHero,
  milkMetadataLine,
  milkMethodologyLines,
  milkPrologueSentences,
  milkVmProducts,
} from "@/lib/comparisons/milk-page-data";

export const metadata: Metadata = milkComparisonMetadata;

export default async function MilkComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/milk-comparison" products={milkVmProducts} />
      <MilkComparisonPage
      products={milkVmProducts}
      metadataLine={milkMetadataLine}
      hero={milkHero}
      prologueSentences={milkPrologueSentences}
      methodologyLines={milkMethodologyLines}
      categoryNote={milkCategoryNote}
      blogLink={milkBlogLink}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
