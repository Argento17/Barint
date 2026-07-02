import type { Metadata } from "next";

import { blogOpenGraph } from "@/lib/seo/open-graph";

import { BlogArticleSeo } from "@/components/seo/blog-article-seo";
import { absoluteUrl } from "@/lib/site-url";
import { HummusArticle } from "@/components/blog/hummus-article";

// SEO brief (TASK-202): see C:\Bari\03_operations\seo\hummus_seo_brief_v1.md
// Primary keyword: חומוס השוואה (high intent, informational)
// Secondary: אחוז טחינה בחומוס, נתרן בחומוס, חומוס שופרסל ניתוח, מה לחפש בחומוס
// URL slug: /blog/hummus (category name, no encoding issues)
// Structured data: Article schema (JSON-LD) — implemented in layout
export const metadata: Metadata = {
  robots: { index: false },
  title: "64 מוצרי חומוס בשופרסל. פער של 46 נקודות. | Bari",
  description:
    "סרקנו את מדף החומוס בשופרסל — 64 מוצרים. אחוז הטחינה הוא הגורם שמסביר הכי הרבה את הפערים. הנתרן משתנה פי-50 על אותו מדף.",
  openGraph: blogOpenGraph({
    title: "64 מוצרי חומוס בשופרסל. פער של 46 נקודות.",
    description:
      "סרקנו את מדף החומוס בשופרסל — 64 מוצרים. אחוז הטחינה הוא הגורם שמסביר הכי הרבה את הפערים. הנתרן משתנה פי-50 על אותו מדף.",
    type: "article",
  }),
};

export default function HummusBlogPage() {
  return (
    <>
    <BlogArticleSeo
      title={"64 מוצרי חומוס בשופרסל. פער של 46 נקודות."}
      description={"סרקנו את מדף החומוס בשופרסל — 64 מוצרים. אחוז הטחינה הוא הגורם שמסביר הכי הרבה את הפערים. הנתרן משתנה פי-50 על אותו מדף."}
      url={absoluteUrl("/blog/hummus")}
    />
      <HummusArticle />
    </>
  );
}
