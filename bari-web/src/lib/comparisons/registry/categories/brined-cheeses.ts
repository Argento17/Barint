import type { ComparisonCategoryDefinition } from "../types";
import {
  brinedCheesesComparisonMetadata,
  brinedCheesesHero,
  getBrinedCheesesCorpusPayload,
  getBrinedCheesesPageData,
} from "../../brined-cheeses-page-data";

export const brinedCheesesCategoryDefinition: ComparisonCategoryDefinition = {
  id: "brined-cheeses",
  routePath: "/hashvaot/brined-cheeses",
  nameHe: brinedCheesesHero.eyebrow,
  metadata: brinedCheesesComparisonMetadata,
  getPageData: getBrinedCheesesPageData,
  getCorpusPayload: getBrinedCheesesCorpusPayload,
};
