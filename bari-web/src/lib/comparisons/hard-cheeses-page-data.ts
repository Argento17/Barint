import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/hard_cheeses_frontend_v2.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterHardCheesesProducts,
  HARD_CHEESES_SHELF_LENS_OPTIONS,
  type HardCheesesShelfFilterId,
} from "@/lib/comparisons/hard-cheeses-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type HardCheesesCorpusMeta = ComparisonCorpusMeta;

function isHardCheesesShelfFilterId(
  filter: string
): filter is HardCheesesShelfFilterId {
  return HARD_CHEESES_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const { meta: hardCheesesCorpusMeta, products: _hardCheesesProductsRaw } =
  loadComparisonCorpus(rawCorpus as unknown as ComparisonCorpusRaw);

// Protein per 100g is the headline differentiator — hard cheeses carry 20–28g/100g.
const hardCheesesProducts: BariProductVM[] = _hardCheesesProductsRaw.map(
  (p) => ({
    ...p,
    metrics: {
      protein_g: p.expansion?.nutrition?.protein ?? null,
    },
  })
);

export { hardCheesesCorpusMeta, hardCheesesProducts };

export const hardCheesesMetadataLine = formatComparisonMetadataLine(
  hardCheesesProducts.length,
  hardCheesesCorpusMeta.generated
);

export const hardCheesesHero = {
  eyebrow: "גבינות קשות וצהובות",
  title: "קונים גבינה קשה בסופרמרקט? הנה מה שאתם צריכים לדעת.",
} as const;

export const hardCheesesPrologueSentences = [
  "אתם בסופר, עומדים מול קיר של גבינות צהובות. כולן נראות דומות — פרוסות, 28%, עמק או גאודה.",
  "הנחת הבסיס היא שזה מוצר פשוט: חלב, מלח, גבינה.",
  "אז זהו — שלא תמיד.",
  "מה שגילינו הוא שהפערים במדף הזה מגיעים משלושה מקורות: נתרן (שנע בין 491 מ\"ג ל-1,300 מ\"ג ל-100 גרם), חלבון (שנע בין 8 גרם ל-33 גרם ל-100 גרם), ורשימת רכיבים (שנעה בין שני רכיבים לגבינה מותכת עם עמילן ומתחלבים).",
  "רוב הגבינות הקשות כאן הן מה שנדמה שהן — מזון פשוט עם רשימה קצרה. אבל לא כולן.",
  "הגרסאות המופחתות שומן לא תמיד נקיות יותר מהגרסה המלאה. גבינה מותכת אחת נכנסת לסקירה כי היא נמכרת על אותו מדף — ההבדלים ברכיבים גלויים לעין.",
] as const;

export const hardCheesesCategoryNote =
  "הערת קטגוריה — למה רוב הגבינות מקבלות B?\n\nרוב הגבינות הקשות במדף הזה מקבלות ציון B. לא בגלל חולשה — אלא בגלל שהקטגוריה הומוגנית במהותה. גבינה צהובה מסורתית היא מזון מינימלי: חלב, מלח, מקריש. ה-B כאן מתאר תחרות צפופה בין מוצרים דומים מאוד, לא גבינה \"בינונית\". מה שמבדיל בין גבינה למקום 1 לגבינה למקום 22 הוא בעיקר הנתרן וכמות התוספות — לא הבדל מהותי בפרופיל.\n\nהערת קטגוריה — 'לייט' לא תמיד אומר מה שחושבים\n\nגבינה 9% שומן לא בהכרח נקייה יותר מגבינה 28%. בסקירה זו, גרסאות מופחתות שומן מסוימות מגיעות עם חומרי שימור שהגרסה המלאה לא צריכה. הציון משקף את כלל הרכיבים, לא רק את אחוז השומן.\n\nהערת קטגוריה — סוכר וסיבים\n\nערכי הסוכר והסיבים לא צוינו בלוחות התזונה של רוב הגבינות בסקירה זו. זה לא אומר שהם אפס — זה אומר שהיצרן לא נדרש לציין אותם כשהם נמוכים מאוד, ובחר שלא. הציון מבוסס על הנתונים שכן היו זמינים.";

export const hardCheesesMethodologyLines = [
  "בדקנו 28 גבינות קשות וצהובות מיוחננוף — רכיבים, ערכי תזונה ורמת עיבוד, לא רק אחוז שומן.",
  "הציונים יחסיים לקטגוריית גבינות קשות בלבד; אחוז השומן על האריזה הוא שומן בחומר רטוב — החישוב משתמש בשומן בפועל (גרם ל-100 גרם).",
  "מוצרים עם נתוני תזונה חלקיים מסומנים בהתאם — הציון מבוסס על הנתונים שהיו זמינים.",
  "מסד הנתונים עודכן ביוני 2026 — ייתכן שינויים בנוסחאות שאינם משתקפים עדיין בציון.",
] as const;

export const hardCheesesComparisonMetadata: Metadata = {
  title: "השוואת גבינות קשות וצהובות | Bari",
  description:
    "השוואת 28 גבינות קשות מהמדף הישראלי — ציון Bari, חלבון, שומן ונתרן ל-100 גרם. מידע, לא המלצה.",
};

const hardCheesesShelfFilters = {
  lensOptions: HARD_CHEESES_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterHardCheesesProducts(
      products,
      activeFilters.filter(isHardCheesesShelfFilterId)
    ),
};

export function getHardCheesesPageData(): ComparisonCategoryPageData {
  return {
    products: hardCheesesProducts,
    metadataLine: hardCheesesMetadataLine,
    hero: hardCheesesHero,
    prologueSentences: hardCheesesPrologueSentences,
    methodologyLines: hardCheesesMethodologyLines,
    corpusMeta: hardCheesesCorpusMeta,
    shelfFilters: hardCheesesShelfFilters,
  };
}

export function getHardCheesesCorpusPayload(): {
  _meta: HardCheesesCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: hardCheesesCorpusMeta,
    products: hardCheesesProducts,
  };
}
