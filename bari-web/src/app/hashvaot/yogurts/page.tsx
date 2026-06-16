import type { Metadata } from "next";

import { YogurtsComparisonPage } from "@/components/comparisons/yogurts-comparison-page";
import {
  yogurtsHero,
  yogurtsMetadataLine,
  yogurtsMethodologyLines,
  yogurtsPrologueSentences,
  yogurtsProducts,
  yogurtsCategoryNote,
  yogurtsComparisonMetadata,
} from "@/lib/comparisons/yogurts-comparison-page-data";
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/yogurts_faq_schema.json";

export const metadata: Metadata = yogurtsComparisonMetadata;

export default function YogurtsComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <YogurtsComparisonPage
        products={yogurtsProducts}
        metadataLine={yogurtsMetadataLine}
        hero={yogurtsHero}
        prologueSentences={yogurtsPrologueSentences}
        methodologyLines={yogurtsMethodologyLines}
        categoryNote={yogurtsCategoryNote}
      />
    </>
  );
}
