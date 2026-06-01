"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  vegetableSpreadsCorpusMeta,
  vegetableSpreadsProducts,
  vegetableSpreadsPrologueSentences,
} from "@/lib/comparisons/vegetable-spreads-comparison-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description?: string;
};

const VEGETABLE_SPREADS_CARD_INSIGHT_LINES = [
  "מטבוחה, ממרח חצילים וממרח פלפלים — ממרחי ירקות בלבד",
  "ממרחי חומוס ומסבחה מוצגים בדף נפרד",
  "הציון מחושב לפי מדד עיבוד, תוספים וערכים תזונתיים",
] as const;

export function FeaturedVegetableSpreadsIntelligenceCard({ href, description }: Props) {
  const cardDescription = description ?? vegetableSpreadsPrologueSentences[0];

  const displayedCount = vegetableSpreadsProducts.length;
  const scoredCount = vegetableSpreadsProducts.filter((product) => product.score != null).length;
  const aGradeCount = vegetableSpreadsProducts.filter((product) => product.grade === "A").length;

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
        categoryTags="ממרחי ירקות · שופרסל"
        title="ממרחי ירקות: מה באמת יש במדף?"
        description={cardDescription}
        insightLines={VEGETABLE_SPREADS_CARD_INSIGHT_LINES}
        stats={[
          { value: displayedCount, label: "מוצרים בהשוואה" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aGradeCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(vegetableSpreadsCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#7E68A6", photo: "/hashvaot/themes/eggplant.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
