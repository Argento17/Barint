import type { Metadata } from "next";

import { blogOpenGraph } from "@/lib/seo/open-graph";

import { BlogArticleSeo } from "@/components/seo/blog-article-seo";
import { absoluteUrl } from "@/lib/site-url";
import { FoodDyesArticle } from "@/components/blog/food-dyes-article";
import { seoMeta } from "@/lib/blog/food-dyes-article-content";

export const metadata: Metadata = {
  title: seoMeta.title,
  description: seoMeta.description,
  openGraph: blogOpenGraph({
    title: seoMeta.ogTitle,
    description: seoMeta.ogDescription,
    type: "article",
  }),
};

export default function FoodDyesBlogPage() {
  return (
    <>
      <BlogArticleSeo
        title={metadata.title as string}
        description={metadata.description as string}
        url={absoluteUrl("/blog/food-dyes")}
        datePublished="2026-06-30"
      />
      <FoodDyesArticle />
    </>
  );
}
