import type { Metadata } from "next";

import { BreadArticle } from "@/components/blog/bread-article";

export const metadata: Metadata = {
  // SEO brief (TASK-200): see C:\Bari\03_operations\seo\bread_seo_brief_v1.md
  // Primary keyword: לחם מלא ישראל (high intent, informational/commercial)
  // Secondary: לחם מחמצת ישראל, לחם שיפון ישראל, מה ההבדל בין לחמים, לחם בריא שופרסל
  // URL slug: /blog/lechem (Hebrew romanised — avoids encoding issues)
  // Structured data: Article schema (JSON-LD) — implemented in layout
  title: "24 מוצרי לחם בשופרסל. מה מפריד בין A ל-B. | Bari",
  description:
    "סרקנו את מדף הלחם של שופרסל — 24 מוצרים עם ציון. מחמצת בשם ≠ מחמצת ברכיבים. מה שמסביר את פער 16 הנקודות בין הלחם הכי גבוה לכי נמוך.",
  openGraph: {
    title: "24 מוצרי לחם בשופרסל. מה מפריד בין A ל-B.",
    description:
      "סרקנו את מדף הלחם של שופרסל — 24 מוצרים עם ציון. מחמצת בשם ≠ מחמצת ברכיבים. מה שמסביר את פער 16 הנקודות בין הלחם הכי גבוה לכי נמוך.",
    type: "article",
  },
};

export default function BreadBlogPage() {
  return <BreadArticle />;
}
