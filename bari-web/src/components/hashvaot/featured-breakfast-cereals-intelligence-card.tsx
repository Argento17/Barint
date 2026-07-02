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
  "פצפוצי אורז מדגן מלא ללא תוספת סוכר — רכיב אחד, ציון B",
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
  const cerealsBCount = cerealsProducts.filter((p) => p.grade === "B").length;
  const cerealsDCount = cerealsProducts.filter((p) => p.grade === "D").length;

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#7A8C5E]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="ניתוח חדש"
        categoryTags="דגני בוקר · שיבולת שועל · קורנפלקס"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={INSIGHT_LINES}
        stats={[
          { value: cerealsProducts.length, label: "מוצרים נותחו" },
          { value: cerealsDCount, label: "בציון D" },
          { value: cerealsBCount, label: "בציון B" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(cerealsCorpusMeta.generated)}
        asLinkChild
        theme={{ photo: "/hashvaot/themes/breakfast-cereals.jpg", accent: "#7A8C5E" }}
        className="group-hover/card:border-[#7A8C5E]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(122,140,94,0.28),0_0_60px_-26px_rgba(122,140,94,0.08)]"
      />
    </Link>
  );
}
