import type { ComparisonCategoryDefinition } from "../types";
import {
  getBreadCorpusPayload,
  getBreadPageData,
  breadComparisonMetadata,
} from "../../bread-comparison-page-data";

export const breadCategoryDefinition: ComparisonCategoryDefinition = {
  id: "bread",
  routePath: "/hashvaot/bread",
  metadata: breadComparisonMetadata,
  getPageData: getBreadPageData,
  getCorpusPayload: getBreadCorpusPayload,
};
