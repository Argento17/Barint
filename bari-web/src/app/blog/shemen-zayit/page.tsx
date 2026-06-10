import type { Metadata } from "next";

import { OliveOilArticle } from "@/components/blog/olive-oil-article";

export const metadata: Metadata = {
  // SEO brief (TASK-199): see C:\Bari\03_operations\seo\olive_oil_seo_brief_v1.md
  // Primary keyword: שמן זית כתית מעולה (high intent, informational)
  // Secondary: תאריך קציר שמן זית, PDO שמן זית, מה לחפש בשמן זית, שמן זית השוואה
  // URL slug: /blog/shemen-zayit (Hebrew romanised — avoids encoding issues)
  // Structured data: Article schema (JSON-LD) — implemented in layout
  title: "13 מוצרי שמן זית בשופרסל. אפס גילויים על תאריך הקציר. | Bari",
  description:
    "סרקנו את מלאי שמן הזית בשופרסל — 13 מוצרים. אף אחד לא מצהיר על תאריך קציר. מה \"כתית מעולה\" מבטיח — ומה הוא לא מחויב לגלות.",
  openGraph: {
    title: "13 מוצרי שמן זית בשופרסל. אפס גילויים על תאריך הקציר.",
    description:
      "סרקנו את מלאי שמן הזית בשופרסל — 13 מוצרים. אף אחד לא מצהיר על תאריך קציר. מה \"כתית מעולה\" מבטיח — ומה הוא לא מחויב לגלות.",
    type: "article",
  },
};

export default function OliveOilBlogPage() {
  return <OliveOilArticle />;
}
