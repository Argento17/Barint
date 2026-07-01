import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/granola_frontend_v2.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterGranolaProducts,
  GRANOLA_SHELF_LENS_OPTIONS,
  type GranolaShelfFilterId,
} from "@/lib/comparisons/granola-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type GranolaCorpusMeta = ComparisonCorpusMeta;

function isGranolaShelfFilterId(filter: string): filter is GranolaShelfFilterId {
  return GRANOLA_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const { meta: granolaCorpusMeta, products: _granolaProductsRaw } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

// Populate sugar_g and protein_g metrics from the nutrition panel (already present in
// the expansion object). TASK-385: sugar replaces fiber as the granola headline metric
// (fiber is gameable via added chicory/inulin and creates fiber-vs-grade inversions).
// The base corpus loader doesn't wire nutrition fields into metrics, so we do it here
// once, at load time. Null is preserved when either field is absent.
// protein_g: shelf range 8.7–23.7g — the GRANOLA_METRIC_SPECS passes a granola-tuned
//   PROTEIN_METRIC override (scaleMax 25) to handle the 23.7g top without clipping.
// sugar_g: shelf range 4.8–25g — calibrated via GRANOLA_SUGAR_METRIC (scaleMax 28).
const granolaProducts: BariProductVM[] = _granolaProductsRaw.map((p) => ({
  ...p,
  metrics: {
    protein_g: p.expansion?.nutrition?.protein ?? null,
    sugar_g: p.expansion?.nutrition?.sugar ?? null,
  },
}));

export { granolaCorpusMeta, granolaProducts };

export const granolaMetadataLine = formatComparisonMetadataLine(
  granolaProducts.length,
  granolaCorpusMeta.generated
);

export const granolaHero = {
  eyebrow: "גרנולה ומוזלי",
  title: "גרנולה ומוזלי: 22 מוצרים, פער של 38.3 נקודות",
} as const;

export const granolaPrologueSentences = [
  "גרנולה נראית כמו ארוחת בוקר בריאה — אבל על המדף היא הרבה פעמים דגנים עם שמן, סירופ ופירות מסוכרים.",
  "בדקנו 22 מוצרים מהמדף הישראלי: אף אחד לא הגיע ל-A. 4 הגיעו ל-B, 8 ל-C, 7 ל-D — ו-3 נחתו ב-E.",
  "הפער בין הטוב ביותר (69.7/B) לנמוך ביותר (31.4/E) הוא 38.3 נקודות — על אותו מדף, לעיתים תחת שם דומה.",
  "מה שמפריד בין B ל-D הוא לא האריזה: זה סוג השמן, סוג הממתיק, והאם הפירות כבר הגיעו מסוכרים.",
] as const;

export const granolaCategoryNote =
  "רוב הגרנולות במדף הישראלי נבנו סביב טעם, לא סביב תזונה: שמן, ממתיק ופריכות הם הנוסחה. רק 4 מתוך 22 מוצרים בבדיקה הגיעו ל-B — 8 נחתו על D. המוצר עתיר-הסוכר בבדיקה עומד על 25 גרם סוכר ל-100 גרם — ראש המדף, ופי חמישה ויותר מהגרנולה הדלה בסוכר (4.8 גרם). מה שמפריד בין תחתית המדף לאמצעו הוא לא רק כמות הסוכר: שמן דקלים, סירופ גלוקוז, פירות מסוכרים מראש וצבעי מאכל הם הסימנים שמגדירים את הגרנולות בדרגות D ו-E.";

export const granolaMethodologyLines = [
  "בדקנו 22 מוצרי גרנולה ומוזלי משלוש רשתות — שופרסל, קרפור ויוחננוף — רכיבים, ערכי תזונה ורמת עיבוד, לא רק קלוריות.",
  "הציונים יחסיים לקטגוריה; בסקירה זו אף מוצר לא הגיע ל-A.",
  "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה שזמין.",
  "הסוכר והחלבון מוצגים כשני מדדים מרכזיים — אבל הציון משקלל גם עיבוד, רכיבים, שומן וקלוריות ותוספים, כך שמוצר דל-סוכר עדיין יכול לקבל ציון נמוך.",
] as const;

export const granolaComparisonMetadata: Metadata = {
  title: "השוואת גרנולה ומוזלי | Bari",
  description:
    "השוואת 22 מוצרי גרנולה ומוזלי מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

const granolaShelfFilters = {
  lensOptions: GRANOLA_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterGranolaProducts(
      products,
      activeFilters.filter(isGranolaShelfFilterId)
    ),
};

export function getGranolaPageData(): ComparisonCategoryPageData {
  return {
    products: granolaProducts,
    metadataLine: granolaMetadataLine,
    hero: granolaHero,
    prologueSentences: granolaPrologueSentences,
    methodologyLines: granolaMethodologyLines,
    corpusMeta: granolaCorpusMeta,
    shelfFilters: granolaShelfFilters,
  };
}

export function getGranolaCorpusPayload(): {
  _meta: GranolaCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: granolaCorpusMeta,
    products: granolaProducts,
  };
}
