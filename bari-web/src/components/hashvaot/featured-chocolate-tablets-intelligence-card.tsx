"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  chocolateTabletCorpusMeta,
  chocolateTabletsProducts,
} from "@/lib/comparisons/chocolate-tablets-comparison-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

const CHOCOLATE_TABLETS_INSIGHT_LINES = [
  "מריר 90% — שני גרם סוכר ל-100 גרם. שוקולד לבן — 58 גרם. הפער הוא 29x",
  "הציון הגבוה ביותר בקטגוריה הוא C — שוקולד הוא ממתק",
  "ככל שאחוז הקקאו עולה, הסוכר יורד ורשימת הרכיבים מתקצרת",
] as const;

export function FeaturedChocolateTabletsIntelligenceCard({ href, description }: Props) {
  const insightLines = chocolateTabletsProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = insightLines.length > 0 ? insightLines : CHOCOLATE_TABLETS_INSIGHT_LINES;

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
        categoryTags="טבלאות שוקולד · שופרסל"
        title="השוואת טבלאות שוקולד"
        description={description}
        insightLines={lines}
        stats={[
          { value: chocolateTabletsProducts.length, label: "בדף ההשוואה" },
          { value: "C", label: "תקרת הקטגוריה" },
          { value: "90%", label: "אחוז קקאו מקסימלי" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(chocolateTabletCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#5C3D2E", photo: "/hashvaot/themes/chocolate-tablets.jpg" }}
        className="group-hover/card:border-[#5C3D2E]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(92,61,46,0.28),0_0_60px_-26px_rgba(92,61,46,0.08)]"
      />
    </Link>
  );
}
