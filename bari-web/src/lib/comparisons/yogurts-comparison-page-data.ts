import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/yogurts_frontend_v2.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import { enrichRowSurface } from "@/lib/comparisons/row-surface";
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
const yogurtsProducts = enrichRowSurface(
  stripYogurtsInternalFields(loaded.products as YogurtsCorpusProduct[])
);

export { yogurtsCorpusMeta, yogurtsProducts };

export const yogurtsMetadataLine = `${yogurtsCorpusMeta.product_count} מוצרים נבדקו · מדגם מדף ישראלי · ממוין לפי ציון Bari`;

export const yogurtsHero = {
  eyebrow: "מנוע השוואה · יוגורטים",
  title: 'יוגורט: לא כל "טבעי" נוצר שווה',
} as const;

// Re-authored for run_yogurt_004 (TASK-143 3b). B-capped shelf, zero A. Numbers cite the
// rounded chip values (ScoreChip renders Math.round): top 79/B; simple cluster 72–76.
export const yogurtsPrologueSentences = [
  "בדקנו מחדש את מדף היוגורט על נתוני אריזה אמיתיים — רכיבים, חלבון, סוכר ושומן כפי שהם מופיעים על המוצר עצמו. התמונה ברורה: אף יוגורט בקטגוריה לא מגיע ל-A. הציון הגבוה הוא 79/B — יוגורט חלבון 0% עם חמישה מרכיבים.",
  "היוגורטים הפשוטים — ביו, נטול לקטוז, חלב עיזים — נעים סביב 72 עד 76, כולם B: בסיס חלבי, תרביות, מעט מרכיבים.",
  "מכאן זה רק יורד. ככל שמתווספים סוכר, חומרי טעם, מייצבים או פצפוצים — הציון נופל. גרסאות הטעם וה'קראנצ'' מגיעות עד C, D ו-E, גם כשכמות החלבון על האריזה זהה. ושומן גבוה לא מעלה ציון: יווני 8% עם 4.8 גרם שומן רווי יורד ל-62/C.",
  "במדף הזה 'הכי טוב' הוא B — ולא יותר.",
] as const;

// Category caveat (cheese gold-standard format), rendered once in the header. Grounded in
// the run_yogurt_004 outcome (B-capped shelf, zero A) and the live data: flavored / "crunch"
// versions fall to C–E on added sugar + stabilizers even at identical protein, while a "0%"
// or "protein" label is not automatically the top score. "diet"/flavor framing is the nuance.
export const yogurtsCategoryNote = [
  "הערת קטגוריה — '0%' או 'עשיר בחלבון' לא תמיד הציון הגבוה\n\nהציון משקלל את ההרכב כולו — חלבון, סוכר, מייצבים ורמת עיבוד — ולא תווית אחת. יוגורט בטעמים עם אותו חלבון בדיוק יכול ליפול ל-C או D ברגע שמתווספים סוכר, חומרי טעם ופצפוצים. מספר החלבון על החזית אינו מספיק כדי לקבוע את הציון.",
  "הערת קטגוריה — 'הכי טוב' כאן הוא B\n\nבמדף הזה אף יוגורט אינו מגיע ל-A. הציון הגבוה הוא 79/B. יוגורט טבעי ופשוט מדורג גבוה מגרסת טעמים — לא בגלל השם, אלא בגלל מה שכתוב ברשימת הרכיבים.",
  "הערת קטגוריה — סיבים תזונתיים\n\nמוצרי חלב כמעט אינם מציינים סיבים תזונתיים על התווית, ולכן ערך זה אינו נכנס לניתוח בקטגוריה זו.",
]
  .join("\n\n");

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
