"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  cakesHardCookiesCorpusMeta,
  cakesHardCookiesHero,
  cakesHardCookiesProducts,
} from "@/lib/comparisons/cakes-hard-cookies-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description: string;
};

const CAKES_INSIGHT_LINES = [
  "ציון C הוא תקרת הקטגוריה — אין כאן מוצר ללא תווית אדומה לפחות אחת",
  "ההבדל בין C ל-E הוא בסוג השומן, כמות הסוכר ומורכבות רשימת הרכיבים",
  "שמן דקל מוקשה ושומן צמחי מוקשה חלקית מסבירים רבים מציוני ה-E",
] as const;

export function FeaturedCakesHardCookiesIntelligenceCard({ href, description }: Props) {
  const insightLines = cakesHardCookiesProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines =
    insightLines.length > 0 ? insightLines : CAKES_INSIGHT_LINES;

  const cCount = cakesHardCookiesProducts.filter((p) => p.grade === "C").length;
  const dCount = cakesHardCookiesProducts.filter((p) => p.grade === "D").length;
  const eCount = cakesHardCookiesProducts.filter((p) => p.grade === "E").length;

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
        categoryTags="עוגות גבינה · עוגות פס · מאפינים · שטרודל · קרנץ"
        title={cakesHardCookiesHero.title}
        description={description}
        insightLines={lines}
        stats={[
          { value: cakesHardCookiesProducts.length, label: "מוצרים נותחו" },
          { value: cCount, label: "בציון C" },
          { value: dCount, label: "בציון D" },
          { value: eCount, label: "בציון E" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(cakesHardCookiesCorpusMeta.generated)}
        asLinkChild
        theme={{
          accent: "#C4975A",
          // Stock CATEGORY image only — product images are banned on cards (owner ruling 2026-06-14).
          photo: "/hashvaot/themes/cakes-hard-cookies.jpg",
        }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
