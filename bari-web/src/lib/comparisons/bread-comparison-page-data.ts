import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/bread_frontend_v2.json";

import {
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import { enrichRowSurface } from "@/lib/comparisons/row-surface";
import {
  filterBreadProducts,
  BREAD_SHELF_LENS_OPTIONS,
  type BreadShelfFilterId,
} from "@/lib/comparisons/bread-shelf-filters";
import { breadComparisonMeta } from "@/lib/blog/bread-analysis-content";
import type { BariProductVM } from "@/lib/view-models";

export type BreadCorpusMeta = ComparisonCorpusMeta;

// `_website_cluster` (the bread lens reads its cluster off bread-retail-curated.json,
// not the loaded VM) is now stripped centrally by loadComparisonCorpus' BariProductVM
// allowlist (TASK-233A) — no local strip needed.
const loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const breadCorpusMeta = loaded.meta;

// TASK-162: bread's headline row metric is fiber, not protein. The shared enrichRowSurface
// (used by hummus/cheese/yogurts/spreads) only populates protein_g, so we additively layer
// fiber_g on top here — bread-only — reading the real per-100g value straight off
// expansion.nutrition.fiber. null passes through untouched (metric column renders "—"); never
// fabricated. protein_g is left intact, so no shared/other-category behavior changes.
const breadProducts = enrichRowSurface(loaded.products)
  .map((product) => ({
    ...product,
    metrics: {
      // protein_g is always set by enrichRowSurface; keep it intact alongside the new fiber_g.
      protein_g: product.metrics?.protein_g ?? null,
      fiber_g: product.expansion.nutrition?.fiber ?? null,
    },
  }))
  // Unlike the other v2 exports, the bread JSON ships in cluster order, not score order,
  // so the shelf rendered out of rank (a 73 above an 80). The shared ComparisonPage
  // preserves corpus order by design, so sort highest-score-first here; INSUFFICIENT
  // products (score null) sink to the bottom. Shelf-lens filters still apply on top.
  .sort((a, b) => (b.score ?? -1) - (a.score ?? -1));

export { breadCorpusMeta, breadProducts };

export const breadMetadataLine = `${breadCorpusMeta.product_count} מוצרים נבדקו · מדגם שופרסל · ממוין לפי ציון Bari`;

/** Shelf copy — bread MVP handoff v1 (2026-05-30). */
export const breadHero = {
  eyebrow: "מנוע השוואה · לחמים",
  title: "לחם: מה שכתוב על האריזה לא תמיד מה שבפנים",
} as const;

export const breadPrologueSentences = [
  "לחם נראה כמו קטגוריה פשוטה: קמח, מים, מחמצת. אבל המדף מספר סיפור יותר מורכב.",
  "חלק מהמוצרים שמציגים 'מחמצת' בשם משתמשים בשמרים תעשייתיים ברכיבים. חלק אחר מסתמכים על כותרת 'מלא' כדי להציג רכיבים מעורבים.",
  "ההשוואה מתבססת על מה שאפשר לבדוק: ערכי חלבון, סיבים, נתרן, ותסיסה מאומתת ברשימת הרכיבים — לא על המיתוג.",
] as const;

// Category caveat (cheese gold-standard format: bold header + 2 short paragraphs),
// rendered once in the header categoryNote slot. Grounded in the documented bread
// scoring nuance (.claude/scoring.md → "Known Constraints and Gaps"): the engine reads
// fermentation and whole-grain only as they appear in the ingredient list, and cannot
// tell genuine sourdough from an industrial sourdough-powder shortcut.
export const breadCategoryNote = [
  "הערת קטגוריה — תסיסה ודגן מלא נקראים מהרשימה, לא מהמיתוג\n\nהציון מזהה מחמצת, דגן מלא וסיבים לפי מה שמופיע ברשימת הרכיבים — לא לפי הכותרת שעל החזית. לחם שכתוב עליו 'מחמצת' או 'מלא' עשוי להישען על שמרים תעשייתיים או על תערובת קמחים, וזה מה שמשתקף בציון.",
  "הערת קטגוריה — איכות התסיסה אינה נמדדת במלואה\n\nהבדיקה מזהה שתסיסה קיימת ברכיבים, אך אינה מבדילה בין מחמצת אמיתית ואיטית לבין אבקת מחמצת תעשייתית. שני לחמים עם 'מחמצת' ברשימה עשויים לקבל זיכוי דומה גם אם תהליך האפייה שלהם שונה לחלוטין.",
]
  .join("\n\n");

export const breadMethodologyLines = [
  "ניתוח לחמים מבוסס על נתונים מגלויות שופרסל — מדגם מדף, לא סקר שוק מלא.",
  "לכל מוצר נבחנו הרכב הרכיבים, ערכי חלבון וסיבים, רמת עיבוד ותסיסה מאומתת ברכיבים.",
  "ציון הלחם אינו מבוסס על קלוריות בלבד — הוא משקלל מבנה, מקור הדגן, ורמת ההנדסה במוצר.",
  "ההשוואה נועדה לעזור בהשוואה בין מוצרים, ולא מהווה המלצה תזונתית אישית.",
  "מדגם מדף שופרסל בלבד.",
] as const;

export const breadComparisonMetadata: Metadata = {
  title: breadComparisonMeta.title,
  description: breadComparisonMeta.description,
};

function isBreadShelfFilterId(filter: string): filter is BreadShelfFilterId {
  return BREAD_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const breadShelfFilters = {
  lensOptions: BREAD_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterBreadProducts(products, activeFilters.filter(isBreadShelfFilterId)),
};

export function getBreadPageData(): ComparisonCategoryPageData {
  return {
    products: breadProducts,
    metadataLine: breadMetadataLine,
    hero: breadHero,
    prologueSentences: breadPrologueSentences,
    methodologyLines: breadMethodologyLines,
    corpusMeta: breadCorpusMeta,
    shelfFilters: breadShelfFilters,
  };
}

export function getBreadCorpusPayload(): {
  _meta: BreadCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: breadCorpusMeta,
    products: breadProducts,
  };
}
