import upfArticleData from "@/data/blog/ultra-processed-food.json";

export const UPF_BLOG_HREF = "/blog/ultra-processed-food";
export const HASHVAOT_HREF = "/hashvaot";

/**
 * Content object for the ultra-processed-food (UPF) evidence explainer
 * ("מזון מעובד-יתר תחת אור זרקורים: מה סדרת הענק בלאנסט באמת אומרת").
 *
 * Provenance (TASK-502): every paragraph, section heading, mechanism sub-point,
 * disclaimer, and citation below is ported VERBATIM from the two-gate-signed-off
 * draft at `tasks/returns/TASK-502_content_draft_v1.md` (PART 1 — Hebrew draft
 * copy v2), which cleared both Content Agent authoring and Adversarial QA /
 * Red-Team sign-off. Do not rephrase, shorten, or "improve" any Hebrew wording
 * here -- any copy edit bypasses the two-gate sign-off.
 *
 * The 4 citation identifiers (titles/DOIs/PMIDs) are cross-checked digit-for-
 * digit against `03_operations/bsip2/evidence_registry/task502_upf_verification_memo_v1.md`
 * §1 (all 4 independently verified via NCBI eutils esearch+esummary).
 *
 * The 4 infographics (`infographics.conditions/confidence/schematic/spectrum`)
 * are NEW structured data authored for this build, grounded only in facts
 * already stated in the body copy above (7 named conditions, the two Milbank
 * confidence tiers, the emulsifier penalize/relief lists) or in live engine
 * behavior (EV-003/EV-019). Infographic #3 (`schematic`) is intentionally
 * generic ("מוצר א׳" / "מוצר ב׳", no score numbers) -- see component doc.
 */
export const upfArticle = upfArticleData;

export const seoMeta = upfArticleData.seo;
