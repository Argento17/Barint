import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { ChocolateTabletsComparisonPage } from "@/components/comparisons/chocolate-tablets-comparison-page";
import {
  chocolateTabletsComparisonMetadata,
  chocolateTabletsHero,
  chocolateTabletsMetadataLine,
  chocolateTabletsMethodologyLines,
  chocolateTabletsPrologueSentences,
  chocolateTabletsProducts,
  chocolateTabletsCategoryNote,
} from "@/lib/comparisons/chocolate-tablets-comparison-page-data";

export const metadata: Metadata = chocolateTabletsComparisonMetadata;

export default async function ChocolateTabletsComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/chocolate-tablets" products={chocolateTabletsProducts} />
    <ChocolateTabletsComparisonPage
      products={chocolateTabletsProducts}
      metadataLine={chocolateTabletsMetadataLine}
      hero={chocolateTabletsHero}
      prologueSentences={chocolateTabletsPrologueSentences}
      methodologyLines={chocolateTabletsMethodologyLines}
      categoryNote={chocolateTabletsCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

    />
    </>
  );
}
