import type { BariProductVM } from "@/lib/view-models";
import { comparisonFilters, milkProducts } from "@/lib/comparisons/milk-page-data";
import type { ComparisonFilterId } from "@/lib/comparisons/milk-types";

// Milk folds onto the shared ComparisonShelfFilters contract (IMP-3). The bespoke milk
// page kept non-matching rows visible-but-dimmed; the unified table FILTERS them out like
// every other category (corpus order preserved by the source array). type:* lenses are
// OR'd within the type group; trait lenses are AND'd — mirrors the original
// productMatchesFilters logic, but keyed by VM id so the universal VM stays clean.
export type MilkShelfFilterId = ComparisonFilterId;

export const MILK_SHELF_LENS_OPTIONS: Array<{ id: MilkShelfFilterId; label: string }> =
  comparisonFilters.map((f) => ({ id: f.id, label: f.label }));

// id ← barcode (see milk-comparison-page-data). Captured once at module load.
const FILTER_TAGS_BY_ID = new Map<string, string[]>(
  milkProducts.map((p) => [p.barcode, p.filterTags])
);

export function filterMilkProducts(
  products: BariProductVM[],
  activeFilters: MilkShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;

  const typeFilters = activeFilters.filter((f) => f.startsWith("type:"));
  const traitFilters = activeFilters.filter((f) => !f.startsWith("type:"));

  return products.filter((product) => {
    const tags = FILTER_TAGS_BY_ID.get(product.id) ?? [];
    if (typeFilters.length > 0 && !typeFilters.some((f) => tags.includes(f))) {
      return false;
    }
    return traitFilters.every((trait) => tags.includes(trait));
  });
}
