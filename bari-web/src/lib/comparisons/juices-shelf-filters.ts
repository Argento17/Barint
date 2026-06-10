import type { BariProductVM } from "@/lib/view-models";

/** Sub-pool filter ids for the juices category. */
export type JuicesShelfFilterId =
  | "juice_100"
  | "nectar"
  | "fruit_drink"
  | "smoothie"
  | "cold_pressed";

export interface JuicesShelfLensOption {
  id: JuicesShelfFilterId;
  label: string;
}

/** Internal corpus fields stripped before the VM reaches the UI. */
interface JuicesCorpusProduct extends BariProductVM {
  subPool?: string;
}

export const JUICES_SHELF_LENS_OPTIONS: JuicesShelfLensOption[] = [
  { id: "juice_100", label: "מיץ 100%" },
  { id: "nectar", label: "נקטר" },
  { id: "smoothie", label: "סמות'י" },
  { id: "cold_pressed", label: "סחוט קר" },
  { id: "fruit_drink", label: "משקה פירות" },
];

function productMatchesJuicesFilter(
  product: JuicesCorpusProduct,
  filter: JuicesShelfFilterId
): boolean {
  return product.subPool === filter;
}

export function filterJuicesProducts(
  products: BariProductVM[],
  activeFilters: JuicesShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.some((filter) =>
      productMatchesJuicesFilter(product as JuicesCorpusProduct, filter)
    )
  );
}
