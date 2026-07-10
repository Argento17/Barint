"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import {
  yogurtSpoonableCorpusMeta,
  yogurtSpoonableHero,
  yogurtSpoonableProducts,
} from "@/lib/comparisons/yogurt-spoonable-page-data";
import { deriveComparisonCardStats } from "@/lib/derived/comparison-card-stats";
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
// no per-product claims, no fresh authorship:
// 1. yogurtSpoonablePrologueSentences[2] (page_copy.prologue.sentences[2])
// 2. yogurtSpoonablePrologueSentences[1] (page_copy.prologue.sentences[1])
// 3. page_copy.caveat.notes[0].title (yogurt_spoonable_frontend_v1.json)
const YOGURT_SPOONABLE_INSIGHT_LINES = [
  "חלק מהיוגורטים מבוססים על חלב וחיידקי יוגורט בלבד, אחרים על ממתיקים ומייצבים",
  "בין היוגורטים המוצקים שנבדקו כאן יש טווח רחב מאוד בכמות החלבון",
  "הסוכר ביוגורט המוצק נבדק יחסית למדף עצמו",
] as const;

export function FeaturedYogurtIntelligenceCard({ href, description }: Props) {
  const stats = deriveComparisonCardStats(yogurtSpoonableProducts, yogurtSpoonableCorpusMeta.generated);

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
        categoryTags="יוגורט · יוגורט מוצק · יווני"
        title={yogurtSpoonableHero.title}
        description={stripCardDigits(description)}
        insightLines={[...YOGURT_SPOONABLE_INSIGHT_LINES].map(stripCardDigits)}
        stats={[
          { value: stats.productCount, label: "מוצרים בהשוואה" },
          { value: stats.scoredCount, label: "קיבלו ציון" },
          { value: stats.gradeCounts.A, label: "בציון A" },
        ]}
        updatedLabel={stats.updatedLabel}
        asLinkChild
        theme={{ accent: "#238C68", photo: "/hashvaot/themes/yogurt.jpg" }}
        className="group-hover/card:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]"
      />
    </Link>
  );
}
