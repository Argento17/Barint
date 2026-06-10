import type { ComparisonCategoryDefinition } from "../types";
import {
  getFrozenVegetablesCorpusPayload,
  getFrozenVegetablesPageData,
  frozenVegetablesComparisonMetadata,
} from "../../frozen-vegetables-comparison-page-data";

export const frozenVegetablesCategoryDefinition: ComparisonCategoryDefinition = {
  id: "frozen-vegetables",
  routePath: "/hashvaot/frozen-vegetables",
  metadata: frozenVegetablesComparisonMetadata,
  getPageData: getFrozenVegetablesPageData,
  getCorpusPayload: getFrozenVegetablesCorpusPayload,
};
