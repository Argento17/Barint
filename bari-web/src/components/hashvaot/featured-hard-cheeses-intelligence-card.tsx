"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  hardCheesesCorpusMeta,
  hardCheesesProducts,
} from "@/lib/comparisons/hard-cheeses-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

const HARD_CHEESES_INSIGHT_LINES = [
  "אף גבינה לא הגיעה ל-A — הציון המרבי הוא 70.8/B, גאודה עם מינימום מרכיבים",
  "גבינה 'לייט' עם מייצבים מקבלת D — המנוע מעניש נכון על עומס תוספים",
  "פרמזן: חלבון 30+ גרם, אבל נתרן 1,400+ מ\"ג מוריד אותו ל-D",
  "האחוז על האריזה הוא שומן בחומר יבש — לא מה שאתם אוכלים בפועל",
] as const;

export function FeaturedHardCheesesIntelligenceCard({ href, description }: Props) {
  const insightLines = hardCheesesProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines =
    insightLines.length > 0 ? insightLines : HARD_CHEESES_INSIGHT_LINES;

  const bCount = hardCheesesProducts.filter((p) => p.grade === "B").length;
  const scoredCount = hardCheesesProducts.filter((p) => p.score != null).length;

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
        title="גבינות קשות: גאודה פשוטה מנצחת 'לייט' עם מייצבים"
        description={description}
        insightLines={lines}
        stats={[
          { value: hardCheesesProducts.length, label: "מוצרים נותחו" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: bCount, label: "בציון B (המרבי)" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(hardCheesesCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#C9A96E", photo: "/hashvaot/themes/hard-cheeses.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
