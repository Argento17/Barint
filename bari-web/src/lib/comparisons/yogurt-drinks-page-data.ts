import type { Metadata } from "next";

import rawCorpus from "@/data/comparisons/yogurt_drinkable_frontend_v1.json";

import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import type { BariConfidence, BariProductVM } from "@/lib/view-models";

// TASK-515A FINAL: drinkable-yogurt frontend wiring. Source: yogurt_drinkable_FINAL_v3.json
// (sha256 ba5f7a10dbc626c61dcc916ce2d444cca6254812c1d0303e41ba8b4b6bb21ea5) — 20 products
// (23-product FINAL_v2 corpus minus 3 exclusions: dedup-drop 6664655 + 2 missing-data
// discards, see _meta.exclusions in the frontend JSON), copy two-gate-signed
// (Content + Adversarial QA), run_gates + validate_comparison_page both PASS. Includes
// the first live E-grade product on any Bari shelf (barcode 55329). The product shape is
// already near-identical to BariProductVM (camelCase nutrition,
// expansion.consumerExplanation, bariInterpretation v2 shape) so this loader stays thin:
// loadComparisonCorpus handles the generic pass-through + grade recompute (verified a
// no-op for this corpus — recomputed grade matches the signed grade on all 20 products),
// and this file only fixes the one real mismatch (confidence vocabulary) plus adds the
// display-only metric column.
//
// Unit basis: every product's expansion.servingNote reads "ל-100 גרם" — this corpus is
// measured per 100g, NOT per 100ml like milk/juices (see yogurt-drinks-comparison-page.tsx
// metric spec comment).

export type YogurtDrinksCorpusMeta = ComparisonCorpusMeta;

/**
 * Backend confidence values on this corpus are "full" | "partial" (never "insufficient" —
 * all 20 products carry usable nutrition/ingredient data). "full" maps to the VM's
 * "verified" state per the view-models language boundary (see the BariConfidence comment
 * in @/lib/view-models). Anything unrecognised degrades to "insufficient" rather than
 * silently letting an invalid string reach the confidence-driven UI (ConfidenceRing /
 * ConfidenceDot in comparison-row.tsx, which branch on `=== "verified"` / `"partial"`).
 */
function normalizeConfidence(raw: unknown): BariConfidence {
  if (raw === "full") return "verified";
  if (raw === "partial") return "partial";
  if (raw === "verified" || raw === "insufficient") return raw;
  return "insufficient";
}

const _loaded = loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);
const yogurtDrinksCorpusMeta = _loaded.meta;

const _rawProducts = (rawCorpus as unknown as { products: Array<{ confidence?: unknown }> })
  .products;

// Re-map confidence vocabulary + populate the metric column (protein/sugar per 100g —
// the headline tradeoff the page_copy prologue and caveat both discuss).
const yogurtDrinksProducts: BariProductVM[] = _loaded.products.map((product, i) => ({
  ...product,
  confidence: normalizeConfidence(_rawProducts[i]?.confidence),
  metrics: {
    protein_g: product.expansion?.nutrition?.protein ?? null,
    sugar_g: product.expansion?.nutrition?.sugar ?? null,
  },
}));

export { yogurtDrinksCorpusMeta, yogurtDrinksProducts };

export const yogurtDrinksMetadataLine = formatComparisonMetadataLine(
  yogurtDrinksProducts.length,
  yogurtDrinksCorpusMeta.generated
);

// page_copy shape (Content + Nutrition signed, TASK-515A FINAL) — matches milk's
// page_copy shape exactly (hero/prologue/methodology/caveat.notes[]); this category has
// no blog_link or shelf_lens_options.
interface YogurtDrinksPageCopy {
  hero: { eyebrow: string; title: string; productCount: number; scoredCount: number };
  prologue: { sentences: string[] };
  methodology: { lines: string[] };
  caveat: { notes: Array<{ title: string; body: string }> };
}

const _pageCopy = (rawCorpus as unknown as { page_copy: YogurtDrinksPageCopy }).page_copy;

export const yogurtDrinksHero = {
  eyebrow: _pageCopy.hero.eyebrow,
  title: _pageCopy.hero.title,
} as const;

// prologue is { sentences: string[] } — spread directly into the array.
export const yogurtDrinksPrologueSentences: readonly string[] = _pageCopy.prologue.sentences;

export const yogurtDrinksMethodologyLines: readonly string[] = _pageCopy.methodology.lines;

// caveat is { notes: [{title, body}] } — join all notes as paragraphs (same shape as milk).
export const yogurtDrinksCategoryNote: string = _pageCopy.caveat.notes
  .map((n) => `${n.title}\n\n${n.body}`)
  .join("\n\n");

export const yogurtDrinksComparisonMetadata: Metadata = {
  title: "השוואת משקאות יוגורט | Bari",
  description:
    'השוואת 20 משקאות יוגורט מהמדף הישראלי — ציון Bari, חלבון וסוכר ל-100 גרם, רכיבים ותוספים. מידע, לא המלצה.',
};

// No shelf filters for this category (page_copy carries no shelf_lens_options, and the
// task scope does not call for any). ComparisonPage's `shelfFilters` prop is required by
// its interface but filtering is globally hidden (FIX-5 in comparison-page.tsx — the
// active-filter set is always []), so a no-op pass-through satisfies the contract without
// inventing a filter surface that isn't in scope.
const yogurtDrinksShelfFilters = {
  lensOptions: [],
  filterProducts: (products: BariProductVM[]) => products,
};

export function getYogurtDrinksPageData(): ComparisonCategoryPageData {
  return {
    products: yogurtDrinksProducts,
    metadataLine: yogurtDrinksMetadataLine,
    hero: yogurtDrinksHero,
    prologueSentences: yogurtDrinksPrologueSentences,
    methodologyLines: yogurtDrinksMethodologyLines,
    corpusMeta: yogurtDrinksCorpusMeta,
    shelfFilters: yogurtDrinksShelfFilters,
  };
}

export function getYogurtDrinksCorpusPayload(): {
  _meta: YogurtDrinksCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: yogurtDrinksCorpusMeta,
    products: yogurtDrinksProducts,
  };
}
