import type { ComparisonCategoryDefinition } from "../types";
import {
  getButterCorpusPayload,
  getButterPageData,
  butterComparisonMetadata,
} from "../../butter-page-data";

export const butterCategoryDefinition: ComparisonCategoryDefinition = {
  id: "butter",
  routePath: "/hashvaot/butter",
  metadata: butterComparisonMetadata,
  getPageData: getButterPageData,
  getCorpusPayload: getButterCorpusPayload,
};
