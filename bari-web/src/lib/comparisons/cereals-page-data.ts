import type { Metadata } from "next";

import { withComparisonOpenGraph } from "@/lib/seo/open-graph";

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
const { meta: cerealsCorpusMeta, products: _cerealsProductsRaw } =
  loadComparisonCorpus(rawCorpus as unknown as ComparisonCorpusRaw);

// Populate sugar_g and protein_g metrics from the nutrition panel (TASK-387).
// The base corpus loader does not wire nutrition fields into metrics, so we map
// them here at load time — mirroring the granola-page-data pattern exactly.
// Shelf ranges (measured from cereals_frontend_v2.json):
//   protein_g: 5.0–12.0g/100g (20/20 values present)
//   sugar_g:   3.8–29.9g/100g (19/20 values; barcode 7297488098688 = null → "—")
// Null is preserved when a field is absent — the MetricColumn renders "—" for null.
const cerealsProducts: BariProductVM[] = _cerealsProductsRaw.map((p) => ({
  ...p,
  metrics: {
    protein_g: p.expansion?.nutrition?.protein ?? null,
    sugar_g: p.expansion?.nutrition?.sugar ?? null,
  },
}));

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
  title: "דגני בוקר: 20 מוצרים, אף אחד לא מגיע ל-A",
} as const;

export const cerealsPrologueSentences = [
  "רוב דגני הבוקר כאן מוכרים דגן מלא, סיבים וויטמינים — אבל בפועל הרבה מהם מוכרים בעיקר סוכר באריזת בריאות.",
  "מתוך 20 מוצרים שבדקנו, אף אחד לא הגיע לציון A — רוב המדף מתקבץ סביב C ו-D.",
  "הפער בין הבטחת האריזה להרכב בפועל הוא הממצא המרכזי — ולא נקודתי: הוא חוזר על עצמו ברוב המוצרים.",
  "יש כאן מוצרים שעושים את העבודה באמת: בסיס דגן מלא אמיתי, רשימת רכיבים קצרה, פרופיל שמצדיק את הציפייה.",
  "ויש מוצרים שלובשים את חולצת ארוחת הבוקר ומבחינת הרכבם קרובים יותר לקינוח שמוזגים עליו חלב.",
  "גרנולה ומוזלי מוצגים בעמוד נפרד.",
] as const;

export const cerealsCategoryNote = [
  "הערת קטגוריה — סף הסוכר והסימון האדום\n\nהתקנה הישראלית מחייבת סימון אדום על מוצרים שמגיעים ל-25 גרם סוכר ל-100 גרם ומעלה. ציון Bari מחיל קנס ציון על מוצרים שחוצים סף זה — לא מכיוון שהתקנה היא גבול קסם תזונתי, אלא מכיוון שרמת סוכר זו מגדירה פרופיל שהמדינה עצמה מסמנת. מוצרים ב-E בסקירה הזאת הם דוגמאות מובהקות לכך.",
  "הערת קטגוריה — העשרה בוויטמינים ומינרלים\n\nרוב דגני הבוקר מועשרים בוויטמינים ומינרלים סינתטיים — ברזל, ויטמיני B, חומצה פולית, ויטמין D. ההעשרה נגזרת מתהליך הייצור: הדגן המעובד מאבד חלק ממיקרו-הרכיבים שלו, והיצרן מחזיר אותם מבחוץ. ציון Bari מבוסס על מבנה המזון — חלבון, סיבים, רמת עיבוד ורשימת רכיבים. הוא אינו מחשב תרומת מיקרו-רכיבים, בין אם מועשרים ובין אם מקוריים.",
  "הערת קטגוריה — טענת 'דגנים מלאים' נקראת מהרשימה, לא מהמיתוג\n\nטענת 'דגנים מלאים' מופיעה על רוב המוצרים בעמוד זה, אך לא בכולם סדר הרכיבים תומך בה — לעיתים קמח לבן מופיע לפני הדגן המלא, או שאחוז הדגן המלא מהווה מיעוט מהבסיס. הציון נקבע לפי ההרכב עצמו, מעבר להצהרות שעל האריזה.",
].join("\n\n");

export const cerealsMethodologyLines = [
  "בדקנו 20 מוצרי דגני בוקר משתי רשתות — שופרסל וקרפור — רכיבים, ערכי תזונה ורמת עיבוד, לא רק קלוריות.",
  "הציונים יחסיים לקטגוריה; בסקירה זו אף מוצר לא הגיע ל-A.",
  "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה שזמין.",
] as const;

export const cerealsComparisonMetadata: Metadata = withComparisonOpenGraph({
  title: "השוואת דגני בוקר | Bari",
  description:
    "השוואת 20 מוצרי דגני בוקר מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
});

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
