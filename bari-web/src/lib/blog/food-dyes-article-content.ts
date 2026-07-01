import foodDyesArticleData from "@/data/blog/food-dyes.json";

export const FOOD_DYES_BLOG_HREF = "/blog/food-dyes";
export const HASHVAOT_HREF = "/hashvaot";

/**
 * Content object for the synthetic-food-dyes explainer
 * ("Nestlé US drops synthetic dyes — what it means for the Israeli shelf").
 *
 * Follows the canonical Bari blog content pattern established by olive-oil.json
 * (TASK-199): a single data file consumed by layout-stable sub-components.
 * Content authors edit the JSON only; components are layout-stable.
 *
 * Provenance: every factual claim traces to the sourced fact pack gathered
 * 2026-06-30 (Nestlé USA press release, FDA, EUR-Lex Reg. 1333/2008, Miller 2022,
 * OEHHA 2021, USDA GAIN IS2024-0020). The Israel warning-label question
 * (EU Reg. 1333/2008 Art. 24 / Annex V transposition) is intentionally framed
 * as UNVERIFIED — do not assert it either way.
 */
export const foodDyesArticle = foodDyesArticleData;

export const seoMeta = foodDyesArticleData.seo;
