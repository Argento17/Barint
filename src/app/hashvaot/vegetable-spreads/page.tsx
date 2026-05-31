import type { Metadata } from "next";

import { VegetableSpreadsComparisonPage } from "@/components/comparisons/vegetable-spreads-comparison-page";
import {
  vegetableSpreadsHero,
  vegetableSpreadsMetadataLine,
  vegetableSpreadsMethodologyLines,
  vegetableSpreadsPrologueSentences,
  vegetableSpreadsProducts,
  vegetableSpreadsComparisonMetadata,
} from "@/lib/comparisons/vegetable-spreads-comparison-page-data";

export const metadata: Metadata = vegetableSpreadsComparisonMetadata;

export default function VegetableSpreadsComparisonRoute() {
  return (
    <VegetableSpreadsComparisonPage
      products={vegetableSpreadsProducts}
      metadataLine={vegetableSpreadsMetadataLine}
      hero={vegetableSpreadsHero}
      prologueSentences={vegetableSpreadsPrologueSentences}
      methodologyLines={vegetableSpreadsMethodologyLines}
    />
  );
}
