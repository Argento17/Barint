"use client";

import Link from "next/link";

import {
  ComparisonIntelligenceHero,
} from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  granolaCorpusMeta,
  granolaProducts,
} from "@/lib/comparisons/granola-page-data";
import { cn } from "@/lib/utils";

const INSIGHT_LINES = [
  "אף מוצר לא מגיע ל-A — הטוב ביותר עוצר ב-76/B",
  "פער של 47 נקודות בין הגבוה לנמוך",
  "הסוכר, השומן והסירופ קובעים את הציון — לא תדמית הבריאות",
  "גרנולת חלבון מול מוזלי פירות — אותו מדף, ציונים רחוקים",
] as const;

type Props = {
  href: string;
  description: string;
};

export function FeaturedGranolaIntelligenceCard({ href, description }: Props) {
  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#7A8C5E]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="קטגוריה חדשה"
        categoryTags="גרנולה · מוזלי · דגן אפוי"
        title="גרנולה ומוזלי: 53 מוצרים, פער של 47 נקודות"
        description={description}
        insightLines={INSIGHT_LINES}
        stats={[
          { value: granolaProducts.length, label: "מוצרים נותחו" },
          { value: 38, label: "פרמטרים הושוו" },
          { value: 47, label: "נקודות פער" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(granolaCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#7A8C5E", photo: "/hashvaot/themes/granola.jpg" }}
        className="group-hover/card:border-[#7A8C5E]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(122,140,94,0.28),0_0_60px_-26px_rgba(122,140,94,0.08)]"
      />
    </Link>
  );
}
