import type { BariProductVM } from "@/lib/view-models";

/**
 * Shelf lens ids for chocolate countline bars.
 * All products in this corpus are grade E — grade filter is uninformative.
 * Instead: sugar-band lenses (≤50g vs >50g per 100g) + a "real-food ingredient"
 * lens (nuts / peanuts present in the product's ingredients, per the scraped
 * ingredients list — not just the name; e.g. Snickers has no nut word in its
 * name but lists peanuts as its third ingredient).
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

/** Nut/peanut keywords — used to detect "real food ingredient" presence.
 *  Stems (not full singular words) so both singular and plural Hebrew forms
 *  match as substrings: Hebrew plurals replace a word-final letter (e.g. "ן")
 *  with a medial letter + suffix (e.g. "ן" -> "נים"), so the full singular
 *  word "בוטן" is never a substring of its own plural "בוטנים". Using the
 *  stem "בוטנ" matches both. */
const REAL_FOOD_KEYWORDS = ["בוטנ", "אגוז", "שקד", "פיסטוק", "קשיו"];

/** Checks both the product name and its scraped ingredients list — the name
 *  alone silently misses products where the nut/peanut content is a named
 *  ingredient but not part of the marketing name (e.g. Snickers: "בוטנים" is
 *  the third listed ingredient, but "בוטנים" never appears in the name). */
function containsRealFoodKeyword(text: string | null | undefined): boolean {
  if (!text) return false;
  const lower = text.toLowerCase();
  return REAL_FOOD_KEYWORDS.some((kw) => lower.includes(kw));
}

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
      return (
        containsRealFoodKeyword(product.name) ||
        containsRealFoodKeyword(product.expansion?.ingredients)
      );
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
