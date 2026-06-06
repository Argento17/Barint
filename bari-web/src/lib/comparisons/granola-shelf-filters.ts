import type { BariProductVM } from "@/lib/view-models";

/** Shelf lens ids for the granola category. */
export type GranolaShelfFilterId =
  | "whole-grain"
  | "grade-B"
  | "grade-C"
  | "grade-D";

export interface GranolaShelfLensOption {
  id: GranolaShelfFilterId;
  label: string;
}

/** Internal corpus fields stripped before the VM reaches the UI. */
interface GranolaCorpusProduct extends BariProductVM {
  _wholeGrainClaim?: boolean;
}

export const GRANOLA_SHELF_LENS_OPTIONS: GranolaShelfLensOption[] = [
  { id: "whole-grain", label: "מוצרי דגנים מלאים" },
  { id: "grade-B", label: "ב" },
  { id: "grade-C", label: "ג" },
  { id: "grade-D", label: "ד" },
];

function productMatchesGranolaFilter(
  product: GranolaCorpusProduct,
  filter: GranolaShelfFilterId
): boolean {
  switch (filter) {
    case "whole-grain":
      return product._wholeGrainClaim === true;
    case "grade-B":
      return product.grade === "B";
    case "grade-C":
      return product.grade === "C";
    case "grade-D":
      return product.grade === "D";
    default:
      return true;
  }
}

export function filterGranolaProducts(
  products: BariProductVM[],
  activeFilters: GranolaShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.every((filter) =>
      productMatchesGranolaFilter(product as GranolaCorpusProduct, filter)
    )
  );
}
