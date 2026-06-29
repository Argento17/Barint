import type { BariProductVM } from "@/lib/view-models";

/**
 * Shelf lens ids for chocolate countline bars.
 * All products in this corpus are grade E — grade filter is uninformative.
 * Instead: sugar-band lenses (≤50g vs >50g per 100g) + a "real-food ingredient"
 * lens (nuts / peanuts present, visible in the product name on this corpus).
 */
export type ChocolateBarsShelfFilterId =
  | "sugar-low"
  | "sugar-high"
  | "has-real-food";

export interface ChocolateBarsShelfLensOption {
  id: ChocolateBarsShelfFilterId;
  label: string;
}

export const CHOCOLATE_BARS_SHELF_LENS_OPTIONS: ChocolateBarsShelfLensOption[] = [
  { id: "has-real-food", label: "אגוזים / בוטנים" },
  { id: "sugar-low", label: "פחות סוכר (≤50 גרם)" },
  { id: "sugar-high", label: "הרבה סוכר (>50 גרם)" },
];

/** Names containing nuts/peanuts — used as a proxy for "real food ingredient".
 *  The filter is conservative: it matches only if the product name contains one
 *  of the Hebrew keywords, which are the authoritative label on this shelf. */
const REAL_FOOD_KEYWORDS = ["בוטן", "אגוז", "שקד", "פיסטוק", "קשיו"];

function productMatchesChocolateBarsFilter(
  product: BariProductVM,
  filter: ChocolateBarsShelfFilterId
): boolean {
  switch (filter) {
    case "sugar-low": {
      const sugar = product.expansion?.nutrition?.sugar;
      return sugar !== null && sugar !== undefined && sugar <= 50;
    }
    case "sugar-high": {
      const sugar = product.expansion?.nutrition?.sugar;
      return sugar !== null && sugar !== undefined && sugar > 50;
    }
    case "has-real-food": {
      const name = product.name.toLowerCase();
      return REAL_FOOD_KEYWORDS.some((kw) => name.includes(kw));
    }
    default:
      return true;
  }
}

export function filterChocolateBarsProducts(
  products: BariProductVM[],
  activeFilters: ChocolateBarsShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.every((filter) => productMatchesChocolateBarsFilter(product, filter))
  );
}
