"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  maadanimCorpusMeta,
  maadanimHero,
  maadanimProducts,
  maadanimPrologueSentences,
} from "@/lib/comparisons/maadanim-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description?: string;
};

const MAADANIM_INSIGHT_LINES = [
  "יוגורט חלבון גבוה לא תמיד מקבל ציון גבוה יותר ממעדן פשוט",
  "מעדנים «דלי שומן» לעיתים נשענים על תוספים למרקם ומתיקות",
  "רשימת רכיבים קצרה לא מבטיחה ציון גבוה — ההקשר הקטגורי נכנס לחישוב",
] as const;

export function FeaturedMaadanimIntelligenceCard({ href, description }: Props) {
  const insightLines = maadanimProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = insightLines.length > 0 ? insightLines.slice(0, 8) : MAADANIM_INSIGHT_LINES;

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="דוח חדש"
        categoryTags="מעדנים · יוגורטים · מוצרי חלבון"
        title={maadanimHero.title}
        description={description ?? maadanimPrologueSentences[0]}
        insightLines={lines}
        stats={[
          { value: maadanimCorpusMeta.product_count, label: "מוצרים בדף" },
          { value: maadanimCorpusMeta.scored_count ?? maadanimProducts.length, label: "קיבלו ציון" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(maadanimCorpusMeta.generated)}
        asLinkChild
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
