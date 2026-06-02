import { breadCategoryDefinition } from "./categories/bread";
import { cheeseCategoryDefinition } from "./categories/cheese";
import { hummusCategoryDefinition } from "./categories/hummus";
import { maadanimCategoryDefinition } from "./categories/maadanim";
import { snacksCategoryDefinition } from "./categories/snacks";
import { vegetableSpreadsCategoryDefinition } from "./categories/vegetable-spreads";
import { yogurtsCategoryDefinition } from "./categories/yogurts";
import type {
  ComparisonCategoryDefinition,
  ComparisonCategoryId,
  ComparisonCategoryPageData,
} from "./types";

const comparisonCategoryRegistry = {
  maadanim: maadanimCategoryDefinition,
  bread: breadCategoryDefinition,
  snacks: snacksCategoryDefinition,
  yogurts: yogurtsCategoryDefinition,
  hummus: hummusCategoryDefinition,
  "vegetable-spreads": vegetableSpreadsCategoryDefinition,
  cheese: cheeseCategoryDefinition,
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
