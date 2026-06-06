"use client";

import Link from "next/link";

import {
  ComparisonIntelligenceHero,
} from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  butterCorpusMeta,
  butterProducts,
} from "@/lib/comparisons/butter-page-data";
import { cn } from "@/lib/utils";

const INSIGHT_LINES = [
  "חמאה טהורה (שמנת בלבד) מקבלת B/70 — מזון שלם, עיבוד נמוך",
  "פער של 25 נקודות בין הפשוטה לממורחת המתובלת",
  "הרכיבים, לא השומן, קובעים את הציון",
  "גהי, חמאה מותססת וממרחים מרוכבים — כולם בדף אחד",
] as const;

type Props = {
  href: string;
  description: string;
};

export function FeaturedButterIntelligenceCard({ href, description }: Props) {
  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#C8A96E]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="קטגוריה חדשה"
        categoryTags="חמאה · גהי · ממרחי חמאה"
        title="חמאה: 39 מוצרים, פער של 25 נקודות"
        description={description}
        insightLines={INSIGHT_LINES}
        stats={[
          { value: butterProducts.length, label: "מוצרים נותחו" },
          { value: 38, label: "פרמטרים הושוו" },
          { value: 25, label: "נקודות פער" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(butterCorpusMeta.generated)}
        asLinkChild
        theme={{
          accent: "#C8A96E",
          photo: "/hashvaot/themes/butter.jpg",
        }}
        className="group-hover/card:border-[#C8A96E]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(200,169,110,0.28),0_0_60px_-26px_rgba(200,169,110,0.08)]"
      />
    </Link>
  );
}
