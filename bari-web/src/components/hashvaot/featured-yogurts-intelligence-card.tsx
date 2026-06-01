"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  yogurtsCorpusMeta,
  yogurtsProducts,
  yogurtsPrologueSentences,
} from "@/lib/comparisons/yogurts-comparison-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description?: string;
};

const YOGURTS_INSIGHT_LINES = [
  "2 מרכיבים מול 8+ — הפער הכי גדול בקטגוריה הוא רשימת הרכיבים, לא המותג",
  "יווני/מסוי מוביל בחלבון — אבל לא תמיד בציון אם יש תוספים",
  "יוגורט 0% טבעי מקבל ציון גבוה ממוצר בטעמים עם אותו 0%",
  "מילקי ויוגורט שתיה — קצה תחתון: מוצרי הנאה, לא בסיס",
] as const;

export function FeaturedYogurtsIntelligenceCard({ href, description }: Props) {
  const insightLines = yogurtsProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = insightLines.length > 0 ? insightLines : YOGURTS_INSIGHT_LINES;
  const cardDescription = description ?? yogurtsPrologueSentences[0];

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
        categoryTags="יוגורטים · מדף ישראלי"
        title='יוגורט: לא כל "טבעי" נוצר שווה'
        description={cardDescription}
        insightLines={lines}
        stats={[
          { value: yogurtsCorpusMeta.product_count, label: "מוצרים נבדקו" },
          { value: yogurtsCorpusMeta.scored_count ?? yogurtsProducts.length, label: "קיבלו ציון" },
          { value: yogurtsProducts.length, label: "בדף ההשוואה" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(yogurtsCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#BC7AA0", photo: "/hashvaot/themes/yogurt.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
