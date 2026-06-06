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

export const metadata: Metadata = {
  title: "השוואת חמאה | Bari",
  description:
    "השוואת 39 מוצרי חמאה מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

export default function ButterComparisonRoute() {
  return (
    <ButterComparisonPage
      products={butterProducts}
      metadataLine={butterMetadataLine}
      hero={butterHero}
      prologueSentences={butterPrologueSentences}
      methodologyLines={butterMethodologyLines}
      categoryNote={butterCategoryNote}
    />
  );
}
