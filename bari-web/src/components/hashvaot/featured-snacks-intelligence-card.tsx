"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  snacksCorpusMeta,
  snacksProducts,
} from "@/lib/comparisons/snacks-comparison-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("snacks").hero;

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

const SNACKS_INSIGHT_LINES = [
  "הציון הגבוה בקטגוריה לא הלך לאף אחד מהשמות המוכרים",
  "חטיפי תמרים עם רכיבים ספורים מובילים את המדף בפשטות מבנית",
  "תווית אדומה על סוכר לא אומרת תמיד ציון נמוך — מקור הסוכר נכנס לחישוב",
  "חטיפי חלבון מעובדים לעיתים מקבלים ציון נמוך יותר מחטיפי תמרים פשוטים",
] as const;

export function FeaturedSnacksIntelligenceCard({ href, description }: Props) {
  const insightLines = snacksProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : SNACKS_INSIGHT_LINES).map(stripCardDigits);

  const eCount = snacksProducts.filter((p) => p.grade === "E").length;

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
        categoryTags="חטיפי דגנים · שופרסל"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={lines}
        stats={[
          { value: snacksProducts.length, label: "בדף ההשוואה" },
          { value: eCount, label: "בציון E" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(snacksCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#BC6A33", photo: "/hashvaot/themes/snacks.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
