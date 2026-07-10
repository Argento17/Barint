import type { ComparisonCategoryDefinition } from "../types";
import {
  getYogurtSpoonableCorpusPayload,
  getYogurtSpoonablePageData,
  yogurtSpoonableComparisonMetadata,
  yogurtSpoonableHero,
} from "../../yogurt-spoonable-page-data";

export const yogurtCategoryDefinition: ComparisonCategoryDefinition = {
  id: "yogurt",
  routePath: "/hashvaot/yogurt",
  nameHe: yogurtSpoonableHero.eyebrow,
  metadata: yogurtSpoonableComparisonMetadata,
  getPageData: getYogurtSpoonablePageData,
  getCorpusPayload: getYogurtSpoonableCorpusPayload,
};
