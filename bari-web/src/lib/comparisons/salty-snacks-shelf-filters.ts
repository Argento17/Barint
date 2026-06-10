import type { BariProductVM } from "@/lib/view-models";

/** Sub-pool filter ids for the salty-snacks category. */
export type SaltySnacksShelfFilterId =
  | "chips"
  | "popcorn"
  | "puffed"
  | "baked"
  | "rice_cakes"
  | "pretzels";

export interface SaltySnacksShelfLensOption {
  id: SaltySnacksShelfFilterId;
  label: string;
}

/** Internal corpus fields stripped before the VM reaches the UI. */
interface SaltySnacksCorpusProduct extends BariProductVM {
  subPool?: string;
}

export const SALTY_SNACKS_SHELF_LENS_OPTIONS: SaltySnacksShelfLensOption[] = [
  { id: "chips", label: "צ'יפס" },
  { id: "popcorn", label: "פופקורן" },
  { id: "puffed", label: "פצפוצים" },
  { id: "baked", label: "אפוי" },
  { id: "rice_cakes", label: "פצפוצי אורז" },
  { id: "pretzels", label: "פרצלים" },
];

function productMatchesSaltySnacksFilter(
  product: SaltySnacksCorpusProduct,
  filter: SaltySnacksShelfFilterId
): boolean {
  return product.subPool === filter;
}

export function filterSaltySnacksProducts(
  products: BariProductVM[],
  activeFilters: SaltySnacksShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.some((filter) =>
      productMatchesSaltySnacksFilter(
        product as SaltySnacksCorpusProduct,
        filter
      )
    )
  );
}
