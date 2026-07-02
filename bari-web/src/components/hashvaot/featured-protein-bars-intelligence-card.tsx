"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  proteinBarsCorpusMeta,
  proteinBarsProducts,
} from "@/lib/comparisons/protein-bars-comparison-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("protein_bars").hero;

function stripCardDigits(text: string): string {
  return text
    .replace(/[0-9]+(?:[.,][0-9]+)?/g, "")
    .replace(/\s{2,}/g, " ")
    .replace(/\s+([,.—–])/g, "$1")
    .trim();
}

type Props = {
  href: string;
  description: string;
};

const PROTEIN_BARS_INSIGHT_LINES = [
  "הציון הגבוה בקטגוריה לא הולך לחטיף עם הכי הרבה חלבון",
  "חלבון גבוה מגיע כמעט תמיד עם ממתיקים ותחליפי סוכר",
  "חטיף חלבון מהונדס לעיתים מקבל ציון נמוך מחטיף תמרים פשוט",
] as const;

export function FeaturedProteinBarsIntelligenceCard({ href, description }: Props) {
  const insightLines = proteinBarsProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : PROTEIN_BARS_INSIGHT_LINES).map(stripCardDigits);

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
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={lines}
        stats={[
          { value: proteinBarsProducts.length, label: "בדף ההשוואה" },
          { value: "25–36", label: "גרם חלבון ל-100 גרם" },
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
