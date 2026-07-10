"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import {
  BREAD_REPORT_STATS,
  breadComparisonPairs,
} from "@/lib/comparisons/bread-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("bread").hero;

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

const BREAD_INSIGHT_LINES = [
  "לחם מחמצת לא תמיד מקבל ציון גבוה יותר מלחם יומיומי",
  "חלק מלחמי הבריאות נשענים על תוספים ולא רק על דגנים מלאים",
  "פערי שקיפות בין מותגים דומים מופיעים גם בתוך אותה קטגוריה",
] as const;

export function FeaturedBreadIntelligenceCardLite({ href, description }: Props) {
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
        categoryTags="לחם · פיתה"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={[...BREAD_INSIGHT_LINES].map(stripCardDigits)}
        stats={[
          { value: BREAD_REPORT_STATS.scanned, label: "מוצרים נסרקו" },
          { value: BREAD_REPORT_STATS.sufficient, label: "עם נתונים מספיקים" },
          { value: breadComparisonPairs.length, label: "זוגות השוואה" },
        ]}
        asLinkChild
        theme={{ accent: "#1F8F6A", photo: "/hashvaot/themes/bread.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
