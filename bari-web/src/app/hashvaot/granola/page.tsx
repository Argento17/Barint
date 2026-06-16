import type { Metadata } from "next";

import { GranolaComparisonPage } from "@/components/comparisons/granola-comparison-page";
import {
  granolaHero,
  granolaMetadataLine,
  granolaMethodologyLines,
  granolaPrologueSentences,
  granolaProducts,
  granolaCategoryNote,
} from "@/lib/comparisons/granola-page-data";
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/granola_faq_schema.json";

export const metadata: Metadata = {
  title: "השוואת גרנולה ומוזלי | Bari",
  description:
    "השוואת 53 מוצרי גרנולה ומוזלי מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

export default function GranolaComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <GranolaComparisonPage
        products={granolaProducts}
        metadataLine={granolaMetadataLine}
        hero={granolaHero}
        prologueSentences={granolaPrologueSentences}
        methodologyLines={granolaMethodologyLines}
        categoryNote={granolaCategoryNote}
      />
    </>
  );
}
