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

export function FeaturedHummusIntelligenceCard({ href, description }: Props) {
  const cardDescription = description ?? hummusPrologueSentences[0];

  // TASK-087C: display-level counts derived from the products actually shown on
  // /hashvaot/hummus — keeps the card in step with the page, not corpus metadata.
  const displayedCount = hummusProducts.length;
  const scoredCount = hummusProducts.filter((product) => product.score != null).length;
  const aGradeCount = hummusProducts.filter((product) => product.grade === "A").length;

  // TASK-100 / TASK-150 fix: insight lines are now DERIVED from the displayed shelf
  // so they cannot go stale against the data the card renders beside them. The two
  // previous static lines claimed "five A" and a "47-point gap" — both false for the
  // displayed spread shelf (0 in grade A, ~17-point gap). The A-absence line is the
  // real story: the strongest chickpea compositions are whole/raw products, not
  // spreads, so among actual spreads even the best carries additives/oil that hold it
  // below A.
  const displayedScores = hummusProducts
    .map((product) => product.score)
    .filter((score): score is number => score != null);
  const topScore = displayedScores.length ? Math.max(...displayedScores) : null;
  const bottomScore = displayedScores.length ? Math.min(...displayedScores) : null;
  const scoreGap = topScore != null && bottomScore != null ? topScore - bottomScore : null;

  const aGradeInsightLine =
    aGradeCount > 0
      ? `${aGradeCount} מוצרים מגיעים לציון A — הרכב חזק עם תוספים מוגבלים`
      : "אף ממרח לא מגיע לציון A — בין הממרחים המוכנים גם המוביל נושא תוספים ושמן שמדללים את ההרכב";

  const gapInsightLine =
    scoreGap != null
      ? `פער של ${scoreGap} נקודות בלבד בין הממרח המוביל לתחתית — מדף צפוף`
      : "כל הממרחים נמדדים על אותו סולם, חומוס מול חומוס בלבד";

  const insightLines = [
    "ממרחי חומוס ומסבחה בלבד — ממרחי ירקות עברו לדף נפרד",
    aGradeInsightLine,
    gapInsightLine,
    "ערכי השומן אינם מוצגים בקטגוריה זו — החלבון הוא המספר האמין להשוואה",
  ] as const;

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
        categoryTags="חומוס · שופרסל"
        title="חומוס: מה באמת יש במדף?"
        description={cardDescription}
        insightLines={insightLines}
        stats={[
          { value: displayedCount, label: "מוצרים בהשוואה" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aGradeCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(hummusCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#BF9540", photo: "/hashvaot/themes/hummus.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
