import type { BariProductVM } from "@/lib/view-models";

// TASK-100: hummus page shows only hummus_spread and masabacha.
// Vegetable spreads (matbucha, eggplant_spread, pepper_spread) are on /hashvaot/vegetable-spreads.
// No sub-lenses needed — all remaining products are legume-based.
export type HummusShelfFilterId = "hummus";

export const HUMMUS_SHELF_LENS_OPTIONS: Array<{
  id: HummusShelfFilterId;
  label: string;
}> = [
  { id: "hummus", label: "חומוס" },
];

export function filterHummusProducts(
  products: BariProductVM[],
  activeFilters: HummusShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products;
}
