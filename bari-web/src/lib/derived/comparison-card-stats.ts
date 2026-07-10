// Shared build-time derivation for the /hashvaot featured intelligence cards (TASK-568).
//
// Replaces per-card hand-typed literals / per-card duplicated `.filter().length` and
// `Math.round(Math.max(...) - Math.min(...))` logic with ONE derivation used everywhere.
// Cards call this with the same `xProducts` / `xCorpusMeta` arrays the actual comparison
// page reads — there is no second data path to drift out of sync.
//
// PURE. No React import. No "use client". Never sorts/rounds in the JSX layer (per the
// view-model doctrine: "UI never rounds") — this module owns the rounding so callers just
// render `stats.scoreSpread` etc. verbatim.
//
// IMPORT RULE (do not violate — this keeps the module runnable by plain `node` in
// scripts/validate-card-stats.mjs with zero new dependencies):
//   - type-only imports from "@/..." aliases are fine (erased by Node's native TS
//     type-stripping; verified empirically — see derived_views_scoping_v1.md §4).
//   - VALUE imports must be relative (e.g. "../comparisons/..."), never "@/...", because
//     plain `node` does not understand the Next.js tsconfig path alias.

import type { BariGrade } from "@/lib/view-models";

// NOTE ON IMPORTS: this file intentionally has ZERO relative value-imports (only the
// type-only "@/lib/view-models" import above, which Node's native TS type-stripping
// erases entirely — verified empirically). That is what lets plain `node` execute this
// module directly with no path-alias resolution and no new devDependency, which is what
// scripts/validate-card-stats.mjs relies on. Two consequences of that constraint:
//   1. `formatComparisonUpdatedLine` below is a deliberate, small, frozen duplicate of
//      ../comparisons/format-comparison-updated-line.ts rather than an import of it — a
//      real relative import needs an explicit ".ts" extension to resolve under plain
//      Node's ESM loader (verified), and TypeScript rejects ".ts"-extension imports
//      unless `allowImportingTsExtensions` is enabled in tsconfig.json — a project-wide
//      compiler-option change this pilot should not make. If the canonical formatter's
//      date-bucket logic (≤7 days → "עודכן השבוע") ever changes, update both call sites.
//   2. Do not add another relative value-import to this file without re-verifying the
//      parity script still runs under plain `node` (see §4-§5 of
//      01_framework/frontend/derived_views_scoping_v1.md).
function formatComparisonUpdatedLine(generatedAt: string): string {
  const parsed = /^(\d{4})-(\d{2})-(\d{2})/.exec(generatedAt);
  if (!parsed) return "עודכן לאחרונה";
  const [, y, mo, d] = parsed;
  const gen = new Date(Number(y), Number(mo) - 1, Number(d));
  const now = new Date();
  const diffDays = Math.floor((now.getTime() - gen.getTime()) / (1000 * 60 * 60 * 24));
  if (diffDays >= 0 && diffDays <= 7) return "עודכן השבוע";
  const dateHe = `${d}.${mo}.${y}`;
  return `עודכן ב-${dateHe}`;
}

export type CardGradeLetter = BariGrade;

/** Minimal structural shape — satisfied by both `BariProductVM` and a raw parsed JSON
 *  product, so the same function runs against the loaded VM array a card imports AND
 *  against `JSON.parse`d raw corpus products in the parity script. */
export interface CardStatsProductInput {
  score: number | null;
  grade: CardGradeLetter | null;
}

export interface ComparisonCardStats {
  productCount: number;
  scoredCount: number;
  gradeCounts: Record<CardGradeLetter, number>;
  /** Best (lowest-letter) grade actually present among scored products; null if none scored. */
  ceilingGrade: CardGradeLetter | null;
  scoreLow: number | null;
  scoreHigh: number | null;
  /** high - low, already rounded to a whole point. */
  scoreSpread: number | null;
  updatedLabel: string;
}

const GRADE_ORDER: CardGradeLetter[] = ["A", "B", "C", "D", "E"];

export function deriveComparisonCardStats(
  products: readonly CardStatsProductInput[],
  generatedAt: string
): ComparisonCardStats {
  const gradeCounts: Record<CardGradeLetter, number> = { A: 0, B: 0, C: 0, D: 0, E: 0 };
  const scores: number[] = [];

  for (const product of products) {
    if (product.grade && Object.prototype.hasOwnProperty.call(gradeCounts, product.grade)) {
      gradeCounts[product.grade]++;
    }
    if (typeof product.score === "number") {
      scores.push(product.score);
    }
  }

  const ceilingGrade = GRADE_ORDER.find((grade) => gradeCounts[grade] > 0) ?? null;
  const scoreLow = scores.length ? Math.min(...scores) : null;
  const scoreHigh = scores.length ? Math.max(...scores) : null;
  const scoreSpread =
    scoreLow !== null && scoreHigh !== null ? Math.round(scoreHigh - scoreLow) : null;

  return {
    productCount: products.length,
    scoredCount: scores.length,
    gradeCounts,
    ceilingGrade,
    scoreLow,
    scoreHigh,
    scoreSpread,
    updatedLabel: formatComparisonUpdatedLine(generatedAt),
  };
}

/** Generic min/max helper for a single numeric per-product metric (e.g. protein g/100g).
 *  Returns null when no product carries a numeric value for the metric. */
export function deriveMetricRange(
  values: readonly (number | null | undefined)[]
): { low: number; high: number } | null {
  const numeric = values.filter((value): value is number => typeof value === "number");
  if (numeric.length === 0) return null;
  return { low: Math.min(...numeric), high: Math.max(...numeric) };
}
