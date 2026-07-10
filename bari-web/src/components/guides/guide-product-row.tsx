"use client";

// Guide product row (TASK-504, plan §3 item 2 / §2 six bars / §4 buy button).
// Progressive disclosure (TASK-504 gauge-unify spec v2 §3): collapsed by default —
// thumbnail/name/brand/isDefaultPick/oneLinerHe/compact badge row/price+buy — with ONE
// per-row expander revealing the full 4-bar ThresholdBarRow detail stack. Reuses the
// canonical `.bari-cmp-exp`/`.bari-cmp-expclip` grid-motion (globals.css) and the
// `ChevronDown` idiom already shipped on /hashvaot's `comparison-row.tsx`, per spec v2
// §3.3 — not a new expand/collapse mechanism.
//
// Deliberately NOT the canonical ComparisonRow/ScoreChip pair — those are
// grade/score-coupled (BariGradeBadge, bandOf(score)) and guides carry zero A–E grade
// or numeric score anywhere (plan §1 verdict layer).
//
// C3 guardrail (P508, coordinator dispatch): the compact badge row below is ALWAYS
// visible, un-gated by the expander — a reader sees every bar's state (including a
// מומלץ-tier product's dose flag) without expanding anything. Only the gauge/ladder
// DETAIL (geometry + caption) sits behind the toggle, never the bar states themselves.

import { useState } from "react";
import Image from "next/image";
import { ChevronDown } from "lucide-react";

import { BarStateBadge } from "@/components/shared/bar-state-badge";
import { ThresholdBarRow } from "@/components/guides/threshold-bar-row";
import { GuideBuyButton } from "@/components/guides/guide-buy-button";
import { comparisonRowStripeClass } from "@/lib/design/bari-comparison-tokens";
import {
  GUIDE_BAR_ORDER,
  GUIDE_BAR_LABELS_HE,
  GUIDE_PRODUCT_CHANNEL_LABELS_HE,
  type GuideBarKey,
  type GuideThresholdGeometry,
  type GuideProductVM,
} from "@/lib/view-models";
import { cn } from "@/lib/utils";

function GuideProductThumbnail({
  imageUrl,
  name,
}: {
  imageUrl?: string | null;
  name: string;
}) {
  const [failed, setFailed] = useState(false);

  if (imageUrl && !failed) {
    return (
      <div className="relative size-14 shrink-0 overflow-hidden rounded-2xl border border-black/[0.06] bg-white shadow-sm">
        <Image
          src={imageUrl}
          alt={name}
          fill
          className="object-contain p-2"
          sizes="56px"
          onError={() => setFailed(true)}
        />
      </div>
    );
  }

  return (
    // TASK-504C M1 fix (Design vision-critic MEDIUM, pre-existing axe
    // aria-prohibited-attr serious): aria-label is not a permitted attribute on a
    // bare <div> (implicit "generic" role) — needs an explicit role first, same
    // pattern BarStateBadge already uses correctly (bar-state-badge.tsx `role="img"`
    // + `aria-label`).
    <div
      className="relative size-14 shrink-0 overflow-hidden rounded-2xl border border-black/[0.06] bg-white shadow-sm"
      role="img"
      aria-label={name}
    >
      <div className="flex h-full items-center justify-center">
        <span
          aria-hidden
          className="select-none text-[1.1rem] leading-none"
          style={{ color: "rgba(17,19,24,0.18)" }}
        >
          ✦
        </span>
      </div>
    </div>
  );
}

export function GuideProductRow({
  product,
  rank,
  suppressedBars,
  thresholdGeometry,
  expanderLabels,
}: {
  product: GuideProductVM;
  /** 1-based position within its tier — used only for zebra tone, never rendered as
   *  a rank number (tiers are unordered within themselves, per the rubric). */
  rank: number;
  /** rubric display_suppression_rule bars to skip rendering entirely for this guide
   *  build (see GuidePageVM.suppressedBars). Bucket/tier math upstream already
   *  evaluated these bars; this only controls whether their row renders. */
  suppressedBars?: GuideBarKey[];
  /** Per-bar gauge geometry, shared across every product row (see
   *  GuidePageVM.thresholdGeometry). A bar absent here renders as a plain name+badge
   *  row (no infographic anatomy defined for it yet). */
  thresholdGeometry?: Partial<Record<GuideBarKey, GuideThresholdGeometry>>;
  /** Content-authored expander toggle copy (magnesium_guide_tier_copy_v1.md Slot 4),
   *  both gates passed. Absent → toggle renders with no label text (icon only). */
  expanderLabels?: { collapsed: string; expanded: string };
}) {
  const [open, setOpen] = useState(false);
  const barByKey = new Map(product.bars.map((b) => [b.bar, b] as const));
  const visibleBars = GUIDE_BAR_ORDER.filter((barKey) => !suppressedBars?.includes(barKey));
  const detailId = `guide-row-${product.id}-detail`;

  return (
    <article
      className={cn(
        "rounded-2xl border border-black/[0.06] p-4",
        comparisonRowStripeClass(rank)
      )}
      dir="rtl"
      data-testid="guide-product-row"
    >
      <div className="flex items-start gap-3">
        <GuideProductThumbnail imageUrl={product.imageUrl} name={product.name} />
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-x-2 gap-y-1">
            <span
              dir="auto"
              className="truncate text-[0.97rem] font-bold leading-[1.3] tracking-[-0.01em] text-[#111318]"
            >
              {product.name}
            </span>
            {product.brand ? (
              <span dir="auto" className="text-[0.85rem] font-semibold text-[#167A58]">
                · {product.brand}
              </span>
            ) : null}
            {product.channel ? (
              <span
                className="rounded-full px-2 py-0.5 text-[10px] font-semibold"
                style={{
                  backgroundColor: "#F3F4F2",
                  color: "#5A6168",
                  border: "1px solid rgba(17,19,24,0.08)",
                }}
                data-testid="guide-product-channel-tag"
              >
                {GUIDE_PRODUCT_CHANNEL_LABELS_HE[product.channel]}
              </span>
            ) : null}
            {product.isDefaultPick ? (
              <span
                className="rounded-full px-2 py-0.5 text-[10px] font-bold"
                style={{
                  backgroundColor: "#F0F4F1",
                  color: "#3A6B50",
                  border: "1px solid #C6D4CB",
                }}
                title="הזול ביותר לגרם אפקטיבי מבין כל המוצרים שעוברים את כל ששת הספים"
              >
                הבחירה הפשוטה
              </span>
            ) : null}
          </div>

          {/* TASK-504B — the product's one-line verdict, ported verbatim from the
              approved copy (חלק 4). Rendered as-is, no summarization. Always visible —
              disclosure never gates this (spec v2 §3.1 / §6 non-goal). */}
          {product.oneLinerHe && !product.oneLinerHe.includes("TODO") ? (
            <p className="mt-1.5 text-[12.5px] leading-[1.55] text-[#3E444A]">
              {product.oneLinerHe}
            </p>
          ) : null}

          {/* Compact badge row — ALWAYS VISIBLE, un-gated by the expander (spec v2
              §3.1; C3 guardrail P508: a מומלץ-tier product's dose flag must be visible
              here without expanding anything). No gauge/caption at this level. */}
          <div className="mt-2.5 flex flex-wrap gap-1.5" data-testid="guide-compact-badge-row">
            {visibleBars.map((barKey) => {
              const result = barByKey.get(barKey);
              if (!result) return null;
              return (
                <BarStateBadge
                  key={barKey}
                  state={result.state}
                  barLabel={GUIDE_BAR_LABELS_HE[barKey]}
                  note={result.note}
                />
              );
            })}
          </div>

          {/* Expander control (spec v2 §3.3) — one per row, reveals the full 4-bar
              threshold-gauge detail. Reuses the canonical chevron idiom
              (comparison-row.tsx) and focus tokens; NOT the whole-card-is-a-button
              idiom, since the price/buy row below contains its own nested interactive
              element (spec v2 §3.3 rationale). */}
          <button
            type="button"
            aria-expanded={open}
            aria-controls={detailId}
            onClick={() => setOpen((prev) => !prev)}
            data-testid="guide-row-expander"
            className="mt-2.5 flex min-h-[40px] w-full items-center justify-center gap-1 border-t text-[12px] font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[#167A58]"
            style={{ borderColor: "rgba(17,19,24,0.05)", color: "#4E5663" }}
          >
            <span>{open ? expanderLabels?.expanded : expanderLabels?.collapsed}</span>
            <ChevronDown
              aria-hidden
              strokeWidth={1.75}
              className={cn(
                "size-[15px] transition-transform duration-200 motion-reduce:transition-none",
                open && "rotate-180"
              )}
              style={{ color: open ? "#9A9FA6" : "#B5BBB6" }}
            />
          </button>

          {/* Expanded detail — the full per-bar threshold-gauge stack (TASK-504C,
              Design spec v1 §4 / v2 §1-2 unification). Suppressed bars are skipped
              entirely, never rendered as an empty/fallback row. */}
          <div id={detailId} aria-hidden={!open} className={cn("bari-cmp-exp", open && "is-open")}>
            <div className="bari-cmp-expclip">
              {/* Gauges render ONLY when expanded (spec v2 §3.2/task item C.3) — not
                  merely visually clipped. Matches comparison-row.tsx's own
                  `{open ? <ExpansionSection ... /> : null}` precedent: the wrapper
                  divs above stay in the DOM for the CSS grid-motion to animate, but
                  the (potentially heavy, ×4-per-row) gauge content itself is not
                  mounted until the first open. */}
              {open ? (
                <div className="pt-2.5">
                  {visibleBars.map((barKey, i) => {
                    const result = barByKey.get(barKey);
                    if (!result) return null;
                    return (
                      <ThresholdBarRow
                        key={barKey}
                        barKey={barKey}
                        result={result}
                        geometry={thresholdGeometry?.[barKey]}
                        placement={product.benchmarks?.[barKey]}
                        isFirst={i === 0}
                      />
                    );
                  })}
                </div>
              ) : null}
            </div>
          </div>

          <div className="mt-3 flex flex-wrap items-center justify-between gap-2">
            {product.pricing ? (
              <span className="text-[13px] font-bold text-[#111318]">
                {product.pricing.pricePerEffectiveUnitLabel}
              </span>
            ) : (
              <span className="text-[13px] text-[#6E756D]">מחיר לא זמין</span>
            )}
            <GuideBuyButton buyUrl={product.buyUrl} />
          </div>
        </div>
      </div>
    </article>
  );
}
