import rawCorpus from "@/data/comparisons/cheese_frontend_v2.json";

import type { BariProductVM } from "@/lib/view-models";

// Shelf lenses = the four cheese-spread sub-pools (run_cheese_003). `_cluster`
// carries the sub-pool on each product; the lens filter narrows the list to a
// pool without re-sorting (Invariant 1). Score-band dividers are derived from
// `score` by the table itself — the sub-pool is the lens, not the divider.
export type CheeseShelfFilterId =
  | "cottage"
  | "white-cheese-quark"
  | "cream-cheese-spread"
  | "labaneh";

export const CHEESE_SHELF_LENS_OPTIONS: Array<{
  id: CheeseShelfFilterId;
  label: string;
}> = [
  { id: "cottage", label: "קוטג'" },
  { id: "white-cheese-quark", label: "גבינה לבנה / קוורק" },
  { id: "cream-cheese-spread", label: "גבינת שמנת / ממרח" },
  { id: "labaneh", label: "לבנה" },
];

type CheeseCorpusProduct = BariProductVM & { _cluster?: CheeseShelfFilterId };

const cheeseClusterByProductId = new Map<string, CheeseShelfFilterId>(
  (rawCorpus.products as CheeseCorpusProduct[])
    .filter((product) => product._cluster != null)
    .map((product) => [product.id, product._cluster!])
);

export function filterCheeseProducts(
  products: BariProductVM[],
  activeFilters: CheeseShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;

  return products.filter((product) => {
    const cluster = cheeseClusterByProductId.get(product.id);
    return cluster != null && activeFilters.includes(cluster);
  });
}
