import type { Metadata } from "next";

import { ChocolateBarsComparisonPage } from "@/components/comparisons/chocolate-bars-comparison-page";
import {
  chocolateBarsComparisonMetadata,
  chocolateBarsHero,
  chocolateBarsMetadataLine,
  chocolateBarsMethodologyLines,
  chocolateBarsPrologueSentences,
  chocolateBarsProducts,
  chocolateBarsCategoryNote,
} from "@/lib/comparisons/chocolate-bars-comparison-page-data";

export const metadata: Metadata = chocolateBarsComparisonMetadata;

export default function ChocolateBarsComparisonRoute() {
  return (
    <ChocolateBarsComparisonPage
      products={chocolateBarsProducts}
      metadataLine={chocolateBarsMetadataLine}
      hero={chocolateBarsHero}
      prologueSentences={chocolateBarsPrologueSentences}
      methodologyLines={chocolateBarsMethodologyLines}
      categoryNote={chocolateBarsCategoryNote}
    />
  );
}
