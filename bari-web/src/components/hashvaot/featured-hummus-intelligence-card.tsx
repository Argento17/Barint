"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  hummusCorpusMeta,
  hummusProducts,
  hummusPrologueSentences,
} from "@/lib/comparisons/hummus-comparison-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("hummus").hero;

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

export function FeaturedHummusIntelligenceCard({ href, description }: Props) {
  const cardDescription = description ?? hummusPrologueSentences[0];

  const displayedCount = hummusProducts.length;
  const scoredCount = hummusProducts.filter((product) => product.score != null).length;
  const aGradeCount = hummusProducts.filter((product) => product.grade === "A").length;

  const aGradeInsightLine =
    aGradeCount > 0
      ? "חלק מהממרחים מגיעים לציון A — הרכב חזק עם תוספים מוגבלים"
      : "אף ממרח לא מגיע לציון A — בין הממרחים המוכנים גם המוביל נושא תוספים ושמן שמדללים";

  const gapInsightLine =
    hummusProducts.some((p) => p.score != null)
      ? "הפער בין הממרח המוביל לתחתית — מדף צפוף יחסית"
      : "כל הממרחים נמדדים על אותו סולם, חומוס מול חומוס בלבד";

  const insightLines = [
    "ממרחי חומוס ומסבחה בלבד — ממרחי ירקות עברו לדף נפרד",
    aGradeInsightLine,
    gapInsightLine,
    "ערכי השומן אינם מוצגים בקטגוריה זו — החלבון הוא המספר האמין להשוואה",
  ];

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
        title={CARD_HERO.title}
        description={stripCardDigits(cardDescription)}
        insightLines={insightLines.map(stripCardDigits)}
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
