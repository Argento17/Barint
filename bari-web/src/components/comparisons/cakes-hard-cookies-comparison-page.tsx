"use client";

import { useMemo, useState, useCallback } from "react";

import { CategoryHero } from "@/components/shared/category-hero";
import { CategoryPrologue } from "@/components/shared/category-prologue";
import { CategoryShelfLenses } from "@/components/shared/category-shelf-lenses";
import { ComparisonTable } from "@/components/shared/comparison-table";
import { MethodologyFooter } from "@/components/shared/methodology-footer";
import { SUGAR_METRIC } from "@/components/shared/comparison-metric-column";
import { partialThresholdMet } from "@/components/comparisons/comparison-page";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";
import type { BariProductVM } from "@/lib/view-models";

// TASK-226: methodology disclaimer moves into the MethodologyFooter.
const METHODOLOGY_FOOTER_NOTE =
  "הציון מסכם את מה שכתוב על תווית המוצר. הוא אינו המלצה ואינו קובע אם המוצר טוב או רע לאכילה.";

// FIX-3: page-level partial-data disclosure.
const PARTIAL_PAGE_DISCLOSURE =
  "חלק מהמוצרים בדף זה מבוססים על נתונים חלקיים מהתווית.\nהציון כולל את המידע שהיה זמין בסריקה.";

type CakesFilterId = "all" | "least_bad" | "has_phvo" | "no_phvo" | "high_sugar";

// Serializable lens option (no function — safe to pass from Server Component)
export interface CakesLensOption {
  id: CakesFilterId;
  label: string;
}

export interface CakesHardCookiesComparisonPageProps {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  categoryNote?: string;
  /** Serializable lens options only — filter logic lives in this Client Component. */
  lensOptions: CakesLensOption[];
  /** Product ids that contain partially-hydrogenated vegetable oil — precomputed in page-data. */
  phvoIds: string[];
  /** Product ids with sugar >= 30g/100g — precomputed in page-data. */
  highSugarIds: string[];
  initialExpandedProductId?: string | null;
}

// Sugar is the headline metric — thesis: sugar + sat-fat.
// Shelf range: 9.9g (best) to ~50g (worst). Scale 0–55. lowerIsBetter.
const CAKES_METRIC_SPECS = [
  {
    ...SUGAR_METRIC,
    label: "סוכר ל-100 גרם",
    scaleMax: 55,
    good: 10,
    poor: 30,
  },
] as const;

/**
 * Cakes & Hard Cookies comparison page — patterned on BrinedCheesesComparisonPage
 * (golden template, TASK-283). Scoped CSS uses .chc-page to prevent any regression
 * to other categories. Filter logic lives here (Client Component) — only serializable
 * data (phvoIds, highSugarIds, lensOptions) passes from the Server Component route.
 */
export function CakesHardCookiesComparisonPage({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  categoryNote,
  lensOptions,
  phvoIds,
  highSugarIds,
  initialExpandedProductId = null,
}: CakesHardCookiesComparisonPageProps) {
  const [activeFilters, setActiveFilters] = useState<CakesFilterId[]>([]);

  // Precompute id sets once from props (stable references)
  const phvoSet = useMemo(() => new Set(phvoIds), [phvoIds]);
  const highSugarSet = useMemo(() => new Set(highSugarIds), [highSugarIds]);

  const onToggle = useCallback((id: CakesFilterId) => {
    setActiveFilters((prev) => {
      if (prev.includes(id)) return prev.filter((f) => f !== id);
      return [...prev, id];
    });
  }, []);

  const filteredProducts = useMemo(() => {
    if (activeFilters.length === 0) return products;
    return activeFilters.reduce((acc, filterId) => {
      switch (filterId) {
        case "least_bad":
          // Category tops out at D after the D4 contested-additive patch — the
          // single former-C product (bc 7290119030095) moved C→D, so the best
          // available grade is now D (2 products). No A/B/C exist (RT-R1).
          return acc.filter((p) => p.grade === "D");
        case "has_phvo":
          return acc.filter((p) => phvoSet.has(p.id));
        case "no_phvo":
          return acc.filter((p) => !phvoSet.has(p.id));
        case "high_sugar":
          return acc.filter((p) => highSugarSet.has(p.id));
        default:
          return acc;
      }
    }, products);
  }, [products, activeFilters, phvoSet, highSugarSet]);

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
     * Cakes-scoped row polish via class "chc-page".
     * All CSS overrides are scoped to .chc-page — NO regression to other categories.
     * Mirrors the bc-page treatment from the brined golden template.
     */
    <div className="chc-page min-h-screen bg-[#EFEFEB] sm:py-8 lg:py-10" dir="rtl">
      {/* Scoped style block — ONLY affects .chc-page descendants */}
      <style>{`
        .chc-page .bari-cmp-row:nth-child(even of .bari-cmp-row) {
          background: #F5F5F2;
        }
        .chc-page .bari-cmp-row {
          border-bottom-color: rgba(17,19,24,0.07);
        }
        .chc-page .bari-cmp-rowhead:hover {
          background: rgba(31,143,106,0.055);
        }
        .chc-page .bari-cmp-rowhead:active {
          background: rgba(31,143,106,0.09);
        }
        .chc-page .bari-cmp-rowhead {
          padding: 16px 16px;
        }
        @container bari-cmptable (min-width: 680px) {
          .chc-page .bari-cmp-rowhead {
            padding: 16px 22px;
          }
        }
        .chc-page .bari-cmp-colhead {
          font-family: var(--font-sans, ui-sans-serif, system-ui, sans-serif);
          font-size: 0.65rem;
          font-weight: 600;
          text-transform: none;
          letter-spacing: 0.04em;
          color: #8A908B;
        }
        .chc-page .bari-cmp-divider {
          background: transparent;
        }
        .chc-page .bc-row-verdict {
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
        {/* Hero */}
        <CategoryHero
          eyebrow={hero.eyebrow}
          title={hero.title}
          metadata={metadataLine}
          wide
        />

        {/* Prologue */}
        <CategoryPrologue sentences={[...prologueSentences]} wide />

        {/* Mandatory "הערת קטגוריה" yellow box (Bari Category Caveat Standard) */}
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

        {/* 5 shelf lens filters — above the product table */}
        {lensOptions.length > 0 ? (
          <div className={cn("px-0 pb-0", comparisonWebSectionPaddingClass())}>
            <CategoryShelfLenses
              activeFilters={activeFilters}
              onToggle={onToggle}
              lensOptions={lensOptions}
              wide
            />
          </div>
        ) : null}

        <ComparisonTable
          key={`${expandedProductId ?? "none"}-${activeFilters.join(",")}`}
          products={filteredProducts}
          metricSpecs={CAKES_METRIC_SPECS}
          initialExpandedProductId={expandedProductId}
          category="cakes-hard-cookies"
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
