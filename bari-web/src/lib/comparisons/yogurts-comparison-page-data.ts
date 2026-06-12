import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/yogurts_frontend_v4.json";

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
  eyebrow: "יוגורטים — שופרסל",
  title: "שני מוצרים הגיעו ל-S. שאר המדף נפרס בין B ל-D.",
} as const;

export const yogurtsPrologueSentences = [
  "בקטגוריית היוגורטים בשופרסל ניתחנו 17 מוצרים. שניים מהם, שתי גרסאות של דנונה פרו, קיבלו ציון S — הציון הגבוה ביותר בסולם, שמשמעותו שכל מרכיבי הניתוח יצאו נקיים ולא הופעל אף קנס.",
  "אחריהם, בטווח A, נמצאים שני מוצרי חלבון גבוה נוספים: יופלה GO מועשר בחלבון ומולר אקטיב לבן. שניהם נתקעו ממש מתחת ל-S בגלל היבט אחד שנשאר מאחור.",
  "מרבית היוגורטים הלבנים הרגילים (ביו תנובה, ללא לקטוז, יווני) נחתו ב-B. ההפרש ביניהם לבין ה-S נובע כמעט כולו מפוטנציאל החלבון: אצל הפשוטים הוא עומד על 5–6 גרם ל-100 גרם, לעומת 10–10.5 גרם אצל ה-S.",
  "ממנגו ווניל ועד קורנפלקס — ברגע שנוספים תוספות, ממתיקים, ציפויים או רשימת רכיבים ארוכה, הציון יורד ל-C ול-D. אין כאן הפתעות: ההפרש בין הפשוט לממותג הוא המדף שאתם רואים.",
] as const;

export const yogurtsCategoryNote =
  "הערת קטגוריה — יוגורטים\n\nהמספר הכי גדול על הגביע אינו בהכרח הסיגנל שמניע את הציון. יוגורט שמכריז על 20 גרם חלבון בגביע יכול לעמוד על שני קצות הסולם: הכל תלוי אם החלבון הגיע עם תוספות וממתיקים או בלי. דנונה פרו 21 ודנונה פרו וניל הם אותה משפחה של מותג, ובין השניים יש הפרש של 20 ציונים.\n\nשני מוצרי הדנונה פרו (20 ו-21 גרם חלבון) קיבלו ציון S — הציון הגבוה ביותר בסולם. שניהם מכילים שני מרכיבים בלבד ועברו את כל שערי הניתוח ללא קנסות. ציון S בקטגוריית יוגורטים נדיר: מתוך 87 מוצרים שנותחו, רק שניים הגיעו אליו. זהו ממצא מבנה — לא תקרה שהוטלה — ומשקף ניקוד אמיתי.\n\nסיבים תזונתיים אינם חלק מניתוח הקטגוריה הזו. מוצרי חלב רבים אינם מדווחים על סיבים בתווית, ולכן הוא הוצא מהחישוב במלואו כדי להבטיח השוואה שוויונית בין כל המוצרים בקטגוריה.";

export const yogurtsMethodologyLines = [
  "הציון שברי נותנת מבוסס על ניתוח של עשרה היבטים: דרגת העיבוד של המוצר, צפיפות רכיבי התזונה, צפיפות קלורית, איכות הפחמימות, כמות ואיכות החלבון, תוספות ומצרכים מלאכותיים, כוח השובע, טיב השומן, עמידה ברגולציה ושלמות המזון.",
  "ביוגורטים, הגורם שמשמש הכי הרבה כמגביל הוא כמות החלבון ומקורו. יוגורט עם 10 גרם חלבון ל-100 גרם יקבל ציון חלבון גבוה בהרבה מיוגורט עם 3.6 גרם — ולכן הפוטנציאל של כל גביע קבוע בנוסחה שלו.",
  "בכל מוצר מעובד (יוגורט עם פירות, ציפוי, קורנפלקס, ממתיק) הניתוח מפעיל מגבלת ניקוד על בסיס עוצמת העיבוד ומספר התוספות. מגבלה זו מציבה תקרה שהציון לא יכול לחצות, בלי קשר לערכים התזונתיים.",
  "סיבים תזונתיים לא נכנסו לניתוח הקטגוריה הזו. מוצרי חלב רבים לא מדווחים על סיבים בתווית, ולכן הגורם הזה הוצא מהחישוב כדי למנוע הטיה בין מוצרים.",
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
