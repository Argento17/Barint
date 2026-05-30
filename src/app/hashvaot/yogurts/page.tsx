import type { Metadata } from "next";

import { YogurtsComparisonPage } from "@/components/comparisons/yogurts-comparison-page";
import {
  yogurtsHero,
  yogurtsMetadataLine,
  yogurtsMethodologyLines,
  yogurtsPrologueSentences,
  yogurtsProducts,
  yogurtsComparisonMetadata,
} from "@/lib/comparisons/yogurts-comparison-page-data";

export const metadata: Metadata = yogurtsComparisonMetadata;

export default function YogurtsComparisonRoute() {
  return (
    <YogurtsComparisonPage
      products={yogurtsProducts}
      metadataLine={yogurtsMetadataLine}
      hero={yogurtsHero}
      prologueSentences={yogurtsPrologueSentences}
      methodologyLines={yogurtsMethodologyLines}
    />
  );
}
