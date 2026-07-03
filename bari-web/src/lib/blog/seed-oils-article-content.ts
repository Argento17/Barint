import seedOilsArticleData from "@/data/blog/seed-oils.json";

export const SEED_OILS_BLOG_HREF = "/blog/seed-oils";
export const HASHVAOT_HREF = "/hashvaot";

/**
 * Content object for the seed-oils evidence explainer
 * ("שמני זרעים: מה המחקר באמת אומר, ומה בארי עושה עם זה").
 *
 * Follows the canonical Bari blog content pattern established by food-dyes.json
 * (TASK-492A): a single data file consumed by layout-stable sub-components.
 * Content authors edit the JSON only; components are layout-stable.
 *
 * Provenance: ported VERBATIM from the approved, two-gate-signed-off draft at
 * 03_operations/reports/content/seed_oils_blog_draft_v1.md (TASK-492A). Do not
 * rephrase, shorten, or "improve" any Hebrew wording here — any copy edit
 * bypasses the two-gate sign-off. Primary anchor sources: Memorial Sloan
 * Kettering (clinical dietitians, Feb 2026) and Johns Hopkins Bloomberg School
 * of Public Health (Dr. Matti Marklund). Corroboration only, declared conflict
 * of interest: Nagra et al., Critical Reviews in Food Science and Nutrition,
 * April 2026.
 *
 * TASK-492A revision (owner review pass): brand name corrected ברי -> בארי
 * throughout; `sections[].chart` (the cookies rank-1-vs-bottom-two proof visual,
 * on the "bari-proof" section) and `claimsTable` (optional claims-vs-evidence
 * table, inset into "institutions") added — both consumed by
 * seed-oils-cookies-chart.tsx / seed-oils-claims-table.tsx, verified against
 * cookies_coffee_frontend_v2.json (117-product corpus).
 */
export const seedOilsArticle = seedOilsArticleData;

export const seoMeta = seedOilsArticleData.seo;
