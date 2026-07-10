"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import {
  hardCheesesCorpusMeta,
  hardCheesesProducts,
} from "@/lib/comparisons/hard-cheeses-page-data";
import { deriveComparisonCardStats } from "@/lib/derived/comparison-card-stats";
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
  "גבינה אחת בלבד מגיעה ל-A — גלבוע 5%, דלת-השומן האמיתית של המדף",
  "רוב המדף מתקבץ ב-B — השומן הרווי המובנה הוא הגורם הכובל המשותף",
  "ההפרשים נולדים בניואנסים: מלח, ניקיון הרשימה וגובה השומן הרווי",
  "האחוז על האריזה הוא שומן בחומר יבש — לא מה שאתם אוכלים בפועל",
] as const;

export function FeaturedHardCheesesIntelligenceCard({ href, description }: Props) {
  const insightLines = hardCheesesProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : HARD_CHEESES_INSIGHT_LINES).map(stripCardDigits);

  const stats = deriveComparisonCardStats(hardCheesesProducts, hardCheesesCorpusMeta.generated);

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
        categoryTags="גבינות קשות · צהובה · בולגרית · צפתית"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={lines}
        stats={[
          { value: stats.productCount, label: "מוצרים נותחו" },
          { value: stats.scoredCount, label: "קיבלו ציון" },
          { value: stats.gradeCounts.B, label: "בציון B" },
        ]}
        updatedLabel={stats.updatedLabel}
        asLinkChild
        theme={{ accent: "#1F8F6A", photo: "/hashvaot/themes/hard-cheeses.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
