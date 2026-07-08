import poultryReportData from "@/data/news/of-poultry-report.json";

/**
 * Content contract for the first חדשות (News) article — an independent
 * honest-broker commentary piece on a third-party investigation (שומרים / Ynet,
 * poultry industry). TASK-521.
 *
 * Structural note: this is a CONTENT CONTRACT — Frontend Agent owns the shape
 * below; Content Agent owns the strings in src/data/news/of-poultry-report.json.
 * Any future edit to that data file still requires sign-off from both the
 * Content Agent and the Adversarial QA / Red-Team gate before it ships
 * (content_signoff_hard_rule).
 *
 * Mirrors the blog article content pattern (src/lib/blog/food-dyes-article-content.ts)
 * — same "data file consumed by layout-stable components" shape — with one
 * addition specific to news: `claimsAudit`, a structured claim-by-claim status
 * spine (מאומת / שנוי במחלוקת / לא אומת) that is the actual point of an
 * honest-broker piece: it separates what the source report established from
 * what remains contested or unconfirmed.
 */

export type ClaimStatus = "מאומת" | "שנוי במחלוקת" | "לא אומת";

export type ClaimAuditItem = {
  claim: string;
  status: ClaimStatus;
  sourceLabel: string;
  sourceUrl?: string;
  note?: string;
};

export type NewsCitation = {
  id: string;
  short: string;
  full: string;
  url: string;
};

export type NewsRelatedItem = {
  slug: string;
  href: string;
  title: string;
  description: string;
  category: string;
  readTime: string;
  cta: string;
  comingSoon?: boolean;
};

export type PoultryReportArticle = {
  slug: string;
  seo: {
    title: string;
    description: string;
    ogTitle: string;
    ogDescription: string;
  };
  hero: {
    eyebrow: string;
    title: string;
    deck: string;
    publishDate: string;
    readTime: string;
    source: {
      label: string;
      text: string;
      url: string;
    };
  };
  disclaimer: string;
  editorialInsight: string;
  whatReportClaims: {
    title: string;
    subtitle: string;
    paragraphs: string[];
  };
  claimsAudit: {
    title: string;
    subtitle: string;
    items: ClaimAuditItem[];
  };
  whatItMeansForYou: {
    title: string;
    subtitle: string;
    items: { title: string; text: string }[];
  };
  sources: {
    title: string;
    items: NewsCitation[];
  };
  closingCta: {
    text: string;
    href: string;
  };
  relatedReading: {
    title: string;
    items: NewsRelatedItem[];
  };
};

export const poultryReportArticle = poultryReportData as PoultryReportArticle;

export const seoMeta = poultryReportArticle.seo;

export const HASHVAOT_HREF = "/hashvaot";
export const NEWS_INDEX_HREF = "/news";
