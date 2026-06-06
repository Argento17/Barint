import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/cereals_frontend_v1.json";

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
  title: "דגני בוקר: 37 מוצרים, אף אחד לא מגיע ל-A",
} as const;

export const cerealsPrologueSentences = [
  "בדקנו 37 מוצרי דגני בוקר מהמדף הישראלי — משופרסל, קרפור ויוחננוף.",
  "אף מוצר לא הגיע ל-A — הציון הגבוה ביותר עוצר ב-78/B.",
  "החלוקה: עשרה מוצרים ב-B, 19 ב-C ושמונה ב-D.",
  "ארבעה מוצרים מיועדים לילדים; הפער בין הגבוה לנמוך הוא 35 נקודות.",
  "גרנולה ומוזלי מוצגים בעמוד נפרד — משפחת מוצרים אחרת.",
] as const;

export const cerealsCategoryNote =
  "טענת 'דגנים מלאים' מופיעה על 20 מוצרים בעמוד זה, אך לא בכולם סדר הרכיבים תומך בה — לעיתים קמח לבן מופיע לפני הדגן המלא. הציון מבוסס על ההרכב בפועל, לא על הטענה שעל האריזה.";

export const cerealsMethodologyLines = [
  "בדקנו 37 מוצרי דגני בוקר משלוש רשתות — שופרסל, קרפור ויוחננוף — רכיבים, ערכי תזונה ורמת עיבוד, לא רק קלוריות.",
  "הציונים יחסיים לקטגוריה; בסקירה זו אף מוצר לא הגיע ל-A.",
  "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה שזמין.",
] as const;

export const cerealsComparisonMetadata: Metadata = {
  title: "השוואת דגני בוקר | Bari",
  description:
    "השוואת 37 מוצרי דגני בוקר מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
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
