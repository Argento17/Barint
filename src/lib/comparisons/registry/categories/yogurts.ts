import type { ComparisonCategoryDefinition } from "../types";
import {
  getYogurtsCorpusPayload,
  getYogurtsPageData,
  yogurtsComparisonMetadata,
} from "../../yogurts-comparison-page-data";

export const yogurtsCategoryDefinition: ComparisonCategoryDefinition = {
  id: "yogurts",
  routePath: "/hashvaot/yogurts",
  metadata: yogurtsComparisonMetadata,
  getPageData: getYogurtsPageData,
  getCorpusPayload: getYogurtsCorpusPayload,
};
