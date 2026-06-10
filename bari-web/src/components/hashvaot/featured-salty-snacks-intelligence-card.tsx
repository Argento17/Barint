"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  saltySnacksCorpusMeta,
  saltySnacksProducts,
} from "@/lib/comparisons/salty-snacks-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

const SALTY_SNACKS_INSIGHT_LINES = [
  "פצפוצי אורז פשוטים בראש המדף — לא כי הם 'בריאים', כי הם פשוטים",
  "חטיפי קטניות אפויים מגיעים ל-A וB בזכות סיבים וחלבון",
  "במבה: B → C אחרי זיהוי תהליך ניפוח תעשייתי — לא הרכיבים, התהליך",
  "חטיפים 'אפויים' ו'ללא גלוטן' מגיעים לD — הנתרן לא יורד עם השמן",
] as const;

export function FeaturedSaltySnacksIntelligenceCard({ href, description }: Props) {
  const insightLines = saltySnacksProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines = insightLines.length > 0 ? insightLines : SALTY_SNACKS_INSIGHT_LINES;

  const aCount = saltySnacksProducts.filter((p) => p.grade === "A").length;
  const scoredCount = saltySnacksProducts.filter((p) => p.score != null).length;

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
        categoryTags="צ'יפס · פופקורן · פצפוצים · פרצלים"
        title="חטיפים מלוחים: מה מסתתר מאחורי 'אפוי' ו'ללא גלוטן'?"
        description={description}
        insightLines={lines}
        stats={[
          { value: saltySnacksProducts.length, label: "מוצרים נותחו" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(saltySnacksCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#C2452D", photo: "/hashvaot/themes/salty-snacks.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
