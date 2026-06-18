import type { Metadata } from "next";

import { CerealsComparisonPage } from "@/components/comparisons/cereals-comparison-page";
import {
  cerealsHero,
  cerealsMetadataLine,
  cerealsMethodologyLines,
  cerealsPrologueSentences,
  cerealsProducts,
  cerealsCategoryNote,
} from "@/lib/comparisons/cereals-page-data";
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/breakfast_cereals_faq_schema.json";

export const metadata: Metadata = {
  title: "השוואת דגני בוקר | Bari",
  description:
    "השוואת 37 מוצרי דגני בוקר מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

export default function BreakfastCerealsComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <CerealsComparisonPage
        products={cerealsProducts}
        metadataLine={cerealsMetadataLine}
        hero={cerealsHero}
        prologueSentences={cerealsPrologueSentences}
        methodologyLines={cerealsMethodologyLines}
        categoryNote={cerealsCategoryNote}
      />
    </>
  );
}
