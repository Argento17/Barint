import type { Metadata } from "next";

import { withComparisonOpenGraph } from "@/lib/seo/open-graph";

import rawCorpus from "@/data/comparisons/hard_cheeses_frontend_v4.json";

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
  title: "איזו גבינה צהובה שווה את המקום בסלסלה?",
} as const;

export const hardCheesesPrologueSentences = [
  "הגבינות הצהובות והקשות הן הקניה האוטומטית — מגיעים לקצה המקרר, לוקחים את אותה האריזה, ויוצאים.",
  "אבל מתחת לדמיון החיצוני יש כאן תמונה אחת ברורה: רוב הגבינות במדף מתקבצות יחד בציון B מוצק, כי השומן הרווי שבהן הוא הגורם הכובל — הוא חלק טבעי ממטריצת החלב, וברי לא מעניש אותו כמו שומן שהוסף בייצור.",
  "מה שכן יוצר הפרשים בתוך הקבוצה הוא הניואנסים: כמה מלח, כמה נקייה רשימת הרכיבים, וכמה גבוה השומן הרווי.",
  "גבינה אחת בלבד יוצאת מהמקבץ — גלבוע 5%, שהיא באמת דלת-שומן ויושבת לבדה בראש.",
] as const;

export const hardCheesesCategoryNote =
  "הערת קטגוריה: למה רוב הגבינות הצהובות מקובצות יחד ב-B? כל הגבינות כאן חולקות אופי דומה — מטריצת חלב עשירה בשומן רווי, שהוא חלק טבעי מהמוצר ולא שומן שהוסף בייצור. בארי לא מעניש את השומן הזה כמו שומן מוסף, אבל השומן הרווי הוא עדיין הגורם הכובל שמחזיק את רוב המדף בציון B מוצק וקרוב זה לזה. בתוך הטווח הצר הזה, ניואנסים הם שמזיזים גבינה למעלה או למטה: רשימת רכיבים נקייה יותר, נתרן נמוך יותר ושומן רווי נמוך יותר מטים לכיוון הגבוה; ריבוי תוספים, נתרן גבוה יותר ושומן רווי גבוה יותר מטים לכיוון הנמוך. אף גורם בודד אינו מכריע בפני עצמו, אלא המשקל המצטבר שלהם יחד. הגבינה היחידה שהגיעה ל-A במדף הזה היא גלבוע 5%, שהיא באמת דלת-שומן ולכן יושבת בנפרד משאר המדף.";

export const hardCheesesMethodologyLines = [
  "בדקנו 31 גבינות קשות וצהובות מהמדף — רכיבים, ערכי תזונה ורמת עיבוד, מעבר לאחוז השומן בלבד.",
  "הציונים יחסיים לקטגוריית גבינות קשות בלבד; אחוז השומן על האריזה הוא שומן בחומר רטוב, והחישוב משתמש בשומן בפועל (גרם ל-100 גרם).",
  "שומן רווי משוקלל כגורם אמיתי, אך גבינה נקייה אינה מקבלת את אותו קנס כמו שומן מהונדס — בהתאם לעדות שמבנה הגבינה ממתן את ההשפעה על הכולסטרול.",
  "מוצרים עם נתוני תזונה חלקיים מסומנים בהתאם, והציון מבוסס על הנתונים שהיו זמינים.",
  "מסד הנתונים עודכן ביוני 2026 — ייתכנו שינויים בנוסחאות שטרם משתקפים בציון.",
] as const;

export const hardCheesesComparisonMetadata: Metadata = withComparisonOpenGraph({
  title: "השוואת גבינות קשות וצהובות | Bari",
  description:
    "השוואת 31 גבינות קשות מהמדף הישראלי — ציון Bari, חלבון, שומן ונתרן ל-100 גרם. מידע, לא המלצה.",
});

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
