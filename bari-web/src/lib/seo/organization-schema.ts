import { SITE_URL, absoluteUrl } from "@/lib/site-url";

export function buildOrganizationSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Bari",
    url: SITE_URL,
    logo: absoluteUrl("/favicon.ico"),
  };
}

export function buildWebSiteSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Bari",
    url: SITE_URL,
    inLanguage: "he",
  };
}

export function buildSiteJsonLd() {
  return [buildOrganizationSchema(), buildWebSiteSchema()];
}
