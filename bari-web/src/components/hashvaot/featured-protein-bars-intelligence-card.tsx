"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  proteinBarsCorpusMeta,
  proteinBarsProducts,
} from "@/lib/comparisons/protein-bars-comparison-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

const PROTEIN_BARS_INSIGHT_LINES = [
  "הציון הגבוה בקטגוריה — 72/B — לא הולך לחטיף עם הכי הרבה חלבון",
  "25–34 גרם חלבון מגיעים כמעט תמיד עם ממתיקים ותחליפי סוכר",
  "חטיף חלבון מהונדס לעיתים מקבל ציון נמוך מחטיף תמרים פשוט",
] as const;

export function FeaturedProteinBarsIntelligenceCard({ href, description }: Props) {
  const insightLines = proteinBarsProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = insightLines.length > 0 ? insightLines : PROTEIN_BARS_INSIGHT_LINES;

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="דוח חדש"
        categoryTags="חטיפי חלבון · שופרסל"
        title="השוואת חטיפי חלבון"
        description={description}
        insightLines={lines}
        stats={[
          { value: proteinBarsProducts.length, label: "בדף ההשוואה" },
          { value: "25–34", label: "גרם חלבון ל-100 גרם" },
          { value: "B", label: "תקרת הקטגוריה" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(proteinBarsCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#3A6B50", photo: "/hashvaot/themes/protein-bars.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
