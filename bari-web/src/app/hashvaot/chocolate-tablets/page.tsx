import type { Metadata } from "next";

import { ChocolateTabletsComparisonPage } from "@/components/comparisons/chocolate-tablets-comparison-page";
import {
  chocolateTabletsComparisonMetadata,
  chocolateTabletsHero,
  chocolateTabletsMetadataLine,
  chocolateTabletsMethodologyLines,
  chocolateTabletsPrologueSentences,
  chocolateTabletsProducts,
  chocolateTabletsCategoryNote,
} from "@/lib/comparisons/chocolate-tablets-comparison-page-data";

export const metadata: Metadata = chocolateTabletsComparisonMetadata;

export default function ChocolateTabletsComparisonRoute() {
  return (
    <ChocolateTabletsComparisonPage
      products={chocolateTabletsProducts}
      metadataLine={chocolateTabletsMetadataLine}
      hero={chocolateTabletsHero}
      prologueSentences={chocolateTabletsPrologueSentences}
      methodologyLines={chocolateTabletsMethodologyLines}
      categoryNote={chocolateTabletsCategoryNote}
    />
  );
}
