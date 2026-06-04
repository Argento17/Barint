"use client";

import { useMemo, useState } from "react";

import { CategoryHero } from "@/components/shared/category-hero";
import { CategoryPrologue } from "@/components/shared/category-prologue";
import { CategoryShelfLenses } from "@/components/shared/category-shelf-lenses";
import { MethodologyFooter } from "@/components/shared/methodology-footer";
import { ComparisonTable } from "@/components/shared/comparison-table";
import type { MetricSpec } from "@/components/shared/comparison-metric-column";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import type { ComparisonShelfFilters } from "@/lib/comparisons/registry/types";
import { cn } from "@/lib/utils";
import type { BariProductVM } from "@/lib/view-models";

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
}

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
}: ComparisonPageProps<TFilterId>) {
  const [activeFilters, setActiveFilters] = useState<TFilterId[]>([]);

  const filteredProducts = useMemo(
    () => shelfFilters.filterProducts(products, activeFilters),
    [activeFilters, products, shelfFilters]
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

        <CategoryShelfLenses
          lensOptions={shelfFilters.lensOptions}
          activeFilters={activeFilters}
          onToggle={(filter) =>
            setActiveFilters((current) =>
              current.includes(filter)
                ? current.filter((value) => value !== filter)
                : [...current, filter]
            )
          }
          wide
        />

        <ComparisonTable
          key={expandedProductId ?? "none"}
          products={filteredProducts}
          metricSpecs={metricSpecs}
          showRail
          initialExpandedProductId={expandedProductId}
          category={category}
        />

        <MethodologyFooter lines={[...methodologyLines]} wide />
      </div>
    </div>
  );
}
