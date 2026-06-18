import type { BariProductVM } from "@/lib/view-models";

/** Shared corpus metadata shape for v2 frontend JSON exports. */
export interface ComparisonCorpusMeta {
  generated: string;
  category: string;
  product_count: number;
  scored_count?: number;
  schema?: string;
  version?: string;
  expansion?: string;
  v2_changes?: Record<string, unknown>;
  production_pass?: string;
}

export type ComparisonCorpusProduct = BariProductVM & {
  _calibration?: unknown;
};

export interface ComparisonCorpusRaw<TMeta extends ComparisonCorpusMeta = ComparisonCorpusMeta> {
  _meta: TMeta;
  products: ComparisonCorpusProduct[];
}

export interface LoadedComparisonCorpus<TMeta extends ComparisonCorpusMeta = ComparisonCorpusMeta> {
  meta: TMeta;
  products: BariProductVM[];
}

export function stripInternalProductFields(
  products: ComparisonCorpusProduct[]
): BariProductVM[] {
  return products.map((product) => {
    const { _calibration, ...rest } = product;
    void _calibration;
    return rest;
  });
}

/**
 * Frontend grade is a pure function of the rounded score on the 5-grade consumer scale
 * (A 80+ · B 65–79 · C 50–64 · D 35–49 · E 0–34 — the engine's 6-grade S≥90 folds into A,
 * since the UI palette has no S). The only sanctioned deviation is the cheese A-ceiling,
 * marked per-product with `_aCappedToB` (a high-scoring product held at B because its
 * saturated fat is over the line the score itself can't see). Centralizing this here
 * removes the boundary drift that had crept into the frozen JSON exports (e.g. 65→C,
 * 50→D, 35→E) and prevents it from returning on the next regeneration. Null/undefined
 * scores (INSUFFICIENT products) keep whatever grade the export carried.
 */
function frontendGradeFromScore(score: number): BariProductVM["grade"] {
  if (score >= 80) return "A";
  if (score >= 65) return "B";
  if (score >= 50) return "C";
  if (score >= 35) return "D";
  return "E";
}

function normalizeGrade(product: ComparisonCorpusProduct): BariProductVM["grade"] {
  if (typeof product.score !== "number") return product.grade;
  if ((product as { _aCappedToB?: boolean })._aCappedToB) return "B";
  return frontendGradeFromScore(product.score);
}

export function loadComparisonCorpus<TMeta extends ComparisonCorpusMeta>(
  raw: ComparisonCorpusRaw<TMeta>
): LoadedComparisonCorpus<TMeta> {
  return {
    meta: raw._meta,
    products: stripInternalProductFields(raw.products).map((product, i) => ({
      ...product,
      grade: normalizeGrade(raw.products[i]),
    })),
  };
}

export function formatComparisonMetadataLine(
  productCount: number,
  generatedIso: string
): string {
  const date = new Date(generatedIso);
  const monthYear = Number.isNaN(date.getTime())
    ? ""
    : date.toLocaleDateString("he-IL", { month: "long", year: "numeric" });
  const updated = monthYear ? `עודכן ב${monthYear}` : "עודכן לאחרונה";
  return `${productCount} מוצרים • ${updated}`;
}
