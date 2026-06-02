import type { Metadata } from "next";

import { HummusComparisonPage } from "@/components/comparisons/hummus-comparison-page";
import {
  hummusHero,
  hummusMetadataLine,
  hummusMethodologyLines,
  hummusPrologueSentences,
  hummusProducts,
  hummusCategoryNote,
  hummusComparisonMetadata,
} from "@/lib/comparisons/hummus-comparison-page-data";

export const metadata: Metadata = hummusComparisonMetadata;

export default function HummusComparisonRoute() {
  return (
    <HummusComparisonPage
      products={hummusProducts}
      metadataLine={hummusMetadataLine}
      hero={hummusHero}
      prologueSentences={hummusPrologueSentences}
      methodologyLines={hummusMethodologyLines}
      categoryNote={hummusCategoryNote}
    />
  );
}
