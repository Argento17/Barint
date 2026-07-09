"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  brinedCheesesCorpusMeta,
  brinedCheesesProducts,
} from "@/lib/comparisons/brined-cheeses-page-data";
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
  "שלושה רכיבים מול שמונה — הפער הכי גדול בקטגוריה הוא רשימת הרכיבים",
  "A בקטגוריה זו לא אומר נמוך בנתרן — אלא הטוב ביותר שאפשר בגבינה מלוחה",
  "פטה עיזים מובילה — חלב, מלח ומשמר אחד בלבד",
  "גבינה עם נתרן קיצוני גם יחסית למדף מקבלת חיסרון נוסף",
] as const;

export function FeaturedBrinedCheesesIntelligenceCard({ href, description }: Props) {
  const insightLines = brinedCheesesProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : BRINED_CHEESES_INSIGHT_LINES).map(stripCardDigits);

  const aCount = brinedCheesesProducts.filter((p) => p.grade === "A").length;
  const bCount = brinedCheesesProducts.filter((p) => p.grade === "B").length;
  const scoredCount = brinedCheesesProducts.filter((p) => p.score != null).length;

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
        categoryTags="בולגרית · פטה · צפתית · חלומי"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
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
          accent: "#176F53",
          photo: "/hashvaot/themes/brined-cheeses.jpg",
        }}
        className="group-hover/card:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]"
      />
    </Link>
  );
}
