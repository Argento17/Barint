import { SITE_URL } from "@/lib/site-url";

/**
 * Sitewide Organization + WebSite JSON-LD (schema.org), injected once in the
 * root layout. Helps search engines resolve the brand entity (knowledge panel,
 * sitelinks) and the site name. No SearchAction is declared because the site
 * has no search endpoint — a schema must not point at a non-existent URL.
 *
 * SEO/platform only — no scoring, corpus, or product-order impact. Values are
 * owner-sourced (legal entity "בארי טכנולוגיות") or already published on the
 * site (name, logo, description); nothing here is invented.
 */
export function SiteStructuredData() {
  const graph = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": `${SITE_URL}/#organization`,
        name: "Bari",
        alternateName: "בארי",
        legalName: "בארי טכנולוגיות",
        url: SITE_URL,
        logo: `${SITE_URL}/bari-logo-optimized.webp`,
        description:
          "אינטליגנציית מזון ישראלית: דירוגים והשוואות שקופות המבוססות על נתונים.",
      },
      {
        "@type": "WebSite",
        "@id": `${SITE_URL}/#website`,
        name: "Bari",
        url: SITE_URL,
        inLanguage: "he-IL",
        publisher: { "@id": `${SITE_URL}/#organization` },
      },
    ],
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(graph) }}
    />
  );
}
