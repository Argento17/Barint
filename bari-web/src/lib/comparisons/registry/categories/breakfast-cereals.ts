import type { ComparisonCategoryDefinition } from "../types";
import {
  getCerealsCorpusPayload,
  getCerealsPageData,
  cerealsComparisonMetadata,
} from "../../cereals-page-data";

export const cerealsCategoryDefinition: ComparisonCategoryDefinition = {
  id: "breakfast-cereals",
  routePath: "/hashvaot/breakfast-cereals",
  metadata: cerealsComparisonMetadata,
  getPageData: getCerealsPageData,
  getCorpusPayload: getCerealsCorpusPayload,
};
