"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  chocolateBarsCorpusMeta,
  chocolateBarsProducts,
} from "@/lib/comparisons/chocolate-bars-comparison-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

const CHOCOLATE_BARS_INSIGHT_LINES = [
  "כל החטיפים מקבלים E — אבל יש הבדל בין ממתק עם בוטנים לממתק של סוכר בלבד",
  "45–60 גרם סוכר ל-100 גרם הוא הטווח שמגדיר את כל המדף הזה",
  "המילה 'חטיף' היא שיווק — זהו מדף ממתקים לכל דבר",
] as const;

export function FeaturedChocolateBarsIntelligenceCard({ href, description }: Props) {
  const insightLines = chocolateBarsProducts.map((product) => product.insightLine).filter(Boolean);
  const lines = insightLines.length > 0 ? insightLines : CHOCOLATE_BARS_INSIGHT_LINES;

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
        categoryTags="חטיפי שוקולד · שופרסל"
        title="השוואת חטיפי שוקולד"
        description={description}
        insightLines={lines}
        stats={[
          { value: chocolateBarsProducts.length, label: "בדף ההשוואה" },
          { value: "E", label: "ציון כל המוצרים" },
          { value: "45–60", label: "גרם סוכר ל-100 גרם" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(chocolateBarsCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#3D2314", photo: "/hashvaot/themes/cakes-hard-cookies.jpg" }}
        className="group-hover/card:border-[#3D2314]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(61,35,20,0.28),0_0_60px_-26px_rgba(61,35,20,0.08)]"
      />
    </Link>
  );
}
