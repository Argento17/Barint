import type { Metadata } from "next";

import { CheeseComparisonPage } from "@/components/comparisons/cheese-comparison-page";
import {
  cheeseHero,
  cheeseMetadataLine,
  cheeseMethodologyLines,
  cheesePrologueSentences,
  cheeseProducts,
  cheeseCategoryNote,
  cheeseComparisonMetadata,
} from "@/lib/comparisons/cheese-comparison-page-data";

export const metadata: Metadata = cheeseComparisonMetadata;

export default function CheeseComparisonRoute() {
  return (
    <CheeseComparisonPage
      products={cheeseProducts}
      metadataLine={cheeseMetadataLine}
      hero={cheeseHero}
      prologueSentences={cheesePrologueSentences}
      methodologyLines={cheeseMethodologyLines}
      categoryNote={cheeseCategoryNote}
    />
  );
}
