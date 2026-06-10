import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/frozen_vegetables_frontend_v1.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import { enrichRowSurface } from "@/lib/comparisons/row-surface";
import {
  filterFrozenVegetablesProducts,
  FROZEN_VEGETABLES_SHELF_LENS_OPTIONS,
  type FrozenVegetablesShelfFilterId,
} from "@/lib/comparisons/frozen-vegetables-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

export type FrozenVegetablesCorpusMeta = ComparisonCorpusMeta;

// `_cluster` (shelf sub-pool, read off the raw JSON in frozen-vegetables-shelf-filters)
// and `source_traceability_status` (internal provenance) are now stripped centrally by
// loadComparisonCorpus' BariProductVM allowlist (TASK-233A) — no local strip needed.
const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const corpusMeta = loaded.meta;
const frozenVegetablesProducts = enrichRowSurface(loaded.products);

export { corpusMeta, frozenVegetablesProducts };

export const frozenVegetablesMetadataLine = `${corpusMeta.product_count} מוצרים נבדקו · מדף ירקות קפואים · ממוין לפי ציון Bari`;

export const frozenVegetablesHero = {
  eyebrow: "מנוע השוואה · ירקות קפואים",
  title: "ירקות קפואים: מה באמת באריזה?",
} as const;

export const frozenVegetablesPrologueSentences = [
  "בדקנו 53 ירקות קפואים ממדף שופרסל — אפונה, ברוקולי, תערובות, תבלינים ועוד — לפי רכיבים, עיבוד וערכים תזונתיים. 35 מתוכם מגיעים ל-A: ירקות וקטניות קפואים בלי תוספות, רכיב אחד, ציון מלא.",
  "תערובות ירקות ומוצרים עם מייצבים או תוספות נופלים ל-B ו-C — גם כשהבסיס הוא ירק. ככל שרשימת הרכיבים מתארכת, הציון יורד. שתי תערובות עם פסטה (P_107622, P_103730) מסומנות בהערה: הירקות מהווים 75% מהמוצר, הפסטה היא מרכיב משני.",
  "במדף הזה 'הכי טוב' הוא A — 85 נקודות לירק קפוא נקי. אין S כאן, גם לא לירק הכי טהור: ירק קפוא הוא מוצר בסיסי ומצוין, לא יוצא דופן. A אומר ירק קפוא טוב באמת — נקי, רכיב אחד, בלי תוספות.",
] as const;

export const frozenVegetablesCategoryNote = [
  "הערת קטגוריה — ירקות קפואים: רכיב אחד מול תערובת\n\nירק קפוא בודד (אפונה, ברוקולי, תרד) הוא תמיד בעל ציון גבוה יותר מתערובת או ממוצר עם תוספות. לא בגלל שמות, אלא בגלל מה שכתוב ברשימת הרכיבים: רכיב אחד מול ארבעה ומעלה. תערובת יכולה להיות מוצר מצוין למטבח — אבל הציון מבטא את רמת העיבוד, לא את השימושיות.",
  "הערת קטגוריה — 'הכי טוב' כאן הוא A, לא S\n\n35 ירקות קפואים על המדף מגיעים ל-A, והגבוה הוא 89/A. אבל אף אחד לא מגיע ל-S, גם המוביל: ירק קפוא בסיסי ומצוין, לא יוצא דופן. A כאן אומר ירק קפוא טוב באמת — לא מושלם, ולא מעבר לכך.",
  "הערת קטגוריה — מוצרים עם פסטה\n\nשתי תערובות ירקות (P_107622, P_103730) מכילות פסטה ומסומנות בהערה נפרדת. הפסטה מורידה את הציון, אף שהירקות מהווים 75% מהמוצר. הציון משקף את ההרכב המלא — ירקות בתוספת פחמימה מעובדת.",
]
  .join("\n\n");

export const frozenVegetablesMethodologyLines = [
  "ניתוח ירקות קפואים מבוסס על תוויות של מוצרים ממדף שופרסל — לא סקר שוק ישראלי מלא.",
  "לכל מוצר נבחנו רכיבים, רמת עיבוד (NOVA), ערכים תזונתיים ותוספים.",
  "תערובות ירקות ומוצרים מעובדים מקבלים ציון נפרד — לא מושווים ישירות לירקות בודדים.",
  "הדירוג נועד לעזור בהבנת ההרכב של המוצר ואינו מהווה המלצה תזונתית אישית.",
] as const;

export const frozenVegetablesComparisonMetadata: Metadata = {
  title: "השוואת ירקות קפואים | Bari",
  description:
    "השוואה בין 53 ירקות קפואים — אפונה, ברוקולי, תערובות, תבלינים ועוד. לפי רכיבים, רמת עיבוד וערכים תזונתיים.",
};

function isShelfFilterId(filter: string): filter is FrozenVegetablesShelfFilterId {
  return FROZEN_VEGETABLES_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const frozenVegetablesShelfFilters = {
  lensOptions: FROZEN_VEGETABLES_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterFrozenVegetablesProducts(products, activeFilters.filter(isShelfFilterId)),
};

export function getFrozenVegetablesPageData(): ComparisonCategoryPageData {
  return {
    products: frozenVegetablesProducts,
    metadataLine: frozenVegetablesMetadataLine,
    hero: frozenVegetablesHero,
    prologueSentences: frozenVegetablesPrologueSentences,
    methodologyLines: frozenVegetablesMethodologyLines,
    corpusMeta,
    shelfFilters: frozenVegetablesShelfFilters,
  };
}

export function getFrozenVegetablesCorpusPayload(): {
  _meta: FrozenVegetablesCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: corpusMeta,
    products: frozenVegetablesProducts,
  };
}
