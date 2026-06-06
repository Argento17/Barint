import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/granola_frontend_v1.json";

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

// Populate fiber_g metric from the nutrition panel (already present in the expansion
// object). The base corpus loader doesn't wire nutrition fields into metrics, so we
// do it here once, at load time. Null is preserved when fiber is absent.
// We reassign only fiber_g; protein_g keeps its original value (required by the VM).
const granolaProducts: BariProductVM[] = _granolaProductsRaw.map((p) => ({
  ...p,
  metrics: {
    protein_g: p.metrics?.protein_g ?? null,
    fiber_g: p.expansion?.nutrition?.fiber ?? null,
  },
}));

export { granolaCorpusMeta, granolaProducts };

export const granolaMetadataLine = formatComparisonMetadataLine(
  granolaProducts.length,
  granolaCorpusMeta.generated
);

export const granolaHero = {
  eyebrow: "גרנולה ומוזלי",
  title: "גרנולה ומוזלי: 53 מוצרים, פער של 47 נקודות",
} as const;

export const granolaPrologueSentences = [
  "בדקנו 53 מוצרי גרנולה ומוזלי מהמדף הישראלי — משופרסל, קרפור ויוחננוף; קטגוריה שהופרדה מדגני הבוקר כי ההרכב והעיבוד שלה שונים.",
  "אף מוצר לא הגיע ל-A: 12 ב-B, 25 ב-C, 15 ב-D ואחד ב-E.",
  "הטוב ביותר מגיע ל-76/B; הנמוך ל-29/E — פער של 47 נקודות על אותו מדף, לעיתים תחת שם דומה.",
  "מה שמפריד בין מוצר ל-B למוצר ל-D הוא כמות הסוכר, השומן והסירופ בפועל — לא תדמית הבריאות.",
] as const;

export const granolaCategoryNote =
  "גרנולה ומוזלי הם דגן אפוי עם שמן וממתיק — לכן רובם עתירים יותר בקלוריות, סוכר ושומן ממרבית דגני הבוקר. הציון משווה אותם זה לזה; קריאת ערכי התזונה למנה חשובה כאן במיוחד.";

export const granolaMethodologyLines = [
  "בדקנו 53 מוצרי גרנולה ומוזלי משלוש רשתות — שופרסל, קרפור ויוחננוף — רכיבים, ערכי תזונה ורמת עיבוד, לא רק קלוריות.",
  "הציונים יחסיים לקטגוריה; בסקירה זו אף מוצר לא הגיע ל-A.",
  "מוצרים עם נתוני רכיבים חלקיים מסומנים בהתאם — הציון מבוסס על מה שזמין.",
] as const;

export const granolaComparisonMetadata: Metadata = {
  title: "השוואת גרנולה ומוזלי | Bari",
  description:
    "השוואת 53 מוצרי גרנולה ומוזלי מהמדף הישראלי — ציון Bari, רכיבים, ערכי תזונה ורמת עיבוד. מידע, לא המלצה.",
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
