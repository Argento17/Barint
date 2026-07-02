import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/brined_cheeses_frontend_v2.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import type { BariProductVM } from "@/lib/view-models";

export type BrinedCheesesCorpusMeta = ComparisonCorpusMeta;

type BrinedCheesesCorpusProduct = BariProductVM & { barcode?: string };

const _brinedCheesesRawProducts = (rawCorpus as ComparisonCorpusRaw).products as BrinedCheesesCorpusProduct[];

const { meta: brinedCheesesCorpusMeta, products: _brinedCheesesProductsRaw } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

// Top-scored product (run_005) — representative hero image for index card (TASK-268 later).
export const brinedCheesesHeroImageUrl =
  _brinedCheesesRawProducts.find((p) => p.barcode === "7290019635826")?.imageUrl ?? null;

// Sodium per 100g is the headline differentiator — brined cheeses are structurally high-sodium.
const brinedCheesesProducts: BariProductVM[] = _brinedCheesesProductsRaw.map(
  (p) => ({
    ...p,
    imageUrl: p.imageUrl ?? null,
    d4_additives: p.d4_additives ?? [],
    metrics: {
      protein_g: p.expansion?.nutrition?.protein ?? null,
      sodium_mg: p.expansion?.nutrition?.sodium ?? null,
    },
  })
);

export { brinedCheesesCorpusMeta, brinedCheesesProducts };

export const brinedCheesesMetadataLine = formatComparisonMetadataLine(
  brinedCheesesProducts.length,
  brinedCheesesCorpusMeta.generated
);

export const brinedCheesesHero = {
  eyebrow: "גבינות מלוחות",
  title: "בולגרית, פטה, צפתית, חלומי — גבינות שהנתרן בהן הוא חלק מהייצור, לא תוספת.",
} as const;

export const brinedCheesesPrologueSentences = [
  "כשאת קונה גבינה מלוחה, המלח הוא לא רכיב שנוסף לטעם — הוא מה שהופך את החלב לגבינה. הכבישה בתמיסת מלח שומרת על הגבינה, מעצבת את המרקם שלה, ומגדירה את אופייה.",
  "זה אומר שלפטה, לבולגרית ולצפתית יש נתרן גבוה מלידה. זו לא בחירה ייצורית — זה מה שהן. בארי לא מענישה אותן על כך. השאלה שנשאלת כאן היא שאלה אחרת: כשהנתרן הוא נתון קבוע, מה בכל זאת מבדיל גבינה טובה מגבינה בינונית?",
  "בארי בחנה 36 גבינות מלוחות — והממצא ברור: רוב המדף מתקבץ סביב B ו-C, ומעטות בלבד מגיעות ל-A. ההבדלים הגדולים נובעים מהרשימה: כמה רכיבים, אילו מייצבים, כמה חלבון, עד כמה הגבינה נשארת פשוטה.",
  "הנדיר כאן הוא המינימליזם: רק שתי גבינות במדף מגיעות בלי שום תוסף — חלב, מלח ותרבית בלבד. המרשימה שבהן היא הבולגרית 13% של יורו מחלבות אירופה: רשימה נקייה, תרבית לקטית חיה, נתרן נמוך יחסית של 720 מ\"ג, וציון בדירוג A. וכאן מתחדדת הנקודה: ראש המדף שייך דווקא לצפתית של מחלבות גד, גבינה מצוינת שנשענת על חומר משמר. הגבינה הנקייה השנייה, טמרה של רג'ב, יושבת דווקא ב-C כי הנתרן שלה הוא הגבוה במדף. רשימת רכיבים נקייה לא תמיד אומרת ציון הכי גבוה, וזה בדיוק מה שבארי באה למדוד.",
] as const;

export const brinedCheesesCategoryNote =
  "הערת קטגוריה\n\nכל הגבינות במדף הזה עשירות בנתרן — זו תכונה מובנית של ייצור גבינה מלוחה, לא חריגה. ציון גבוה בקטגוריה זו אינו מעיד שהגבינה נמוכה בנתרן; הוא מעיד על הרכב רכיבים נקי, שומן מתון ועיבוד מינימלי ביחס לשאר המדף. מי שנדרש לצמצם נתרן מטעמים רפואיים יתייעץ עם איש מקצוע.";
export const brinedCheesesMethodologyLines = [
  "כל גבינה מלוחה מקבלת הגנת קטגוריה, כי הנתרן שלה הוא חלק ממה שהיא ולא תוסף שנבחר. המנגנון אינו מתייחס לנתרן כאל כשל — הוא מדרג אותו יחסית למדף. רק גבינה שנמצאת מעל 200 מ\"ג מחציון הקטגוריה מקבלת חיסרון נוסף. לא כל גבינה שעל החציון.",
  "מה שמניע את ההבדלים האמיתיים: מספר הרכיבים, נוכחות מייצבים ומתחלבים, ואחוז השומן. חלב, מלח ותרבית לקטית הם הגרעין. גומי זרעי חרובים, אגר וגלוקונו-דלתא-לקטון הם שכבה אחרת לגמרי. החלבון שוקל לחיוב — גבינה מלוחה היא מקור חלבון ממשי, וזה מה שהמנגנון מתגמל עליו.",
  "כל מוצר שמוצג כאן עבר אימות מלא: רשימת רכיבים ונתוני תזונה ממקור ישיר. גבינה שלא ניתן היה לאמת אותה לא מופיעה. הערה לגבי אחוזי שומן: '24%' בשם גבינה כמעט תמיד מתייחס לשומן בחומר היבש — מדד תעשייתי שאינו שווה ערך לשומן ב-100 גרם מוכנה. בארי עובדת עם הנתון שעל התווית.",
] as const;

export const brinedCheesesComparisonMetadata: Metadata = {
  title: "השוואת גבינות מלוחות | Bari",
  description:
    "השוואת 36 גבינות מלוחות מהמדף הישראלי — ציון Bari, נתרן, חלבון ושומן ל-100 גרם. מידע, לא המלצה.",
};

const brinedCheesesShelfFilters = {
  lensOptions: [],
  filterProducts: (products: BariProductVM[], _activeFilters: string[]) => products,
};

export function getBrinedCheesesPageData(): ComparisonCategoryPageData {
  return {
    products: brinedCheesesProducts,
    metadataLine: brinedCheesesMetadataLine,
    hero: brinedCheesesHero,
    prologueSentences: brinedCheesesPrologueSentences,
    methodologyLines: brinedCheesesMethodologyLines,
    corpusMeta: brinedCheesesCorpusMeta,
    shelfFilters: brinedCheesesShelfFilters,
  };
}

export function getBrinedCheesesCorpusPayload(): {
  _meta: BrinedCheesesCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: brinedCheesesCorpusMeta,
    products: brinedCheesesProducts,
  };
}
