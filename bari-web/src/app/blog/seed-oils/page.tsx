import type { Metadata } from "next";

import { BlogArticleSeo } from "@/components/seo/blog-article-seo";
import { absoluteUrl } from "@/lib/site-url";
import { SeedOilsArticle } from "@/components/blog/seed-oils-article";
import { seoMeta } from "@/lib/blog/seed-oils-article-content";

export const metadata: Metadata = {
  title: seoMeta.title,
  description: seoMeta.description,
  openGraph: {
    title: seoMeta.ogTitle,
    description: seoMeta.ogDescription,
    type: "article",
  },
};

export default function SeedOilsBlogPage() {
  return (
    <>
      <BlogArticleSeo
        title={metadata.title as string}
        description={metadata.description as string}
        url={absoluteUrl("/blog/seed-oils")}
        datePublished="2026-07-03"
      />
      <SeedOilsArticle />
    </>
  );
}
