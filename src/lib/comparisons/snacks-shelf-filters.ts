import {
  SNACK_FILTERS,
  snackMatchesFilter,
  snackProducts,
} from "@/lib/comparisons/snack-page-data";
import type { SnackFilterId } from "@/lib/comparisons/snack-types";
import type { BariProductVM } from "@/lib/view-models";

/** CE-approved lens ids for shelf display (excludes all and insufficient). */
export type SnacksShelfFilterId = Exclude<SnackFilterId, "all" | "insufficient">;

export const SNACKS_SHELF_LENS_OPTIONS = SNACK_FILTERS.filter(
  (filter): filter is { id: SnacksShelfFilterId; label: string } =>
    filter.id !== "all" && filter.id !== "insufficient"
);

const snackByProductId = new Map(snackProducts.map((product) => [product.id, product]));

export function filterSnacksProducts(
  products: BariProductVM[],
  activeFilters: SnacksShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;

  return products.filter((product) => {
    const snack = snackByProductId.get(product.id);
    if (!snack || !snack.displayable) return false;
    return activeFilters.every((filterId) => snackMatchesFilter(snack, filterId));
  });
}
