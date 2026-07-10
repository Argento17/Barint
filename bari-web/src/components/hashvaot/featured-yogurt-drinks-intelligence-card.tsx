"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  yogurtDrinksCorpusMeta,
  yogurtDrinksHero,
  yogurtDrinksProducts,
} from "@/lib/comparisons/yogurt-drinks-page-data";
import { cn } from "@/lib/utils";

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

// Sourced (TASK-546), each line condensed from already two-gate-signed page_copy —
// no per-product claims, no fresh authorship. Photo: yogurt-drinks.jpg — a drinkable
// yogurt in a glass (owner 2026-07-09: yogurt.jpg's strawberry jars read as DENSE yogurt
// and belong on the spoonable card; this card needed a drink-specific shot).
// 1. yogurtDrinksPrologueSentences[1] (page_copy.prologue.sentences[1])
// 2. yogurtDrinksPrologueSentences[2] (page_copy.prologue.sentences[2])
// 3. page_copy.caveat.notes[0].title (yogurt_drinkable_frontend_v1.json)
const YOGURT_DRINKS_INSIGHT_LINES = [
  "בין משקאות היוגורט שנבדקו כאן יש טווח רחב ברשימת הרכיבים",
  "חלק מהמשקאות נשען על מחיות פרי אמיתיות, אחרים על ממתיקים מלאכותיים",
  "סוכר במשקאות יוגורט נבדק מול רף קבוע מראש",
] as const;

export function FeaturedYogurtDrinksIntelligenceCard({ href, description }: Props) {
  const displayedCount = yogurtDrinksProducts.length;
  const scoredCount = yogurtDrinksProducts.filter((product) => product.score != null).length;
  const aGradeCount = yogurtDrinksProducts.filter((product) => product.grade === "A").length;

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-[3px] motion-reduce:transition-none motion-reduce:hover:translate-y-0",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="קטגוריה חדשה"
        categoryTags="משקאות יוגורט · יוגורט לשתייה · כפיר"
        title={yogurtDrinksHero.title}
        description={stripCardDigits(description)}
        insightLines={[...YOGURT_DRINKS_INSIGHT_LINES].map(stripCardDigits)}
        stats={[
          { value: displayedCount, label: "מוצרים בהשוואה" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aGradeCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(yogurtDrinksCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#1D7A5C", photo: "/hashvaot/themes/yogurt-drinks.jpg" }}
        className="group-hover/card:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]"
      />
    </Link>
  );
}
