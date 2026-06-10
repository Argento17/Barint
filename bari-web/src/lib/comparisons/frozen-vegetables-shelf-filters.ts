import rawCorpus from "@/data/comparisons/frozen_vegetables_frontend_v1.json";

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

// `_cluster` carries each product's shelf sub-pool, but the page data loader strips
// it from the runtime VM (it is an internal field). So we read it eagerly from the raw
// JSON at module init — keyed by product id — and look it up at filter time. Reading it
// off the passed-in (already-stripped) products would make every lens return zero
// products. Mirrors the cheese-shelf-filters pattern.
type FrozenVegetablesCorpusProduct = BariProductVM & {
  _cluster?: FrozenVegetablesShelfFilterId;
};

const frozenVegetablesClusterByProductId = new Map<string, FrozenVegetablesShelfFilterId>(
  (rawCorpus.products as FrozenVegetablesCorpusProduct[])
    .filter((product) => product._cluster != null)
    .map((product) => [product.id, product._cluster!])
);

export function filterFrozenVegetablesProducts(
  products: BariProductVM[],
  activeFilters: FrozenVegetablesShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) => {
    const cluster = frozenVegetablesClusterByProductId.get(product.id);
    return cluster != null && activeFilters.includes(cluster);
  });
}
