import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/yogurts_frontend_v1.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterYogurtsProducts,
  YOGURTS_SHELF_LENS_OPTIONS,
  type YogurtsShelfFilterId,
} from "@/lib/comparisons/yogurts-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type YogurtsCorpusMeta = ComparisonCorpusMeta;

type YogurtsCorpusProduct = BariProductVM & {
  _cluster?: string;
};

function stripYogurtsInternalFields(
  products: YogurtsCorpusProduct[]
): BariProductVM[] {
  return products.map((product) => {
    const { _cluster, ...rest } = product;
    void _cluster;
    return rest;
  });
}

const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const yogurtsCorpusMeta = loaded.meta;
const yogurtsProducts = stripYogurtsInternalFields(
  loaded.products as YogurtsCorpusProduct[]
);

export { yogurtsCorpusMeta, yogurtsProducts };

export const yogurtsMetadataLine = `${yogurtsCorpusMeta.product_count} מוצרים נבדקו · מדגם מדף ישראלי · ממוין לפי ציון Bari`;

export const yogurtsHero = {
  eyebrow: "מנוע השוואה · יוגורטים",
  title: 'יוגורט: לא כל "טבעי" נוצר שווה',
} as const;

export const yogurtsPrologueSentences = [
  "יוגורט נראה כמו מזון פשוט — חלב ותרבית. אבל המדף מציג ספקטרום רחב: ממוצרים עם 2 מרכיבים בלבד ועד מוצרים עם 8+ רכיבים, סוכר וממתיקים.",
  "ציון Bari ליוגורטים מבדיל בין יוגורט טבעי לא מתוק, יוגורט מועשר בתרביות, ועד יוגורט בטעמים ויוגורט שתיה — לפי מה שכתוב ברשימת הרכיבים.",
  "הנתון הבודד שהכי מדבר: רשימת הרכיבים. כמה מרכיבים, מה בהם — ומה לא.",
] as const;

export const yogurtsMethodologyLines = [
  "ניתוח יוגורטים מבוסס על לייבלים של מוצרים נבחרים מהמדף הישראלי.",
  "לכל מוצר נבחנו הרכב הרכיבים, רמת חלבון, תוספי מייצבים, סוכר מוסף ורמת עיבוד.",
  "ציון יוגורט טבעי מבוסס גבוה יותר ממוצר בטעמים — לא בגלל שמות, אלא בגלל מה שכתוב ברשימת הרכיבים.",
  "מעדני חלב — מוצרים עם שכבות שוקולד, קצפת, או מבנה קינוח — אינם נכללים בהשוואה; הם מוצרי הנאה נפרדים. יוגורט שתיה נכלל ומקבל ציון כמוצר יוגורט מעובד.",
  "הדירוג נועד לעזור בהשוואה בין מוצרים ואינו מהווה המלצה תזונתית אישית.",
] as const;

export const yogurtsComparisonMetadata: Metadata = {
  title: "השוואת יוגורטים | Bari",
  description:
    "השוואה בין יוגורטים טבעיים, יווניים, ללא חלב ומוצרים בטעמים — לפי רכיבים, חלבון ורמת עיבוד.",
};

function isYogurtsShelfFilterId(filter: string): filter is YogurtsShelfFilterId {
  return YOGURTS_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const yogurtsShelfFilters = {
  lensOptions: YOGURTS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterYogurtsProducts(products, activeFilters.filter(isYogurtsShelfFilterId)),
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
