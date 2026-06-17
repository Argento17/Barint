"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  cookiesCoffeeCorpusMeta,
  cookiesCoffeeHero,
  cookiesCoffeeProducts,
} from "@/lib/comparisons/cookies-coffee-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

const COOKIES_COFFEE_INSIGHT_LINES = [
  "ציון C הוא תקרת הקטגוריה — אין כאן מוצר ללא תווית אדומה לפחות אחת",
  "ההבדל בין C ל-E הוא בסוג השומן ובמידת הפשטות של רשימת הרכיבים",
  "נתרן אינו הנושא — הוא נמוך בכל המוצרים ואינו מה שמבדיל כאן",
] as const;

export function FeaturedCookiesCoffeeIntelligenceCard({ href, description }: Props) {
  const insightLines = cookiesCoffeeProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines =
    insightLines.length > 0 ? insightLines : COOKIES_COFFEE_INSIGHT_LINES;

  const cCount = cookiesCoffeeProducts.filter((p) => p.grade === "C").length;
  const dCount = cookiesCoffeeProducts.filter((p) => p.grade === "D").length;
  const eCount = cookiesCoffeeProducts.filter((p) => p.grade === "E").length;

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
        categoryTags="ביסקוויטים · לוטוס · ליים · קרמבו · מריה"
        title={cookiesCoffeeHero.title}
        description={description}
        insightLines={lines}
        stats={[
          { value: cookiesCoffeeProducts.length, label: "מוצרים נותחו" },
          { value: eCount, label: "בציון E" },
          { value: cCount, label: "בציון C" },
          { value: dCount, label: "בציון D" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(cookiesCoffeeCorpusMeta.generated)}
        asLinkChild
        theme={{
          accent: "#C4975A",
          // Stock CATEGORY image only — product images are banned on cards (owner ruling 2026-06-14).
          photo: "/hashvaot/themes/cookies-coffee.jpg",
        }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
