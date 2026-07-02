import { breadCategoryDefinition } from "./categories/bread";
import { cerealsCategoryDefinition } from "./categories/breakfast-cereals";
import { granolaCategoryDefinition } from "./categories/granola";
import { cheeseCategoryDefinition } from "./categories/cheese";
import { hummusCategoryDefinition } from "./categories/hummus";
import { snacksCategoryDefinition } from "./categories/snacks";
import { crackersCategoryDefinition } from "./categories/crackers";
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
