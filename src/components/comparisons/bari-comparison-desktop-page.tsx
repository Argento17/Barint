"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { BariProductShelfRow } from "@/components/comparisons/bari-product-shelf-row";
import {
  ComparisonIntelligenceHero,
  type ComparisonHeroStat,
  type ComparisonIntelligenceHeroProps,
} from "@/components/comparisons/comparison-intelligence-hero";
import { HomeContainer } from "@/components/home/section-frame";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import type { BariProductVM } from "@/lib/view-models";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

export interface BariComparisonDesktopPageProps<TFilterId extends string = string> {
  products: BariProductVM[];
  hero: ComparisonIntelligenceHeroProps;
  prologueSentences?: readonly string[];
  methodologyLines: readonly string[];
  lensOptions: readonly { id: TFilterId; label: string }[];
  filterProducts: (products: BariProductVM[], activeFilters: TFilterId[]) => BariProductVM[];
  blogLink?: { href: string; label: string };
}

export function BariComparisonDesktopPage<TFilterId extends string = string>({
  products,
  hero,
  prologueSentences = [],
  methodologyLines,
  lensOptions,
  filterProducts,
  blogLink,
}: BariComparisonDesktopPageProps<TFilterId>) {
  const [activeFilters, setActiveFilters] = useState<TFilterId[]>([]);

  const filteredProducts = useMemo(
    () => filterProducts(products, activeFilters),
    [activeFilters, filterProducts, products]
  );

  const toggleFilter = (filter: TFilterId) => {
    setActiveFilters((current) =>
      current.includes(filter)
        ? current.filter((value) => value !== filter)
        : [...current, filter]
    );
  };

  return (
    <main className="relative bg-[#F7F7F2] text-[#111318]" dir="rtl">
      <section className={cn(siteHeaderOffsetClass, "border-b border-black/[0.06] bg-[#F7F7F2]")}>
        <HomeContainer className="py-8 md:py-10">
          <Link
            href="/hashvaot"
            className="mb-6 inline-flex w-fit shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
          >
            <ArrowRight className="size-4" aria-hidden />
            חזרה להשוואות
          </Link>

          <ComparisonIntelligenceHero {...hero} />

          {prologueSentences.length > 0 ? (
            <div className="mx-auto mt-8 max-w-3xl space-y-3 text-right">
              {prologueSentences.map((sentence) => (
                <p key={sentence} className="text-base leading-relaxed text-[#4E5663]">
                  {sentence}
                </p>
              ))}
            </div>
          ) : null}

          {blogLink ? (
            <p className="mt-6 text-sm font-semibold text-[#1F8F6A]">
              <Link href={blogLink.href} className="hover:underline">
                {blogLink.label}
              </Link>
            </p>
          ) : null}
        </HomeContainer>
      </section>

      <section
        id="comparison-grid"
        className="border-t border-black/[0.08] bg-[#F7F7F2] py-10 md:py-14"
      >
        <HomeContainer className="space-y-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className={BARI_COMPARISON_TOKENS.typography.sectionEyebrow}>מנוע השוואה</p>
              <h2 className={BARI_COMPARISON_TOKENS.typography.sectionTitle}>
                כל המוצרים · סינון ופירוט
              </h2>
              <p className={BARI_COMPARISON_TOKENS.typography.sectionMeta}>
                {filteredProducts.length} מוצרים מוצגים מתוך {products.length} · ממוין לפי ציון
                Bari
              </p>
            </div>
            <span className="text-sm font-semibold text-[#7A817C]">השוואת מדף שקטה ומובנית</span>
          </div>

          <div className="flex flex-wrap gap-2">
            {lensOptions.map((option) => {
              const on = activeFilters.includes(option.id);
              return (
                <button
                  key={option.id}
                  type="button"
                  onClick={() => toggleFilter(option.id)}
                  className={cn(
                    "rounded-full border px-3.5 py-2 text-sm font-semibold transition-colors",
                    on
                      ? "border-[#1F8F6A]/35 bg-[#1F8F6A] text-[#F7F7F2]"
                      : "border-black/[0.08] bg-[#FFFFFF] text-[#4E5663] hover:border-[#1F8F6A]/20"
                  )}
                >
                  {option.label}
                </button>
              );
            })}
            {activeFilters.length > 0 ? (
              <button
                type="button"
                onClick={() => setActiveFilters([])}
                className="rounded-full px-3 py-2 text-sm font-semibold text-[#7A817C] underline-offset-2 hover:underline"
              >
                נקה סינון
              </button>
            ) : null}
          </div>

          <div className={BARI_COMPARISON_TOKENS.rows.zebraContainerClass}>
            {filteredProducts.length === 0 ? (
              <p className="p-8 text-center text-sm text-[#4E5663]">
                אין מוצרים התואמים לסינון — נסו להסיר פילטר.
              </p>
            ) : (
              filteredProducts.map((product, index) => (
                <BariProductShelfRow key={product.id} product={product} rank={index + 1} />
              ))
            )}
          </div>

          <section className="rounded-[1.1rem] border border-black/[0.06] bg-[#FFFFFF]/75 px-5 py-4 text-sm leading-relaxed text-[#4E5663] md:px-6">
            {methodologyLines.map((line, index) => (
              <p key={line} className={index === 0 ? undefined : "mt-2"}>
                {line}
              </p>
            ))}
          </section>
        </HomeContainer>
      </section>
    </main>
  );
}

/** Build rotating insight lines from product shelf copy. */
export function productInsightLines(products: BariProductVM[]): string[] {
  return products.map((product) => product.insightLine).filter(Boolean);
}

export type { ComparisonHeroStat };
