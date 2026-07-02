"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { magnesiumProducts } from "@/lib/comparisons/magnesium-page-data";
import { cn } from "@/lib/utils";


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

// TASK-384 v3 rebuild: v3 has B grades. Static fallback updated — old "no A or B" claim is wrong.
const MAGNESIUM_INSIGHT_LINES = [
  "המספר הגדול על האריזה לא אומר כמה מגנזיום מגיע לגוף — הצורה הכימית קובעת",
  "ציטראט וביסגליצינט נספגים טוב יותר מאוקסיד — אבל מינון נמוך גם בצורה טובה ייתן פחות",
  "ארבעה מוצרים עם מינון מעל הגבול העליון המומלץ לתוספים (IOM)",
  "שלושה מוצרים ללא ציון כי התווית לא מאפשרת חישוב מינון אמין",
] as const;

export function FeaturedMagnesiumIntelligenceCard({ href, description }: Props) {
  const insightLines = magnesiumProducts
    .map((product) => product.insightLine)
    .filter((l) => Boolean(l) && !l.startsWith("[PLACEHOLDER]"));
  const lines = (insightLines.length > 0 ? insightLines : MAGNESIUM_INSIGHT_LINES).map(stripCardDigits);

  const bCount = magnesiumProducts.filter((p) => p.grade === "B").length;
  const cCount = magnesiumProducts.filter((p) => p.grade === "C").length;
  const dCount = magnesiumProducts.filter((p) => p.grade === "D").length;

  return (
    <Link
      href={href}
      className={cn(
        "group/card block transition-[transform] duration-500 ease-out hover:-translate-y-1",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1F8F6A]"
      )}
    >
      <ComparisonIntelligenceHero
        badge="מעודכן"
        categoryTags="מגנזיום · תוספי תזונה · ישראל"
        title="קונים תוסף מגנזיום? הצורה הכימית היא שקובעת כמה מהמגנזיום ייספג בגוף — הרבה יותר מהספרה הגדולה על האריזה"
        description={stripCardDigits(description)}
        insightLines={lines}
        stats={[
          { value: magnesiumProducts.length, label: "מוצרים נותחו" },
          { value: bCount, label: "בציון B" },
          { value: cCount, label: "בציון C" },
          { value: dCount, label: "בציון D" },
        ]}
        updatedLabel="עודכן יוני 2026"
        asLinkChild
        theme={{ accent: "#4A7B8C", photo: "/hashvaot/themes/magnesium.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
