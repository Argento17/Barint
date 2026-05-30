import type { ComparisonCategoryDefinition } from "../types";
import {
  getSnacksCorpusPayload,
  getSnacksPageData,
  snacksComparisonMetadata,
} from "../../snacks-comparison-page-data";

export const snacksCategoryDefinition: ComparisonCategoryDefinition = {
  id: "snacks",
  routePath: "/hashvaot/snacks",
  metadata: snacksComparisonMetadata,
  getPageData: getSnacksPageData,
  getCorpusPayload: getSnacksCorpusPayload,
};
