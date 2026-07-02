import type { ComparisonCategoryDefinition } from "../types";
import {
  getHummusCorpusPayload,
  getHummusPageData,
  hummusComparisonMetadata,
} from "../../hummus-comparison-page-data";

export const hummusCategoryDefinition: ComparisonCategoryDefinition = {
  id: "hummus",
  routePath: "/hashvaot/hummus",
  nameHe: "חומוס וממרחים",
  metadata: hummusComparisonMetadata,
  getPageData: getHummusPageData,
  getCorpusPayload: getHummusCorpusPayload,
};
