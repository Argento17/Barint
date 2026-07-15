import algimelTahiniAlertData from "@/data/news/algimel-tahini-alert.json";
import type { PoultryReportArticle } from "@/lib/news/of-poultry-report-content";

/**
 * Content contract for the second חדשות (News) article — an independent
 * honest-broker commentary on a Ministry of Health consumer-safety warning
 * (Algimel raw tahini: Salmonella found on routine market sampling, plus an
 * unauthorized-import finding for the brand's products). TASK-769.
 *
 * Reuses the PoultryReportArticle type contract verbatim — same shape (hero /
 * disclaimer / editorialInsight / whatReportClaims / claimsAudit /
 * whatItMeansForYou / sources / closingCta / relatedReading) as the first
 * news piece (src/lib/news/of-poultry-report-content.ts). No duplicate type
 * definition: this file imports and reuses PoultryReportArticle rather than
 * redeclaring it, per the of-poultry-report pattern.
 *
 * Structural note: this is a CONTENT CONTRACT — Frontend Agent owns the shape
 * above; Content Agent owns the strings in
 * src/data/news/algimel-tahini-alert.json. Any future edit to that data file
 * still requires sign-off from both the Content Agent and the Adversarial QA
 * / Red-Team gate before it ships (content_signoff_hard_rule).
 */
export const algimelTahiniAlertArticle = algimelTahiniAlertData as PoultryReportArticle;

export const seoMeta = algimelTahiniAlertArticle.seo;
