import type { Metadata } from "next";

import { ComparisonPageSeo } from "@/components/seo/comparison-page-seo";
import { CookiesCoffeeComparisonPage } from "@/components/comparisons/cookies-coffee-comparison-page";
import {
  cookiesCoffeeCategoryNote,
  cookiesCoffeeComparisonMetadata,
  cookiesCoffeeHero,
  cookiesCoffeeMetadataLine,
  cookiesCoffeeMethodologyLines,
  cookiesCoffeePrologueSentences,
  cookiesCoffeeProducts,
} from "@/lib/comparisons/cookies-coffee-page-data";

export const metadata: Metadata = cookiesCoffeeComparisonMetadata;

export default async function CookiesCoffeeComparisonRoute({
  searchParams,
}: {
  searchParams: Promise<{ product?: string }>;
}) {
  const params = await searchParams;
  const initialExpandedProductId = params.product ?? null;

  return (
    <>
      <ComparisonPageSeo pagePath="/hashvaot/cookies-coffee" products={cookiesCoffeeProducts} faqKey="cookies_coffee" />
      <CookiesCoffeeComparisonPage
      products={cookiesCoffeeProducts}
      metadataLine={cookiesCoffeeMetadataLine}
      hero={cookiesCoffeeHero}
      prologueSentences={cookiesCoffeePrologueSentences}
      methodologyLines={cookiesCoffeeMethodologyLines}
      categoryNote={cookiesCoffeeCategoryNote}
      initialExpandedProductId={initialExpandedProductId}

      />
    </>
  );
}
