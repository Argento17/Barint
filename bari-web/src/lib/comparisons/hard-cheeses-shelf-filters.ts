import type { BariProductVM } from "@/lib/view-models";

/** Sub-pool filter ids for the hard-cheeses category (v2 corpus: Yohananof). */
export type HardCheesesShelfFilterId =
  | "yellow"
  | "yellow_light"
  | "hard_grating"
  | "processed";

export interface HardCheesesShelfLensOption {
  id: HardCheesesShelfFilterId;
  label: string;
}

/** Internal corpus fields stripped before the VM reaches the UI. */
interface HardCheesesCorpusProduct extends BariProductVM {
  subPool?: string;
}

export const HARD_CHEESES_SHELF_LENS_OPTIONS: HardCheesesShelfLensOption[] = [
  { id: "yellow", label: "גבינה צהובה" },
  { id: "yellow_light", label: "צהובה מופחת" },
  { id: "hard_grating", label: "גבינה קשה" },
  { id: "processed", label: "מעובדת" },
];

function productMatchesHardCheesesFilter(
  product: HardCheesesCorpusProduct,
  filter: HardCheesesShelfFilterId
): boolean {
  return product.subPool === filter;
}

export function filterHardCheesesProducts(
  products: BariProductVM[],
  activeFilters: HardCheesesShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.some((filter) =>
      productMatchesHardCheesesFilter(
        product as HardCheesesCorpusProduct,
        filter
      )
    )
  );
}
