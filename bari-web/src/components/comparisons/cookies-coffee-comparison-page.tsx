"use client";

import { useMemo } from "react";

import { CategoryHero } from "@/components/shared/category-hero";
import { CategoryPrologue } from "@/components/shared/category-prologue";
import { ComparisonTable } from "@/components/shared/comparison-table";
import { MethodologyFooter } from "@/components/shared/methodology-footer";
import {
  SUGAR_METRIC,
  COOKIES_COFFEE_SAT_FAT_METRIC,
} from "@/components/shared/comparison-metric-column";
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

export interface CookiesCoffeeComparisonPageProps {
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

const cookiesCoffeeShelfFilters = {
  lensOptions: [],
  // Filters are hidden — always return the full corpus unchanged.
  filterProducts: (products: BariProductVM[]) => products,
};

// Sugar + saturated-fat are the two headline row metrics — the thesis is sugar+sat-fat, NOT sodium.
// Sugar: shelf median ~21.5g. Scale 0–45 covers the full range (max observed 44.3g).
//   The SUGAR_METRIC default (scaleMax:15, good:5, poor:10) is tuned for drinks; override for biscuits.
// Sat-fat: shelf range 0.4–17.0g, median ~9g. See COOKIES_COFFEE_SAT_FAT_METRIC for calibration.
const COOKIES_COFFEE_METRIC_SPECS = [
  {
    ...SUGAR_METRIC,
    label: "סוכר ל-100 גרם",
    scaleMax: 45,
    good: 10,
    poor: 25,
    neutralBarFill: "#7A817C" as string,
  },
  COOKIES_COFFEE_SAT_FAT_METRIC,
] as const;

/**
 * Cookies & Coffee — comparison page (TASK-275).
 * Cloned from BrinedCheesesComparisonPage (golden template).
 * No charts in this step — charts are a separate task.
 * Scoped CSS uses .cc-page to avoid any regression to other categories.
 */
export function CookiesCoffeeComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  initialExpandedProductId = null,
}: CookiesCoffeeComparisonPageProps) {
  const filteredProducts = useMemo(
    () => cookiesCoffeeShelfFilters.filterProducts(products),
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
     * Cookies-scoped row polish via class "cc-page".
     * All CSS overrides are scoped to .cc-page so NO other category is affected.
     * Mirrors the bc-page treatment from the brined golden template.
     */
    <div className="cc-page min-h-screen bg-[#EFEFEB] sm:py-8 lg:py-10" dir="rtl">
      {/* Scoped style block — ONLY affects .cc-page descendants */}
      <style>{`
        /* even-row warm bg — overrides global .bari-cmp-row:nth-child(even of .bari-cmp-row) */
        .cc-page .bari-cmp-row:nth-child(even of .bari-cmp-row) {
          background: #F5F5F2;
        }
        /* row border: slightly deeper */
        .cc-page .bari-cmp-row {
          border-bottom-color: rgba(17,19,24,0.07);
        }
        /* hover + active — warmer green tint */
        .cc-page .bari-cmp-rowhead:hover {
          background: rgba(31,143,106,0.055);
        }
        .cc-page .bari-cmp-rowhead:active {
          background: rgba(31,143,106,0.09);
        }
        /* mobile row padding: 16px 16px */
        .cc-page .bari-cmp-rowhead {
          padding: 16px 16px;
        }
        /* desktop row padding: 16px 22px */
        @container bari-cmptable (min-width: 680px) {
          .cc-page .bari-cmp-rowhead {
            padding: 16px 22px;
          }
        }
        /* column header: drop monospace/uppercase → font-sans, human label */
        .cc-page .bari-cmp-colhead {
          font-family: var(--font-sans, ui-sans-serif, system-ui, sans-serif);
          font-size: 0.65rem;
          font-weight: 600;
          text-transform: none;
          letter-spacing: 0.04em;
          color: #8A908B;
        }
        /* band dividers: transparent bg (remove #fafaf7 stripe) */
        .cc-page .bari-cmp-divider {
          background: transparent;
        }
        /* rowVerdict margin */
        .cc-page .bc-row-verdict {
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

        {/* 1px separator between prologue/note block and table */}
        <div
          className={cn(
            "mx-4 border-t border-[rgba(17,19,24,0.06)]",
            comparisonWebSectionPaddingClass() && "lg:mx-8 xl:mx-10 2xl:mx-12"
          )}
          aria-hidden
        />

        {/* Category note — px-4 py-3 rounded-xl leading-[1.6] */}
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
          metricSpecs={COOKIES_COFFEE_METRIC_SPECS}
          initialExpandedProductId={expandedProductId}
          category="cookies-coffee"
          suppressPartialBadges={suppressPartialBadges}
        />

        <MethodologyFooter
          lines={[...methodologyLines, METHODOLOGY_FOOTER_NOTE]}
          wide
        />
      </div>
    </div>
  );
}
