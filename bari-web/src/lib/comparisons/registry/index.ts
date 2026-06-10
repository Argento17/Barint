import { breadCategoryDefinition } from "./categories/bread";
import { butterCategoryDefinition } from "./categories/butter";
import { cerealsCategoryDefinition } from "./categories/breakfast-cereals";
import { granolaCategoryDefinition } from "./categories/granola";
import { cheeseCategoryDefinition } from "./categories/cheese";
import { hummusCategoryDefinition } from "./categories/hummus";
import { maadanimCategoryDefinition } from "./categories/maadanim";
import { saltySnacksCategoryDefinition } from "./categories/salty-snacks";
import { snacksCategoryDefinition } from "./categories/snacks";
import { vegetableSpreadsCategoryDefinition } from "./categories/vegetable-spreads";
import { yogurtsCategoryDefinition } from "./categories/yogurts";
import { frozenVegetablesCategoryDefinition } from "./categories/frozen-vegetables";
import type {
  ComparisonCategoryDefinition,
  ComparisonCategoryId,
  ComparisonCategoryPageData,
} from "./types";

const comparisonCategoryRegistry = {
  maadanim: maadanimCategoryDefinition,
  bread: breadCategoryDefinition,
  butter: butterCategoryDefinition,
  snacks: snacksCategoryDefinition,
  "salty-snacks": saltySnacksCategoryDefinition,
  yogurts: yogurtsCategoryDefinition,
  hummus: hummusCategoryDefinition,
  "vegetable-spreads": vegetableSpreadsCategoryDefinition,
  cheese: cheeseCategoryDefinition,
  "breakfast-cereals": cerealsCategoryDefinition,
  granola: granolaCategoryDefinition,
  "frozen-vegetables": frozenVegetablesCategoryDefinition,
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
