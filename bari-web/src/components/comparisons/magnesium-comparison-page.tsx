"use client";

// Magnesium supplement comparison page wrapper.
// Cloned from cereals-comparison-page.tsx.
// No shelf filters for the prototype (empty lens set — filterProducts passes all through).
//
// TASK-384A: MagnesiumSafetyBox injected above the ComparisonPage prologue area.
// It uses the collapseMobileNote collapse pattern already in place for the category note.

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { MagnesiumSafetyBox } from "@/components/shared/magnesium-safety-box";
import type { BariProductVM } from "@/lib/view-models";

export interface MagnesiumComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  /** Single category-wide caveat, shown once in the header (standard format). */
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

// No shelf filters for the prototype — pass all products through unchanged.
const magnesiumShelfFilters = {
  lensOptions: [] as { id: string; label: string }[],
  filterProducts: (products: BariProductVM[], _activeFilters: string[]) => products,
} as const;

// No headline metric — supplements don't have a single dominant numeric column.
const MAGNESIUM_METRIC_SPECS = [] as const;

export function MagnesiumComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: MagnesiumComparisonPageProps) {
  return (
    <ComparisonPage
      products={products}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={magnesiumShelfFilters}
      metricSpecs={MAGNESIUM_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="magnesium"
      collapseMobileNote
      collapseMobilePrologue
      noAutoExpand
      headerSlot={<MagnesiumSafetyBox />}
      clampVerdictLines={3}
      compactDividers
      forcePartialDisclosure
    />
  );
}
