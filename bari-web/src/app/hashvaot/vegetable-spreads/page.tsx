import type { Metadata } from "next";

import { VegetableSpreadsComparisonPage } from "@/components/comparisons/vegetable-spreads-comparison-page";
import {
  vegetableSpreadsHero,
  vegetableSpreadsMetadataLine,
  vegetableSpreadsMethodologyLines,
  vegetableSpreadsPrologueSentences,
  vegetableSpreadsProducts,
  vegetableSpreadsCategoryNote,
  vegetableSpreadsComparisonMetadata,
} from "@/lib/comparisons/vegetable-spreads-comparison-page-data";
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/vegetable_spreads_faq_schema.json";

export const metadata: Metadata = vegetableSpreadsComparisonMetadata;

export default function VegetableSpreadsComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <VegetableSpreadsComparisonPage
        products={vegetableSpreadsProducts}
        metadataLine={vegetableSpreadsMetadataLine}
        hero={vegetableSpreadsHero}
        prologueSentences={vegetableSpreadsPrologueSentences}
        methodologyLines={vegetableSpreadsMethodologyLines}
        categoryNote={vegetableSpreadsCategoryNote}
      />
    </>
  );
}
