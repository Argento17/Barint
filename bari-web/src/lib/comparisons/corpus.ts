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
  // Internal fields some categories carry on the raw JSON. Declared loosely so the
  // loader can index them; none of these survive stripInternalProductFields except
  // the explicitly allowlisted lens/split fields below.
  [key: string]: unknown;
};

export interface ComparisonCorpusRaw<TMeta extends ComparisonCorpusMeta = ComparisonCorpusMeta> {
  _meta: TMeta;
  products: ComparisonCorpusProduct[];
}

export interface LoadedComparisonCorpus<TMeta extends ComparisonCorpusMeta = ComparisonCorpusMeta> {
  meta: TMeta;
  products: BariProductVM[];
}

// ─── Field allowlist (TASK-233A) ────────────────────────────────────────────────
// The loader emits ONLY the keys below. Everything else on the raw product —
// source_traceability_status, _cluster, _subpool (where unused), _internal_cluster,
// novaGroup, _calibration, _aCappedToB, barcode, retailer, retailer_he, brand,
// provenance, confidence_level, trace blobs, etc. — is dropped at load time, for ALL
// categories. This is the cross-category fix for the source_traceability_status leak
// (shipped in 10/13 categories) and the internal-vocabulary leak generally.

/** Public consumer-facing fields — every key declared on BariProductVM. */
const BARI_VM_KEYS: readonly string[] = [
  "id",
  "name",
  "imageUrl",
  "score",
  "grade",
  "insightLine",
  "confidence",
  "confidence_label_he",
  "confidence_tooltip_he",
  "confidence_sub_reason",
  "expansion",
  "metrics",
  "rowReason",
  "rowVerdict",
  "glassBox",
  "d4_additives",
  "d3_processing",
];

// Internal fields that are NOT part of BariProductVM but are read off the LOADED
// product (not the raw JSON) by a category's shelf-lens or corpus-split logic. These
// MUST survive the strip or those lenses/splits return zero. They are never rendered
// in any JSX string — they only drive client-side filtering. Categories reading these:
//   _subpool / _isChildrens / _wholeGrainClaim → cereals (granola uses _wholeGrainClaim)
//   subtype                                    → butter
//   subPool                                    → salty-snacks, hard-cheeses
//   _product_type                              → hummus / vegetable-spreads corpus split
// (Cluster-style fields like _cluster / _internal_cluster / website_cluster are read off
//  the RAW JSON by their lenses, so they are correctly dropped here.)
const LENS_INTERNAL_KEYS: readonly string[] = [
  "_subpool",
  "_isChildrens",
  "_wholeGrainClaim",
  "subtype",
  "subPool",
  "_product_type",
];

const ALLOWED_PRODUCT_KEYS: ReadonlySet<string> = new Set([
  ...BARI_VM_KEYS,
  ...LENS_INTERNAL_KEYS,
]);

const VALID_GRADES: ReadonlySet<string> = new Set(["A", "B", "C", "D", "E"]);

/**
 * Lightweight runtime conformance check (TASK-233A). BariProductVM is a compile-time
 * type only; the imported JSON is `any` at the trust boundary. This asserts the shape
 * the UI depends on actually holds at runtime. Surfaces loudly (throw in dev, console
 * error in prod) so a malformed regenerated export cannot pass silently.
 */
function assertProductConforms(product: ComparisonCorpusProduct, index: number): void {
  const errors: string[] = [];
  if (typeof product.id !== "string" || product.id.length === 0) errors.push("missing 'id'");
  if (typeof product.name !== "string" || product.name.length === 0) errors.push("missing 'name'");
  if (typeof product.confidence !== "string") errors.push("missing 'confidence'");
  if (product.expansion == null || typeof product.expansion !== "object") {
    errors.push("missing 'expansion'");
  }
  if (
    product.score != null &&
    !(typeof product.score === "number" && Number.isInteger(product.score))
  ) {
    errors.push(`'score' must be an integer or null (got ${JSON.stringify(product.score)})`);
  }
  if (product.grade != null && !VALID_GRADES.has(product.grade as string)) {
    errors.push(`'grade' must be A–E or null (got ${JSON.stringify(product.grade)})`);
  }

  if (errors.length > 0) {
    const id = typeof product.id === "string" ? product.id : `index ${index}`;
    const message = `[corpus] VM conformance violation on product ${id}: ${errors.join("; ")}`;
    if (process.env.NODE_ENV !== "production") {
      throw new Error(message);
    }
    // Production: surface, do not crash the page.
    console.error(message);
  }
}

export function stripInternalProductFields(
  products: ComparisonCorpusProduct[]
): BariProductVM[] {
  return products.map((product, index) => {
    assertProductConforms(product, index);
    const emitted: Record<string, unknown> = {};
    for (const key of Object.keys(product)) {
      if (ALLOWED_PRODUCT_KEYS.has(key)) {
        emitted[key] = (product as Record<string, unknown>)[key];
      }
    }
    return emitted as unknown as BariProductVM;
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
