import type { Metadata } from "next";

import { BreadComparisonPage } from "@/components/comparisons/bread-comparison-page";
import {
  breadHero,
  breadMetadataLine,
  breadMethodologyLines,
  breadPrologueSentences,
  breadProducts,
  breadComparisonMetadata,
} from "@/lib/comparisons/bread-comparison-page-data";

export const metadata: Metadata = breadComparisonMetadata;

export default function BreadComparisonRoute() {
  return (
    <BreadComparisonPage
      products={breadProducts}
      metadataLine={breadMetadataLine}
      hero={breadHero}
      prologueSentences={breadPrologueSentences}
      methodologyLines={breadMethodologyLines}
    />
  );
}
