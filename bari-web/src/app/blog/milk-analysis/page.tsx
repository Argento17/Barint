import type { Metadata } from "next";

import { MilkAnalysisArticle } from "@/components/blog/milk-analysis-article";
import { milkAnalysisArticle } from "@/lib/blog/milk-analysis-content";

export const metadata: Metadata = {
  title: "מה באמת קורה במדף החלב? | בלוג Bari",
  description:
    "ניתוח עיתונאי של מוצרי חלב ותחליפי חלב פופולריים בישראל — מגמות, טריידאופים והקשר קטגוריאלי. לקישור להשוואה האינטראקטיבית המלאה.",
  openGraph: {
    title: "מה באמת קורה במדף החלב? | Bari",
    description: milkAnalysisArticle.hero.subtitle,
    type: "article",
  },
};

export default function MilkAnalysisBlogPage() {
  return <MilkAnalysisArticle />;
}
