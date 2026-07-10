import type { ComparisonCategoryDefinition } from "../types";
import {
  chocolateBarsComparisonMetadata,
  chocolateBarsHero,
  getChocolateBarsCorpusPayload,
  getChocolateBarsPageData,
} from "../../chocolate-bars-comparison-page-data";

export const chocolateBarsCategoryDefinition: ComparisonCategoryDefinition = {
  id: "chocolate-bars",
  routePath: "/hashvaot/chocolate-bars",
  nameHe: chocolateBarsHero.eyebrow,
  metadata: chocolateBarsComparisonMetadata,
  getPageData: getChocolateBarsPageData,
  getCorpusPayload: getChocolateBarsCorpusPayload,
};
