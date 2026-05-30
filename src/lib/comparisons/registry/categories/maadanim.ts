import type { ComparisonCategoryDefinition } from "../types";
import {
  getMaadanimCorpusPayload,
  getMaadanimPageData,
  maadanimComparisonMetadata,
} from "../../maadanim-page-data";

export const maadanimCategoryDefinition: ComparisonCategoryDefinition = {
  id: "maadanim",
  routePath: "/hashvaot/maadanim",
  metadata: maadanimComparisonMetadata,
  getPageData: getMaadanimPageData,
  getCorpusPayload: getMaadanimCorpusPayload,
};
