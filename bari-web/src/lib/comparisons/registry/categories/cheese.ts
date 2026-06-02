import type { ComparisonCategoryDefinition } from "../types";
import {
  getCheeseCorpusPayload,
  getCheesePageData,
  cheeseComparisonMetadata,
} from "../../cheese-comparison-page-data";

export const cheeseCategoryDefinition: ComparisonCategoryDefinition = {
  id: "cheese",
  routePath: "/hashvaot/cheese",
  metadata: cheeseComparisonMetadata,
  getPageData: getCheesePageData,
  getCorpusPayload: getCheeseCorpusPayload,
};
