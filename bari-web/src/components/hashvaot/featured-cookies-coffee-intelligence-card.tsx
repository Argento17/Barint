"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import {
  cookiesCoffeeCorpusMeta,
  cookiesCoffeeProducts,
} from "@/lib/comparisons/cookies-coffee-page-data";
import { deriveComparisonCardStats } from "@/lib/derived/comparison-card-stats";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("cookies_coffee").hero;

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

const COOKIES_COFFEE_INSIGHT_LINES = [
  "ציון C הוא תקרת הקטגוריה, ורוב המדף מתכנס סביב E",
  "ההבדל בין C ל-E הוא בסוג השומן ובמידת הפשטות של רשימת הרכיבים",
  "נתרן אינו הנושא — הוא נמוך בכל המוצרים ואינו מה שמבדיל כאן",
] as const;

export function FeaturedCookiesCoffeeIntelligenceCard({ href, description }: Props) {
  const insightLines = cookiesCoffeeProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : COOKIES_COFFEE_INSIGHT_LINES).map(stripCardDigits);

  const stats = deriveComparisonCardStats(cookiesCoffeeProducts, cookiesCoffeeCorpusMeta.generated);

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="חדש"
        categoryTags="ביסקוויטים · לוטוס · ליים · קרמבו · מריה"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={lines}
        stats={[
          { value: stats.productCount, label: "מוצרים נותחו" },
          { value: stats.gradeCounts.E, label: "בציון E" },
          { value: stats.gradeCounts.C, label: "בציון C" },
          { value: stats.gradeCounts.D, label: "בציון D" },
        ]}
        updatedLabel={stats.updatedLabel}
        asLinkChild
        theme={{
          accent: "#1F8F6A",
          photo: "/hashvaot/themes/cookies-coffee.jpg",
        }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
