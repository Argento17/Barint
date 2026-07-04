import type { Metadata } from "next";

import { BlogArticleSeo } from "@/components/seo/blog-article-seo";
import { absoluteUrl } from "@/lib/site-url";
import { UpfArticle } from "@/components/blog/upf-article";
import { seoMeta } from "@/lib/blog/upf-article-content";

export const metadata: Metadata = {
  title: seoMeta.title,
  description: seoMeta.description,
  openGraph: {
    title: seoMeta.ogTitle,
    description: seoMeta.ogDescription,
    type: "article",
  },
};

export default function UpfBlogPage() {
  return (
    <>
      <BlogArticleSeo
        title={metadata.title as string}
        description={metadata.description as string}
        url={absoluteUrl("/blog/ultra-processed-food")}
        datePublished="2026-07-04"
      />
      <UpfArticle />
    </>
  );
}
