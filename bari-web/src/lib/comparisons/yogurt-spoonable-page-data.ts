import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/yogurt_spoonable_frontend_v1.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import type { BariConfidence, BariProductVM } from "@/lib/view-models";

// TASK-515B: spoonable-yogurt frontend wiring. Source: yogurt_spoonable_FINAL_v2.json
// (sha256 83590cb7a5a288d2e60ea466dcfc51aef163c52268761c5d1e501a77abcaf447) — 78 products,
// copy two-gate-signed (Content + Adversarial QA), run_gates PASS (G2/G3/G5 WARN-only —
// image coverage 74/78 and no --run trace dir to cross-check scores, not blockers).
// Mirrors yogurt-drinks-page-data.ts (same category system, same page_copy shape).
//
// Grades: this corpus carries 2 "S" products (92.6, 90.6) alongside A/B/C/D (no E).
// loadComparisonCorpus's normalizeGrade already folds the engine's 6-grade S≥90 into "A"
// (the frozen ScoreChip has no S slot — see corpus.ts frontendGradeFromScore) — both S
// products recompute to "A" here, which is correct, not a bug: neither product's copy
// mentions the letter S, so there is no copy/chip mismatch.
//
// Unit basis: every product's expansion.servingNote reads "ל-100 גרם" — per 100g, same
// basis as yogurt-drinks (NOT per 100ml like milk/juices).

export type YogurtSpoonableCorpusMeta = ComparisonCorpusMeta;

/**
 * Backend confidence values on this corpus are "full" | "partial" (same vocabulary as
 * yogurt-drinks). "full" maps to the VM's "verified" state per the view-models language
 * boundary (see the BariConfidence comment in @/lib/view-models). Anything unrecognised
 * degrades to "insufficient" rather than silently letting an invalid string reach the
 * confidence-driven UI (ConfidenceRing / ConfidenceDot in comparison-row.tsx).
 */
function normalizeConfidence(raw: unknown): BariConfidence {
  if (raw === "full") return "verified";
  if (raw === "partial") return "partial";
  if (raw === "verified" || raw === "insufficient") return raw;
  return "insufficient";
}

const _loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const yogurtSpoonableCorpusMeta = _loaded.meta;

const _rawProducts = (rawCorpus as unknown as { products: Array<{ confidence?: unknown }> })
  .products;

// Re-map confidence vocabulary + populate the metric column (protein/sugar per 100g —
// the headline tradeoff this shelf's prologue and caveat both discuss).
const yogurtSpoonableProducts: BariProductVM[] = _loaded.products.map((product, i) => ({
  ...product,
  confidence: normalizeConfidence(_rawProducts[i]?.confidence),
  metrics: {
    protein_g: product.expansion?.nutrition?.protein ?? null,
    sugar_g: product.expansion?.nutrition?.sugar ?? null,
  },
}));

export { yogurtSpoonableCorpusMeta, yogurtSpoonableProducts };

export const yogurtSpoonableMetadataLine = formatComparisonMetadataLine(
  yogurtSpoonableProducts.length,
  yogurtSpoonableCorpusMeta.generated
);

// page_copy shape (Content + Nutrition signed, TASK-515 FINAL) — matches yogurt-drinks'
// page_copy shape exactly (hero/prologue/methodology/caveat.notes[]); this category has
// no blog_link or shelf_lens_options.
interface YogurtSpoonablePageCopy {
  hero: { eyebrow: string; title: string; productCount: number; scoredCount: number };
  prologue: { sentences: string[] };
  methodology: { lines: string[] };
  caveat: { notes: Array<{ title: string; body: string }> };
}

const _pageCopy = (rawCorpus as unknown as { page_copy: YogurtSpoonablePageCopy }).page_copy;

export const yogurtSpoonableHero = {
  eyebrow: _pageCopy.hero.eyebrow,
  title: _pageCopy.hero.title,
} as const;

// prologue is { sentences: string[] } — spread directly into the array.
export const yogurtSpoonablePrologueSentences: readonly string[] = _pageCopy.prologue.sentences;

export const yogurtSpoonableMethodologyLines: readonly string[] = _pageCopy.methodology.lines;

// caveat is { notes: [{title, body}] } — join all notes as paragraphs (same shape as
// yogurt-drinks/milk).
export const yogurtSpoonableCategoryNote: string = _pageCopy.caveat.notes
  .map((n) => `${n.title}\n\n${n.body}`)
  .join("\n\n");

export const yogurtSpoonableComparisonMetadata: Metadata = {
  title: "השוואת יוגורטים לאכילה בכפית | Bari",
  description:
    'השוואת 78 יוגורטים לאכילה בכפית מהמדף הישראלי — ציון Bari, חלבון וסוכר ל-100 גרם, רכיבים ותוספים. מידע, לא המלצה.',
};

// No shelf filters for this category (page_copy carries no shelf_lens_options, and the
// task scope does not call for any). ComparisonPage's `shelfFilters` prop is required by
// its interface but filtering is globally hidden (FIX-5 in comparison-page.tsx — the
// active-filter set is always []), so a no-op pass-through satisfies the contract without
// inventing a filter surface that isn't in scope.
const yogurtSpoonableShelfFilters = {
  lensOptions: [],
  filterProducts: (products: BariProductVM[]) => products,
};

export function getYogurtSpoonablePageData(): ComparisonCategoryPageData {
  return {
    products: yogurtSpoonableProducts,
    metadataLine: yogurtSpoonableMetadataLine,
    hero: yogurtSpoonableHero,
    prologueSentences: yogurtSpoonablePrologueSentences,
    methodologyLines: yogurtSpoonableMethodologyLines,
    corpusMeta: yogurtSpoonableCorpusMeta,
    shelfFilters: yogurtSpoonableShelfFilters,
  };
}

export function getYogurtSpoonableCorpusPayload(): {
  _meta: YogurtSpoonableCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: yogurtSpoonableCorpusMeta,
    products: yogurtSpoonableProducts,
  };
}
