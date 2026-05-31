import type { ComparisonCategoryDefinition } from "../types";
import {
  getVegetableSpreadsCorpusPayload,
  getVegetableSpreadsPageData,
  vegetableSpreadsComparisonMetadata,
} from "../../vegetable-spreads-comparison-page-data";

export const vegetableSpreadsCategoryDefinition: ComparisonCategoryDefinition = {
  id: "vegetable-spreads",
  routePath: "/hashvaot/vegetable-spreads",
  metadata: vegetableSpreadsComparisonMetadata,
  getPageData: getVegetableSpreadsPageData,
  getCorpusPayload: getVegetableSpreadsCorpusPayload,
};
