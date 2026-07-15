"use client";

import { OfPoultryReportArticle } from "@/components/news/of-poultry-report-article";
import { algimelTahiniAlertArticle } from "@/lib/news/algimel-tahini-alert-content";

/**
 * AlgimelTahiniAlertArticle — second חדשות (News) piece, a thin wrapper
 * around the shared, data-driven OfPoultryReportArticle renderer (generalized
 * in TASK-769 to take an `article` prop instead of hard-importing poultry
 * data). Same honest-broker layout as the first news piece: hero → disclaimer
 * → what-the-report-claims → editorial insight → claim-by-claim audit →
 * what-it-means-for-you → sources → closing CTA → related reading → footer
 * nav. No new component was cloned — see TASK-769 return for the reuse
 * rationale.
 */
export function AlgimelTahiniAlertArticle() {
  return <OfPoultryReportArticle article={algimelTahiniAlertArticle} />;
}
