import type { BariProductVM } from "@/lib/view-models";

/**
 * Shelf lens ids for chocolate tablets. Grade-based (C/D/E spread exists on this corpus).
 * Same self-contained pattern as snacks/protein-bars — NO separate ghost module.
 */
export type ChocolateTabletsShelfFilterId = "grade-B" | "grade-C" | "grade-D" | "grade-E";

export interface ChocolateTabletsShelfLensOption {
  id: ChocolateTabletsShelfFilterId;
  label: string;
}

export const CHOCOLATE_TABLETS_SHELF_LENS_OPTIONS: ChocolateTabletsShelfLensOption[] = [
  { id: "grade-B", label: "ב" },
  { id: "grade-C", label: "ג" },
  { id: "grade-D", label: "ד" },
  { id: "grade-E", label: "ה" },
];

function productMatchesChocolateTabletsFilter(
  product: BariProductVM,
  filter: ChocolateTabletsShelfFilterId
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

export function filterChocolateTabletsProducts(
  products: BariProductVM[],
  activeFilters: ChocolateTabletsShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.every((filter) => productMatchesChocolateTabletsFilter(product, filter))
  );
}
