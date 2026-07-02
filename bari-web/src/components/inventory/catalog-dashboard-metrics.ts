/**
 * Pure dashboard metric helpers for /catalog — derived live from row data at render time.
 * NO loader/registry imports; consumed by client components only.
 */

import type { BariGrade, InventoryProductRowVM } from "@/lib/view-models";

const GRADED_KEYS: BariGrade[] = ["A", "B", "C", "D", "E"];

export type CatalogGradeDistribution = Record<BariGrade, number> & { unscored: number };

export interface CatalogDashboardMetrics {
  totalProducts: number;
  categoryCount: number;
  gradeDistribution: CatalogGradeDistribution;
  verifiedCount: number;
  fullDataPercent: number;
}

/** Mirrors buildInventorySummary grade bucketing — keeps KPI counts self-consistent. */
export function computeCatalogDashboardMetrics(
  rows: InventoryProductRowVM[],
): CatalogDashboardMetrics {
  const categoryIds = new Set<string>();
  const gradeDistribution: CatalogGradeDistribution = {
    A: 0,
    B: 0,
    C: 0,
    D: 0,
    E: 0,
    unscored: 0,
  };
  let verifiedCount = 0;

  for (const row of rows) {
    categoryIds.add(row.categoryId);
    if (row.score === null || row.grade === null) {
      gradeDistribution.unscored++;
    } else {
      gradeDistribution[row.grade]++;
    }
    if (row.confidence === "verified") verifiedCount++;
  }

  const totalProducts = rows.length;
  const fullDataPercent =
    totalProducts > 0 ? Math.round((verifiedCount / totalProducts) * 100) : 0;

  return {
    totalProducts,
    categoryCount: categoryIds.size,
    gradeDistribution,
    verifiedCount,
    fullDataPercent,
  };
}

export { GRADED_KEYS };
