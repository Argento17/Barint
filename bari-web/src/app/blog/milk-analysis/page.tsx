import type { Metadata } from "next";

import { blogOpenGraph } from "@/lib/seo/open-graph";

import { BlogArticleSeo } from "@/components/seo/blog-article-seo";
import { absoluteUrl } from "@/lib/site-url";
import { MilkAnalysisArticle } from "@/components/blog/milk-analysis-article";
import { milkAnalysisArticle } from "@/lib/blog/milk-analysis-content";

export const metadata: Metadata = {
  title: "מה באמת קורה במדף החלב? | בלוג Bari",
  description:
    "ניתוח עיתונאי של מוצרי חלב ותחליפי חלב פופולריים בישראל — מגמות, טריידאופים והקשר קטגוריאלי. לקישור להשוואה האינטראקטיבית המלאה.",
  openGraph: blogOpenGraph({
    title: "מה באמת קורה במדף החלב? | Bari",
    description: milkAnalysisArticle.hero.subtitle,
    type: "article",
  }),
};

export default function MilkAnalysisBlogPage() {
  return (
    <>
    <BlogArticleSeo
      title={"מה באמת קורה במדף החלב? | בלוג Bari"}
      description={"ניתוח עיתונאי של מוצרי חלב ותחליפי חלב פופולריים בישראל — מגמות, טריידאופים והקשר קטגוריאלי. לקישור להשוואה האינטראקטיבית המלאה."}
      url={absoluteUrl("/blog/milk-analysis")}
    />
      <MilkAnalysisArticle />
    </>
  );
}
