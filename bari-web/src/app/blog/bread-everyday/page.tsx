import type { Metadata } from "next";

import { BreadEditorialArticle } from "@/components/blog/bread-editorial-article";
import { breadArticlesBySlug } from "@/lib/blog/bread-analysis-content";

const article = breadArticlesBySlug["bread-everyday"];

export const metadata: Metadata = {
  title: article.metaTitle,
  description: article.metaDescription,
  openGraph: {
    title: article.metaTitle,
    description: article.metaDescription,
    type: "article",
  },
};

export default function BreadEverydayArticlePage() {
  return <BreadEditorialArticle article={article} />;
}
