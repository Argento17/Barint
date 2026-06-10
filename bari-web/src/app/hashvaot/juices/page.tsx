import type { Metadata } from "next";

import { JuicesComparisonPage } from "@/components/comparisons/juices-comparison-page";
import {
  juicesCategoryNote,
  juicesHero,
  juicesMetadataLine,
  juicesMethodologyLines,
  juicesPrologueSentences,
  juicesProducts,
} from "@/lib/comparisons/juices-page-data";

export const metadata: Metadata = {
  title: "השוואת מיצים ומשקאות פירות | Bari",
  description:
    'השוואת 65 מיצים ומשקאות פירות מהמדף הישראלי — ציון Bari, סוכר ל-100 מ"ל, ריכוז פרי ורמת עיבוד. מידע, לא המלצה.',
};

export default function JuicesComparisonRoute() {
  return (
    <JuicesComparisonPage
      products={juicesProducts}
      metadataLine={juicesMetadataLine}
      hero={juicesHero}
      prologueSentences={juicesPrologueSentences}
      methodologyLines={juicesMethodologyLines}
      categoryNote={juicesCategoryNote}
    />
  );
}
