import type { ComparisonCategoryDefinition } from "../types";
import {
  getCrackersCorpusPayload,
  getCrackersPageData,
  crackersComparisonMetadata,
} from "../../crackers-page-data";

export const crackersCategoryDefinition: ComparisonCategoryDefinition = {
  id: "crackers",
  routePath: "/hashvaot/crackers",
  nameHe: "קרקרים",
  metadata: crackersComparisonMetadata,
  getPageData: getCrackersPageData,
  getCorpusPayload: getCrackersCorpusPayload,
};
