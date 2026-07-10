"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  juicesCorpusMeta,
  juicesProducts,
} from "@/lib/comparisons/juices-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("juices").hero;

function stripCardDigits(text: string): string {
  return text
    .replace(/[0-9]+(?:[.,][0-9]+)?/g, "")
    .replace(/\s{2,}/g, " ")
    .replace(/\s+([,.—–])/g, "$1")
    .trim();
}

type Props = {
  href: string;
  description: string;
};

const JUICES_INSIGHT_LINES = [
  "רק מיצים סחוטים 100% מגיעים ל-A — כל השאר יורדים ל-D ול-E",
  "גם מיץ 100% הוא סוכר נוזלי: כל הסוכר של הפרי, בלי הסיבים",
  "נקטרים ומשקאות פרי נשענים על מים, סוכר ורכז — והציון משקף את זה",
  "גם בין מיצי הפרי המלאים יש פער בכמות הסוכר — רימונים מעל תפוזים",
] as const;

export function FeaturedJuicesIntelligenceCard({ href, description }: Props) {
  const insightLines = juicesProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : JUICES_INSIGHT_LINES).map(stripCardDigits);

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
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
        insightLines={lines}
        stats={[
          { value: juicesProducts.length, label: "מוצרים נותחו" },
          { value: scoredCount, label: "קיבלו ציון" },
          { value: aCount, label: "בציון A" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(juicesCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#1F8F6A", photo: "/hashvaot/themes/juices.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
