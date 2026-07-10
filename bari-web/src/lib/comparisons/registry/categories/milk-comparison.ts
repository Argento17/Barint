import type { ComparisonCategoryDefinition } from "../types";
import {
  getMilkCorpusPayload,
  getMilkPageData,
  milkComparisonMetadata,
  milkHero,
} from "../../milk-page-data";

export const milkCategoryDefinition: ComparisonCategoryDefinition = {
  id: "milk-comparison",
  routePath: "/hashvaot/milk-comparison",
  nameHe: milkHero.eyebrow,
  metadata: milkComparisonMetadata,
  getPageData: getMilkPageData,
  getCorpusPayload: getMilkCorpusPayload,
};
