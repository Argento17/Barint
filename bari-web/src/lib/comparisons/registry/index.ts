import { breadCategoryDefinition } from "./categories/bread";
import { cerealsCategoryDefinition } from "./categories/breakfast-cereals";
import { granolaCategoryDefinition } from "./categories/granola";
import { cheeseCategoryDefinition } from "./categories/cheese";
import { hummusCategoryDefinition } from "./categories/hummus";
import { snacksCategoryDefinition } from "./categories/snacks";
import { crackersCategoryDefinition } from "./categories/crackers";
import { brinedCheesesCategoryDefinition } from "./categories/brined-cheeses";
import { cakesCategoryDefinition } from "./categories/cakes";
import { chocolateBarsCategoryDefinition } from "./categories/chocolate-bars";
import { chocolateTabletsCategoryDefinition } from "./categories/chocolate-tablets";
import { cookiesCoffeeCategoryDefinition } from "./categories/cookies-coffee";
import { hardCheesesCategoryDefinition } from "./categories/hard-cheeses";
import { juicesCategoryDefinition } from "./categories/juices";
import { milkCategoryDefinition } from "./categories/milk-comparison";
import { proteinBarsCategoryDefinition } from "./categories/protein-bars";
import { yogurtCategoryDefinition } from "./categories/yogurt";
import { yogurtDrinksCategoryDefinition } from "./categories/yogurt-drinks";
import type {
  ComparisonCategoryDefinition,
  ComparisonCategoryId,
  ComparisonCategoryPageData,
} from "./types";

const comparisonCategoryRegistry = {
  bread: breadCategoryDefinition,
  snacks: snacksCategoryDefinition,
  hummus: hummusCategoryDefinition,
  cheese: cheeseCategoryDefinition,
  "breakfast-cereals": cerealsCategoryDefinition,
  granola: granolaCategoryDefinition,
  crackers: crackersCategoryDefinition,
  "brined-cheeses": brinedCheesesCategoryDefinition,
  cakes: cakesCategoryDefinition,
  "chocolate-bars": chocolateBarsCategoryDefinition,
  "chocolate-tablets": chocolateTabletsCategoryDefinition,
  "cookies-coffee": cookiesCoffeeCategoryDefinition,
  "hard-cheeses": hardCheesesCategoryDefinition,
  juices: juicesCategoryDefinition,
  "milk-comparison": milkCategoryDefinition,
  "protein-bars": proteinBarsCategoryDefinition,
  yogurt: yogurtCategoryDefinition,
  "yogurt-drinks": yogurtDrinksCategoryDefinition,
} as const satisfies Record<ComparisonCategoryId, ComparisonCategoryDefinition>;

export type { ComparisonCategoryDefinition, ComparisonCategoryId, ComparisonCategoryPageData };
export type { ComparisonShelfFilters, ComparisonPageCopy } from "./types";
export type { ComparisonCorpusMeta } from "../corpus";

export const comparisonCategories = comparisonCategoryRegistry;

export function getComparisonCategory(
  id: ComparisonCategoryId
): ComparisonCategoryDefinition {
  return comparisonCategoryRegistry[id];
}

export function listComparisonCategoryIds(): ComparisonCategoryId[] {
  return Object.keys(comparisonCategoryRegistry) as ComparisonCategoryId[];
}

export function getComparisonCategoryPageData(
  id: ComparisonCategoryId
): ComparisonCategoryPageData {
  return getComparisonCategory(id).getPageData();
}

export function getComparisonCategoryCorpusPayload(id: ComparisonCategoryId) {
  return getComparisonCategory(id).getCorpusPayload();
}
