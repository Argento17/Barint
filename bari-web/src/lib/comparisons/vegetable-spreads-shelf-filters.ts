import rawCorpus from "@/data/comparisons/hummus_frontend_v4.json";

import type { BariProductVM } from "@/lib/view-models";

export type VegetableSpreadsShelfFilterId = "matbucha" | "eggplant" | "pepper";

export const VEGETABLE_SPREADS_SHELF_LENS_OPTIONS: Array<{
  id: VegetableSpreadsShelfFilterId;
  label: string;
}> = [
  { id: "matbucha", label: "מטבוחה" },
  { id: "eggplant", label: "ממרח חצילים" },
  { id: "pepper", label: "ממרח פלפלים" },
];

type VegetableSpreadsCorpusProduct = BariProductVM & { _product_type?: string };

const vegetableSpreadTypeById = new Map<string, VegetableSpreadsShelfFilterId>(
  (rawCorpus.products as VegetableSpreadsCorpusProduct[])
    .filter((p) => p._product_type != null)
    .flatMap((p) => {
      const pt = p._product_type!;
      let filterId: VegetableSpreadsShelfFilterId | null = null;
      if (pt === "matbucha") filterId = "matbucha";
      else if (pt === "eggplant_spread") filterId = "eggplant";
      else if (pt === "pepper_spread") filterId = "pepper";
      return filterId != null ? [[p.id, filterId] as [string, VegetableSpreadsShelfFilterId]] : [];
    })
);

export function filterVegetableSpreadsProducts(
  products: BariProductVM[],
  activeFilters: VegetableSpreadsShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;

  return products.filter((product) => {
    const filterId = vegetableSpreadTypeById.get(product.id);
    return filterId != null && activeFilters.includes(filterId);
  });
}
