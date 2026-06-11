import type { BariProductVM } from "@/lib/view-models";

export type FrozenVegetablesShelfFilterId = "plain-veg" | "legumes" | "mixes" | "pasta-blends" | "processed" | "herbs-seasonings";

export const FROZEN_VEGETABLES_SHELF_LENS_OPTIONS = [
  { id: "plain-veg" as const, label: "ירקות בודדים" },
  { id: "legumes" as const, label: "קטניות" },
  { id: "mixes" as const, label: "תערובות" },
  { id: "pasta-blends" as const, label: "עם פסטה" },
  { id: "processed" as const, label: "מעובד" },
  { id: "herbs-seasonings" as const, label: "תבלינים וממרחים" },
];

export function filterFrozenVegetablesProducts(
  products: BariProductVM[],
  activeFilters: FrozenVegetablesShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((p) => {
    const cluster = (p as { _cluster?: string })._cluster;
    return cluster && activeFilters.includes(cluster as FrozenVegetablesShelfFilterId);
  });
}
