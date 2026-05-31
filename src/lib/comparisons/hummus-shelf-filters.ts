import rawCorpus from "@/data/comparisons/hummus_frontend_v3.json";

import type { BariProductVM } from "@/lib/view-models";

export type HummusShelfFilterId = "hummus" | "matbucha" | "spreads";

export const HUMMUS_SHELF_LENS_OPTIONS: Array<{
  id: HummusShelfFilterId;
  label: string;
}> = [
  { id: "hummus", label: "חומוס" },
  { id: "matbucha", label: "מטבוחה" },
  { id: "spreads", label: "ממרחים אחרים" },
];

type HummusCorpusProduct = BariProductVM & { _product_type?: string };

const SPREADS_TYPES = new Set(["eggplant_spread", "pepper_spread", "masabacha"]);

const hummusProductTypeById = new Map<string, HummusShelfFilterId>(
  (rawCorpus.products as HummusCorpusProduct[])
    .filter((p) => p._product_type != null)
    .map((p) => {
      const pt = p._product_type!;
      let filterId: HummusShelfFilterId;
      if (pt === "hummus_spread") {
        filterId = "hummus";
      } else if (pt === "matbucha") {
        filterId = "matbucha";
      } else {
        filterId = "spreads";
      }
      return [p.id, filterId];
    })
);

export function filterHummusProducts(
  products: BariProductVM[],
  activeFilters: HummusShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;

  return products.filter((product) => {
    const filterId = hummusProductTypeById.get(product.id);
    return filterId != null && activeFilters.includes(filterId);
  });
}

void SPREADS_TYPES;
