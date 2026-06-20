import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/protein_bars_frontend_v1.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import { enrichRowReasonOnly } from "@/lib/comparisons/row-surface";
import {
  filterProteinBarsProducts,
  PROTEIN_BARS_SHELF_LENS_OPTIONS,
  type ProteinBarsShelfFilterId,
} from "@/lib/comparisons/protein-bars-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type ProteinBarsCorpusMeta = ComparisonCorpusMeta;

const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const proteinBarsCorpusMeta = loaded.meta;
// rowReason only — NO metric bar (same posture as snacks: a single dominant
// numeric signal would be misleading across these products).
const proteinBarsProducts = enrichRowReasonOnly(loaded.products as BariProductVM[]);

export { proteinBarsCorpusMeta, proteinBarsProducts };

const proteinBarsMetadataUpdated = (() => {
  const date = new Date(proteinBarsCorpusMeta.generated);
  return Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleDateString("he-IL", { month: "long", year: "numeric" });
})();

export const proteinBarsMetadataLine = proteinBarsMetadataUpdated
  ? `${proteinBarsProducts.length} חטיפי חלבון בדף · נסרקו ממדף החטיפים בשופרסל · עודכן ב${proteinBarsMetadataUpdated}`
  : `${proteinBarsProducts.length} חטיפי חלבון בדף · נסרקו ממדף החטיפים בשופרסל`;

export const proteinBarsHero = {
  eyebrow: "חטיפי חלבון",
  title: "חטיפי חלבון: הרבה חלבון — אבל מה המחיר ההנדסי?",
} as const;

export const proteinBarsPrologueSentences = [
  "חטיף חלבון מבטיח דבר אחד גדול: 25–34 גרם חלבון בחטיף אחד. זה הרבה, וזה אמיתי.",
  "אבל החלבון הזה לרוב לא מגיע לבד — לצידו ממתיקים מלאכותיים, תחליפי סוכר (מלטיטול, סורביטול), שומן צמחי ורשימת רכיבים ארוכה.",
  "השאלה כאן היא לא 'כמה חלבון' אלא 'כמה מהונדס' — וזה מה שמפריד בין חטיף לחטיף במדף הזה.",
] as const;

export const proteinBarsCategoryNote = [
  "הערת קטגוריה — 'הכי טוב' כאן הוא B, לא A\n\nבמדף חטיפי החלבון אף מוצר אינו מגיע ל-A. הציון הגבוה בקטגוריה הוא 72/B. חטיף חלבון הוא מוצר מהונדס סביב ריכוז חלבון גבוה — והציון משקף את ההרכב, לא את כמות החלבון בלבד.",
  "הערת קטגוריה — חטיפי דגנים נמדדים בנפרד\n\nהעמוד הזה מציג חטיפי חלבון בלבד (25–34 גרם חלבון ל-100 גרם). חטיפי דגנים, תמרים ושיבולת שועל — מוצרים שאינם בנויים סביב חלבון מרוכז — נמדדים בקטגוריה משלהם ומוצגים בעמוד נפרד.",
  "הערת קטגוריה — ההשוואה היא בתוך הקטגוריה בלבד\n\nחטיף חלבון נמדד מול חטיפי חלבון אחרים. ציון B כאן אומר 'הטוב יחסית במדף חטיפי החלבון' — לא שהמוצר שקול לארוחה או לבסיס מזון מלא.",
].join("\n\n");

export const proteinBarsMethodologyLines = [
  "ניתחנו את חטיפי החלבון במדף שופרסל — שמות, רכיבים וערכי תזונה ל-100 גרם ישירות מדף המוצר.",
  "כל ערך תזונה עבר בדיקת סבירות ל-100 גרם; פאנלים לא־סבירים הוצאו מהדירוג.",
  "הציון נשען על מבנה המוצר — מקור החלבון, רמת העיבוד, הממתיקים ורשימת הרכיבים — לא על כמות החלבון בלבד.",
  "ציוני Bari מתעדים מבנה מוצר ואינם המלצה תזונתית.",
] as const;

export const proteinBarsComparisonMetadata: Metadata = {
  title: "השוואת חטיפי חלבון | Bari",
  description:
    "השוואת חטיפי חלבון מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
};

const proteinBarsShelfFilters = {
  lensOptions: PROTEIN_BARS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterProteinBarsProducts(
      products,
      activeFilters.filter((f): f is ProteinBarsShelfFilterId =>
        PROTEIN_BARS_SHELF_LENS_OPTIONS.some((o) => o.id === f)
      )
    ),
};

export function getProteinBarsPageData(): ComparisonCategoryPageData {
  return {
    products: proteinBarsProducts,
    metadataLine: proteinBarsMetadataLine,
    hero: proteinBarsHero,
    prologueSentences: proteinBarsPrologueSentences,
    methodologyLines: proteinBarsMethodologyLines,
    corpusMeta: proteinBarsCorpusMeta,
    shelfFilters: proteinBarsShelfFilters,
  };
}

export function getProteinBarsCorpusPayload(): {
  _meta: ProteinBarsCorpusMeta;
  products: BariProductVM[];
} {
  return { _meta: proteinBarsCorpusMeta, products: proteinBarsProducts };
}
