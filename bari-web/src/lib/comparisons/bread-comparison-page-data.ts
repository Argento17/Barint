import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/bread_frontend_v2.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterBreadProducts,
  BREAD_SHELF_LENS_OPTIONS,
  type BreadShelfFilterId,
} from "@/lib/comparisons/bread-shelf-filters";
import { breadComparisonMeta } from "@/lib/blog/bread-analysis-content";
import type { BariProductVM } from "@/lib/view-models";

export type BreadCorpusMeta = ComparisonCorpusMeta;

type BreadCorpusProduct = BariProductVM & {
  _website_cluster?: string;
};

function stripBreadInternalFields(products: BreadCorpusProduct[]): BariProductVM[] {
  return products.map((product) => {
    const { _website_cluster, ...rest } = product;
    void _website_cluster;
    return rest;
  });
}

const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const breadCorpusMeta = loaded.meta;
const breadProducts = stripBreadInternalFields(
  loaded.products as BreadCorpusProduct[]
);

export { breadCorpusMeta, breadProducts };

export const breadMetadataLine = `${breadCorpusMeta.product_count} מוצרים נבדקו · מדגם שופרסל · ממוין לפי ציון Bari`;

/** Shelf copy — bread MVP handoff v1 (2026-05-30). */
export const breadHero = {
  eyebrow: "מנוע השוואה · לחמים",
  title: "לחם: מה שכתוב על האריזה לא תמיד מה שבפנים",
} as const;

export const breadPrologueSentences = [
  "לחם נראה כמו קטגוריה פשוטה: קמח, מים, מחמצת. אבל המדף מספר סיפור יותר מורכב.",
  "חלק מהמוצרים שמציגים 'מחמצת' בשם משתמשים בשמרים תעשייתיים ברכיבים. חלק אחר מסתמכים על כותרת 'מלא' כדי להציג רכיבים מעורבים.",
  "ההשוואה מתבססת על מה שאפשר לבדוק: ערכי חלבון, סיבים, נתרן, ותסיסה מאומתת ברשימת הרכיבים — לא על המיתוג.",
] as const;

export const breadMethodologyLines = [
  "ניתוח לחמים מבוסס על נתונים מגלויות שופרסל — מדגם מדף, לא סקר שוק מלא.",
  "לכל מוצר נבחנו הרכב הרכיבים, ערכי חלבון וסיבים, רמת עיבוד ותסיסה מאומתת ברכיבים.",
  "ציון הלחם אינו מבוסס על קלוריות בלבד — הוא משקלל מבנה, מקור הדגן, ורמת ההנדסה במוצר.",
  "ההשוואה נועדה לעזור בהשוואה בין מוצרים, ולא מהווה המלצה תזונתית אישית.",
  "מדגם מדף שופרסל בלבד.",
] as const;

export const breadComparisonMetadata: Metadata = {
  title: breadComparisonMeta.title,
  description: breadComparisonMeta.description,
};

function isBreadShelfFilterId(filter: string): filter is BreadShelfFilterId {
  return BREAD_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const breadShelfFilters = {
  lensOptions: BREAD_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterBreadProducts(products, activeFilters.filter(isBreadShelfFilterId)),
};

export function getBreadPageData(): ComparisonCategoryPageData {
  return {
    products: breadProducts,
    metadataLine: breadMetadataLine,
    hero: breadHero,
    prologueSentences: breadPrologueSentences,
    methodologyLines: breadMethodologyLines,
    corpusMeta: breadCorpusMeta,
    shelfFilters: breadShelfFilters,
  };
}

export function getBreadCorpusPayload(): {
  _meta: BreadCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: breadCorpusMeta,
    products: breadProducts,
  };
}
