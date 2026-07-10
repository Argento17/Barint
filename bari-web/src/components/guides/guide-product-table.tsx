"use client";

// Guide layer 2 — product recommendation-tier table (TASK-504 4-tier build, replaces
// the earlier bucket-label rendering). Groups products into the 4 RANKED tiers
// (מומלץ מאוד / מומלץ / טוב / לא מומלץ), in that fixed order, derived from bar-states
// via `computeRecommendationTier` — never a hardcoded product-id list (see
// src/lib/guides/guide-recommendation-tiers.ts). `cannot_assess` products (a genuine
// data gap, e.g. TRIOMAG) render in a SEPARATE section below the 4 tiers, never folded
// into לא מומלץ — rubric `recommendation_tier_mapping.tiers[cannot_assess].display_position`.
//
// Tiers are unordered internally — array order within a tier carries no ranking signal
// (no re-sort; this preserves the products array's own stable order).

import { Check } from "lucide-react";

import {
  GUIDE_BUCKET_LABELS_HE,
  GUIDE_RECOMMENDATION_TIER_LABELS_HE,
  GUIDE_RECOMMENDATION_TIER_ORDER,
  GUIDE_BAR_ORDER,
  type GuideBarKey,
  type GuideHeadlineFinding as GuideHeadlineFindingVM,
  type GuideProductVM,
  type GuideRecommendationTier,
  type GuideThresholdGeometry,
} from "@/lib/view-models";
import { computeRecommendationTier } from "@/lib/guides/guide-recommendation-tiers";
import { GUIDE_BAR_TONE } from "@/components/shared/bar-state-badge";
import { GuideProductRow } from "@/components/guides/guide-product-row";
import { GuideHeadlineFinding } from "@/components/guides/guide-headline-finding";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

// Tier-header verdict palette (Design spec magnesium_guide_verdict_color_spec_v1.md
// §2.2/§3) — ONE shared token system with the bar-state chip: 3 of the 5 tiers reuse a
// `GUIDE_BAR_TONE` entry EXACTLY (very_recommended=pass, good=flag, not_recommended=
// fail, cannot_assess=cannot_verify); `recommended` is the one genuinely new,
// tier-only "bridge" tone (spec §2.3: same 166° hue as pass, lighter/less saturated —
// the composite "clears every bar except a single flagged dose" case, not identical to
// either neighbor). Contrast (spec §2.2): very_recommended 6.73:1, recommended 5.42:1,
// good 5.56:1, not_recommended 6.29:1, cannot_assess 6.71:1 — all clear AA.
const TIER_TONE: Record<
  GuideRecommendationTier | "cannot_assess",
  { bg: string; border: string; text: string; icon: typeof Check }
> = {
  very_recommended: GUIDE_BAR_TONE.pass,
  recommended: { bg: "#E9F5F0", border: "#146F5F33", text: "#146F5F", icon: Check },
  good: GUIDE_BAR_TONE.flag,
  not_recommended: GUIDE_BAR_TONE.fail,
  cannot_assess: GUIDE_BAR_TONE.cannot_verify,
};

function groupByTier(
  products: GuideProductVM[],
  displayedBars: readonly GuideBarKey[],
  bandExcludedBars: readonly GuideBarKey[]
): { tiers: Record<GuideRecommendationTier, GuideProductVM[]>; cannotAssess: GuideProductVM[] } {
  const tiers = {
    very_recommended: [],
    recommended: [],
    good: [],
    not_recommended: [],
  } as Record<GuideRecommendationTier, GuideProductVM[]>;
  const cannotAssess: GuideProductVM[] = [];

  for (const product of products) {
    const tier = computeRecommendationTier(product, displayedBars, bandExcludedBars);
    if (tier === null) {
      cannotAssess.push(product);
    } else {
      tiers[tier].push(product);
    }
  }

  // No within-tier sort — products render in stable source-array order (Product §7:
  // tiers are unordered internally, array order carries no ranking signal).
  return { tiers, cannotAssess };
}

function TierSectionHeader({
  label,
  count,
  tone,
}: {
  label: string;
  count: number;
  tone: { bg: string; border: string; text: string; icon: typeof Check };
}) {
  const Icon = tone.icon;
  return (
    <div className="mb-3 flex items-center gap-2 rounded-xl">
      {/* Verdict-color spec v1 §2.1: the plain gray mono <h2> becomes a colored pill —
          count + trailing hairline divider stay pixel-identical to before (spec: "do
          not touch their styling, spacing"). */}
      <h2
        className="inline-flex items-center gap-1.5 whitespace-nowrap rounded-full font-extrabold"
        style={{
          padding: "5px 12px",
          fontSize: "13px",
          backgroundColor: tone.bg,
          border: `1px solid ${tone.border}`,
          color: tone.text,
        }}
      >
        <Icon aria-hidden size={13} strokeWidth={2.25} />
        {label}
      </h2>
      <span className="text-[11px] font-semibold text-[#4E5663]">({count})</span>
      <span className="h-px flex-1 bg-black/[0.06]" aria-hidden />
    </div>
  );
}

export function GuideProductTable({
  products,
  buyLinkDisclosureLine,
  headlineFinding,
  suppressedBars,
  suppressedBarsDisclosureHe,
  recommendationTierCaptions,
  veryRecommendedEmptyStateHe,
  cannotAssessSectionIntroHe,
  expanderLabels,
  thresholdGeometry,
  bandExcludedBars,
  domesticBandsDisclosureHe,
  benchmarkProducts,
  benchmarkSectionHeadingHe,
  wide = false,
}: {
  products: GuideProductVM[];
  buyLinkDisclosureLine: string;
  /** Rendered above the tier list — the guide's own honest headline finding. */
  headlineFinding?: GuideHeadlineFindingVM | null;
  /** rubric display_suppression_rule bars. Passed straight through to every
   *  GuideProductRow; also gates the guide-level disclosure line below and the
   *  dose_adequacy_sole_caveat predicate's "displayed bars" scope. */
  suppressedBars?: GuideBarKey[];
  /** See GuidePageVM.suppressedBarsDisclosureHe. RT-7: rendered in the SAME view as
   *  the tier list (this section), so the tier captions' "the only reservation is
   *  dose" framing stays honest about what else isn't shown. */
  suppressedBarsDisclosureHe?: string | null;
  /** See GuidePageVM.recommendationTierCaptions. */
  recommendationTierCaptions?: Partial<Record<GuideRecommendationTier, string>>;
  /** See GuidePageVM.veryRecommendedEmptyStateHe. */
  veryRecommendedEmptyStateHe?: string | null;
  /** See GuidePageVM.cannotAssessSectionIntroHe. */
  cannotAssessSectionIntroHe?: string | null;
  /** See GuidePageVM.expanderLabels. */
  expanderLabels?: { collapsed: string; expanded: string };
  /** See GuidePageVM.thresholdGeometry. */
  thresholdGeometry?: Partial<Record<GuideBarKey, GuideThresholdGeometry>>;
  bandExcludedBars?: GuideBarKey[];
  domesticBandsDisclosureHe?: string | null;
  benchmarkProducts?: GuideProductVM[];
  benchmarkSectionHeadingHe?: string | null;
  wide?: boolean;
}) {
  const displayedBars = GUIDE_BAR_ORDER.filter((bar) => !suppressedBars?.includes(bar));
  const excluded = bandExcludedBars ?? [];
  const { tiers, cannotAssess } = groupByTier(products, displayedBars, excluded);

  return (
    <section
      id="guide-products"
      className={cn("px-4 py-4", wide && cn(comparisonWebSectionPaddingClass(), "lg:py-6"))}
      dir="rtl"
      data-testid="guide-product-table"
    >
      {/* Plan §4 on-page mechanical-separation rule, rendered verbatim near the buy
          buttons — never re-authored here. */}
      <p className="text-[11px] leading-relaxed text-[#6B7070]">{buyLinkDisclosureLine}</p>

      {/* RT-7 disclosure adjacency: rendered in the SAME view as the tier list below,
          never on a separate scroll/tab, so the tier captions' "dose is the only
          reservation" framing stays honest about the two bars this build doesn't
          show at all. rubric honesty_constraint: disclosed, never silently vanished. */}
      {suppressedBars && suppressedBars.length > 0 && suppressedBarsDisclosureHe ? (
        <p
          className="mt-1.5 text-[11px] leading-relaxed"
          style={{ color: "#8A6300" }}
          data-testid="guide-suppressed-bars-disclosure"
        >
          {suppressedBarsDisclosureHe}
        </p>
      ) : null}

      {headlineFinding ? (
        <div className="mt-4">
          <GuideHeadlineFinding finding={headlineFinding} />
        </div>
      ) : null}

      {domesticBandsDisclosureHe ? (
        <p
          className="mt-4 text-[12px] leading-[1.55] text-[#3E444A]"
          data-testid="guide-domestic-bands-disclosure"
        >
          {domesticBandsDisclosureHe}
        </p>
      ) : null}

      <div className="mt-4 space-y-8" data-testid="guide-domestic-bands">
        {GUIDE_RECOMMENDATION_TIER_ORDER.map((tier) => {
          const tierProducts = tiers[tier];
          const isEmpty = tierProducts.length === 0;
          // very_recommended renders unconditionally even when empty (rubric
          // empty_state_handling — an empty top tier IS the guide's headline finding,
          // not a display bug to hide). Every other empty tier is simply omitted.
          if (isEmpty && tier !== "very_recommended") return null;

          return (
            <div key={tier} data-testid={`guide-tier-${tier}`}>
              {/* EXCEPTION-003: GUIDE_RECOMMENDATION_TIER_LABELS_HE values are the
                  ONLY sanctioned use of the 4 tier words — field values here, never
                  prose elsewhere on this page. */}
              <TierSectionHeader
                label={GUIDE_RECOMMENDATION_TIER_LABELS_HE[tier]}
                count={tierProducts.length}
                tone={TIER_TONE[tier]}
              />
              {isEmpty ? (
                veryRecommendedEmptyStateHe ? (
                  <p
                    className="-mt-1.5 mb-3 text-[12px] leading-[1.5]"
                    style={{ color: "#6E756D" }}
                    data-testid="guide-tier-empty-state"
                  >
                    {veryRecommendedEmptyStateHe}
                  </p>
                ) : null
              ) : recommendationTierCaptions?.[tier] ? (
                <p
                  className="-mt-1.5 mb-3 text-[12px] leading-[1.5]"
                  style={{ color: "#6E756D" }}
                  data-testid={`guide-tier-caption-${tier}`}
                >
                  {recommendationTierCaptions[tier]}
                </p>
              ) : null}
              {!isEmpty ? (
                <div className="space-y-3">
                  {tierProducts.map((product, i) => (
                    <GuideProductRow
                      key={product.id}
                      product={product}
                      rank={i + 1}
                      suppressedBars={suppressedBars}
                      thresholdGeometry={thresholdGeometry}
                      expanderLabels={expanderLabels}
                    />
                  ))}
                </div>
              ) : null}
            </div>
          );
        })}
      </div>

      {/* cannot_assess — a separate, out-of-tier section (never folded into
          לא מומלץ): a genuine data gap (e.g. TRIOMAG's undisclosed blend) is not an
          actionable negative finding (missing-data-discard doctrine). Reuses the
          existing structural bucket label "לא ניתן להעריך" (GUIDE_BUCKET_LABELS_HE) —
          not one of the 4 EXCEPTION-003 tier words, so no leak-gate concern. */}
      {cannotAssess.length > 0 ? (
        <div className="mt-8" data-testid="guide-tier-cannot-assess-outside">
          <TierSectionHeader
            label={GUIDE_BUCKET_LABELS_HE.cannot_assess}
            count={cannotAssess.length}
            tone={TIER_TONE.cannot_assess}
          />
          {cannotAssessSectionIntroHe ? (
            <p
              className="-mt-1.5 mb-3 text-[12px] leading-[1.5]"
              style={{ color: "#6E756D" }}
              data-testid="guide-cannot-assess-intro"
            >
              {cannotAssessSectionIntroHe}
            </p>
          ) : null}
          <div className="space-y-3">
            {cannotAssess.map((product, i) => (
              <GuideProductRow
                key={product.id}
                product={product}
                rank={i + 1}
                suppressedBars={suppressedBars}
                thresholdGeometry={thresholdGeometry}
                expanderLabels={expanderLabels}
              />
            ))}
          </div>
        </div>
      ) : null}
      {benchmarkProducts && benchmarkProducts.length > 0 ? (
        <div className="mt-10" data-testid="guide-tier-benchmark">
          {benchmarkSectionHeadingHe ? (
            <h2
              className="mb-4 text-[15px] font-extrabold leading-snug text-[#111318]"
              data-testid="guide-benchmark-heading"
            >
              {benchmarkSectionHeadingHe}
            </h2>
          ) : null}
          <div className="space-y-3">
            {benchmarkProducts.map((product, i) => (
              <GuideProductRow
                key={product.id}
                product={product}
                rank={i + 1}
                suppressedBars={suppressedBars}
                thresholdGeometry={thresholdGeometry}
                expanderLabels={expanderLabels}
              />
            ))}
          </div>
        </div>
      ) : null}
    </section>
  );
}
