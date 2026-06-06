import type { Metadata } from "next";

import { MaadanimComparisonPage } from "@/components/comparisons/maadanim-comparison-page";
import {
  maadanimHero,
  maadanimMetadataLine,
  maadanimMethodologyLines,
  maadanimPrologueSentences,
  maadanimProducts,
  maadanimCategoryNote,
} from "@/lib/comparisons/maadanim-page-data";

export const metadata: Metadata = {
  title: "השוואת מעדנים | Bari",
  description:
    "השוואת מעדנים וקינוחי חלב מהמדף הישראלי — ציון Bari, רכיבים, חלבון והקשר במדף. מידע, לא המלצה.",
};

export default function MaadanimComparisonRoute() {
  return (
    <MaadanimComparisonPage
      products={maadanimProducts}
      metadataLine={maadanimMetadataLine}
      hero={maadanimHero}
      prologueSentences={maadanimPrologueSentences}
      methodologyLines={maadanimMethodologyLines}
      categoryNote={maadanimCategoryNote}
      glassBoxMethodologyLink
    />
  );
}
