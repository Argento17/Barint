import type { Metadata } from "next";

import { blogOpenGraph } from "@/lib/seo/open-graph";

import { BlogArticleSeo } from "@/components/seo/blog-article-seo";
import { absoluteUrl } from "@/lib/site-url";
import { BreadEditorialArticle } from "@/components/blog/bread-editorial-article";
import { breadArticlesBySlug } from "@/lib/blog/bread-analysis-content";

const article = breadArticlesBySlug["bread-wellness-gap"];

export const metadata: Metadata = {
  robots: { index: false },
  title: article.metaTitle,
  description: article.metaDescription,
  openGraph: blogOpenGraph({
    title: article.metaTitle,
    description: article.metaDescription,
    type: "article",
  }),
};

export default function BreadWellnessGapArticlePage() {
  return (
    <>
    <BlogArticleSeo
      title={article.metaTitle}
      description={article.metaDescription}
      url={absoluteUrl("/blog/bread-wellness-gap")}
    />
      <BreadEditorialArticle article={article} />
    </>
  );
}
