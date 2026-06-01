"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import { SNACK_REPORT_STATS } from "@/lib/comparisons/snack-page-data";
import {
  snacksCorpusMeta,
  snacksProducts,
} from "@/lib/comparisons/snacks-comparison-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

const SNACKS_INSIGHT_LINES = [
  "הציון הגבוה ביותר בקטגוריה — 70/B — לא הלך לאף אחד מהשמות המוכרים",
  "חטיפי תמרים עם 3–4 מרכיבים מובילים את המדף בפשטות מבנית",
  "תווית אדומה על סוכר לא אומרת תמיד ציון נמוך — מקור הסוכר נכנס לחישוב",
  "חטיפי חלבון מעובדים לעיתים מקבלים ציון נמוך יותר מחטיפי תמרים פשוטים",
] as const;

export function FeaturedSnacksIntelligenceCard({ href, description }: Props) {
  const insightLines = snacksProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = insightLines.length > 0 ? insightLines : SNACKS_INSIGHT_LINES;

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
        categoryTags="חטיפים · מדף יוחננוף"
        title="השוואת חטיפים"
        description={description}
        insightLines={lines}
        stats={[
          { value: SNACK_REPORT_STATS.scraped, label: "מוצרים נסרקו" },
          { value: SNACK_REPORT_STATS.scored, label: "קיבלו ציון" },
          { value: snacksProducts.length, label: "בדף ההשוואה" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(snacksCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#BC6A33", photo: "/hashvaot/themes/snacks.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
