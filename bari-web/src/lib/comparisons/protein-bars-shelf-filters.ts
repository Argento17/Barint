import type { BariProductVM } from "@/lib/view-models";

/**
 * Shelf lens ids for protein bars. Grade-based, read DIRECTLY off the live corpus
 * (same self-contained pattern as snacks/cereals) — NO separate ghost module.
 */
export type ProteinBarsShelfFilterId = "grade-B" | "grade-C" | "grade-D" | "grade-E";

export interface ProteinBarsShelfLensOption {
  id: ProteinBarsShelfFilterId;
  label: string;
}

export const PROTEIN_BARS_SHELF_LENS_OPTIONS: ProteinBarsShelfLensOption[] = [
  { id: "grade-B", label: "ב" },
  { id: "grade-C", label: "ג" },
  { id: "grade-D", label: "ד" },
  { id: "grade-E", label: "ה" },
];

function productMatchesProteinBarsFilter(
  product: BariProductVM,
  filter: ProteinBarsShelfFilterId
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

export function filterProteinBarsProducts(
  products: BariProductVM[],
  activeFilters: ProteinBarsShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.every((filter) => productMatchesProteinBarsFilter(product, filter))
  );
}
