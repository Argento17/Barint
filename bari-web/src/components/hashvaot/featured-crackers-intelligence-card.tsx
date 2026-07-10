"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  crackersCorpusMeta,
  crackersHero,
  crackersProducts,
} from "@/lib/comparisons/crackers-page-data";
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

const CRACKERS_INSIGHT_LINES = [
  "לא כל קרקר שנראה בריא באמת מבוסס על דגן מלא",
  "אורך רשימת הרכיבים ומספר מקורות הסוכר מפרידים בין המוצרים",
  "כל קרקר מושווה מול קרקרים אחרים בלבד — לא מול לחם",
] as const;

export function FeaturedCrackersIntelligenceCard({ href, description }: Props) {
  const displayedCount = crackersProducts.length;
  const scoredCount = crackersProducts.filter((product) => product.score != null).length;
  const aGradeCount = crackersProducts.filter((product) => product.grade === "A").length;

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="קטגוריה חדשה"
        categoryTags="קרקרים · קרקר דק · פריכיות"
        title={crackersHero.title}
        description={stripCardDigits(description)}
        insightLines={[...CRACKERS_INSIGHT_LINES].map(stripCardDigits)}
        stats={[
          { value: displayedCount, label: "מוצרים בהשוואה" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aGradeCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(crackersCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#1F8F6A", photo: "/hashvaot/themes/crackers.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
