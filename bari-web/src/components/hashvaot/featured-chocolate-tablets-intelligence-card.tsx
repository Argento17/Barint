"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  chocolateTabletCorpusMeta,
  chocolateTabletsProducts,
} from "@/lib/comparisons/chocolate-tablets-comparison-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("chocolate_tablets").hero;

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

const CHOCOLATE_TABLETS_INSIGHT_LINES = [
  "מריר אמיתי — מה שנקרא שוקולד לבן הוא בעיקרו שמן, סוכר וחלב, בלי מוצקי קקאו כלל",
  "הציון הגבוה ביותר בקטגוריה הוא C — שוקולד הוא ממתק",
  "ככל שאחוז הקקאו עולה, הסוכר יורד ורשימת הרכיבים מתקצרת",
] as const;

export function FeaturedChocolateTabletsIntelligenceCard({ href, description }: Props) {
  const insightLines = chocolateTabletsProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : CHOCOLATE_TABLETS_INSIGHT_LINES).map(stripCardDigits);

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
        categoryTags="טבלאות שוקולד · שופרסל"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={lines}
        stats={[
          { value: chocolateTabletsProducts.length, label: "בדף ההשוואה" },
          { value: "C", label: "תקרת הקטגוריה" },
          { value: "90%", label: "אחוז קקאו מקסימלי" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(chocolateTabletCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#5C3D2E", photo: "/hashvaot/themes/chocolate-tablets.jpg" }}
        className="group-hover/card:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]"
      />
    </Link>
  );
}
