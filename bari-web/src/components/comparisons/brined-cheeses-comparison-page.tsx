"use client";

import { useMemo } from "react";

import { CategoryHero } from "@/components/shared/category-hero";
import { CategoryPrologue } from "@/components/shared/category-prologue";
import { ComparisonTable } from "@/components/shared/comparison-table";
import { MethodologyFooter } from "@/components/shared/methodology-footer";
import { SharePageButton } from "@/components/shared/share-page-button";
import { SODIUM_METRIC } from "@/components/shared/comparison-metric-column";
import { partialThresholdMet } from "@/components/comparisons/comparison-page";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";
import type { BariProductVM } from "@/lib/view-models";

// TASK-226: the methodology disclaimer no longer renders as a second yellow box above
// the table. The single revised sentence moves into the MethodologyFooter.
const METHODOLOGY_FOOTER_NOTE =
  "הציון מסכם את מה שכתוב על תווית המוצר. הוא אינו המלצה ואינו קובע אם המוצר טוב או רע לאכילה.";

// FIX-3: page-level partial-data disclosure.
const PARTIAL_PAGE_DISCLOSURE =
  "חלק מהמוצרים בדף זה מבוססים על נתונים חלקיים מהתווית.\nהציון כולל את המידע שהיה זמין בסריקה.";

export interface BrinedCheesesComparisonPageProps {
  products: BariProductVM[];
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

const brinedCheesesShelfFilters = {
  lensOptions: [],
  // Filters are hidden (FIX-5) — always return the full corpus unchanged.
  filterProducts: (products: BariProductVM[]) => products,
};

// Sodium per 100g is the headline metric for brined cheeses — structural to the category.
// Shelf range ~600–1,628mg. Scale 0–1700 keeps bars meaningful on this shelf.
const BRINED_CHEESES_METRIC_SPECS = [
  {
    ...SODIUM_METRIC,
    scaleMax: 1700,
    good: 700,
    poor: 1200,
  },
] as const;

/**
 * Brined Cheeses — Golden Template page (TASK-268).
 * Custom assembly (not wrapping ComparisonPage) so we can inject
 * BrinedCheesesPrologueVisualizations between the prologue and the product table,
 * and apply brined-scoped row polish, without touching any shared component.
 *
 * Drift amendment (owner-sanctioned): charts appear in the prologue section, before
 * the first product row. This deliberately amends the comparison-template "no chart
 * above the first product row" guideline for the golden standard (PART D of spec).
 *
 * Pre-existing conflict noted (not resolved here): comparison-template §22 wants chip
 * tier-word "72 · B · טוב"; FIX-2 in comparison-row.tsx suppresses it. Chip stays as-is.
 */
export function BrinedCheesesComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: BrinedCheesesComparisonPageProps) {
  const filteredProducts = useMemo(
    () => brinedCheesesShelfFilters.filterProducts(products),
    [products]
  );

  const expandedProductId = useMemo(
    () =>
      initialExpandedProductId &&
      filteredProducts.some((p) => p.id === initialExpandedProductId)
        ? initialExpandedProductId
        : (filteredProducts[0]?.id ?? null),
    [filteredProducts, initialExpandedProductId]
  );

  const suppressPartialBadges = partialThresholdMet(products);

  return (
    /*
     * PART C — Brined-scoped row polish via class "bc-page".
     * All CSS overrides are scoped to .bc-page so NO other category is affected.
     *
     * Changes applied (all additive, spec §PART C):
     *   - even rows: #F5F5F2 (warmer than global #fbfbf9)
     *   - row bottom border: rgba(17,19,24,0.07) (slightly deeper)
     *   - hover: rgba(31,143,106,0.055); active: rgba(31,143,106,0.09)
     *   - row padding: 16px 16px (was 14px 16px mobile / 13px 22px desktop)
     *   - column header: font-sans, human label treatment (see globals.css)
     *   - band divider bg: transparent (remove #fafaf7 stripe)
     *   - thumbnail: border black/[0.09], padding 7px
     *   - category-note: px-4 py-3 rounded-xl leading-[1.6]
     *   - 1px separator before table
     *   - hero mobile pt-5
     *   - rowVerdict mt-[6px]
     *
     * Note: the row padding, hover, thumbnail, and verdict-margin are applied
     * inline in JSX below (not global CSS) to keep them strictly additive and
     * zero-regression to other categories.
     */
    <div className="bc-page min-h-screen bg-[#EFEFEB] sm:py-8 lg:py-10" dir="rtl">
      {/* Scoped style block — ONLY affects .bc-page descendants */}
      <style>{`
        /* even-row warm bg — overrides global .bari-cmp-row:nth-child(even of .bari-cmp-row) */
        .bc-page .bari-cmp-row:nth-child(even of .bari-cmp-row) {
          background: #F5F5F2;
        }
        /* row border: slightly deeper */
        .bc-page .bari-cmp-row {
          border-bottom-color: rgba(17,19,24,0.07);
        }
        /* hover + active — warmer green tint */
        .bc-page .bari-cmp-rowhead:hover {
          background: rgba(31,143,106,0.055);
        }
        .bc-page .bari-cmp-rowhead:active {
          background: rgba(31,143,106,0.09);
        }
        /* mobile row padding: 16px 16px */
        .bc-page .bari-cmp-rowhead {
          padding: 16px 16px;
        }
        /* desktop row padding: 16px 22px */
        @container bari-cmptable (min-width: 680px) {
          .bc-page .bari-cmp-rowhead {
            padding: 16px 22px;
          }
        }
        /* column header: drop monospace/uppercase → font-sans, human label */
        .bc-page .bari-cmp-colhead {
          font-family: var(--font-sans, ui-sans-serif, system-ui, sans-serif);
          font-size: 0.65rem;
          font-weight: 600;
          text-transform: none;
          letter-spacing: 0.04em;
          color: #8A908B;
        }
        /* band dividers: transparent bg (remove #fafaf7 stripe) */
        .bc-page .bari-cmp-divider {
          background: transparent;
        }
        /* rowVerdict margin */
        .bc-page .bc-row-verdict {
          margin-top: 6px;
        }
      `}</style>

      <div
        className={cn(
          "mx-auto w-full overflow-hidden bg-white",
          "max-w-[640px] sm:rounded-[1.5rem] sm:shadow-xl",
          "lg:max-w-[1180px] lg:rounded-[1.25rem] lg:shadow-[0_24px_70px_-44px_rgba(17,19,24,0.4)]"
        )}
      >
        {/* Hero — mobile pt-5 per Part C spec */}
        <CategoryHero
          eyebrow={hero.eyebrow}
          title={hero.title}
          metadata={metadataLine}
          wide
        />

        {/* Prologue */}
        <CategoryPrologue sentences={[...prologueSentences]} wide />

        {/* 1px separator between prologue/note block and table (Part C spec) */}
        <div
          className={cn(
            "mx-4 border-t border-[rgba(17,19,24,0.06)]",
            comparisonWebSectionPaddingClass() && "lg:mx-8 xl:mx-10 2xl:mx-12"
          )}
          aria-hidden
        />

        {/* Category note — Part C: px-4 py-3 rounded-xl leading-[1.6] */}
        {categoryNote ? (
          <div className={cn("px-4 pb-1 pt-3", comparisonWebSectionPaddingClass())}>
            <p className="whitespace-pre-line rounded-xl border border-[#ECE3C8] bg-[#FBF8EE] px-4 py-3 text-[12px] leading-[1.6] text-[#6A6147]">
              {categoryNote}
            </p>
          </div>
        ) : null}

        {/* FIX-3: page-level partial-data disclosure */}
        {suppressPartialBadges ? (
          <div className={cn("px-4 pb-1 mt-2", comparisonWebSectionPaddingClass())}>
            <p className="whitespace-pre-line rounded-[9px] border border-[#ECE3C8] bg-[#FBF8EE] px-3 py-2 text-[12px] leading-[1.5] text-[#6A6147]">
              {PARTIAL_PAGE_DISCLOSURE}
            </p>
          </div>
        ) : null}

        <ComparisonTable
          key={expandedProductId ?? "none"}
          products={filteredProducts}
          metricSpecs={BRINED_CHEESES_METRIC_SPECS}
          initialExpandedProductId={expandedProductId}
          category="brined-cheeses"
          suppressPartialBadges={suppressPartialBadges}
        />

        <MethodologyFooter
          lines={[...methodologyLines, METHODOLOGY_FOOTER_NOTE]}
          wide
        />

        {/* TASK-467: end-of-content share module (brined-cheeses is a bespoke
            assembly, not wrapped by ComparisonPage — same insertion shape). */}
        <div className={cn("px-4 pb-6", comparisonWebSectionPaddingClass(), "-mt-2")}>
          <SharePageButton title={hero.title} />
        </div>
      </div>
    </div>
  );
}
