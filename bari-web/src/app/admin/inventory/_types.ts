/**
 * Inventory Dashboard VM types — re-exported from @/lib/view-models.
 * The Data agent landed BariRetailerRefVM, InventoryProductRowVM,
 * and InventorySummaryVM in the canonical view-models index (2026-07-01).
 * Local mirrors deleted — single source of truth is @/lib/view-models.
 */

export type {
  BariGrade,
  BariConfidence,
  BariRetailerRefVM,
  InventoryProductRowVM,
  InventorySummaryVM,
} from "@/lib/view-models";

/** Paginated products response shape (matches /api/admin/inventory/products). */
export interface InventoryProductsResponseVM {
  rows: import("@/lib/view-models").InventoryProductRowVM[];
  total: number;
  page: number;
}
