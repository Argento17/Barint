import type { Metadata } from "next";

import { BreadAnalysisArticle } from "@/components/blog/bread-analysis-article";
import { breadAnalysisArticle } from "@/lib/blog/bread-analysis-content";

export const metadata: Metadata = {
  title: "מה באמת קורה במדף הלחמים? | בלוג Bari",
  description:
    "ניתוח עיתונאי של מדף הלחמים והקרקרים בישראל — מחמצת, מקור סיבים, רמת עיבוד והפער בין מה שכתוב על האריזה לבין איך המוצר באמת בנוי.",
  openGraph: {
    title: "מה באמת קורה במדף הלחמים? | Bari",
    description: breadAnalysisArticle.hero.subtitle,
    type: "article",
  },
};

export default function BreadAnalysisBlogPage() {
  return <BreadAnalysisArticle />;
}
