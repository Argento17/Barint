import type { BariProductVM } from "@/lib/view-models";

/** Shelf lens ids for the butter category. */
export type ButterShelfFilterId =
  | "plain"
  | "salted"
  | "cultured-fermented"
  | "ghee"
  | "grade-B"
  | "grade-C";

export interface ButterShelfLensOption {
  id: ButterShelfFilterId;
  label: string;
}

/** Internal corpus fields stripped before the VM reaches the UI. */
interface ButterCorpusProduct extends BariProductVM {
  subtype?: string;
}

export const BUTTER_SHELF_LENS_OPTIONS: ButterShelfLensOption[] = [
  { id: "plain", label: "חמאה רגילה" },
  { id: "salted", label: "חמאה מלוחה" },
  { id: "cultured-fermented", label: "חמאה מותססת" },
  { id: "ghee", label: "גהי" },
  { id: "grade-B", label: "ב" },
  { id: "grade-C", label: "ג" },
];

function productMatchesButterFilter(
  product: ButterCorpusProduct,
  filter: ButterShelfFilterId
): boolean {
  switch (filter) {
    case "plain":
      return product.subtype === "plain";
    case "salted":
      return product.subtype === "salted";
    case "cultured-fermented":
      return product.subtype === "cultured_fermented";
    case "ghee":
      return product.subtype === "ghee";
    case "grade-B":
      return product.grade === "B";
    case "grade-C":
      return product.grade === "C";
    default:
      return true;
  }
}

export function filterButterProducts(
  products: BariProductVM[],
  activeFilters: ButterShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.every((filter) =>
      productMatchesButterFilter(product as ButterCorpusProduct, filter)
    )
  );
}
