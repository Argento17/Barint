import type { Metadata } from "next";
import rawCorpus from "@/data/comparisons/cheese_frontend_v5.json";
import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import type { BariProductVM } from "@/lib/view-models";

export type CheeseCorpusMeta = ComparisonCorpusMeta;

type CheeseRaw = typeof rawCorpus & {
  page_copy: {
    hero: { eyebrow: string; title: string };
    prologue: string[];
    methodology: { body: string; lines: string[] };
    category_caveat: string;
  };
};

const _typedRaw = rawCorpus as CheeseRaw;
const _pageCopy = _typedRaw.page_copy;

const { meta: cheeseCorpusMeta, products: _cheeseProductsRaw } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

const cheeseProducts: BariProductVM[] = _cheeseProductsRaw.map((p) => ({
  ...p,
  imageUrl: p.imageUrl ?? null,
  d4_additives: p.d4_additives ?? [],
  metrics: {
    protein_g: p.expansion?.nutrition?.protein ?? null,
  },
}));

export { cheeseCorpusMeta, cheeseProducts };

export const cheeseMetadataLine = formatComparisonMetadataLine(
  cheeseProducts.length,
  cheeseCorpusMeta.generated
);

export const cheeseHero = {
  eyebrow: _pageCopy.hero.eyebrow,
  title: _pageCopy.hero.title,
} as const;

// v4 JSON ships prologue as string[] (4 paragraphs) — use directly
export const cheesePrologueSentences: readonly string[] = _pageCopy.prologue;
export const cheeseMethodologyLines: readonly string[] = _pageCopy.methodology.lines;
// v4 JSON ships category_caveat as a flat string
export const cheeseCategoryNote: string = _pageCopy.category_caveat;

export const cheeseComparisonMetadata: Metadata = {
  title: "השוואת גבינות לבנות וממרחים | Bari",
  description:
    "השוואה בין גבינות לבנות, קוטג', ממרחי גבינת שמנת ולבנה — לפי רכיבים, חלבון, שומן ורמת עיבוד. מידע, לא המלצה.",
};

const cheeseShelfFilters = {
  lensOptions: [] as Array<{ id: string; label: string }>,
  filterProducts: (products: BariProductVM[], _activeFilters: string[]) => products,
};

export function getCheesePageData(): ComparisonCategoryPageData {
  return {
    products: cheeseProducts,
    metadataLine: cheeseMetadataLine,
    hero: cheeseHero,
    prologueSentences: cheesePrologueSentences,
    methodologyLines: cheeseMethodologyLines,
    corpusMeta: cheeseCorpusMeta,
    shelfFilters: cheeseShelfFilters,
  };
}

export function getCheeseCorpusPayload(): {
  _meta: CheeseCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: cheeseCorpusMeta,
    products: cheeseProducts,
  };
}
