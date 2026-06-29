import { absoluteUrl } from "@/lib/site-url";

export function buildArticleSchema({
  title,
  description,
  url,
  datePublished,
  inLanguage = "he",
}: {
  title: string;
  description: string;
  url: string;
  datePublished?: string;
  inLanguage?: string;
}) {
  const pageUrl = url.startsWith("http") ? url : absoluteUrl(url);
  return {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: title,
    description,
    url: pageUrl,
    mainEntityOfPage: pageUrl,
    inLanguage,
    publisher: {
      "@type": "Organization",
      name: "Bari",
      url: absoluteUrl("/"),
    },
    ...(datePublished ? { datePublished } : {}),
  };
}
