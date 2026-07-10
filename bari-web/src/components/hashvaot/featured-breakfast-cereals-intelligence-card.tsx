"use client";

import Link from "next/link";

import {
  ComparisonIntelligenceHero,
} from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  cerealsCorpusMeta,
  cerealsProducts,
} from "@/lib/comparisons/cereals-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("cereals").hero;

function stripCardDigits(text: string): string {
  return text
    .replace(/[0-9]+(?:[.,][0-9]+)?/g, "")
    .replace(/\s{2,}/g, " ")
    .replace(/\s+([,.—–])/g, "$1")
    .trim();
}

const INSIGHT_LINES = [
  "תווית «דגנים מלאים» מופיעה על מוצרים שמדורגים D",
  "שיבולת שועל בגרסה העבה — רכיב אחד, ציון B גבוה",
  "אף מוצר לא מגיע ל-A — הטוב ביותר עוצר ב-B",
  "טענת «דגנים מלאים» על חלק מהמדף — לא בכולם הסדר תומך בה",
  "יש מוצרים שמיועדים לילדים",
  "גרנולה, מוזלי ושיבולת שועל אינם בעמוד זה",
] as const;

type Props = {
  href: string;
  description: string;
};

export function FeaturedBreakfastCerealsIntelligenceCard({ href, description }: Props) {
  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-[3px] motion-reduce:transition-none motion-reduce:hover:translate-y-0",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="ניתוח חדש"
        categoryTags="דגני בוקר · שיבולת שועל · קורנפלקס"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={[...INSIGHT_LINES].map(stripCardDigits)}
        stats={[
          { value: cerealsProducts.length, label: "מוצרים נותחו" },
          { value: 38, label: "פרמטרים הושוו" },
          { value: 4, label: "קטגוריות" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(cerealsCorpusMeta.generated)}
        asLinkChild
        theme={{ photo: "/hashvaot/themes/breakfast-cereals.jpg", accent: "#1F8F6A" }}
        className="group-hover/card:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]"
      />
    </Link>
  );
}
