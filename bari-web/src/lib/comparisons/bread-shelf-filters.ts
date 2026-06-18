import curated from "@/data/bread-retail-curated.json";

import { BREAD_CLUSTER_FILTERS } from "@/lib/comparisons/bread-page-data";
import type { BariProductVM } from "@/lib/view-models";

/** CE-approved cluster ids from bread-page-data (excludes "all"). */
export type BreadShelfFilterId = Exclude<
  (typeof BREAD_CLUSTER_FILTERS)[number]["id"],
  "all"
>;

export const BREAD_SHELF_LENS_OPTIONS = BREAD_CLUSTER_FILTERS.filter(
  (filter): filter is { id: BreadShelfFilterId; label: string } =>
    filter.id !== "all"
);

const breadClusterByProductId = new Map(
  curated.all_products.map((product) => [product.product_id, product.website_cluster] as const)
);

export function filterBreadProducts(
  products: BariProductVM[],
  activeFilters: BreadShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;

  return products.filter((product) => {
    const cluster = breadClusterByProductId.get(product.id);
    return cluster != null && activeFilters.includes(cluster as BreadShelfFilterId);
  });
}
