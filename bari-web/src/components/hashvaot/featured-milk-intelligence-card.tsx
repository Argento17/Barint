"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import {
  milkCorpusMeta,
  milkVmProducts,
  milkPrologueSentences,
} from "@/lib/comparisons/milk-page-data";
import { deriveComparisonCardStats } from "@/lib/derived/comparison-card-stats";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("milk").hero;

function stripCardDigits(text: string): string {
  return text
    .replace(/[0-9]+(?:[.,][0-9]+)?/g, "")
    .replace(/\s{2,}/g, " ")
    .replace(/\s+([,.—–])/g, "$1")
    .trim();
}

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
  const lines = (insightLines.length > 0 ? insightLines : MILK_INSIGHT_LINES).map(stripCardDigits);
  const cardDescription = description ?? milkPrologueSentences[0];
  const stats = deriveComparisonCardStats(milkVmProducts, milkCorpusMeta.generated);

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
        title={CARD_HERO.title}
        description={stripCardDigits(cardDescription)}
        insightLines={lines}
        stats={[
          { value: stats.productCount, label: "מוצרים נבדקו" },
          { value: stats.scoredCount, label: "קיבלו ציון" },
          { value: stats.productCount, label: "בדף ההשוואה" },
        ]}
        updatedLabel={stats.updatedLabel}
        asLinkChild
        theme={{ accent: "#2E7D60", photo: "/hashvaot/themes/milk.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
