"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  juicesCorpusMeta,
  juicesProducts,
} from "@/lib/comparisons/juices-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

const JUICES_INSIGHT_LINES = [
  "A אחד בכל הקטגוריה — סחוט תפוזים טרי בלבד",
  "גם סחוט קר מגיע ל-C: סוכר נוזלי מנצח את ה'בריאות' על האריזה",
  "נקטרים עם 25–99% פרי נופלים ל-C ו-D — הפרי הדומיננטי הוא סוכר",
  "טווח הסוכר במיץ 100%: 1.75–16.8 גרם ל-100 מ\"ל — פער עצום בתוך אותה קטגוריה",
] as const;

export function FeaturedJuicesIntelligenceCard({ href, description }: Props) {
  const insightLines = juicesProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines = insightLines.length > 0 ? insightLines : JUICES_INSIGHT_LINES;

  const aCount = juicesProducts.filter((p) => p.grade === "A").length;
  const scoredCount = juicesProducts.filter((p) => p.score != null).length;

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
        categoryTags="מיצים · נקטרים · משקאות פירות"
        title="מיצים ומשקאות פירות: מה בין סחוט טרי למשקה פירות?"
        description={description}
        insightLines={lines}
        stats={[
          { value: juicesProducts.length, label: "מוצרים נותחו" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(juicesCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#E8A020", photo: "/hashvaot/themes/juices.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
