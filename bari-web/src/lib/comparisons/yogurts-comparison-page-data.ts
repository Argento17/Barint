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

// Re-authored for run_yogurt_006_recal_p0_trim (TASK-169D). Recal lifts the shelf: 6 reach A,
// top 89/A. Numbers cite the rounded chip values (ScoreChip renders Math.round): top 89/A;
// simple ביו/נטול-לקטוז cluster 80–81/A; עיזים 77/B; greek 78–79/B; flavored down to 40/D.
export const yogurtsPrologueSentences = [
  "בדקנו מחדש את מדף היוגורט על נתוני אריזה אמיתיים — רכיבים, חלבון, סוכר ושומן כפי שהם מופיעים על המוצר עצמו. התמונה התהפכה מהבדיקה הקודמת: שישה יוגורטים על המדף מגיעים ל-A. הציון הגבוה הוא 89/A — יופלה GO מועשר בחלבון, על בסיס חלבון גבוה ותרביות חיות.",
  "היוגורטים הפשוטים של תנובה — ביו 3% וביו 1.5% — וגם נטול הלקטוז מגיעים ל-80 עד 81, כולם A: בסיס חלבי, חיידקי ביפידוס, מעט מרכיבים. יוגורט עיזים נשאר ב-77/B, בעיקר כי החלבון בו נמוך יותר.",
  "מכאן זה יורד. ככל שמתווספים סוכר, חומרי טעם, מייצבים או פצפוצים — הציון נופל. גרסאות הטעם וה'קראנצ'' מגיעות עד C ו-D, גם כשכמות החלבון על האריזה זהה. ושומן גבוה לא מעלה ציון: יווני 8% עם 4.8 גרם שומן רווי עוצר ב-79/B, מתחת לבסיסים הרזים.",
  "במדף הזה 'הכי טוב' הוא A — אבל לא S. גם היוגורט המוביל נעצר ב-A: ציון החלבון והתרביות מרים אותו גבוה, אך לא הופך אותו ליוצא דופן. הכי טוב, לא מושלם.",
] as const;

// Category caveat (cheese gold-standard format), rendered once in the header. Grounded in
// the run_yogurt_006_recal_p0_trim outcome (6 reach A, top 89/A, S withheld) and the live data:
// the same "0%"/"protein" label sits at both ends — A-tier when the base is clean, but C–D
// once a flavored version stacks on sugar + stabilizers at the same protein. The cap (top = A,
// no S) is the new ceiling story: protein density alone does not earn the apex grade.
export const yogurtsCategoryNote = [
  "הערת קטגוריה — אותה תווית, שני קצוות\n\nהציון משקלל את ההרכב כולו — חלבון, סוכר, מייצבים ורמת עיבוד — ולא תווית אחת. אותו 'עשיר בחלבון' יכול לשבת בראש המדף כשהבסיס פשוט, וליפול ל-C או D בגרסת טעמים שמוסיפה סוכר, חומרי טעם ופצפוצים על אותו חלבון בדיוק. מספר החלבון על החזית אינו מספיק כדי לקבוע את הציון.",
  "הערת קטגוריה — 'הכי טוב' כאן הוא A, לא S\n\nשישה יוגורטים על המדף מגיעים ל-A, והגבוה הוא 89/A. אבל אף אחד לא מגיע ל-S, גם המוביל: חלבון גבוה ותרביות חיות מרימים את הציון, ואינם הופכים יוגורט ליוצא דופן. A כאן אומר יוגורט טוב באמת — לא מושלם, ולא מעבר לכך.",
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
