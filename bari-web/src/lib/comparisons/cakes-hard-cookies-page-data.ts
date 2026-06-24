import rawCorpus from "@/data/comparisons/cakes_hard_cookies_frontend_v1.json";

import {
  formatComparisonMetadataLine,
  type ComparisonCorpusMeta,
} from "@/lib/comparisons/corpus";
import type { BariProductVM, BariNutritionVM, BariConfidence } from "@/lib/view-models";

// ─── Types for the raw JSON shape ─────────────────────────────────────────────

interface CakesRawNutrition {
  energy_kcal?: number | null;
  fat_g?: number | null;
  saturated_fat_g?: number | null;
  carbs_g?: number | null;
  sugar_g?: number | null;
  protein_g?: number | null;
  sodium_mg?: number | null;
  fiber_g?: number | null;
}

interface CakesRawProduct {
  id: string;
  name: string;
  brand?: string | null;
  barcode?: string;
  imageUrl?: string | null;
  score: number | null;
  grade: BariProductVM["grade"];
  confidence: number | string;
  confidence_label_he?: string;
  confidence_tooltip_he?: string;
  confidence_sub_reason?: string | null;
  insightLine?: string;
  rowVerdict?: string;
  expansion: {
    nutrition: CakesRawNutrition | null;
    ingredients: string | null;
    confidenceLabel: string;
    servingNote: string;
    positiveSignals?: string[];
    limitingFactors?: string[];
    bottomLine?: string;
  };
  d4_additives?: BariProductVM["d4_additives"];
  _has_phvo?: boolean;
  _source_retailers?: string[];
}

// page_copy shape from JSON
interface CakesPageCopy {
  hero: { title: string; tagline: string; productCount: number; scoredCount: number };
  prologue: { sentences: string[] };
  methodology: { body: string };
  caveat: { title: string; body: string };
  filters: Array<{ id: string; label_he: string; count: number; description_he?: string }>;
}

type CakesRawCorpus = {
  _meta: ComparisonCorpusMeta & {
    generated: string;
    product_count: number;
  };
  page_copy: CakesPageCopy;
  products: CakesRawProduct[];
};

// ─── Normalizers ──────────────────────────────────────────────────────────────

/** Map numeric confidence score → BariConfidence enum */
function normalizeConfidence(raw: number | string): BariConfidence {
  if (typeof raw === "string") {
    if (raw === "verified" || raw === "partial" || raw === "insufficient") return raw;
    return "partial";
  }
  if (raw >= 0.9) return "verified";
  if (raw >= 0.5) return "partial";
  return "insufficient";
}

/** Map snake_case nutrition fields to VM camelCase */
function normalizeNutrition(raw: CakesRawNutrition | null): BariNutritionVM | null {
  if (!raw) return null;
  return {
    energyKcal: raw.energy_kcal ?? null,
    fat: raw.fat_g ?? null,
    satFat: raw.saturated_fat_g ?? null,
    sugar: raw.sugar_g ?? null,
    protein: raw.protein_g ?? null,
    sodium: raw.sodium_mg ?? null,
    fiber: raw.fiber_g ?? null,
  };
}

// ─── Load corpus ──────────────────────────────────────────────────────────────

const _typedRaw = rawCorpus as unknown as CakesRawCorpus;
const _pageCopy = _typedRaw.page_copy;

export const cakesHardCookiesCorpusMeta: ComparisonCorpusMeta = {
  generated: _typedRaw._meta.generated,
  category: "cakes-hard-cookies",
  product_count: _typedRaw._meta.product_count,
};

export const cakesHardCookiesProducts: BariProductVM[] = _typedRaw.products.map(
  (p): BariProductVM => {
    const rawNutrition = p.expansion?.nutrition as CakesRawNutrition | null;
    return {
      id: p.id,
      name: p.name,
      brand: p.brand ?? null,
      imageUrl: p.imageUrl ?? null,
      score: p.score,
      grade: p.grade,
      insightLine: p.insightLine ?? "",
      rowVerdict: p.rowVerdict,
      confidence: normalizeConfidence(p.confidence),
      confidence_label_he: p.confidence_label_he,
      confidence_tooltip_he: p.confidence_tooltip_he,
      confidence_sub_reason: p.confidence_sub_reason ?? null,
      d4_additives: p.d4_additives ?? [],
      expansion: {
        nutrition: normalizeNutrition(rawNutrition),
        ingredients: p.expansion?.ingredients ?? null,
        confidenceLabel: p.expansion?.confidenceLabel ?? "",
        servingNote: p.expansion?.servingNote ?? "הנתונים מחושבים לפי 100 גרם מוצר.",
        positiveSignals: p.expansion?.positiveSignals ?? [],
        limitingFactors: p.expansion?.limitingFactors ?? [],
        bottomLine: p.expansion?.bottomLine,
      },
      // sugar is the headline metric for cakes (thesis: sugar + sat-fat)
      metrics: {
        protein_g: null,
        sugar_g: rawNutrition?.sugar_g ?? null,
      },
    };
  }
);

export const cakesHardCookiesMetadataLine = formatComparisonMetadataLine(
  cakesHardCookiesProducts.length,
  cakesHardCookiesCorpusMeta.generated
);

// ── Shell strings — sourced from JSON page_copy (single source of truth) ──────

export const cakesHardCookiesHero = {
  eyebrow: _pageCopy.hero.title,
  title: _pageCopy.hero.tagline,
} as const;

export const cakesHardCookiesPrologueSentences: readonly string[] =
  _pageCopy.prologue.sentences;

export const cakesHardCookiesMethodologyLines: readonly string[] = [
  _pageCopy.methodology.body,
];

export const cakesHardCookiesCategoryNote =
  `${_pageCopy.caveat.title}\n\n${_pageCopy.caveat.body}`;

// ── Serializable lens options — filter IDs + Hebrew labels only (no functions) ─
// The actual filter logic lives in the Client Component (cakes-hard-cookies-comparison-page.tsx).
export type CakesFilterId = "all" | "least_bad" | "has_phvo" | "no_phvo" | "high_sugar";

export const cakesHardCookiesLensOptions: Array<{ id: CakesFilterId; label: string }> =
  _pageCopy.filters
    .filter((f) => f.id !== "all")
    .map((f) => ({ id: f.id as CakesFilterId, label: f.label_he }));

// ── Precomputed id sets — passed as serializable string arrays to the Client Component ──

/** Product ids that contain partially-hydrogenated vegetable oil */
export const cakesHardCookiesPhvoIds: string[] = _typedRaw.products
  .filter((p) => p._has_phvo === true)
  .map((p) => p.id);

/** Product ids with sugar >= 30g/100g */
export const cakesHardCookiesHighSugarIds: string[] = _typedRaw.products
  .filter((p) => {
    const s = (p.expansion?.nutrition as CakesRawNutrition)?.sugar_g;
    return typeof s === "number" && s >= 30;
  })
  .map((p) => p.id);

export function getCakesHardCookiesCorpusPayload(): {
  _meta: ComparisonCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: cakesHardCookiesCorpusMeta,
    products: cakesHardCookiesProducts,
  };
}
