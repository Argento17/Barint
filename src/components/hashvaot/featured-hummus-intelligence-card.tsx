"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  hummusCorpusMeta,
  hummusProducts,
  hummusPrologueSentences,
} from "@/lib/comparisons/hummus-comparison-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description?: string;
};

const HUMMUS_CARD_INSIGHT_LINES = [
  "59 מוצרים — ממרחי חומוס, מטבוחה, חצילים, פלפלים ומסבחה",
  "מוצר אחד בציון A: הרכב חזק עם תוספים מוגבלים",
  "פער ציון של 37 נקודות בין הממרח המוביל לתחתית",
  "ערכי שומן אינם מוצגים — מגבלת נתוני מקור",
] as const;

export function FeaturedHummusIntelligenceCard({ href, description }: Props) {
  const cardDescription = description ?? hummusPrologueSentences[0];

  // TASK-087C: display-level counts derived from the products actually shown on
  // /hashvaot/hummus — keeps the card in step with the page, not corpus metadata.
  const displayedCount = hummusProducts.length;
  const scoredCount = hummusProducts.filter((product) => product.score != null).length;
  const aGradeCount = hummusProducts.filter((product) => product.grade === "A").length;

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
        categoryTags="חומוס וממרחים · שופרסל"
        title="חומוס וממרחים: מה באמת יש במדף?"
        description={cardDescription}
        insightLines={HUMMUS_CARD_INSIGHT_LINES}
        stats={[
          { value: displayedCount, label: "מוצרים בהשוואה" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aGradeCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(hummusCorpusMeta.generated)}
        asLinkChild
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
