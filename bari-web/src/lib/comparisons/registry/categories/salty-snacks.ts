import type { ComparisonCategoryDefinition } from "../types";
import {
  getSaltySnacksCorpusPayload,
  getSaltySnacksPageData,
  saltySnacksComparisonMetadata,
} from "../../salty-snacks-page-data";

export const saltySnacksCategoryDefinition: ComparisonCategoryDefinition = {
  id: "salty-snacks",
  routePath: "/hashvaot/salty-snacks",
  metadata: saltySnacksComparisonMetadata,
  getPageData: getSaltySnacksPageData,
  getCorpusPayload: getSaltySnacksCorpusPayload,
};
