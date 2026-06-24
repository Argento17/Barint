import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/cookies_coffee_frontend_v2.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import type { BariProductVM } from "@/lib/view-models";

export type CookiesCoffeeCorpusMeta = ComparisonCorpusMeta;

type CookiesCoffeeCorpusProduct = BariProductVM & { barcode?: string };

// page_copy is the authoritative source for all shell strings (RT-3 fix).
// The raw JSON ships a page_copy object; we extract it here so page-data.ts
// is never the source of truth for consumer-facing copy.
type CookiesCoffeeRaw = typeof rawCorpus & {
  page_copy: {
    hero: { tagline: string };
    prologue: { sentences: string[] };
    methodology: { lines: string[] };
    caveat: { title: string; body: string };
  };
};

const _typedRaw = rawCorpus as CookiesCoffeeRaw;
const _pageCopy = _typedRaw.page_copy;

const _cookiesCoffeeRawProducts = (rawCorpus as ComparisonCorpusRaw).products as CookiesCoffeeCorpusProduct[];

const { meta: cookiesCoffeeCorpusMeta, products: _cookiesCoffeeProductsRaw } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

// Top-scored product — representative hero image for index card.
export const cookiesCoffeeHeroImageUrl =
  _cookiesCoffeeRawProducts.find((p) => p.barcode === "7290013453693")?.imageUrl ?? null;

// Sugar is the headline differentiator — the page thesis is sugar+sat-fat, not sodium.
// sodium is NOT mapped here (the page copy explicitly says "נתרן אינו הנושא").
const cookiesCoffeeProducts: BariProductVM[] = _cookiesCoffeeProductsRaw.map(
  (p) => ({
    ...p,
    imageUrl: p.imageUrl ?? null,
    d4_additives: p.d4_additives ?? [],
    metrics: {
      // sugar + sat-fat are the two headline row metrics (page thesis: sugar+sat-fat, NOT sodium).
      // protein_g is required by BariProductMetricsVM; set null as it is not a cookie differentiator.
      protein_g: null,
      sugar_g: p.expansion?.nutrition?.sugar ?? null,
      // satFat is camelCase in the JSON (expansion.nutrition.satFat); map to fat_saturated_g (TASK-393).
      fat_saturated_g: p.expansion?.nutrition?.satFat ?? null,
    },
  })
);

export { cookiesCoffeeCorpusMeta, cookiesCoffeeProducts };

export const cookiesCoffeeMetadataLine = formatComparisonMetadataLine(
  cookiesCoffeeProducts.length,
  cookiesCoffeeCorpusMeta.generated
);

// ── Shell strings — read from JSON page_copy (RT-3 fix) ─────────────────────
// Single source of truth is cookies_coffee_frontend_v2.json:page_copy.
// The hardcoded Hebrew strings that caused RT-3 ("מעל 17 גרם", "61 מוצרים",
// "תשעה", "לכל אחד מהם...שחצות") have been removed from this file.

export const cookiesCoffeeHero = {
  eyebrow: "עוגיות לקפה",
  title: _pageCopy.hero.tagline,
} as const;

export const cookiesCoffeePrologueSentences: readonly string[] =
  _pageCopy.prologue.sentences;

export const cookiesCoffeeMethodologyLines: readonly string[] =
  _pageCopy.methodology.lines;

// categoryCaveat: rendered as a single string with title + body
// (matches the yellow-box pattern in the comparison page component).
export const cookiesCoffeeCategoryNote =
  `${_pageCopy.caveat.title}\n\n${_pageCopy.caveat.body}`;

export const cookiesCoffeeComparisonMetadata: Metadata = {
  title: "השוואת עוגיות לקפה | Bari",
  description:
    `השוואת ${cookiesCoffeeProducts.length} ביסקוויטים מהמדף הישראלי — ציון Bari, שומן רווי, סוכר ורשימת רכיבים. מידע, לא המלצה.`,
};

const cookiesCoffeeShelfFilters = {
  lensOptions: [],
  filterProducts: (products: BariProductVM[], _activeFilters: string[]) => products,
};

export function getCookiesCoffeePageData(): ComparisonCategoryPageData {
  return {
    products: cookiesCoffeeProducts,
    metadataLine: cookiesCoffeeMetadataLine,
    hero: cookiesCoffeeHero,
    prologueSentences: cookiesCoffeePrologueSentences,
    methodologyLines: cookiesCoffeeMethodologyLines,
    corpusMeta: cookiesCoffeeCorpusMeta,
    shelfFilters: cookiesCoffeeShelfFilters,
  };
}

export function getCookiesCoffeeCorpusPayload(): {
  _meta: CookiesCoffeeCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: cookiesCoffeeCorpusMeta,
    products: cookiesCoffeeProducts,
  };
}
