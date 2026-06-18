import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/yogurts_frontend_v1.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import type { BariProductVM } from "@/lib/view-models";

export type YogurtsCorpusMeta = ComparisonCorpusMeta;

// page_copy is the authoritative source for all shell strings.
// The v1 JSON ships prologue as a single paragraph string (not an array).
type YogurtsRaw = typeof rawCorpus & {
  page_copy: {
    hero: { eyebrow: string; title: string };
    prologue: string;
    methodology: { body: string; lines: string[] };
    category_caveat: { title: string; body: string };
  };
};

const _typedRaw = rawCorpus as YogurtsRaw;
const _pageCopy = _typedRaw.page_copy;

const { meta: yogurtsCorpusMeta, products: _yogurtsProductsRaw } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

const yogurtsProducts: BariProductVM[] = _yogurtsProductsRaw.map((p) => ({
  ...p,
  imageUrl: p.imageUrl ?? null,
  d4_additives: p.d4_additives ?? [],
  metrics: {
    protein_g: p.expansion?.nutrition?.protein ?? null,
    sugar_g: p.expansion?.nutrition?.sugar ?? null,
  },
}));

export { yogurtsCorpusMeta, yogurtsProducts };

export const yogurtsMetadataLine = formatComparisonMetadataLine(
  yogurtsProducts.length,
  yogurtsCorpusMeta.generated
);

export const yogurtsHero = {
  eyebrow: _pageCopy.hero.eyebrow,
  title: _pageCopy.hero.title,
} as const;

// The v1 JSON ships prologue as a single paragraph. Wrapped in array to satisfy
// prologueSentences: readonly string[] (CategoryPrologue renders each element separately).
export const yogurtsPrologueSentences: readonly string[] = [_pageCopy.prologue];

export const yogurtsMethodologyLines: readonly string[] = _pageCopy.methodology.lines;

export const yogurtsCategoryNote =
  `${_pageCopy.category_caveat.title}\n\n${_pageCopy.category_caveat.body}`;

export const yogurtsComparisonMetadata: Metadata = {
  title: "השוואת יוגורטים | Bari",
  description: `השוואת ${yogurtsProducts.length} יוגורטים מהמדף הישראלי — ציון Bari, חלבון, סוכר ורמת עיבוד. מידע, לא המלצה.`,
};

const yogurtsShelfFilters = {
  lensOptions: [] as Array<{ id: string; label: string }>,
  filterProducts: (products: BariProductVM[], _activeFilters: string[]) => products,
};

export function getYogurtsPageData(): ComparisonCategoryPageData {
  return {
    products: yogurtsProducts,
    metadataLine: yogurtsMetadataLine,
    hero: yogurtsHero,
    prologueSentences: yogurtsPrologueSentences,
    methodologyLines: yogurtsMethodologyLines,
    corpusMeta: yogurtsCorpusMeta,
    shelfFilters: yogurtsShelfFilters,
  };
}

export function getYogurtsCorpusPayload(): {
  _meta: YogurtsCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: yogurtsCorpusMeta,
    products: yogurtsProducts,
  };
}
