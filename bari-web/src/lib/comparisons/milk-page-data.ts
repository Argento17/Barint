/**
 * TASK-321 Wave 3 — uniform milk loader (milk-page-data.ts rewrite).
 *
 * This file serves two cohorts:
 *  1. LEGACY consumers (blog, home-flagship, dimension-bars, bari-grade-badge, …) — the
 *     original exports kept 100% unchanged so those files compile without modification.
 *  2. NEW uniform route consumers (milk-comparison-page.tsx, milk-comparison/page.tsx,
 *     featured-milk-intelligence-card.tsx) — BariProductVM[] exports driven by the
 *     uniform milk_frontend_v1.json corpus.
 *
 * `milkProducts` stays typed as MilkComparisonProduct[] to avoid breaking
 * src/lib/blog/milk-analysis-content.ts and milk-analysis-chart-data.ts, which are
 * out of scope for this structural conform (task instruction: "leave [blog] untouched").
 * New route consumers use `milkVmProducts: BariProductVM[]` instead.
 */

import type { Metadata } from "next";

import { withComparisonOpenGraph } from "@/lib/seo/open-graph";

// ─── Legacy imports ────────────────────────────────────────────────────────────
import rawPage from "@/data/milk-comparison.json";
import { formatGram } from "@/lib/format/numbers";
import type {
  ComparisonFilterId,
  MilkComparisonPageData,
  MilkComparisonProduct,
} from "@/lib/comparisons/milk-types";

// ─── Uniform-corpus imports ────────────────────────────────────────────────────
import rawCorpus from "@/data/comparisons/milk_frontend_v1.json";
import {
  formatComparisonMetadataLine,
  loadComparisonCorpus,
  type ComparisonCorpusMeta,
  type ComparisonCorpusRaw,
} from "@/lib/comparisons/corpus";
import type { ComparisonCategoryPageData } from "@/lib/comparisons/registry/types";
import type { BariProductVM } from "@/lib/view-models";

// ═══════════════════════════════════════════════════════════════════════════════
// LEGACY BLOCK — preserved verbatim for blog / home-flagship / dimension-bars
// ═══════════════════════════════════════════════════════════════════════════════

export const milkComparisonPage = rawPage as MilkComparisonPageData;

export const milkProducts: MilkComparisonProduct[] = milkComparisonPage.products;

export const GRADE_COLORS: Record<
  string,
  { bg: string; text: string; border: string }
> = {
  A: { bg: "#2E7D32", text: "#FFFFFF", border: "#2E7D3215" },
  B: { bg: "#558B2F", text: "#FFFFFF", border: "#558B2F15" },
  C: { bg: "#F9A825", text: "#111318", border: "#F9A82520" },
  D: { bg: "#EF6C00", text: "#FFFFFF", border: "#EF6C0020" },
  E: { bg: "#C62828", text: "#FFFFFF", border: "#C6282820" },
};

export const DEGRADATION_LABELS: Record<string, string> = {
  minimal: "פירוק מבני מינימלי",
  low: "פירוק מבני נמוך",
  moderate: "פירוק מבני בינוני",
  high: "פירוק מבני גבוה",
  severe: "פירוק מבני חמור",
  extreme: "פירוק מבני קיצוני",
};

export const PRIMARY_DIMENSION_KEYS = [
  "processing_quality",
  "nutrient_density",
  "protein_quality",
  "additive_quality",
  "fat_quality",
  "glycemic_quality",
  "whole_food_integrity",
] as const;

export const comparisonFilters: {
  id: ComparisonFilterId;
  label: string;
  group: "type" | "trait";
}[] = [
  { id: "type:dairy", label: "חלב פרה", group: "type" },
  { id: "type:oat", label: "שיבולת שועל", group: "type" },
  { id: "type:soy", label: "סויה", group: "type" },
  { id: "type:almond", label: "שקדים", group: "type" },
  { id: "type:rice", label: "אורז", group: "type" },
  { id: "no_additives", label: "ללא תוספים", group: "trait" },
  { id: "high_protein", label: "חלבון גבוה", group: "trait" },
  { id: "low_sugar", label: "פחות סוכר", group: "trait" },
  { id: "coffee", label: "הכי מתאים לקפה", group: "trait" },
  { id: "high_score", label: "ציון Bari הגבוה", group: "trait" },
];

export const howToReadComparison = [
  "הציון משקף מבנה, רכיבים, תרומה תזונתית והקשר קטגוריאלי — בהשוואה למוצרים דומים.",
  "חלבון גבוה משרת מטרה אחת; פשטות רכיבים משרתת אחרת. בחרו לפי השימוש שלכם.",
  "למה קיבל את הציון? מפרק תרומה, טריידאופים והשוואה לעמיתים באותה משפחה.",
  "פירוט לפי היבטים זמין למי שרוצה עומק — אפשר להבין את העיקר גם בלי להיכנס לשם.",
] as const;

export function formatNutrient(value: number | null, unit = " ג׳"): string {
  return formatGram(value, unit);
}

export function productMatchesFilters(
  product: MilkComparisonProduct,
  active: Set<ComparisonFilterId>
): boolean {
  if (active.size === 0) return true;

  const typeFilters = [...active].filter((f) => f.startsWith("type:"));
  const traitFilters = [...active].filter((f) => !f.startsWith("type:"));

  if (typeFilters.length > 0) {
    const typeMatch = typeFilters.some((f) => product.filterTags.includes(f));
    if (!typeMatch) return false;
  }

  for (const trait of traitFilters) {
    if (!product.filterTags.includes(trait)) return false;
  }

  return true;
}

export function getRowEmphasis(
  product: MilkComparisonProduct,
  active: Set<ComparisonFilterId>
): "emphasized" | "muted" | "neutral" {
  if (active.size === 0) return "neutral";
  return productMatchesFilters(product, active) ? "emphasized" : "muted";
}

export function countVisible(active: Set<ComparisonFilterId>): number {
  return milkProducts.filter((p) => productMatchesFilters(p, active)).length;
}

// ═══════════════════════════════════════════════════════════════════════════════
// UNIFORM VM BLOCK — new, driven by milk_frontend_v1.json
// ═══════════════════════════════════════════════════════════════════════════════

export type MilkCorpusMeta = ComparisonCorpusMeta;

// milk page_copy shape (differs from yogurt):
//   hero:              { eyebrow, title, productCount, scoredCount }
//   prologue:          { sentences: string[] }         ← dict, NOT a plain string
//   methodology:       { lines: string[] }
//   caveat:            { notes: Array<{title, body}> } ← multi-note array, NOT {title, body}
//   blog_link:         { href, label }
//   shelf_lens_options: Array<{id, label, group}>
type MilkCorpusRaw = typeof rawCorpus & {
  page_copy: {
    hero: { eyebrow: string; title: string; productCount: number; scoredCount: number };
    prologue: { sentences: string[] };
    methodology: { lines: string[] };
    caveat: { notes: Array<{ title: string; body: string }> };
    blog_link: { href: string; label: string };
    shelf_lens_options: Array<{ id: string; label: string; group: string }>;
  };
};

const _typedRaw = rawCorpus as MilkCorpusRaw;
const _pageCopy = _typedRaw.page_copy;

const { meta: milkCorpusMeta, products: _milkVmProductsRaw } =
  loadComparisonCorpus(rawCorpus as ComparisonCorpusRaw);

export { milkCorpusMeta };

export const milkVmProducts: BariProductVM[] = _milkVmProductsRaw.map((p) => ({
  ...p,
  imageUrl: p.imageUrl ?? null,
  d4_additives: p.d4_additives ?? [],
  metrics: {
    protein_g: p.expansion?.nutrition?.protein ?? null,
    sugar_g: p.expansion?.nutrition?.sugar ?? null,
  },
}));

export const milkMetadataLine = formatComparisonMetadataLine(
  milkVmProducts.length,
  milkCorpusMeta.generated
);

export const milkHero = {
  eyebrow: _pageCopy.hero.eyebrow,
  title: _pageCopy.hero.title,
} as const;

// prologue is { sentences: string[] } — spread directly into the array.
export const milkPrologueSentences: readonly string[] = _pageCopy.prologue.sentences;

export const milkMethodologyLines: readonly string[] = _pageCopy.methodology.lines;

// caveat is { notes: [{title, body}] } — join all notes as paragraphs.
export const milkCategoryNote: string = _pageCopy.caveat.notes
  .map((n) => `${n.title}\n\n${n.body}`)
  .join("\n\n");

export const milkBlogLink = {
  href: _pageCopy.blog_link.href,
  label: _pageCopy.blog_link.label,
} as const;

export const milkComparisonMetadata: Metadata = withComparisonOpenGraph({
  title: "השוואת חלב ואלטרנטיבות | Bari",
  description:
    `השוואת ${milkVmProducts.length} מוצרי חלב ותחליפים ממדפי סופרים — ציון Bari, חלבון, סוכר, תוספים. מידע, לא המלצה.`,
});

// ─── Shelf filters ─────────────────────────────────────────────────────────────
// 10 lens options from page_copy.shelf_lens_options.
// type:* filters are OR'd within the group; trait filters are AND'd.
// Filter key: filterTags[] on each product in the corpus (copied verbatim into the VM).

export type MilkFilterId = string;

const MILK_LENS_OPTIONS: Array<{ id: MilkFilterId; label: string }> =
  _pageCopy.shelf_lens_options.map((opt) => ({ id: opt.id, label: opt.label }));

// Build a filterTags lookup keyed by product id (e.g. "milk_7290000051352").
const FILTER_TAGS_BY_VM_ID = new Map<string, string[]>(
  (rawCorpus.products as Array<{ id: string; filterTags?: string[] }>).map((p) => [
    p.id,
    p.filterTags ?? [],
  ])
);

function filterMilkVmProducts(
  products: BariProductVM[],
  activeFilters: MilkFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;

  const typeFilters = activeFilters.filter((f) => f.startsWith("type:"));
  const traitFilters = activeFilters.filter((f) => !f.startsWith("type:"));

  return products.filter((product) => {
    const tags = FILTER_TAGS_BY_VM_ID.get(product.id) ?? [];
    if (typeFilters.length > 0 && !typeFilters.some((f) => tags.includes(f))) {
      return false;
    }
    return traitFilters.every((trait) => tags.includes(trait));
  });
}

export const milkShelfFilters = {
  lensOptions: MILK_LENS_OPTIONS,
  filterProducts: filterMilkVmProducts,
};

export function getMilkPageData(): ComparisonCategoryPageData<MilkFilterId> {
  return {
    products: milkVmProducts,
    metadataLine: milkMetadataLine,
    hero: milkHero,
    prologueSentences: milkPrologueSentences,
    methodologyLines: milkMethodologyLines,
    corpusMeta: milkCorpusMeta,
    shelfFilters: milkShelfFilters,
  };
}

export function getMilkCorpusPayload(): {
  _meta: MilkCorpusMeta;
  products: BariProductVM[];
} {
  return {
    _meta: milkCorpusMeta,
    products: milkVmProducts,
  };
}
