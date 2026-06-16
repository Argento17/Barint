import type { Metadata } from "next";

import { SaltySnacksComparisonPage } from "@/components/comparisons/salty-snacks-comparison-page";
import {
  saltySnacksHero,
  saltySnacksMetadataLine,
  saltySnacksMethodologyLines,
  saltySnacksPrologueSentences,
  saltySnacksProducts,
  saltySnacksCategoryNote,
} from "@/lib/comparisons/salty-snacks-page-data";
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/salty_snacks_faq_schema.json";

export const metadata: Metadata = {
  title: "השוואת חטיפים מלוחים | Bari",
  description:
    "השוואת 29 חטיפים מלוחים מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

export default function SaltySnacksComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <SaltySnacksComparisonPage
        products={saltySnacksProducts}
        metadataLine={saltySnacksMetadataLine}
        hero={saltySnacksHero}
        prologueSentences={saltySnacksPrologueSentences}
        methodologyLines={saltySnacksMethodologyLines}
        categoryNote={saltySnacksCategoryNote}
      />
    </>
  );
}
