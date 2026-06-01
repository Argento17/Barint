import rawCorpus from "@/data/comparisons/yogurts_frontend_v1.json";

import type { BariProductVM } from "@/lib/view-models";

export type YogurtsShelfFilterId =
  | "plain"
  | "greek"
  | "dairy-free"
  | "high-protein"
  | "flavored";

export const YOGURTS_SHELF_LENS_OPTIONS: Array<{
  id: YogurtsShelfFilterId;
  label: string;
}> = [
  { id: "plain", label: "טבעי/נטורל" },
  { id: "greek", label: "יווני/מסוי" },
  { id: "dairy-free", label: "ללא חלב" },
  { id: "high-protein", label: "עתיר חלבון" },
  { id: "flavored", label: "בטעמים" },
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
