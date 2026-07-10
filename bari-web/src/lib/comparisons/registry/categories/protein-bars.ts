import type { ComparisonCategoryDefinition } from "../types";
import {
  getProteinBarsCorpusPayload,
  getProteinBarsPageData,
  proteinBarsComparisonMetadata,
  proteinBarsHero,
} from "../../protein-bars-comparison-page-data";

export const proteinBarsCategoryDefinition: ComparisonCategoryDefinition = {
  id: "protein-bars",
  routePath: "/hashvaot/protein-bars",
  nameHe: proteinBarsHero.eyebrow,
  metadata: proteinBarsComparisonMetadata,
  getPageData: getProteinBarsPageData,
  getCorpusPayload: getProteinBarsCorpusPayload,
};
