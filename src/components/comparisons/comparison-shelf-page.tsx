"use client";

import { useMemo, useState } from "react";

import { CategoryHero } from "@/components/shared/category-hero";
import { CategoryPrologue } from "@/components/shared/category-prologue";
import { CategoryShelfLenses } from "@/components/shared/category-shelf-lenses";
import { MethodologyFooter } from "@/components/shared/methodology-footer";
import { ProductTable } from "@/components/shared/product-table";
import {
  ComparisonLayoutProvider,
  type ComparisonLayoutMode,
} from "@/lib/comparisons/comparison-layout-context";
import type { ComparisonShelfFilters } from "@/lib/comparisons/registry/types";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";
import type { BariProductVM } from "@/lib/view-models";

const WEB = BARI_COMPARISON_TOKENS.webTable;

export interface ComparisonShelfPageProps<TFilterId extends string = string> {
  products: BariProductVM[];
  metadataLine: string;
  hero: {
    eyebrow: string;
    title: string;
  };
  prologueSentences: readonly string[];
  methodologyLines: readonly string[];
  shelfFilters: ComparisonShelfFilters<TFilterId>;
  initialExpandedProductId?: string | null;
  /** `shelf` = phone-frame (default). `web` = Comparison Web Template v1 on lg+; mobile unchanged. */
  layout?: ComparisonLayoutMode;
}

export function ComparisonShelfPage<TFilterId extends string = string>({
  products,
  metadataLine,
  hero,
  prologueSentences,
  methodologyLines,
  shelfFilters,
  initialExpandedProductId = null,
  layout = "shelf",
}: ComparisonShelfPageProps<TFilterId>) {
  const [activeFilters, setActiveFilters] = useState<TFilterId[]>([]);

  const filteredProducts = useMemo(
    () => shelfFilters.filterProducts(products, activeFilters),
    [activeFilters, products, shelfFilters]
  );

  const expandedProductId = useMemo(
    () =>
      initialExpandedProductId &&
      filteredProducts.some((product) => product.id === initialExpandedProductId)
        ? initialExpandedProductId
        : (filteredProducts[0]?.id ?? null),
    [filteredProducts, initialExpandedProductId]
  );

  const isWeb = layout === "web";

  return (
    <ComparisonLayoutProvider mode={layout}>
      <div
        className={cn(
          "min-h-screen bg-[#EFEFEB]",
          isWeb
            ? cn(
                "max-lg:flex max-lg:justify-center max-lg:sm:py-10 lg:py-6",
                WEB.shellViewportPaddingClass
              )
            : "flex justify-center sm:py-10"
        )}
        dir="rtl"
      >
        <div
          className={cn(
            "w-full overflow-hidden bg-white",
            isWeb
              ? cn(
                  "max-lg:sm:max-w-[375px] max-lg:sm:rounded-[2rem] max-lg:sm:shadow-2xl",
                  WEB.shellMaxWidthClass,
                  WEB.shellSurfaceClass
                )
              : "sm:max-w-[375px] sm:rounded-[2rem] sm:shadow-2xl"
          )}
        >
          <CategoryHero
            eyebrow={hero.eyebrow}
            title={hero.title}
            metadata={metadataLine}
            wide={isWeb}
          />
          <CategoryPrologue sentences={[...prologueSentences]} wide={isWeb} />
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
            wide={isWeb}
          />
          <ProductTable
            key={expandedProductId ?? "none"}
            products={filteredProducts}
            initialExpandedProductId={expandedProductId}
          />
          <MethodologyFooter lines={[...methodologyLines]} wide={isWeb} />
        </div>
      </div>
    </ComparisonLayoutProvider>
  );
}
