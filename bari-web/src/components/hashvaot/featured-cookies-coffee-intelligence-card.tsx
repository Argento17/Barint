"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  cookiesCoffeeCorpusMeta,
  cookiesCoffeeProducts,
} from "@/lib/comparisons/cookies-coffee-page-data";
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
  "ציון C הוא תקרת הקטגוריה — אין כאן מוצר ללא תווית אדומה לפחות אחת",
  "ההבדל בין C ל-E הוא בסוג השומן ובמידת הפשטות של רשימת הרכיבים",
  "נתרן אינו הנושא — הוא נמוך בכל המוצרים ואינו מה שמבדיל כאן",
] as const;

export function FeaturedCookiesCoffeeIntelligenceCard({ href, description }: Props) {
  const insightLines = cookiesCoffeeProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : COOKIES_COFFEE_INSIGHT_LINES).map(stripCardDigits);

  const cCount = cookiesCoffeeProducts.filter((p) => p.grade === "C").length;
  const dCount = cookiesCoffeeProducts.filter((p) => p.grade === "D").length;
  const eCount = cookiesCoffeeProducts.filter((p) => p.grade === "E").length;

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-[3px] motion-reduce:transition-none motion-reduce:hover:translate-y-0",
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
          { value: cookiesCoffeeProducts.length, label: "מוצרים נותחו" },
          { value: eCount, label: "בציון E" },
          { value: cCount, label: "בציון C" },
          { value: dCount, label: "בציון D" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(cookiesCoffeeCorpusMeta.generated)}
        asLinkChild
        theme={{
          // green accent stripe, site-wide (owner ruling 2026-07-09): no brown accents
          accent: "#1F8F6A",
          photo: "/hashvaot/themes/cookies-coffee.jpg",
        }}
        className="group-hover/card:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]"
      />
    </Link>
  );
}
