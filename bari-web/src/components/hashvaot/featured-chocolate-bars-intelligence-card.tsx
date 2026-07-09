"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  chocolateBarsCorpusMeta,
  chocolateBarsProducts,
} from "@/lib/comparisons/chocolate-bars-comparison-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("chocolate_bars").hero;

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

const CHOCOLATE_BARS_INSIGHT_LINES = [
  "כל החטיפים מקבלים E — אבל יש הבדל בין ממתק עם בוטנים לממתק של סוכר בלבד",
  "הסוכר, השמן והסירופ קובעים את הציון — לא שם המוצר",
  "המילה חטיף היא שיווק — זהו מדף ממתקים לכל דבר",
] as const;

export function FeaturedChocolateBarsIntelligenceCard({ href, description }: Props) {
  const insightLines = chocolateBarsProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : CHOCOLATE_BARS_INSIGHT_LINES).map(stripCardDigits);

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-[3px] motion-reduce:transition-none motion-reduce:hover:translate-y-0",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="דוח חדש"
        categoryTags="חטיפי שוקולד · שופרסל"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={lines}
        stats={[
          { value: chocolateBarsProducts.length, label: "בדף ההשוואה" },
          { value: "E", label: "ציון כל המוצרים" },
          { value: "45–60", label: "גרם סוכר ל-100 גרם" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(chocolateBarsCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#3D2314", photo: "/hashvaot/themes/chocolate-bars.jpg" }}
        className="group-hover/card:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]"
      />
    </Link>
  );
}
