import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/cereals_frontend_v2.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterCerealsProducts,
  CEREALS_SHELF_LENS_OPTIONS,
  type CerealsShelfFilterId,
} from "@/lib/comparisons/cereals-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type CerealsCorpusMeta = ComparisonCorpusMeta;

function isCerealsShelfFilterId(filter: string): filter is CerealsShelfFilterId {
  return CEREALS_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

// loadComparisonCorpus strips only _calibration. The _subpool / _isChildrens /
// _wholeGrainClaim internal fields remain on the product objects at runtime —
// the shelf-filters cast to CerealsCorpusProduct to access them. They are never
// forwarded to any rendered JSX string.
const { meta: cerealsCorpusMeta, products: cerealsProducts } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

export { cerealsCorpusMeta, cerealsProducts };

export function formatCerealsMetadataLine(
  productCount: number,
  generatedIso: string
): string {
  return formatComparisonMetadataLine(productCount, generatedIso);
}

export const cerealsMetadataLine = formatCerealsMetadataLine(
  cerealsProducts.length,
  cerealsCorpusMeta.generated
);

export const cerealsHero = {
  eyebrow: "דגני בוקר",
  title: "דגני בוקר: 34 מוצרים, אף אחד לא מגיע ל-A",
} as const;

export const cerealsPrologueSentences = [
  "בדקנו 34 מוצרי דגני בוקר מהמדף הישראלי — משופרסל וקרפור.",
  "אף מוצר לא הגיע ל-A — הציון הגבוה ביותר עוצר ב-75/B.",
  "החלוקה: שישה מוצרים ב-B, 11 ב-C, 16 ב-D ואחד ב-E.",
  "חמישה מוצרים מיועדים לילדים; הפער בין הגבוה לנמוך הוא 43 נקודות.",
  "גרנולה ומוזלי מוצגים בעמוד נפרד — משפחת מוצרים אחרת.",
] as const;

export const cerealsCategoryNote = [
  "הערת קטגוריה — העשרה בוויטמינים ומינרלים\n\nרוב דגני הבוקר מועשרים בוויטמינים ומינרלים סינתטיים — ברזל, ויטמיני B, חומצה פולית, ויטמין D. ההעשרה נגזרת מתהליך הייצור: הדגן המעובד מאבד חלק ממיקרו-הרכיבים שלו, והיצרן מחזיר אותם מבחוץ. ציון Bari מבוסס על מבנה המזון — כמות החלבון, הסיבים, רמת העיבוד ושלמות רשימת הרכיבים. הוא אינו מחשב תרומת מיקרו-רכיבים, בין אם מועשרים ובין אם מקוריים. מוצר מועשר עשוי לספק ברזל או ויטמין D שאינם משתקפים בציון.",
  "הערת קטגוריה — טענת 'דגנים מלאים' נקראת מהרשימה, לא מהמיתוג\n\nטענת 'דגנים מלאים' מופיעה על 20 מוצרים בעמוד זה, אך לא בכולם סדר הרכיבים תומך בה — לעיתים קמח לבן מופיע לפני הדגן המלא. הציון מבוסס על ההרכב בפועל, לא על הטענה שעל האריזה.",
].join("\n\n");

export const cerealsMethodologyLines = [
  "בדקנו 34 מוצרי דגני בוקר משתי רשתות — שופרסל וקרפור — רכיבים, ערכי תזונה ורמת עיבוד, לא רק קלוריות.",
  "הציונים יחסיים לקטגוריה; בסקירה זו אף מוצר לא הגיע ל-A.",
  "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה שזמין.",
] as const;

export const cerealsComparisonMetadata: Metadata = {
  title: "השוואת דגני בוקר | Bari",
  description:
    "השוואת 34 מוצרי דגני בוקר מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

const cerealsShelfFilters = {
  lensOptions: CEREALS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterCerealsProducts(
      products,
      activeFilters.filter(isCerealsShelfFilterId)
    ),
};

export function getCerealsPageData(): ComparisonCategoryPageData {
  return {
    products: cerealsProducts,
    metadataLine: cerealsMetadataLine,
    hero: cerealsHero,
    prologueSentences: cerealsPrologueSentences,
    methodologyLines: cerealsMethodologyLines,
    corpusMeta: cerealsCorpusMeta,
    shelfFilters: cerealsShelfFilters,
  };
}

export function getCerealsCorpusPayload(): {
  _meta: CerealsCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: cerealsCorpusMeta,
    products: cerealsProducts,
  };
}
