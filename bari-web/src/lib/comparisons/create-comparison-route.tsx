import type { Metadata } from "next";

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import {
  getComparisonCategory,
  type ComparisonCategoryId,
} from "@/lib/comparisons/registry";

/**
 * Factory for hashvaot comparison routes. Maadanim keeps its dedicated route file;
 * future categories can use this helper to avoid duplicating the server shell.
 */
export function createComparisonCategoryRoute(categoryId: ComparisonCategoryId) {
  const category = getComparisonCategory(categoryId);

  const metadata: Metadata = category.metadata;

  function ComparisonCategoryRoute() {
    const pageData = category.getPageData();

    return (
      <ComparisonPage
        products={pageData.products}
        metadataLine={pageData.metadataLine}
        hero={pageData.hero}
        prologueSentences={pageData.prologueSentences}
        methodologyLines={pageData.methodologyLines}
        shelfFilters={pageData.shelfFilters}
        metricSpecs={[]}
      />
    );
  }

  return { metadata, ComparisonCategoryRoute };
}
