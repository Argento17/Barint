import type { Metadata } from "next";

import { CheeseComparisonPage } from "@/components/comparisons/cheese-comparison-page";
import {
  cheeseHero,
  cheeseMetadataLine,
  cheeseMethodologyLines,
  cheesePrologueSentences,
  cheeseProducts,
  cheeseCategoryNote,
  cheeseComparisonMetadata,
} from "@/lib/comparisons/cheese-comparison-page-data";
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/cheese_faq_schema.json";

export const metadata: Metadata = cheeseComparisonMetadata;

export default function CheeseComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <CheeseComparisonPage
        products={cheeseProducts}
        metadataLine={cheeseMetadataLine}
        hero={cheeseHero}
        prologueSentences={cheesePrologueSentences}
        methodologyLines={cheeseMethodologyLines}
        categoryNote={cheeseCategoryNote}
      />
    </>
  );
}
