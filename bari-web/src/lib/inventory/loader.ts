/**
 * Bari Inventory Loader
 *
 * Cross-category rollup of the full Bari corpus. Driven entirely off the
 * comparison registry — adding a new registry category requires zero code changes
 * here (listComparisonCategoryIds() + getComparisonCategoryCorpusPayload()
 * do the work automatically).
 *
 * categoryNameHe comes from ComparisonCategoryDefinition.nameHe — the field that
 * lives on each category's own definition file. TypeScript enforces it is present
 * on every registered category, so no parallel name map is needed here.
 *
 * DISPLAY-ONLY: reads already-computed grade/score from corpus VMs.
 * Never recomputes, never reorders, never invents data.
 * Dedup unit = unique `id` within a category (the corpus already collapses
 * multi-chain variants for the same SKU).
 *
 * AUTH: none. This module has ZERO dependency on isAuthed / cookies / session.
 * Auth lives exclusively in the two route handlers under app/api/admin/inventory/.
 * This file is safe to import from a public Next.js Server Component.
 *
 * retailer resolution order (per orchestrator decision, 2026-07-01):
 *   1. per-product `retailer` field (raw JSON carries it as a string)
 *   2. _meta.retailer fallback
 *   3. CATEGORY_RETAILER_OVERRIDE — authoritative BSIP0-sourced category-level
 *      retailer for categories whose shipped JSON omits the retailer field.
 *      Snacks: all 21 products trace to retailer_id "shufersal" in the BSIP0
 *      artifact (bars_bsip0_raw_20260620T121703.json, 21/21 barcode match, one-shot
 *      verified 2026-07-01). This is deterministic, not fabricated.
 *   4. normalizeRetailer(raw) → canonical BariRetailerRefVM (→ "other" if unmatched)
 */

import {
  listComparisonCategoryIds,
  getComparisonCategory,
  getComparisonCategoryCorpusPayload,
} from "@/lib/comparisons/registry";
import type { ComparisonCategoryId } from "@/lib/comparisons/registry/types";
import type {
  BariGrade,
  BariProductVM,
  InventoryProductRowVM,
  InventorySummaryVM,
} from "@/lib/view-models";
import { normalizeRetailer } from "./retailer-map";

/**
 * Category-level retailer overrides sourced from authoritative BSIP0 artifacts.
 * Applied when the shipped frontend JSON carries no per-product or _meta.retailer.
 *
 * Snacks: bars_bsip0_raw_20260620T121703.json — all 120 raw products carry
 * retailer_id="shufersal" / retailer_name="שופרסל". Cross-checked against the 21
 * frontend barcodes: 21/21 matched to shufersal (0 unmatched). Verified 2026-07-01.
 * The frontend JSON never propagated this field — this override restores it.
 */
const CATEGORY_RETAILER_OVERRIDE: Partial<Record<ComparisonCategoryId, string>> = {
  snacks: "shufersal",
};

const ALL_GRADES: BariGrade[] = ["A", "B", "C", "D", "E"];

/** 5% threshold: if "other" share exceeds this, attach a _meta.warning. */
const OTHER_WARNING_THRESHOLD = 0.05;

/**
 * Build the full flat list of InventoryProductRowVM from the live registry.
 * Pure function — no auth, no I/O, no side effects.
 * Safe to call from public Server Components and auth-gated route handlers alike.
 */
export function buildInventoryRows(): InventoryProductRowVM[] {
  const rows: InventoryProductRowVM[] = [];

  for (const categoryId of listComparisonCategoryIds()) {
    const { _meta, products } = getComparisonCategoryCorpusPayload(categoryId);

    // nameHe and routePath come from the category definition — no separate map needed.
    const categoryDef = getComparisonCategory(categoryId);
    const nameHe = categoryDef.nameHe;
    // comparisonHref base: the registry routePath directly — never hardcode /hashvaot/{id}
    // so future categories with different paths stay correct automatically. The per-product
    // `?product={id}` is appended below; the comparison page already reads that param and
    // scrolls to + opens that exact product (initialExpandedProductId).
    const categoryRoute = categoryDef.routePath;

    // _meta.retailer is the category-level fallback for per-product absent retailer
    const metaAny = _meta as unknown as Record<string, unknown>;
    const metaRetailerRaw =
      typeof metaAny.retailer === "string" ? metaAny.retailer : null;

    // Category-level BSIP0-sourced override (applied when both per-product and meta are absent)
    const categoryOverride = CATEGORY_RETAILER_OVERRIDE[categoryId] ?? null;

    for (const product of products) {
      // Cast to access JSON fields that the VM type doesn't formally expose
      const raw = product as unknown as Record<string, unknown>;

      // Resolution order: per-product field → _meta.retailer → BSIP0 category override
      const perProductRetailerRaw =
        typeof raw.retailer === "string" ? raw.retailer : null;
      const retailerRaw =
        perProductRetailerRaw ?? metaRetailerRaw ?? categoryOverride;

      // Normalize to canonical BariRetailerRefVM
      const retailer = normalizeRetailer(retailerRaw);

      // sku = existing barcode field as string; null when absent
      const sku = raw.barcode != null ? String(raw.barcode) : null;

      rows.push({
        id: product.id,
        name: product.name,
        brand: product.brand ?? null,
        categoryId,
        categoryNameHe: nameHe,
        grade: product.grade ?? null,
        score: product.score ?? null,
        confidence: product.confidence,
        retailer,
        sku,
        imageUrl: product.imageUrl ?? null,
        comparisonHref: `${categoryRoute}?product=${encodeURIComponent(product.id)}`,
      });
    }
  }

  return rows;
}

/**
 * Build InventorySummaryVM from the full row set.
 * All arithmetic is derived from the same buildInventoryRows() call so every
 * count is guaranteed self-consistent.
 * Pure function — safe to call from public Server Components.
 */
export function buildInventorySummary(
  rows: InventoryProductRowVM[]
): InventorySummaryVM {
  const totalProducts = rows.length;
  const categoryIds = listComparisonCategoryIds();
  const categoryCount = categoryIds.length;

  // ── Retailer breakdown ────────────────────────────────────────────────────
  const retailerCountMap = new Map<
    string,
    { ref: { id: string; nameHe: string }; count: number }
  >();
  for (const row of rows) {
    const key = row.retailer.id;
    const existing = retailerCountMap.get(key);
    if (existing) {
      existing.count++;
    } else {
      retailerCountMap.set(key, {
        ref: { id: row.retailer.id, nameHe: row.retailer.nameHe },
        count: 1,
      });
    }
  }
  const retailerBreakdown = Array.from(retailerCountMap.values()).map((e) => ({
    id: e.ref.id,
    nameHe: e.ref.nameHe,
    count: e.count,
  }));

  // Guardrail: warn if "other" share > 5%
  const otherEntry = retailerCountMap.get("other");
  const otherCount = otherEntry?.count ?? 0;
  const otherShare = totalProducts > 0 ? otherCount / totalProducts : 0;

  // ── Grade distribution ────────────────────────────────────────────────────
  const gradeDistribution: Record<BariGrade, number> & { unscored: number } = {
    A: 0,
    B: 0,
    C: 0,
    D: 0,
    E: 0,
    unscored: 0,
  };
  for (const row of rows) {
    if (row.score === null || row.grade === null) {
      gradeDistribution.unscored++;
    } else {
      gradeDistribution[row.grade]++;
    }
  }

  // ── Top categories ────────────────────────────────────────────────────────
  // nameHe sourced from each category's own definition (via getComparisonCategory).
  const topCategories = categoryIds.map((categoryId) => {
    const catRows = rows.filter((r) => r.categoryId === categoryId);
    const count = catRows.length;
    const nameHe = getComparisonCategory(categoryId).nameHe;

    // dominantGrade = modal grade among scored products
    const gradeCounts = new Map<BariGrade, number>();
    for (const row of catRows) {
      if (row.grade !== null && row.score !== null) {
        gradeCounts.set(row.grade, (gradeCounts.get(row.grade) ?? 0) + 1);
      }
    }
    let dominantGrade: BariGrade | null = null;
    let maxGradeCount = 0;
    for (const grade of ALL_GRADES) {
      const c = gradeCounts.get(grade) ?? 0;
      if (c > maxGradeCount) {
        maxGradeCount = c;
        dominantGrade = grade;
      }
    }

    return { categoryId, nameHe, count, dominantGrade };
  });

  const metaWarning =
    otherShare > OTHER_WARNING_THRESHOLD
      ? `"other" retailer share is ${(otherShare * 100).toFixed(1)}% (${otherCount}/${totalProducts}), exceeding the 5% threshold — donut may be misleading`
      : undefined;

  return {
    generatedAt: new Date().toISOString(),
    totalProducts,
    categoryCount,
    retailerBreakdown,
    topCategories,
    gradeDistribution,
    ...(metaWarning ? { _meta: { warning: metaWarning } } : {}),
  };
}

/**
 * Build a Map<productId, BariProductVM> for the catalog's per-product expansion panel.
 *
 * Sources from the same getComparisonCategoryCorpusPayload used by buildInventoryRows,
 * so the detail set is guaranteed to match the 174 catalog rows exactly (same corpus,
 * same hummus curation, same normalizeProductBrandDisplay already applied by
 * loadComparisonCorpus inside each category's getCorpusPayload).
 *
 * Payload size (measured 2026-07-01): 464 KB serialized for the 6 registered categories
 * → safely under the 1.5 MB embed threshold → embedded in the page at render time.
 * Expansions render lazily on user interaction, so the data weight is acceptable.
 *
 * Pure function — no auth, no I/O. Safe to call from public Server Components.
 */
export function buildInventoryProductDetails(): Map<string, BariProductVM> {
  const map = new Map<string, BariProductVM>();

  for (const categoryId of listComparisonCategoryIds()) {
    const { products } = getComparisonCategoryCorpusPayload(categoryId);
    for (const product of products) {
      map.set(product.id, product);
    }
  }

  return map;
}

// ─── Barcode product index (TASK-471) ────────────────────────────────────────

/**
 * One entry in the barcode → product index that backs the canonical /p/[barcode]
 * page. Joins the flat row (which already carries `sku` = barcode, categoryNameHe,
 * comparisonHref, retailer) with the full BariProductVM detail (editorial fields,
 * nutrition, ingredients) by the shared product `id`.
 *
 * DISPLAY-ONLY: both halves are read verbatim from the existing corpus payload.
 * Nothing here recomputes, reorders, or rounds a score/grade/nutrition value.
 */
export interface BarcodeProductEntry {
  row: InventoryProductRowVM;
  detail: BariProductVM;
}

/**
 * Build a Map<barcode, BarcodeProductEntry> across the full live registry.
 *
 * Products with a null/absent barcode are excluded — they simply have no
 * canonical /p/ page (never fabricate a barcode to give them one).
 *
 * If two products across categories somehow share a barcode (not expected in the
 * live corpus — each category's barcodes are scoped to its own scrape), the last
 * one encountered wins; this mirrors the existing dedup-by-id behavior of
 * buildInventoryProductDetails and is a display-only tie-break, never a scoring one.
 *
 * Pure function — no auth, no I/O. Safe to call from generateStaticParams and
 * from the page Server Component alike.
 */
export function buildBarcodeProductIndex(): Map<string, BarcodeProductEntry> {
  const rows = buildInventoryRows();
  const details = buildInventoryProductDetails();
  const index = new Map<string, BarcodeProductEntry>();

  for (const row of rows) {
    if (!row.sku) continue; // no fabricated barcodes — skip products without one
    const detail = details.get(row.id);
    if (!detail) continue; // defensive: row without a matching detail VM
    index.set(row.sku, { row, detail });
  }

  return index;
}

/** Look up a single product by barcode. Returns null when not found (→ notFound()). */
export function getProductByBarcode(barcode: string): BarcodeProductEntry | null {
  return buildBarcodeProductIndex().get(barcode) ?? null;
}
