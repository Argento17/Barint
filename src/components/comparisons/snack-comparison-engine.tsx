"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { Search } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { ComparisonMoment } from "@/components/snack/comparison-moment";
import {
  defaultSnackEngineFilters,
  FilterPanel,
  snackMatchesEngineFilters,
} from "@/components/snack/filter-panel";
import { MapSection } from "@/components/snack/map-section";
import { ProductCardGrid } from "@/components/snack/product-card-grid";
import { SnackProductDetailPanel } from "@/components/snack/snack-product-detail-panel";
import { SnackShelfStatBar } from "@/components/snack/snack-shelf-stat-bar";
import { SNACK_FLAGSHIP_HREF } from "@/lib/blog/snack-analysis-content";
import { snackBlogMap, snackEnginePresets } from "@/lib/blog/snack-editorial-content";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import {
  SNACK_REPORT_STATS,
  snackDisplayableProducts,
} from "@/lib/comparisons/snack-page-data";
import type { SnackEngineFilters, SnackProduct } from "@/lib/comparisons/snack-types";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

function normalize(value: string) {
  return value.trim().toLowerCase();
}

export function SnackComparisonEngine() {
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState<SnackEngineFilters>(defaultSnackEngineFilters);
  const [detailProduct, setDetailProduct] = useState<SnackProduct | null>(null);
  const [presetMoment, setPresetMoment] = useState<(typeof snackEnginePresets)[number] | null>(
    null
  );

  const filtered = useMemo(() => {
    const needle = normalize(query);
    return [...snackDisplayableProducts]
      .filter((product) => snackMatchesEngineFilters(product, filters))
      .filter((product) => {
        if (!needle) return true;
        const haystack = normalize(`${product.name_he} ${product.brand} ${product.segment}`);
        return haystack.includes(needle);
      })
      .sort((a, b) => (b.score ?? -1) - (a.score ?? -1));
  }, [filters, query]);

  return (
    <main className={cn("min-h-screen bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)}>
      <HomeContainer className="py-8 md:py-10">
        <p className="text-sm text-[#4E5663]">
          כל החטיפים — {SNACK_REPORT_STATS.scraped} מוצרים, {SNACK_REPORT_STATS.retailer},{" "}
          {SNACK_REPORT_STATS.snapshotDate}
        </p>

        <div className="relative mt-4">
          <Search className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-[#7A817C]" />
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="חיפוש לפי שם, מותג או קטגוריה..."
            className="w-full rounded-full border border-black/[0.1] bg-[#FFFFFF] py-3 pr-10 pl-4 text-sm"
          />
        </div>

        <div className="mt-6">
          <ProductCardGrid
            products={filtered}
            onOpenProduct={setDetailProduct}
          />
        </div>

        <div className="mt-6 flex flex-wrap items-center gap-4">
          <FilterPanel
            filters={filters}
            onApply={setFilters}
            onClear={() => setFilters(defaultSnackEngineFilters)}
          />
        </div>

        <section className="mt-10 border-t border-black/[0.06] pt-10">
          <p className={BARI_COMPARISON_TOKENS.typography.sectionEyebrow}>השוואות מוכנות</p>
          <ul className="mt-3 space-y-2">
            {snackEnginePresets.map((preset) => (
              <li key={preset.label}>
                <button
                  type="button"
                  onClick={() => setPresetMoment(preset)}
                  className="text-sm font-semibold text-[#1F8F6A] hover:underline"
                >
                  {preset.label} →
                </button>
              </li>
            ))}
          </ul>
          {presetMoment ? (
            <div className="mt-8">
              <ComparisonMoment {...presetMoment.moment} />
            </div>
          ) : null}
        </section>

        <MapSection
          title="עומק עיבוד וסוכר — 53 חטיפים"
          caption={snackBlogMap.caption}
          products={snackDisplayableProducts}
          annotatedIds={[...snackBlogMap.annotatedIds]}
          annotations={snackBlogMap.annotations}
          defaultCollapsed
          collapseLabel="מפת המדף ▼"
        />

        <div className="mt-10 border-t border-black/[0.06] pt-8">
          <SnackShelfStatBar />
        </div>

        <p className="mt-8 text-sm text-[#4E5663]">
          <Link href={SNACK_FLAGSHIP_HREF} className="font-semibold text-[#1F8F6A] hover:underline">
            חזרה לחקירת החטיפים
          </Link>
        </p>
      </HomeContainer>

      {detailProduct ? (
        <SnackProductDetailPanel product={detailProduct} onClose={() => setDetailProduct(null)} />
      ) : null}
    </main>
  );
}
