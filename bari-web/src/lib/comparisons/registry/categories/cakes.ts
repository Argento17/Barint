import type { ComparisonCategoryDefinition } from "../types";
import {
  cakesHardCookiesComparisonMetadata,
  cakesHardCookiesHero,
  getCakesHardCookiesCorpusPayload,
  getCakesHardCookiesPageData,
} from "../../cakes-hard-cookies-page-data";

export const cakesCategoryDefinition: ComparisonCategoryDefinition = {
  id: "cakes",
  routePath: "/hashvaot/cakes",
  nameHe: cakesHardCookiesHero.eyebrow,
  metadata: cakesHardCookiesComparisonMetadata,
  getPageData: getCakesHardCookiesPageData,
  getCorpusPayload: getCakesHardCookiesCorpusPayload,
};
