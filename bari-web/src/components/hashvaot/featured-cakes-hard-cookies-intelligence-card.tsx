"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  cakesHardCookiesCorpusMeta,
  cakesHardCookiesProducts,
} from "@/lib/comparisons/cakes-hard-cookies-page-data";
import { getComparisonPageChrome } from "@/lib/site-content/comparison-page-chrome";
import { cn } from "@/lib/utils";

const CARD_HERO = getComparisonPageChrome("cakes_hard_cookies").hero;

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

const CAKES_INSIGHT_LINES = [
  "ציון C הוא תקרת הקטגוריה — אין כאן מוצר ללא תווית אדומה לפחות אחת",
  "ההבדל בין C ל-E הוא בסוג השומן, כמות הסוכר ומורכבות רשימת הרכיבים",
  "שמן דקל מוקש ושומן צמחי מוקש חלקית מסבירים רבים מציוני ה-E",
] as const;

export function FeaturedCakesHardCookiesIntelligenceCard({ href, description }: Props) {
  const insightLines = cakesHardCookiesProducts
    .map((product) => product.insightLine)
    .filter(Boolean);
  const lines = (insightLines.length > 0 ? insightLines : CAKES_INSIGHT_LINES).map(stripCardDigits);

  const cCount = cakesHardCookiesProducts.filter((p) => p.grade === "C").length;
  const dCount = cakesHardCookiesProducts.filter((p) => p.grade === "D").length;
  const eCount = cakesHardCookiesProducts.filter((p) => p.grade === "E").length;

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-[3px] motion-reduce:transition-none motion-reduce:hover:translate-y-0",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="חדש"
        categoryTags="עוגות גבינה · עוגות פס · מאפינים · שטרודל · קרנץ"
        title={CARD_HERO.title}
        description={stripCardDigits(description)}
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
          photo: "/hashvaot/themes/cakes-hard-cookies.jpg",
        }}
        className="group-hover/card:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]"
      />
    </Link>
  );
}
