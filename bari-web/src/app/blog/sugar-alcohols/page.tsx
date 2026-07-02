import type { Metadata } from "next";

import { blogOpenGraph } from "@/lib/seo/open-graph";

import { BlogArticleSeo } from "@/components/seo/blog-article-seo";
import { absoluteUrl } from "@/lib/site-url";
import { SugarAlcoholsArticle } from "@/components/blog/sugar-alcohols-article";
import { seoMeta } from "@/lib/blog/sugar-alcohols-article-content";

export const metadata: Metadata = {
  title: seoMeta.title,
  description: seoMeta.description,
  openGraph: blogOpenGraph({
    title: seoMeta.ogTitle,
    description: seoMeta.ogDescription,
    type: "article",
  }),
};

export default function SugarAlcoholsBlogPage() {
  return (
    <>
    <BlogArticleSeo
      title={metadata.title as string}
      description={metadata.description as string}
      url={absoluteUrl("/blog/sugar-alcohols")}
    />
      <SugarAlcoholsArticle />
    </>
  );
}
