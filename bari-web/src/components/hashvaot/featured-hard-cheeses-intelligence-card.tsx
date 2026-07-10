"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  hardCheesesCorpusMeta,
  hardCheesesProducts,
} from "@/lib/comparisons/hard-cheeses-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("hard_cheeses").hero;

function stripCardDigits(text: string): string {
  return text
    .replace(/[0-9]+(?:[.,][0-9]+)?/g, "")
    .replace(/\s{2,}/g, " ")
    .replace(/\s+([,.—–])/g, "$1")
    .trim();
}

type Props = {
  href: string;
  description: string;
};

const HARD_CHEESES_INSIGHT_LINES = [
  "אף גבינה לא הגיעה ל-A — הציון המרבי שייך לגאודה עם מינימום מרכיבים",
  "גבינת לייט עם מייצבים מקבלת D — המנוע מעניש נכון על עומס תוספים",
  "פרמזן: חלבון גבוה מאוד, אבל נתרן קיצוני מוריד אותו ל-D",
  "האחוז על האריזה הוא שומן בחומר יבש — לא מה שאתם אוכלים בפועל",
] as const;

export function FeaturedHardCheesesIntelligenceCard({ href, description }: Props) {
  const insightLines = hardCheesesProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : HARD_CHEESES_INSIGHT_LINES).map(stripCardDigits);

  const bCount = hardCheesesProducts.filter((p) => p.grade === "B").length;
  const scoredCount = hardCheesesProducts.filter((p) => p.score != null).length;

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-[3px] motion-reduce:transition-none motion-reduce:hover:translate-y-0",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="חדש"
        categoryTags="גבינות קשות · צהובה · בולגרית · צפתית"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={lines}
        stats={[
          { value: hardCheesesProducts.length, label: "מוצרים נותחו" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: bCount, label: "בציון B (המרבי)" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(hardCheesesCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#1F8F6A", photo: "/hashvaot/themes/hard-cheeses.jpg" }}
        className="group-hover/card:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]"
      />
    </Link>
  );
}
