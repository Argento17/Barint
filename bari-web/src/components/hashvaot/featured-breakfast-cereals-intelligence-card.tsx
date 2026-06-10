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
import { cn } from "@/lib/utils";

const INSIGHT_LINES = [
  "תווית «דגנים מלאים» מופיעה על מוצרים שמדורגים D",
  "שיבולת שועל בגרסה העבה — רכיב אחד, ציון B גבוה",
  "אף מוצר לא מגיע ל-A — הטוב ביותר עוצר ב-75/B",
  "טענת «דגנים מלאים» על 20 מוצרים — לא בכולם הסדר תומך בה",
  "חמישה מוצרים מיועדים לילדים",
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
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#7A8C5E]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="ניתוח חדש"
        categoryTags="דגני בוקר · שיבולת שועל · קורנפלקס"
        title="דגני בוקר: 37 מוצרים, אף אחד לא מגיע ל-A"
        description={description}
        insightLines={INSIGHT_LINES}
        stats={[
          { value: cerealsProducts.length, label: "מוצרים נותחו" },
          { value: 38, label: "פרמטרים הושוו" },
          { value: 4, label: "קטגוריות" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(cerealsCorpusMeta.generated)}
        asLinkChild
        theme={{ photo: "/hashvaot/themes/breakfast-cereals.jpg", accent: "#7A8C5E" }}
        className="group-hover/card:border-[#7A8C5E]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(122,140,94,0.28),0_0_60px_-26px_rgba(122,140,94,0.08)]"
      />
    </Link>
  );
}
