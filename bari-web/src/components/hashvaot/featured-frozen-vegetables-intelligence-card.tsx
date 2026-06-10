"use client";

import Link from "next/link";

import { ComparisonIntelligenceHero } from "@/components/comparisons/comparison-intelligence-hero";
import { formatComparisonUpdatedLine } from "@/lib/comparisons/format-comparison-updated-line";
import {
  corpusMeta as frozenVegetablesCorpusMeta,
  frozenVegetablesBands,
  frozenVegetablesHero,
  frozenVegetablesPrologueSentences,
  frozenVegetablesV2Products,
} from "@/lib/comparisons/frozen-vegetables-comparison-page-data";
import { cn } from "@/lib/utils";

type Props = {
  href: string;
  description?: string;
};

// TASK-235 Phase 4 — SCORE-FREE index card for Frozen Vegetables v2.
// No score, no grade, no "A"/"S", no scored-count. The frozen shelf is presented by its
// four kitchen-use bands; counts are per-band totals, never quality tiers.
export function FeaturedFrozenVegetablesIntelligenceCard({ href, description }: Props) {
  const cardDescription = description ?? frozenVegetablesPrologueSentences[0];

  const displayedCount = frozenVegetablesV2Products.length;
  const bandCount = frozenVegetablesBands.length;

  const bandTotals = new Map<string, number>();
  for (const product of frozenVegetablesV2Products) {
    bandTotals.set(product.band, (bandTotals.get(product.band) ?? 0) + 1);
  }

  // Score-free insight lines: what each use-band is, and that the page does not rank or score.
  const insightLines = [
    ...frozenVegetablesBands.map((band) => {
      const count = bandTotals.get(band.id) ?? 0;
      return `${band.title}: ${count} מוצרים — ${band.standingMarker}`;
    }),
    "אין כאן ציון ואין דירוג — כל מוצר מתואר לפי מה שהוא מביא לשימוש שלו",
  ] as readonly string[];

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
        categoryTags="ירקות קפואים · שופרסל"
        title={frozenVegetablesHero.title}
        description={cardDescription}
        insightLines={insightLines}
        stats={[
          { value: displayedCount, label: "מוצרים בהשוואה" },
          { value: bandCount, label: "שימושים במטבח" },
        ]}
        updatedLabel={formatComparisonUpdatedLine(frozenVegetablesCorpusMeta.generated)}
        asLinkChild
        theme={{ accent: "#1F8F6A", photo: "/hashvaot/themes/vegetables.jpg" }}
        className="group-hover/card:border-[#1F8F6A]/30 group-hover/card:shadow-[0_40px_120px_-58px_rgba(31,143,106,0.28),0_0_60px_-26px_rgba(31,143,106,0.08)]"
      />
    </Link>
  );
}
