"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import {
  brinedCheesesCorpusMeta,
  brinedCheesesProducts,
} from "@/lib/comparisons/brined-cheeses-page-data";
import { deriveComparisonCardStats } from "@/lib/derived/comparison-card-stats";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("brined_cheeses").hero;

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

const BRINED_CHEESES_INSIGHT_LINES = [
  "שני רכיבים מול עשרה — הפער הכי גדול בקטגוריה הוא רשימת הרכיבים",
  "A בקטגוריה זו לא אומר נמוך בנתרן — אלא הטוב ביותר שאפשר בגבינה מלוחה",
  "הצפתיות של מחלבות גד מובילות — חלב, מלח ומשמר אחד בלבד",
  "גבינה עם נתרן קיצוני גם יחסית למדף מקבלת חיסרון נוסף",
] as const;

export function FeaturedBrinedCheesesIntelligenceCard({ href, description }: Props) {
  const insightLines = brinedCheesesProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : BRINED_CHEESES_INSIGHT_LINES).map(stripCardDigits);

  const stats = deriveComparisonCardStats(brinedCheesesProducts, brinedCheesesCorpusMeta.generated);

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
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={lines}
        stats={[
          { value: stats.productCount, label: "מוצרים נותחו" },
          { value: stats.scoredCount, label: "קיבלו ציון" },
          { value: stats.gradeCounts.A, label: "בציון A" },
          { value: stats.gradeCounts.B, label: "בציון B" },
        ]}
        updatedLabel={stats.updatedLabel}
        asLinkChild
        theme={{
          accent: "#176F53",
          photo: "/hashvaot/themes/brined-cheeses.jpg",
        }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
