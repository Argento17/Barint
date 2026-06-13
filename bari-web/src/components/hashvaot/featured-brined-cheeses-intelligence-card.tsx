"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  brinedCheesesCorpusMeta,
  brinedCheesesHero,
  brinedCheesesHeroImageUrl,
  brinedCheesesProducts,
} from "@/lib/comparisons/brined-cheeses-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

const BRINED_CHEESES_INSIGHT_LINES = [
  "שלושה רכיבים מול שמונה — הפער הכי גדול בקטגוריה הוא רשימת הרכיבים",
  "A בקטגוריה זו לא אומר 'נמוך בנתרן' — אלא הטוב ביותר שאפשר בגבינה מלוחה",
  "פטה עיזים 5% מובילה — חלב, מלח ומשמר אחד בלבד",
  "גבינה עם נתרן קיצוני גם יחסית למדף מקבלת חיסרון נוסף",
] as const;

export function FeaturedBrinedCheesesIntelligenceCard({ href, description }: Props) {
  const insightLines = brinedCheesesProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines =
    insightLines.length > 0 ? insightLines : BRINED_CHEESES_INSIGHT_LINES;

  const aCount = brinedCheesesProducts.filter((p) => p.grade === "A").length;
  const bCount = brinedCheesesProducts.filter((p) => p.grade === "B").length;
  const scoredCount = brinedCheesesProducts.filter((p) => p.score != null).length;

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
        categoryTags="בולגרית · פטה · צפתית · חלומי"
        title={brinedCheesesHero.title}
        description={description}
        insightLines={lines}
        stats={[
          { value: brinedCheesesProducts.length, label: "מוצרים נותחו" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aCount, label: "בציון A" },
          { value: bCount, label: "בציון B" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(brinedCheesesCorpusMeta.generated)}
        asLinkChild
        theme={{
          accent: "#7FA8B8",
          photo: brinedCheesesHeroImageUrl ?? undefined,
        }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
