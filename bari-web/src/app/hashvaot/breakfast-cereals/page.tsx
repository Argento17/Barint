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

export const metadata: Metadata = {
  title: "השוואת דגני בוקר | Bari",
  description:
    "השוואת 37 מוצרי דגני בוקר מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

export default function BreakfastCerealsComparisonRoute() {
  return (
    <CerealsComparisonPage
      products={cerealsProducts}
      metadataLine={cerealsMetadataLine}
      hero={cerealsHero}
      prologueSentences={cerealsPrologueSentences}
      methodologyLines={cerealsMethodologyLines}
      categoryNote={cerealsCategoryNote}
    />
  );
}
