import type { Metadata } from "next";

import { HardCheesesComparisonPage } from "@/components/comparisons/hard-cheeses-comparison-page";
import {
  hardCheesesCategoryNote,
  hardCheesesHero,
  hardCheesesMetadataLine,
  hardCheesesMethodologyLines,
  hardCheesesPrologueSentences,
  hardCheesesProducts,
} from "@/lib/comparisons/hard-cheeses-page-data";

export const metadata: Metadata = {
  title: "השוואת גבינות קשות וצהובות | Bari",
  description:
    "השוואת 37 גבינות קשות מהמדף הישראלי — ציון Bari, חלבון, שומן ונתרן ל-100 גרם. מידע, לא המלצה.",
};

export default function HardCheesesComparisonRoute() {
  return (
    <HardCheesesComparisonPage
      products={hardCheesesProducts}
      metadataLine={hardCheesesMetadataLine}
      hero={hardCheesesHero}
      prologueSentences={hardCheesesPrologueSentences}
      methodologyLines={hardCheesesMethodologyLines}
      categoryNote={hardCheesesCategoryNote}
    />
  );
}
