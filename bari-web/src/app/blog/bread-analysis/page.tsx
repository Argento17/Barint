import { redirect } from "next/navigation";

import { BREAD_BLOG_HREF } from "@/lib/blog/bread-analysis-content";

export default function LegacyBreadAnalysisBlogPage() {
  redirect(BREAD_BLOG_HREF);
}
