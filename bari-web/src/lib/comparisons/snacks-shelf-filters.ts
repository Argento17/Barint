import type { BariProductVM } from "@/lib/view-models";

/**
 * Shelf lens ids for snack bars. Grade-based, read DIRECTLY off the live corpus
 * (the same self-contained pattern as cereals-shelf-filters) — NO dependency on
 * any separate snack-page-data / snack-types ghost module. TASK-362: the old
 * filters matched live products by id into a retired 19-product yochananof corpus,
 * which silently dropped 7 products and mismatched the rest. Killed.
 */
export type SnacksShelfFilterId = "grade-B" | "grade-C" | "grade-D" | "grade-E";

export interface SnacksShelfLensOption {
  id: SnacksShelfFilterId;
  label: string;
}

/** Visual filter chips for חטיפי דגנים. Grade dimension only — every chip maps to
 *  a grade that actually exists on the live shelf. */
export const SNACKS_SHELF_LENS_OPTIONS: SnacksShelfLensOption[] = [
  { id: "grade-B", label: "ב" },
  { id: "grade-C", label: "ג" },
  { id: "grade-D", label: "ד" },
  { id: "grade-E", label: "ה" },
];

function productMatchesSnacksFilter(
  product: BariProductVM,
  filter: SnacksShelfFilterId
): boolean {
  switch (filter) {
    case "grade-B":
      return product.grade === "B";
    case "grade-C":
      return product.grade === "C";
    case "grade-D":
      return product.grade === "D";
    case "grade-E":
      return product.grade === "E";
    default:
      return true;
  }
}

export function filterSnacksProducts(
  products: BariProductVM[],
  activeFilters: SnacksShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.every((filter) => productMatchesSnacksFilter(product, filter))
  );
}
