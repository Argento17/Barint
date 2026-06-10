import type { Metadata } from "next";

import { YogurtArticle } from "@/components/blog/yogurt-article";

// SEO brief (TASK-201): see C:\Bari\03_operations\seo\yogurt_seo_brief_v1.md
// Primary keyword: יוגורט בריא (high intent, informational)
// Secondary: יוגורט 0 אחוז שומן, יוגורט לבן מול ממותק, יוגורט עם חלבון, יוגורט תרביות חיות
// URL slug: /blog/yogurt (English slug — avoids encoding issues, consistent with /blog/shemen-zayit)
// Structured data: Article schema (JSON-LD) — implemented in layout

export const metadata: Metadata = {
  title: "19 יוגורטים. שתי רשתות. מה שמניע את הציונים. | Bari",
  description:
    "סרקנו 19 יוגורטים משופרסל ויוחננוף. יוגורט לבן פשוט הגיע ל-A. יוגורט 0% שומן בטעם תות — C. מה באמת מבדיל בין הגביעים.",
  openGraph: {
    title: "19 יוגורטים. שתי רשתות. מה שמניע את הציונים.",
    description:
      "סרקנו 19 יוגורטים משופרסל ויוחננוף. יוגורט לבן פשוט הגיע ל-A. יוגורט 0% שומן בטעם תות — C. מה באמת מבדיל בין הגביעים.",
    type: "article",
  },
};

export default function YogurtBlogPage() {
  return <YogurtArticle />;
}
