"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  cheeseCorpusMeta,
  cheeseProducts,
  cheesePrologueSentences,
} from "@/lib/comparisons/cheese-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("cheese").hero;

function stripCardDigits(text: string): string {
  return text
    .replace(/[0-9]+(?:[.,][0-9]+)?/g, "")
    .replace(/\s{2,}/g, " ")
    .replace(/\s+([,.—–])/g, "$1")
    .trim();
}

type Props = {
  href: string;
  description?: string;
};

const CHEESE_CARD_INSIGHT_LINES = [
  "ארבע קבוצות במדף: קוטג', גבינה לבנה / קוורק, ממרחי גבינת שמנת ולבנה",
  "הקוטג' והגבינות הלבנות מובילות — חלבון גבוה ל-100 גרם",
  "ממרחי גבינת שמנת נופלים נמוך יותר ברגע שסופרים את השומן האמיתי",
  "במדף הזה 'הכי טוב' הוא B — אף מוצר לא מגיע ל-A",
] as const;

export function FeaturedCheeseIntelligenceCard({ href, description }: Props) {
  const cardDescription = description ?? cheesePrologueSentences[0];
  const displayedCount = cheeseProducts.length;
  const scoredCount = cheeseProducts.filter((product) => product.score != null).length;
  const aGradeCount = cheeseProducts.filter((product) => product.grade === "A").length;

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
        categoryTags="גבינות לבנות וממרחים · שופרסל"
        title={CARD_HERO.title}
        description={stripCardDigits(cardDescription)}
        insightLines={CHEESE_CARD_INSIGHT_LINES}
        stats={[
          { value: displayedCount, label: "מוצרים בהשוואה" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aGradeCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(cheeseCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#D8CBB0", photo: "/hashvaot/themes/cheese.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
