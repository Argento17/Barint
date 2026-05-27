import type { Metadata } from "next";

import { BreadComparisonDashboard } from "@/components/comparisons/bread-comparison-dashboard";
import { breadComparisonMeta } from "@/lib/blog/bread-analysis-content";

export const metadata: Metadata = {
  title: breadComparisonMeta.title,
  description: breadComparisonMeta.description,
};

export default function BreadComparisonRoute() {
  return <BreadComparisonDashboard />;
}
