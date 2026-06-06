import type { BariProductVM } from "@/lib/view-models";

/** Shelf lens ids for breakfast-cereals. */
export type CerealsShelfFilterId =
  | "granola"
  | "standard"
  | "whole-grain"
  | "grade-B"
  | "grade-C"
  | "grade-D"
  | "childrens";

export interface CerealsShelfLensOption {
  id: CerealsShelfFilterId;
  label: string;
}

/** Internal corpus fields stripped before the VM reaches the UI. */
interface CerealsCorpusProduct extends BariProductVM {
  _subpool?: string;
  _isChildrens?: boolean;
  _wholeGrainClaim?: boolean;
}

/** Visual filter chips for דגני בוקר. Labels verbatim from cereals_editorial_v1.json. */
// Granola was split into its own category (TASK-140, owner 2026-06-05), so the
// pool dimension (granola / standard) is gone — every product here is a standard cereal.
export const CEREALS_SHELF_LENS_OPTIONS: CerealsShelfLensOption[] = [
  // whole-grain dimension
  { id: "whole-grain", label: "מוצרי דגנים מלאים" },
  // grade dimension
  { id: "grade-B", label: "ב" },
  { id: "grade-C", label: "ג" },
  { id: "grade-D", label: "ד" },
  // childrens dimension
  { id: "childrens", label: "מוצרים לילדים" },
];

function productMatchesCerealsFilter(
  product: CerealsCorpusProduct,
  filter: CerealsShelfFilterId
): boolean {
  switch (filter) {
    case "granola":
      return product._subpool === "granola";
    case "standard":
      return product._subpool === "standard_cereal";
    case "whole-grain":
      return product._wholeGrainClaim === true;
    case "grade-B":
      return product.grade === "B";
    case "grade-C":
      return product.grade === "C";
    case "grade-D":
      return product.grade === "D";
    case "childrens":
      return product._isChildrens === true;
    default:
      return true;
  }
}

export function filterCerealsProducts(
  products: BariProductVM[],
  activeFilters: CerealsShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.every((filter) =>
      productMatchesCerealsFilter(product as CerealsCorpusProduct, filter)
    )
  );
}
