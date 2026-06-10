import type { Metadata } from "next";

import { FrozenVegetablesComparisonPage } from "@/components/comparisons/frozen-vegetables-comparison-page";
import {
  frozenVegetablesCategoryNote,
  frozenVegetablesComparisonMetadata,
  frozenVegetablesHero,
  frozenVegetablesMetadataLine,
  frozenVegetablesMethodologyLines,
  frozenVegetablesPrologueSentences,
  frozenVegetablesProducts,
} from "@/lib/comparisons/frozen-vegetables-comparison-page-data";

export const metadata: Metadata = frozenVegetablesComparisonMetadata;

export default function FrozenVegetablesComparisonRoute() {
  return (
    <FrozenVegetablesComparisonPage
      products={frozenVegetablesProducts}
      metadataLine={frozenVegetablesMetadataLine}
      hero={frozenVegetablesHero}
      prologueSentences={frozenVegetablesPrologueSentences}
      methodologyLines={frozenVegetablesMethodologyLines}
      categoryNote={frozenVegetablesCategoryNote}
    />
  );
}
