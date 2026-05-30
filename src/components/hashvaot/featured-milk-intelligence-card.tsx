"use client";

import Link from "next/link";
import { useMemo } from "react";

import {
  ComparisonIntelligenceHero,
} from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  milkComparisonPage,
  milkProducts,
  PRIMARY_DIMENSION_KEYS,
} from "@/lib/comparisons/milk-page-data";
import { cn } from "@/lib/utils";

const INSIGHT_LINES = [
  "משקאות שיבולת שועל נוטים להכיל יותר מייצבים",
  "חלק ממוצרי הסויה מובילים בכמות החלבון",
  "מוצרים עתירי חלבון מגיעים לעיתים עם יותר עיבוד",
  "שקדים דל קלוריות אך גם דל יחסית בחלבון",
  "חלב פרה בסיסי לרוב עם פחות רכיבים תפקודיים מאשר תחליפים",
  "חלק מהמועשרים מציגים סידן או ויטמין D בתווית — ההשוואה מציגה את הפרטים",
] as const;

type Props = {
  href: string;
  description: string;
};

export function FeaturedMilkIntelligenceCard({ href, description }: Props) {
  const metadata = useMemo(() => {
    const productCount = milkProducts.length;
    const categoryKeys = new Set(milkProducts.map((p) => p.productType));
    const pillarCount =
      milkProducts.find((p) => p.bariInterpretation?.length)?.bariInterpretation?.length ?? 6;
    const paramSlots = PRIMARY_DIMENSION_KEYS.length * pillarCount;
    return {
      productCount,
      categoryCount: categoryKeys.size,
      paramCount: paramSlots >= 42 ? paramSlots : 42,
    };
  }, []);

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="דוח ראשון"
        categoryTags="חלב · תחליפי חלב · משקאות חלבון"
        title={milkComparisonPage.comparison_title}
        description={description}
        insightLines={INSIGHT_LINES}
        stats={[
          { value: metadata.productCount, label: "מוצרים נותחו" },
          { value: metadata.paramCount, label: "פרמטרים הושוו" },
          { value: metadata.categoryCount, label: "קטגוריות" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(milkComparisonPage.generated_at)}
        asLinkChild
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
