import type { ComparisonCategoryDefinition } from "../types";
import {
  cookiesCoffeeComparisonMetadata,
  cookiesCoffeeHero,
  getCookiesCoffeeCorpusPayload,
  getCookiesCoffeePageData,
} from "../../cookies-coffee-page-data";

export const cookiesCoffeeCategoryDefinition: ComparisonCategoryDefinition = {
  id: "cookies-coffee",
  routePath: "/hashvaot/cookies-coffee",
  nameHe: cookiesCoffeeHero.eyebrow,
  metadata: cookiesCoffeeComparisonMetadata,
  getPageData: getCookiesCoffeePageData,
  getCorpusPayload: getCookiesCoffeeCorpusPayload,
};
