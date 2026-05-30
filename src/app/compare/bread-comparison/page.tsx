import type { Metadata } from "next";
import { redirect } from "next/navigation";

import {
  BREAD_COMPARISON_HREF,
  breadComparisonMeta,
} from "@/lib/blog/bread-analysis-content";

export const metadata: Metadata = {
  title: breadComparisonMeta.title,
  description: breadComparisonMeta.description,
};

export default function LegacyCompareBreadComparisonRoute() {
  redirect(BREAD_COMPARISON_HREF);
}
