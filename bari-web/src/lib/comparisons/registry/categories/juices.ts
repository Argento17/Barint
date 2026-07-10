import type { ComparisonCategoryDefinition } from "../types";
import {
  getJuicesCorpusPayload,
  getJuicesPageData,
  juicesComparisonMetadata,
  juicesHero,
} from "../../juices-page-data";

export const juicesCategoryDefinition: ComparisonCategoryDefinition = {
  id: "juices",
  routePath: "/hashvaot/juices",
  nameHe: juicesHero.eyebrow,
  metadata: juicesComparisonMetadata,
  getPageData: getJuicesPageData,
  getCorpusPayload: getJuicesCorpusPayload,
};
