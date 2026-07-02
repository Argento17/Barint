import type { Metadata } from "next";

import { withComparisonOpenGraph } from "@/lib/seo/open-graph";

import rawCorpus from "@/data/comparisons/crackers_frontend_v1.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import {
  filterCrackersProducts,
  CRACKERS_SHELF_LENS_OPTIONS,
  type CrackersShelfFilterId,
} from "@/lib/comparisons/crackers-shelf-filters";
import type { BariProductVM } from "@/lib/view-models";

// TASK-433: crackers frontend wiring. Data layer (crackers_frontend_v1.json) is verified —
// 19 products (1 dropped as insufficient_data), rank 1-19, _website_cluster assigned, OFF=0,
// both gates PASS (run_gates + validate_comparison_page), Adversarial QA re-verify GO. This
// loader wires it through the SAME uniform spine as bread/cheese (loadComparisonCorpus is the single path).
//
// Fiber metric: crackers displays fiber_g as its row metric, same rationale as bread
// (grain-based category; fiber is the meaningful headline number, mirrors the
// whole/mixed/refined-grain shelf clusters). expansion.nutrition.fiber is the canonical
// source (per-100g, from BSIP1 panel). Display-only mapping, no score logic.
//
// COPY STATUS: all per-product insightLine/rowVerdict/expansion copy in the source JSON is
// PENDING_COPY (Content Agent fills next). Hero/prologue/methodology/category-note below are
// PENDING_CONTENT placeholders authored by Frontend only to keep the page structurally
// renderable — NOT final consumer copy. Do not treat any string below as approved.

export type CrackersCorpusMeta = ComparisonCorpusMeta;

const _loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const crackersCorpusMeta = _loaded.meta;

// Populate metrics.fiber_g from expansion.nutrition.fiber for the ComparisonPage metric column.
const crackersProducts = _loaded.products.map((product) => ({
  ...product,
  metrics: {
    protein_g: product.metrics?.protein_g ?? null,
    fiber_g: product.expansion?.nutrition?.fiber ?? null,
  },
}));

export { crackersCorpusMeta, crackersProducts };

export function formatCrackersMetadataLine(
  productCount: number,
  generatedIso: string
): string {
  return formatComparisonMetadataLine(productCount, generatedIso);
}

export const crackersMetadataLine = formatCrackersMetadataLine(
  crackersProducts.length,
  crackersCorpusMeta.generated
);

/**
 * DRAFT copy — Content Agent (Tom-Bari voice), TASK-433.
 * NOT approved: pending the Adversarial QA / Red-Team gate (two-gate content rule).
 * Do not ship any string below until both gates sign off.
 */
export const crackersHero = {
  eyebrow: "השוואת קרקרים",
  title: "קונים קרקרים בסופר? הנה מה שבאמת מבדיל ביניהם.",
} as const;

/** DRAFT prologue — pending Adversarial QA gate. */
export const crackersPrologueSentences = [
  "אתם מול מדף הקרקרים, מחפשים בסיס לגבינה, לממרח או סתם משהו פריך לנשנש.",
  "כל האריזות מבטיחות דבר דומה — קל, פריך, טבעי — אבל רשימת הרכיבים מספרת סיפור אחר.",
  "ההבדל האמיתי בין קרקר לקרקר הוא לא הקלוריות, אלא כמה מהבסיס הוא דגן מלא, כמה קצרה רשימת הרכיבים, וכמה סיבים המוצר באמת תורם.",
  "בדקנו עשרים קרקרים מהמדף לפי הרכב הרכיבים והערכים התזונתיים שעל האריזה, והשווינו כל אחד מול השאר — לא מול לחם.",
] as const;

/**
 * Category caveat (הערת קטגוריה) — mandatory yellow box.
 * Sourced from crackers_frontend_v1.json:_meta.categoryCaveat when the Content Agent
 * has populated it (owns that JSON; not edited here — see TASK-433 handoff note).
 * Falls back to a structural DRAFT placeholder — pending Adversarial QA gate — only
 * while _meta.categoryCaveat is absent, so the page never renders without a caveat.
 */
const _metaCategoryCaveat = (crackersCorpusMeta as ComparisonCorpusMeta & {
  categoryCaveat?: string;
}).categoryCaveat;

const CRACKERS_CATEGORY_NOTE_FALLBACK =
  "קרקרים הם מוצר יבש בתהליך אפייה שמסלק כמעט את כל המים, ולכן הקלוריות ל-100 גרם גבוהות יותר מבלחם — וזה נובע מהמבנה של הקרקר, לא מאיכות הרכיבים. בארי משווה כל קרקר מול קרקרים אחרים, לא מול לחם, כך שהקלוריות הגבוהות אינן נחשבות לחיסרון. מה שבאמת מבדיל בין המוצרים במדף הוא כמה מהבסיס הוא דגן מלא לעומת קמח מזוקק ומילויי עמילן, אורך רשימת הרכיבים ומספר מקורות הסוכר, וכמות הסיבים — ושם, ולא בקלוריות, נמצא הפער הגדול בציונים.";

export const crackersCategoryNote = _metaCategoryCaveat ?? CRACKERS_CATEGORY_NOTE_FALLBACK;

/** DRAFT methodology lines — pending Adversarial QA gate. */
export const crackersMethodologyLines = [
  "הציון מבוסס על הרכב הרכיבים והערכים התזונתיים כפי שמופיעים על אריזת המוצר.",
  "כל קרקר מושווה מול קרקרים אחרים — הקלוריות נמדדות מול מדף הקרקרים היבש, לא מול לחם.",
  "משקל רב ניתן לדומיננטיות של דגן מלא בבסיס, לאורך רשימת הרכיבים ולתרומת הסיבים והחלבון.",
  "לא הוספנו נתונים שלא הופיעו על האריזה; במקום שבו נתון חסר, הוא מסומן ככזה.",
] as const;

export const crackersComparisonMetadata: Metadata = withComparisonOpenGraph({
  title: "השוואת קרקרים — מה באמת מבדיל ביניהם | בארי",
  description:
    "השוואה של עשרים קרקרים מהמדף לפי דומיננטיות דגן מלא, אורך רשימת הרכיבים ותרומת סיבים — לא לפי קלוריות. כל קרקר מושווה מול קרקרים אחרים, לא מול לחם.",
});

function isCrackersShelfFilterId(filter: string): filter is CrackersShelfFilterId {
  return CRACKERS_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

const crackersShelfFilters = {
  lensOptions: CRACKERS_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: string[]) =>
    filterCrackersProducts(products, activeFilters.filter(isCrackersShelfFilterId)),
};

export function getCrackersPageData(): ComparisonCategoryPageData {
  return {
    products: crackersProducts,
    metadataLine: crackersMetadataLine,
    hero: crackersHero,
    prologueSentences: crackersPrologueSentences,
    methodologyLines: crackersMethodologyLines,
    corpusMeta: crackersCorpusMeta,
    shelfFilters: crackersShelfFilters,
  };
}

export function getCrackersCorpusPayload(): {
  _meta: CrackersCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: crackersCorpusMeta,
    products: crackersProducts,
  };
}
