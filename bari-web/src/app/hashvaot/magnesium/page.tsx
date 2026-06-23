// Magnesium supplement comparison route.
// Published 2026-06-23 after the absorbed-mg rescore + red-team v4 (CONDITIONAL GO),
// data pass (Magnox discarded, Tink count corrected) and owner go-live sign-off.

import type { Metadata } from "next";

import { MagnesiumComparisonPage } from "@/components/comparisons/magnesium-comparison-page";
import {
  magnesiumHero,
  magnesiumMetadataLine,
  magnesiumMethodologyLines,
  magnesiumPrologueSentences,
  magnesiumProducts,
  magnesiumCategoryNote,
} from "@/lib/comparisons/magnesium-page-data";

export const metadata: Metadata = {
  title: "תוספי מגנזיום | Bari",
  description:
    "השוואת 18 תוספי מגנזיום מהמדף הישראלי — ציון Bari לפי מינון יסודי, צורת ספיגה ועדות מדעית. מידע, לא המלצה.",
};

export default function MagnesiumComparisonRoute() {
  return (
    <MagnesiumComparisonPage
      products={magnesiumProducts}
      metadataLine={magnesiumMetadataLine}
      hero={magnesiumHero}
      prologueSentences={magnesiumPrologueSentences}
      methodologyLines={magnesiumMethodologyLines}
      categoryNote={magnesiumCategoryNote}
    />
  );
}
