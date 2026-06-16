import type { Metadata } from "next";

import { BrinedCheesesComparisonPage } from "@/components/comparisons/brined-cheeses-comparison-page";
import {
  brinedCheesesCategoryNote,
  brinedCheesesHero,
  brinedCheesesMetadataLine,
  brinedCheesesMethodologyLines,
  brinedCheesesPrologueSentences,
  brinedCheesesProducts,
} from "@/lib/comparisons/brined-cheeses-page-data";
import { buildFaqScript } from "@/lib/seo/faq-schema";
import rawFaqSchema from "@/data/seo/brined_cheeses_faq_schema.json";

export const metadata: Metadata = {
  title: "השוואת גבינות מלוחות | Bari",
  description:
    "השוואת 36 גבינות מלוחות מהמדף הישראלי — ציון Bari, נתרן, חלבון ושומן ל-100 גרם. מידע, לא המלצה.",
};

export default function BrinedCheesesComparisonRoute() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: buildFaqScript(rawFaqSchema) }} />
      <BrinedCheesesComparisonPage
        products={brinedCheesesProducts}
        metadataLine={brinedCheesesMetadataLine}
        hero={brinedCheesesHero}
        prologueSentences={brinedCheesesPrologueSentences}
        methodologyLines={brinedCheesesMethodologyLines}
        categoryNote={brinedCheesesCategoryNote}
      />
    </>
  );
}
