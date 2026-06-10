"use client";

import React, { useMemo } from "react";

import { CategoryHero } from "@/components/shared/category-hero";
import { CategoryPrologue } from "@/components/shared/category-prologue";
import { MethodologyFooter } from "@/components/shared/methodology-footer";
import { ComparisonTable } from "@/components/shared/comparison-table";
import type { MetricSpec } from "@/components/shared/comparison-metric-column";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import type { ComparisonShelfFilters } from "@/lib/comparisons/registry/types";
import { cn } from "@/lib/utils";
import type { BariProductVM } from "@/lib/view-models";

// FIX-1: methodology note — appears on every comparison page, below the category note.
// Text is fixed; does not vary by category.
const METHODOLOGY_NOTE =
  "ציוני ברי מחושבים על ידי מערכת הערכה שבוחנת בצורה שיטתית ערכים תזונתיים, רכיבים ורמת עיבוד על בסיס נתוני התווית הזמנים. הציון מתאר את מה שנמצא במוצר לפי הנתונים הזמינים לנו. הוא אינו המלצה וגם לא קובע אם המוצר טוב או רע לאכילה, אלא מספק הקשר רחב יותר למה שנכנס לגוף שלך.";

// FIX-3: If ≥50% of products have confidence==="partial", suppress per-product badges
// and show a page-level disclosure note instead.
const PARTIAL_PAGE_DISCLOSURE =
  "חלק מהמוצרים בדף זה מבוססים על נתונים חלקיים מהתווית.\nהציון כולל את המידע שהיה זמין בסריקה.";

function partialThresholdMet(products: BariProductVM[]): boolean {
  if (products.length === 0) return false;
  const partialCount = products.filter((p) => p.confidence === "partial").length;
  return partialCount / products.length >= 0.5;
}

// The single unified comparison page (IMP-1 + IMP-4). Responsive from one tree:
// the table reflows phone↔desktop via container queries (no second component), the
// side band rail appears on lg+, and the chrome (hero/prologue/lenses/methodology)
// is the shared, `wide`-aware set. Replaces both ComparisonShelfPage (phone frame)
// and BariComparisonDesktopPage (bespoke desktop chrome).

export interface ComparisonPageProps<TFilterId extends string = string> {
  products: BariProductVM[];
  metadataLine: string;
  hero: { eyebrow: string; title: string };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  shelfFilters: ComparisonShelfFilters<TFilterId>;
  /** Category-scoped metric set (README §7). Empty → no metric column. */
  metricSpecs: readonly MetricSpec[];
  /** IMP-6: a single category-wide caveat shown once in the header (not per row). */
  categoryNote?: string;
  /** Optional editorial CTA (e.g. a blog deep-dive) shown under the prologue. */
  blogLink?: { href: string; label: string };
  initialExpandedProductId?: string | null;
  /** Category slug for analytics context (TASK-179T — additive panel engagement events). */
  category?: string;
  /** TASK-181Q: when true + NEXT_PUBLIC_GLASSBOX_W5=on, appends a "פירוט המתודולוגיה" inline link
   *  to /research/glass-box at the end of the methodology footer. When W5 is OFF, byte-identical to HEAD. */
  glassBoxMethodologyLink?: boolean;
  /**
   * Optional escape hatch for categories that need custom product rendering (e.g. section
   * grouping). When provided, replaces the default <ComparisonTable> call entirely.
   * Receives the filtered product list and the resolved initialExpandedProductId so the
   * caller can pass them through to its own <ComparisonTable> instances.
   */
  renderProducts?: (
    filteredProducts: BariProductVM[],
    expandedProductId: string | null
  ) => React.ReactNode;
}

/** Exposed so ComparisonTable can receive it without prop-drilling through page props. */
export { partialThresholdMet };

export function ComparisonPage<TFilterId extends string = string>({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  shelfFilters,
  metricSpecs,
  categoryNote,
  blogLink,
  initialExpandedProductId = null,
  category,
  glassBoxMethodologyLink = false,
  renderProducts,
}: ComparisonPageProps<TFilterId>) {
  // FIX-5: filters are hidden — active set is always empty. The shelfFilters prop is
  // retained on the interface so pages compile unchanged; filterProducts receives [] and
  // returns the full corpus (no filtering applied).
  const filteredProducts = useMemo(
    () => shelfFilters.filterProducts(products, []),
    [products, shelfFilters]
  );

  // Corpus order is preserved by filterProducts (Invariant 1); pick the first visible
  // product as the initially-open row when the chosen one is filtered out.
  const expandedProductId = useMemo(
    () =>
      initialExpandedProductId &&
      filteredProducts.some((p) => p.id === initialExpandedProductId)
        ? initialExpandedProductId
        : (filteredProducts[0]?.id ?? null),
    [filteredProducts, initialExpandedProductId]
  );

  // FIX-3: compute threshold once against the full (unfiltered) product list so the
  // page-level disclosure appears regardless of which shelf lens is active.
  const suppressPartialBadges = partialThresholdMet(products);

  return (
    <div className="min-h-screen bg-[#EFEFEB] sm:py-8 lg:py-10" dir="rtl">
      <div
        className={cn(
          "mx-auto w-full overflow-hidden bg-white",
          "max-w-[640px] sm:rounded-[1.5rem] sm:shadow-xl",
          "lg:max-w-[1180px] lg:rounded-[1.25rem] lg:shadow-[0_24px_70px_-44px_rgba(17,19,24,0.4)]"
        )}
      >
        <CategoryHero eyebrow={hero.eyebrow} title={hero.title} metadata={metadataLine} wide />
        <CategoryPrologue sentences={[...prologueSentences]} wide />

        {blogLink ? (
          <div className={cn("px-4 pb-1", comparisonWebSectionPaddingClass())}>
            <a
              href={blogLink.href}
              className="text-[13px] font-semibold text-[#1F8F6A] hover:underline"
            >
              {blogLink.label}
            </a>
          </div>
        ) : null}

        {categoryNote ? (
          <div className={cn("px-4 pb-1", comparisonWebSectionPaddingClass())}>
            <p className="whitespace-pre-line rounded-[9px] border border-[#ECE3C8] bg-[#FBF8EE] px-3 py-2 text-[12px] leading-[1.5] text-[#6A6147]">
              {categoryNote}
            </p>
          </div>
        ) : null}

        {/* FIX-1: methodology disclaimer — appears on every page, below category note. */}
        <div className={cn("px-4 pb-1 mt-2", comparisonWebSectionPaddingClass())}>
          <p className="whitespace-pre-line rounded-[9px] border border-[#ECE3C8] bg-[#FBF8EE] px-3 py-2 text-[12px] leading-[1.5] text-[#6A6147]">
            {METHODOLOGY_NOTE}
          </p>
        </div>

        {/* FIX-3: page-level partial-data disclosure (shown when ≥50% of products are partial). */}
        {suppressPartialBadges ? (
          <div className={cn("px-4 pb-1 mt-2", comparisonWebSectionPaddingClass())}>
            <p className="whitespace-pre-line rounded-[9px] border border-[#ECE3C8] bg-[#FBF8EE] px-3 py-2 text-[12px] leading-[1.5] text-[#6A6147]">
              {PARTIAL_PAGE_DISCLOSURE}
            </p>
          </div>
        ) : null}

        {/* FIX-5: filter boxes hidden until a proper taxonomy is designed. The
            CategoryShelfLenses component is kept in the tree but not rendered. */}

        {renderProducts ? (
          renderProducts(filteredProducts, expandedProductId)
        ) : (
          <ComparisonTable
            key={expandedProductId ?? "none"}
            products={filteredProducts}
            metricSpecs={metricSpecs}
            showRail
            initialExpandedProductId={expandedProductId}
            category={category}
            suppressPartialBadges={suppressPartialBadges}
          />
        )}

        <MethodologyFooter lines={[...methodologyLines]} wide glassBoxMethodologyLink={glassBoxMethodologyLink} />
      </div>
    </div>
  );
}
