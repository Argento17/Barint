import type { ComparisonCategoryDefinition } from "../types";
import {
  getGranolaCorpusPayload,
  getGranolaPageData,
  granolaComparisonMetadata,
} from "../../granola-page-data";

export const granolaCategoryDefinition: ComparisonCategoryDefinition = {
  id: "granola",
  routePath: "/hashvaot/granola",
  nameHe: "גרנולה ומוזלי",
  metadata: granolaComparisonMetadata,
  getPageData: getGranolaPageData,
  getCorpusPayload: getGranolaCorpusPayload,
};
