"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  milkCorpusMeta,
  milkVmProducts,
  milkPrologueSentences,
} from "@/lib/comparisons/milk-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description?: string;
};

const MILK_INSIGHT_LINES = [
  "משקאות שיבולת שועל נוטים להכיל יותר מייצבים",
  "חלק ממוצרי הסויה מובילים בכמות החלבון",
  "מוצרים עתירי חלבון מגיעים לעיתים עם יותר עיבוד",
  "שקדים דל קלוריות אך גם דל יחסית בחלבון",
  "חלב פרה בסיסי לרוב עם פחות רכיבים תפקודיים מאשר תחליפים",
  "חלק מהמועשרים מציגים סידן או ויטמין D בתווית — ההשוואה מציגה את הפרטים",
] as const;

export function FeaturedMilkIntelligenceCard({ href, description }: Props) {
  const insightLines = milkVmProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = insightLines.length > 0 ? insightLines : MILK_INSIGHT_LINES;
  const cardDescription = description ?? milkPrologueSentences[0];

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="ניתוח מובייל"
        categoryTags="חלב · תחליפי חלב · משקאות חלבון"
        title="השוואת חלב ותחליפי חלב"
        description={cardDescription}
        insightLines={lines}
        stats={[
          { value: milkCorpusMeta.product_count, label: "מוצרים נבדקו" },
          { value: milkCorpusMeta.scored_count ?? milkVmProducts.length, label: "קיבלו ציון" },
          { value: milkVmProducts.length, label: "בדף ההשוואה" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(milkCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#5C7FB0", photo: "/hashvaot/themes/milk.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
