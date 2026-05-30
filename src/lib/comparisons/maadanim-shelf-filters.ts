import type { BariProductVM } from "@/lib/view-models";

/** Shelf lens ids — temporary until BariCategoryPageVM owns category filters. */
export type MaadanimShelfFilterId =
  | "less-sweet"
  | "relatively-high-protein"
  | "short-ingredient-list";

export interface MaadanimShelfLensOption {
  id: MaadanimShelfFilterId;
  label: string;
}

/** Visual filter chips for מעדנים — not yet driven by BariCategoryPageVM.filters. */
export const MAADANIM_SHELF_LENS_OPTIONS: MaadanimShelfLensOption[] = [
  { id: "less-sweet", label: "פחות מתוק" },
  { id: "relatively-high-protein", label: "חלבון גבוה יחסית" },
  { id: "short-ingredient-list", label: "רשימת רכיבים קצרה" },
];

function hasShortIngredientList(ingredients: string | null): boolean {
  if (!ingredients) return false;
  const parts = ingredients
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
  return parts.length > 0 && parts.length <= 6;
}

function productMatchesShelfFilter(
  product: BariProductVM,
  filter: MaadanimShelfFilterId
): boolean {
  const nutrition = product.expansion.nutrition;
  if (filter === "less-sweet") {
    return (nutrition?.sugar ?? Number.POSITIVE_INFINITY) <= 10;
  }

  if (filter === "relatively-high-protein") {
    return (nutrition?.protein ?? -1) >= 8;
  }

  return hasShortIngredientList(product.expansion.ingredients);
}

export function filterMaadanimProducts(
  products: BariProductVM[],
  activeFilters: MaadanimShelfFilterId[]
): BariProductVM[] {
  if (activeFilters.length === 0) return products;
  return products.filter((product) =>
    activeFilters.every((filter) => productMatchesShelfFilter(product, filter))
  );
}
