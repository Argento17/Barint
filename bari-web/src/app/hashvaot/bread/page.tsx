import type { Metadata } from "next";

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
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/bread_faq_schema.json";

export const metadata: Metadata = breadComparisonMetadata;

export default function BreadComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <BreadComparisonPage
        products={breadProducts}
        metadataLine={breadMetadataLine}
        hero={breadHero}
        prologueSentences={breadPrologueSentences}
        methodologyLines={breadMethodologyLines}
        categoryNote={breadCategoryNote}
      />
    </>
  );
}
