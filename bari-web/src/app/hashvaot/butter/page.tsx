import type { Metadata } from "next";

import { ButterComparisonPage } from "@/components/comparisons/butter-comparison-page";
import {
  butterHero,
  butterMetadataLine,
  butterMethodologyLines,
  butterPrologueSentences,
  butterProducts,
  butterCategoryNote,
} from "@/lib/comparisons/butter-page-data";
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/butter_faq_schema.json";

export const metadata: Metadata = {
  title: "השוואת חמאה | Bari",
  description:
    "השוואת 39 מוצרי חמאה מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

export default function ButterComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <ButterComparisonPage
        products={butterProducts}
        metadataLine={butterMetadataLine}
        hero={butterHero}
        prologueSentences={butterPrologueSentences}
        methodologyLines={butterMethodologyLines}
        categoryNote={butterCategoryNote}
      />
    </>
  );
}
