import type { Metadata } from "next";

import { SugarAlcoholsArticle } from "@/components/blog/sugar-alcohols-article";
import { seoMeta } from "@/lib/blog/sugar-alcohols-article-content";

export const metadata: Metadata = {
  title: seoMeta.title,
  description: seoMeta.description,
  openGraph: {
    title: seoMeta.ogTitle,
    description: seoMeta.ogDescription,
    type: "article",
  },
};

export default function SugarAlcoholsBlogPage() {
  return <SugarAlcoholsArticle />;
}
