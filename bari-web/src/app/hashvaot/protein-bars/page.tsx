import type { Metadata } from "next";

import { ProteinBarsComparisonPage } from "@/components/comparisons/protein-bars-comparison-page";
import {
  proteinBarsComparisonMetadata,
  proteinBarsHero,
  proteinBarsMetadataLine,
  proteinBarsMethodologyLines,
  proteinBarsPrologueSentences,
  proteinBarsProducts,
  proteinBarsCategoryNote,
} from "@/lib/comparisons/protein-bars-comparison-page-data";

export const metadata: Metadata = proteinBarsComparisonMetadata;

export default function ProteinBarsComparisonRoute() {
  return (
    <ProteinBarsComparisonPage
      products={proteinBarsProducts}
      metadataLine={proteinBarsMetadataLine}
      hero={proteinBarsHero}
      prologueSentences={proteinBarsPrologueSentences}
      methodologyLines={proteinBarsMethodologyLines}
      categoryNote={proteinBarsCategoryNote}
    />
  );
}
