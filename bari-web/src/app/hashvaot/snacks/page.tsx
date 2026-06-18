import type { Metadata } from "next";

import { SnacksComparisonPage } from "@/components/comparisons/snacks-comparison-page";
import {
  snacksComparisonMetadata,
  snacksHero,
  snacksMetadataLine,
  snacksMethodologyLines,
  snacksPrologueSentences,
  snacksProducts,
  snacksCategoryNote,
} from "@/lib/comparisons/snacks-comparison-page-data";

export const metadata: Metadata = snacksComparisonMetadata;

export default function SnacksComparisonRoute() {
  return (
    <SnacksComparisonPage
      products={snacksProducts}
      metadataLine={snacksMetadataLine}
      hero={snacksHero}
      prologueSentences={snacksPrologueSentences}
      methodologyLines={snacksMethodologyLines}
      categoryNote={snacksCategoryNote}
    />
  );
}
