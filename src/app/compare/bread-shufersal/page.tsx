import { redirect } from "next/navigation";

import { BREAD_COMPARISON_HREF } from "@/lib/blog/bread-analysis-content";

export default function BreadShufersalComparisonRoute() {
  redirect(BREAD_COMPARISON_HREF);
}
