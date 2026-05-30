import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/snacks_frontend_v2.json";

import {
  snacksShelfMethodologyLines,
  snackComparisonMeta,
} from "@/lib/blog/snack-analysis-content";
import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterSnacksProducts,
  SNACKS_SHELF_LENS_OPTIONS,
  type SnacksShelfFilterId,
} from "@/lib/comparisons/snacks-shelf-filters";
import { snackHeroLine } from "@/lib/comparisons/snack-page-data";
import type { BariProductVM } from "@/lib/view-models";

export type SnacksCorpusMeta = ComparisonCorpusMeta;

type SnacksCorpusProduct = BariProductVM & {
  _internal_cluster?: string;
};

function stripSnacksInternalFields(products: SnacksCorpusProduct[]): BariProductVM[] {
  return products.map((product) => {
    const { _internal_cluster, ...rest } = product;
    void _internal_cluster;
    return rest;
  });
}

const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const snacksCorpusMeta = loaded.meta;
const snacksProducts = stripSnacksInternalFields(
  loaded.products as SnacksCorpusProduct[]
);

export { snacksCorpusMeta, snacksProducts };

const snacksMetadataUpdated = (() => {
  const date = new Date(snacksCorpusMeta.generated);
  return Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleDateString("he-IL", { month: "long", year: "numeric" });
})();

/** CE framing: 18 displayed · 53 scanned · 48 scored (hero metadata line). */
export const snacksMetadataLine = snacksMetadataUpdated
  ? `18 מוצרים בדף · 53 נסרקו · 48 קיבלו ציון · עודכן ב${snacksMetadataUpdated}`
  : "18 מוצרים בדף · 53 נסרקו · 48 קיבלו ציון";

/** Shelf copy from CE-stabilized snack comparison hero line. */
export const snacksHero = {
  eyebrow: "חטיפים",
  title: "השוואת חטיפים",
} as const;

/** Verbatim sentences from snack-editorial-content.ts (snackShelfIntro closing lines) + snackHeroLine. */
export const snacksPrologueSentences = [
  snackHeroLine,
  "מתוך 53 מוצרים שנסרקו, 48 קיבלו ציון, ו-18 נבחרו לתצוגה על בסיס מגוון קטגוריות ופערי ציון משמעותיים.",
  "הציון הגבוה ביותר — 70/B — לא הלך לאף אחד מהשמות שהזכרנו.",
] as const;

export const snacksMethodologyLines = snacksShelfMethodologyLines;

export const snacksComparisonMetadata: Metadata = {
  title: snackComparisonMeta.title,
  description: snackComparisonMeta.description,
};

function isSnacksShelfFilterId(filter: string): filter is SnacksShelfFilterId {
  return SNACKS_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const snacksShelfFilters = {
  lensOptions: SNACKS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterSnacksProducts(products, activeFilters.filter(isSnacksShelfFilterId)),
};

export function getSnacksPageData(): ComparisonCategoryPageData {
  return {
    products: snacksProducts,
    metadataLine: snacksMetadataLine,
    hero: snacksHero,
    prologueSentences: snacksPrologueSentences,
    methodologyLines: snacksMethodologyLines,
    corpusMeta: snacksCorpusMeta,
    shelfFilters: snacksShelfFilters,
  };
}

export function getSnacksCorpusPayload(): {
  _meta: SnacksCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: snacksCorpusMeta,
    products: snacksProducts,
  };
}
