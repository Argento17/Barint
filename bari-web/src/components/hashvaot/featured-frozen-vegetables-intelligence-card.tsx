"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  corpusMeta as frozenVegetablesCorpusMeta,
  frozenVegetablesProducts,
  frozenVegetablesPrologueSentences,
} from "@/lib/comparisons/frozen-vegetables-comparison-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description?: string;
};

export function FeaturedFrozenVegetablesIntelligenceCard({ href, description }: Props) {
  const cardDescription = description ?? frozenVegetablesPrologueSentences[0];

  const displayedCount = frozenVegetablesProducts.length;
  const scoredCount = frozenVegetablesProducts.filter((product) => product.score != null).length;
  const aGradeCount = frozenVegetablesProducts.filter((product) => product.grade === "A").length;

  const displayedScores = frozenVegetablesProducts
    .map((product) => product.score)
    .filter((score): score is number => score != null);
  const topScore = displayedScores.length ? Math.max(...displayedScores) : null;
  const bottomScore = displayedScores.length ? Math.min(...displayedScores) : null;
  const scoreGap = topScore != null && bottomScore != null ? topScore - bottomScore : null;

  const aGradeInsightLine =
    aGradeCount > 0
      ? `${aGradeCount} מוצרים מגיעים לציון A — ירק קפוא בלי תוספות, רכיב אחד`
      : "אף מוצר לא מגיע לציון A בירקות קפואים";

  const gapInsightLine =
    scoreGap != null
      ? `פער של ${scoreGap} נקודות בין המוביל לתחתית — מתערובות עם תוספות ועד ירקות בודדים`
      : "";

  const insightLines = [
    "35 מוצרים עם רכיב אחד בלבד — אפונה, תרד, ברוקולי, שעועית, תירס — מקבלים A",
    aGradeInsightLine,
    gapInsightLine,
    "אין S בירקות קפואים — A הוא הגבוה האפשרי, ואפילו המוביל (89/A) הוא לא יוצא דופן",
  ].filter(Boolean) as readonly string[];

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
        categoryTags="ירקות קפואים · שופרסל"
        title="ירקות קפואים: מה באמת באריזה?"
        description={cardDescription}
        insightLines={insightLines}
        stats={[
          { value: displayedCount, label: "מוצרים בהשוואה" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aGradeCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(frozenVegetablesCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#1F8F6A", photo: "/hashvaot/themes/vegetables.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
