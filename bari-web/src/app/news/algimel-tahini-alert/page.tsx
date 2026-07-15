import type { Metadata } from "next";

import { BlogArticleSeo } from "@/components/seo/blog-article-seo";
import { absoluteUrl } from "@/lib/site-url";
import { AlgimelTahiniAlertArticle } from "@/components/news/algimel-tahini-alert-article";
import { seoMeta } from "@/lib/news/algimel-tahini-alert-content";

export const metadata: Metadata = {
  title: seoMeta.title,
  description: seoMeta.description,
  openGraph: {
    title: seoMeta.ogTitle,
    description: seoMeta.ogDescription,
    type: "article",
  },
};

export default function AlgimelTahiniAlertNewsPage() {
  return (
    <>
      <BlogArticleSeo
        title={metadata.title as string}
        description={metadata.description as string}
        url={absoluteUrl("/news/algimel-tahini-alert")}
      />
      <AlgimelTahiniAlertArticle />
    </>
  );
}
