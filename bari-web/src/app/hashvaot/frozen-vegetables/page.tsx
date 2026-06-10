import type { Metadata } from "next";

import { FrozenVegetablesComparisonPage } from "@/components/comparisons/frozen-vegetables-comparison-page";
import {
  frozenVegetablesBands,
  frozenVegetablesCategoryNote,
  frozenVegetablesComparisonMetadata,
  frozenVegetablesFooterNote,
  frozenVegetablesHero,
  frozenVegetablesMetadataLine,
  frozenVegetablesMethodologyLines,
  frozenVegetablesPrologueSentences,
  frozenVegetablesV2Products,
} from "@/lib/comparisons/frozen-vegetables-comparison-page-data";

export const metadata: Metadata = frozenVegetablesComparisonMetadata;

export default function FrozenVegetablesComparisonRoute() {
  return (
    <FrozenVegetablesComparisonPage
      bands={frozenVegetablesBands}
      products={frozenVegetablesV2Products}
      hero={frozenVegetablesHero}
      metadataLine={frozenVegetablesMetadataLine}
      prologueSentences={frozenVegetablesPrologueSentences}
      categoryNote={frozenVegetablesCategoryNote}
      methodologyLines={frozenVegetablesMethodologyLines}
      footerNote={frozenVegetablesFooterNote}
    />
  );
}
