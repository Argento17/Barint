import type { ComparisonCategoryDefinition } from "../types";
import {
  getHardCheesesCorpusPayload,
  getHardCheesesPageData,
  hardCheesesComparisonMetadata,
  hardCheesesHero,
} from "../../hard-cheeses-page-data";

export const hardCheesesCategoryDefinition: ComparisonCategoryDefinition = {
  id: "hard-cheeses",
  routePath: "/hashvaot/hard-cheeses",
  nameHe: hardCheesesHero.eyebrow,
  metadata: hardCheesesComparisonMetadata,
  getPageData: getHardCheesesPageData,
  getCorpusPayload: getHardCheesesCorpusPayload,
};
