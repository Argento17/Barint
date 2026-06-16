import type { Metadata } from "next";

import { HummusComparisonPage } from "@/components/comparisons/hummus-comparison-page";
import {
  hummusHero,
  hummusMetadataLine,
  hummusMethodologyLines,
  hummusPrologueSentences,
  hummusProducts,
  hummusCategoryNote,
  hummusComparisonMetadata,
} from "@/lib/comparisons/hummus-comparison-page-data";
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/hummus_faq_schema.json";

export const metadata: Metadata = hummusComparisonMetadata;

export default function HummusComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <HummusComparisonPage
        products={hummusProducts}
        metadataLine={hummusMetadataLine}
        hero={hummusHero}
        prologueSentences={hummusPrologueSentences}
        methodologyLines={hummusMethodologyLines}
        categoryNote={hummusCategoryNote}
        glassBoxMethodologyLink
      />
    </>
  );
}
