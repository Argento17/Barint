import type { ComparisonCategoryDefinition } from "../types";
import {
  getYogurtDrinksCorpusPayload,
  getYogurtDrinksPageData,
  yogurtDrinksComparisonMetadata,
  yogurtDrinksHero,
} from "../../yogurt-drinks-page-data";

export const yogurtDrinksCategoryDefinition: ComparisonCategoryDefinition = {
  id: "yogurt-drinks",
  routePath: "/hashvaot/yogurt-drinks",
  nameHe: yogurtDrinksHero.eyebrow,
  metadata: yogurtDrinksComparisonMetadata,
  getPageData: getYogurtDrinksPageData,
  getCorpusPayload: getYogurtDrinksCorpusPayload,
};
