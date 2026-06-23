"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { magnesiumProducts } from "@/lib/comparisons/magnesium-page-data";
import { cn } from "@/lib/utils";

// IMAGE ASSET MISSING: /hashvaot/themes/magnesium.jpg does not exist yet.
// The theme.photo field is intentionally omitted below so the card renders
// the accent tint wash + animated backdrop only — no broken image, no product
// photo, no OFF. Commission a stock supplements/magnesium category image and
// place it at public/hashvaot/themes/magnesium.jpg to complete this card.

type Props = {
  href: string;
  description: string;
};

// TASK-384 v3 rebuild: v3 has B grades. Static fallback updated — old "no A or B" claim is wrong.
// Static fallback shown when product insightLines not yet available (pre two-gate sign-off).
const MAGNESIUM_INSIGHT_LINES = [
  "המספר הגדול על האריזה לא אומר כמה מגנזיום מגיע לגוף — הצורה הכימית קובעת",
  "ציטראט וביסגליצינט נספגים טוב יותר מאוקסיד — אבל מינון נמוך גם בצורה טובה ייתן פחות",
  "ארבעה מוצרים עם 450–520 מ\"ג יסודי ביום — מעל הגבול העליון המומלץ לתוספים (IOM)",
  "שלושה מוצרים ללא ציון כי התווית לא מאפשרת חישוב מינון אמין",
] as const;

export function FeaturedMagnesiumIntelligenceCard({ href, description }: Props) {
  const insightLines = magnesiumProducts
    .map((product) => product.insightLine)
    .filter((l) => Boolean(l) && !l.startsWith("[PLACEHOLDER]"));
  const lines = insightLines.length > 0 ? insightLines : MAGNESIUM_INSIGHT_LINES;

  const bCount = magnesiumProducts.filter((p) => p.grade === "B").length;
  const cCount = magnesiumProducts.filter((p) => p.grade === "C").length;
  const dCount = magnesiumProducts.filter((p) => p.grade === "D").length;
  const eCount = magnesiumProducts.filter((p) => p.grade === "E").length;

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
        title="קונים תוסף מגנזיום? הנה מה שהמספר הגדול על האריזה לא אומר לכם"
        description={description}
        insightLines={lines}
        stats={[
          { value: magnesiumProducts.length, label: "מוצרים נותחו" },
          { value: bCount, label: "בציון B" },
          { value: cCount, label: "בציון C" },
          { value: dCount, label: "בציון D" },
        ]}
        updatedLabel="עודכן יוני 2026"
        asLinkChild
        // photo intentionally omitted — asset not yet commissioned.
        // Replace with: theme={{ accent: "#4A7B8C", photo: "/hashvaot/themes/magnesium.jpg" }}
        // once public/hashvaot/themes/magnesium.jpg is available.
        theme={{ accent: "#4A7B8C" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
