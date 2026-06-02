"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  cheeseCorpusMeta,
  cheeseProducts,
  cheesePrologueSentences,
} from "@/lib/comparisons/cheese-comparison-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description?: string;
};

// TASK-152: reviewed & refined by Content Agent against the insight-line spec
// (4 sub-pools; cream-cheese spreads fall once real fat is counted, EV-029).
const CHEESE_CARD_INSIGHT_LINES = [
  "ארבע קבוצות במדף: קוטג', גבינה לבנה / קוורק, ממרחי גבינת שמנת ולבנה",
  "הקוטג' והגבינות הלבנות מובילות — חלבון של עד 11.5 גרם ל-100 גרם",
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
        title="גבינה לבנה: מה מפריד גבינה מממרח?"
        description={cardDescription}
        insightLines={CHEESE_CARD_INSIGHT_LINES}
        stats={[
          { value: displayedCount, label: "מוצרים בהשוואה" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aGradeCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(cheeseCorpusMeta.generated)}
        asLinkChild
        // Cottage/white-cheese cream accent + category-true fresh-white-cheese photo
        // (white cheese balls in oil/brine). Brings the index card to visual parity
        // with the other featured boxes, all of which carry a /hashvaot/themes photo.
        // milk.jpg was previously rejected (read as the wrong dairy product); this
        // asset reads unambiguously as fresh white cheese, not milk or yogurt.
        theme={{ accent: "#D8CBB0", photo: "/hashvaot/themes/cheese.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
