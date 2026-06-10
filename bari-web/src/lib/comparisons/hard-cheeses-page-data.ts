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
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

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
  title: 'גבינה קשה היא בין מקורות החלבון הנפוצים בארץ — וגם אחד התחומים שבהם "לייט" לא תמיד אומר מה שחושבים.',
} as const;

export const hardCheesesPrologueSentences = [
  "רוב הגבינות הקשות בסופרמרקט עוברות פחות עיבוד ממה שנדמה: חלב, מלח, תרביות ומקריש. החלבון גבוה, השומן גבוה, הנתרן בדרך כלל גבוה גם הוא. הגרסאות המופחתות שומן (9%–5%) אכן מכילות פחות שומן — אבל חלקן מגיעות עם מייצבים ומשמרים שהגרסה המלאה לא צריכה. הציון משקף את כלל התמונה.",
] as const;

export const hardCheesesCategoryNote =
  'הציון לא נקבע לפי אחוז השומן בלבד. גבינה 28% עם רכיבים מינימליים עשויה לצאת עם ציון גבוה יותר מגבינה 5% שמכילה מייצבים ומשמרים. "לייט" אומר פחות קלוריות — לא בהכרח פחות תוספות.\n\nאחוז השומן המצוין על האריזה ("28%") הוא שומן מתוך משקל המוצר הרטוב, לא מתוך המוצר היבש. גבינות קשות ומיושנות עם אותו מספר אחוזים עשויות להכיל שיעורי שומן שונים לגמרי כשמשווים על בסיס יבש.';

export const hardCheesesMethodologyLines = [
  "בדקנו 30 גבינות קשות וצהובות מיוחננוף — רכיבים, ערכי תזונה ורמת עיבוד.",
  "הציונים יחסיים לקטגוריית גבינות קשות בלבד; אחוז השומן על האריזה הוא שומן בחומר יבש — החישוב משתמש בשומן בפועל (גרם ל-100 גרם).",
  "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה שזמין על האריזה.",
  "מסד הנתונים עודכן ביוני 2026 — ייתכן שינויים בנוסחאות שאינם משתקפים עדיין בציון.",
] as const;

export const hardCheesesComparisonMetadata: Metadata = {
  title: "השוואת גבינות קשות וצהובות | Bari",
  description:
    "השוואת 30 גבינות קשות מהמדף הישראלי — ציון Bari, חלבון, שומן ונתרן ל-100 גרם. מידע, לא המלצה.",
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
