import type { Metadata } from "next";

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
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/cookies_coffee_faq_schema.json";

export const metadata: Metadata = cookiesCoffeeComparisonMetadata;

export default function CookiesCoffeeComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <CookiesCoffeeComparisonPage
        products={cookiesCoffeeProducts}
        metadataLine={cookiesCoffeeMetadataLine}
        hero={cookiesCoffeeHero}
        prologueSentences={cookiesCoffeePrologueSentences}
        methodologyLines={cookiesCoffeeMethodologyLines}
        categoryNote={cookiesCoffeeCategoryNote}
      />
    </>
  );
}
