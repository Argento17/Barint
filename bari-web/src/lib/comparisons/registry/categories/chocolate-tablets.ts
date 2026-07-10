import type { ComparisonCategoryDefinition } from "../types";
import {
  chocolateTabletsComparisonMetadata,
  chocolateTabletsHero,
  getChocolateTabletsCorpusPayload,
  getChocolateTabletsPageData,
} from "../../chocolate-tablets-comparison-page-data";

export const chocolateTabletsCategoryDefinition: ComparisonCategoryDefinition = {
  id: "chocolate-tablets",
  routePath: "/hashvaot/chocolate-tablets",
  nameHe: chocolateTabletsHero.eyebrow,
  metadata: chocolateTabletsComparisonMetadata,
  getPageData: getChocolateTabletsPageData,
  getCorpusPayload: getChocolateTabletsCorpusPayload,
};
