"use client";

// Creatine supplement comparison page wrapper — TASK-492C.
// Cloned from magnesium-comparison-page.tsx (structural template per delegation).
//
// Product ruling 1: NO A–E grade / no numeric score. ScoreChip already renders "—"
// cleanly for score/grade null (same no-score row pattern magnesium uses for its
// 3 UNRESOLVED products) — reused as-is, no changes to ScoreChip needed.
//
// Two sections (Israeli shelf 18 / worldwide benchmark 13) render via the
// ComparisonPage `renderProducts` escape hatch as two separate ComparisonTable
// instances with a section heading between them, mirroring §1.2/§1.3 of the
// content package. Each section keeps its own corpus order (already sorted by
// price-per-effective-gram within dose-honesty tier in creatine-page-data.ts) —
// the UI never re-sorts (Invariant 1).

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { ComparisonTable } from "@/components/shared/comparison-table";
import { CreatineEvidenceSection } from "@/components/shared/creatine-evidence-section";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";
import type { BariProductVM } from "@/lib/view-models";
import {
  creatineIsraeliSectionLabel,
  creatineWorldwideSectionLabel,
  creatineEvidenceSections,
} from "@/lib/comparisons/creatine-page-data";

export interface CreatineComparisonPageProps {
  israeliProducts: BariProductVM[];
  worldwideProducts: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  categoryNote?: string;
  initialExpandedProductId?: string | null;
}

// No shelf filters — same posture as magnesium (empty lens set, all products pass through).
const creatineShelfFilters = {
  lensOptions: [] as { id: string; label: string }[],
  filterProducts: (products: BariProductVM[], _activeFilters: string[]) => products,
} as const;

// No headline metric column — supplements don't have a single dominant numeric column.
const CREATINE_METRIC_SPECS = [] as const;

function SectionHeading({ label }: { label: string }) {
  return (
    <div className={cn("px-4 pt-3 pb-1", comparisonWebSectionPaddingClass())}>
      <h2
        className="font-mono text-[11px] font-bold uppercase tracking-[0.1em] text-[#6E756D]"
        dir="rtl"
      >
        {label}
      </h2>
    </div>
  );
}

export function CreatineComparisonPage({
  israeliProducts,
  worldwideProducts,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: CreatineComparisonPageProps) {
  // Combined corpus for auto-expand / deep-link resolution — the two tables below
  // slice back out of the same two source arrays so corpus order is preserved.
  const allProducts = [...israeliProducts, ...worldwideProducts];

  return (
    <ComparisonPage
      products={allProducts}
      metadataLine={metadataLine}
      hero={hero}
      prologueSentences={prologueSentences}
      methodologyLines={methodologyLines}
      shelfFilters={creatineShelfFilters}
      metricSpecs={CREATINE_METRIC_SPECS}
      categoryNote={categoryNote}
      initialExpandedProductId={initialExpandedProductId}
      category="creatine"
      exploreNextCategoryId="creatine"
      collapseMobileNote
      collapseMobilePrologue
      noAutoExpand
      clampVerdictLines={3}
      compactDividers
      forcePartialDisclosure
      renderProducts={(_filteredProducts, expandedProductId) => (
        <>
          <SectionHeading label={creatineIsraeliSectionLabel} />
          <ComparisonTable
            key={`israeli-${expandedProductId ?? "none"}`}
            products={israeliProducts}
            metricSpecs={CREATINE_METRIC_SPECS}
            showRank={false}
            initialExpandedProductId={expandedProductId}
            category="creatine"
            suppressPartialBadges
            clampVerdictLines={3}
            compactDividers
          />
          <SectionHeading label={creatineWorldwideSectionLabel} />
          <ComparisonTable
            key={`worldwide-${expandedProductId ?? "none"}`}
            products={worldwideProducts}
            metricSpecs={CREATINE_METRIC_SPECS}
            showRank={false}
            initialExpandedProductId={expandedProductId}
            category="creatine"
            suppressPartialBadges
            clampVerdictLines={3}
            compactDividers
          />
          {/* TASK-492C FIX 1: evidence prose (efficacy tiers, effective dose, forms,
              safety, dose-honesty tier definitions, dairy annotation) renders BELOW
              the product tables — the 31-row comparison is the hero of the page. */}
          <div className={cn("px-4 pt-2", comparisonWebSectionPaddingClass())}>
            <CreatineEvidenceSection sections={[...creatineEvidenceSections]} />
          </div>
        </>
      )}
    />
  );
}
