import type { Metadata } from "next";

import { MilkComparisonPage } from "@/components/comparisons/milk-comparison-page";
import {
  milkBlogLink,
  milkCategoryNote,
  milkComparisonMetadata,
  milkHero,
  milkMetadataLine,
  milkMethodologyLines,
  milkPrologueSentences,
  milkVmProducts,
} from "@/lib/comparisons/milk-comparison-page-data";

export const metadata: Metadata = milkComparisonMetadata;

export default function MilkComparisonRoute() {
  return (
    <MilkComparisonPage
      products={milkVmProducts}
      metadataLine={milkMetadataLine}
      hero={milkHero}
      prologueSentences={milkPrologueSentences}
      methodologyLines={milkMethodologyLines}
      categoryNote={milkCategoryNote}
      blogLink={milkBlogLink}
    />
  );
}
