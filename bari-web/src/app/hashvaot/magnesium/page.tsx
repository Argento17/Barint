// Magnesium supplement comparison route — v3 rebuild (TASK-384).
// Data source: magnesium_v3_latest.json (administered elemental mg + bioavailability class model).
// Grade distribution v3: B(4) · C(4) · D(6) · E(1) + no-score(3). 18 products shown.
// DO NOT COMMIT / DEPLOY — Stage E (orchestrator) handles publish after gate verification.

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
  title: "השוואת תוספי מגנזיום | Bari",
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
