import type { Metadata } from "next";

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
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/snacks_faq_schema.json";

export const metadata: Metadata = snacksComparisonMetadata;

export default function SnacksComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <SnacksComparisonPage
        products={snacksProducts}
        metadataLine={snacksMetadataLine}
        hero={snacksHero}
        prologueSentences={snacksPrologueSentences}
        methodologyLines={snacksMethodologyLines}
        categoryNote={snacksCategoryNote}
      />
    </>
  );
}
