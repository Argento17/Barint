import rawCorpus from "@/data/comparisons/yogurts_frontend_v4.json";

import type { BariProductVM } from "@/lib/view-models";

// "dairy-free" retired with the v2 swap (TASK-143): run_yogurt_004 contains zero plant-base
// yogurts (soy/coconut deferred to a dedicated plant run per the 3a ruling), so the lens has
// no members. Restore it when a plant pool ships.
// "bio" added in TASK-249 (run_yogurt_006): Bio Natural and related bio/probiotic products
// now have sufficient corpus representation to warrant a dedicated shelf lens.
export type YogurtsShelfFilterId =
  | "plain"
  | "greek"
  | "high-protein"
  | "flavored"
  | "bio";

export const YOGURTS_SHELF_LENS_OPTIONS: Array<{
  id: YogurtsShelfFilterId;
  label: string;
}> = [
  { id: "plain", label: "טבעי/נטורל" },
  { id: "greek", label: "יווני/מסוי" },
  { id: "high-protein", label: "עתיר חלבון" },
  { id: "flavored", label: "בטעמים" },
  { id: "bio", label: "ביו/פרוביוטי" },
];

type YogurtsCorpusProduct = BariProductVM & { _cluster?: YogurtsShelfFilterId };

const yogurtsClusterByProductId = new Map<string, YogurtsShelfFilterId>(
  (rawCorpus.products as YogurtsCorpusProduct[])
    .filter((product) => product._cluster != null)
    .map((product) => [product.id, product._cluster!])
);

export function filterYogurtsProducts(
  products: BariProductVM[],
  activeFilters: YogurtsShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;

  return products.filter((product) => {
    const cluster = yogurtsClusterByProductId.get(product.id);
    return cluster != null && activeFilters.includes(cluster);
  });
}
