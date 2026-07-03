"use client";

import { memo, type KeyboardEvent } from "react";
import { ChevronDown } from "lucide-react";

import { BariGradeBadge } from "@/components/comparisons/bari-grade-badge";
import { BariProductThumbnail } from "@/components/comparisons/bari-product-thumbnail";
import {
  ConfidenceDot,
  ConfidenceRing,
  NullScorePill,
} from "@/components/shared/confidence-marker";
import { ExpansionSection } from "@/components/shared/expansion-section";
import { GlassBoxPartialFlag } from "@/components/shared/glass-box-flag";
import {
  MetricColumn,
  type MetricSpec,
} from "@/components/shared/comparison-metric-column";
import type { BariProductVM } from "@/lib/view-models";
import { GLASS_BOX_WITHHOLD_LABEL } from "@/lib/view-models";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import { GLASSBOX_D5D6_ON, GLASSBOX_W4_ON } from "@/lib/feature-flags";
import { cn } from "@/lib/utils";

// TASK-179I — Glass Box gate read, flag-gated. With the flag OFF these are always
// false/undefined, so the row renders byte-identically to today.
function glassBoxState(product: BariProductVM) {
  if (!GLASSBOX_D5D6_ON) return { isWithheld: false, isDemoted: false } as const;
  const gate = product.glassBox?.gateState;
  return {
    isWithheld: gate === "withhold",
    isDemoted: gate === "demote",
  } as const;
}

// FIX-2: qualitative adjective labels removed. The chip renders only grade letter + numeric
// score (e.g. "82 / B"). The GRADE_LABELS mapping is intentionally deleted; the gradeLabel
// prop passed to BariGradeBadge is replaced with the grade letter itself so the chip
// reads "B" rather than "B · טוב". Confidence labels (נתונים חלקיים etc.) are unaffected.

// Strongest +/− beneath the name on the collapsed row (spec §3.3), from rowReason.
function RowReason({ product }: { product: BariProductVM }) {
  const positive = product.rowReason?.positive ?? null;
  const limiting = product.rowReason?.limiting ?? null;
  if (!positive && !limiting) return null;

  return (
    <div className="mt-[5px] flex flex-col gap-0.5">
      {positive ? (
        <p className="truncate text-[0.8rem] leading-[1.45] text-[#3C443F]">
          <span className="font-extrabold text-[#167A58]" aria-hidden>
            +{" "}
          </span>
          {positive}
        </p>
      ) : null}
      {limiting ? (
        <p className="truncate text-[0.8rem] leading-[1.45] text-[#6E756F]">
          <span className="font-extrabold text-[#B5882F]" aria-hidden>
            −{" "}
          </span>
          {limiting}
        </p>
      ) : null}
    </div>
  );
}

function GradeCell({ product }: { product: BariProductVM }) {
  const { isWithheld } = glassBoxState(product);

  // TASK-179I — Glass Box WITHHOLD: show `לא נוקד` where the grade chip would be.
  // Same neutral box as an unscored product (no error look, no number), distinct
  // label text. Only when the flag is ON and the product is gated to withhold.
  if (isWithheld) {
    const rowTokens = BARI_COMPARISON_TOKENS.score.rowChip;
    return (
      <div
        className={cn(rowTokens.container, rowTokens.size.sm)}
        style={{
          backgroundColor: "#F7F7F2",
          borderColor: "rgba(17,19,24,0.10)",
        }}
        aria-label={GLASS_BOX_WITHHOLD_LABEL}
      >
        <span
          className={cn(rowTokens.scoreClass, rowTokens.scoreSize.sm)}
          style={{ color: "#6B7070" }}
          aria-hidden
        >
          —
        </span>
        <span
          className={cn(rowTokens.labelClass, rowTokens.labelSize.sm)}
          style={{ color: "#6B7070" }}
          aria-hidden
        >
          {GLASS_BOX_WITHHOLD_LABEL}
        </span>
      </div>
    );
  }

  // State 7 — `insufficient` / unscored: SUPPRESS the grade chip and render the
  // null-state pill in its footprint (spec §5). Same width band / radius / row height
  // as the chip → no layout shift vs scored rows. No digits, no grade letter, no hue.
  if (product.score == null || product.grade == null) {
    return <NullScorePill />;
  }

  // Scored row. The confidence ring (partial only) is an absolute overlay on the chip's
  // footprint — wrap in a relative span so the outline registers against the chip box
  // without enlarging its layout width (spec §2/§7, 0 extra width / no CLS).
  // FIX-2: pass empty gradeLabel so BariGradeBadge renders only the grade letter (no adjective).
  return (
    <span className="relative inline-flex">
      <BariGradeBadge
        score={product.score}
        grade={product.grade}
        gradeLabel=""
        size="sm"
        context="row"
      />
      <ConfidenceRing confidence={product.confidence} />
    </span>
  );
}

export const ComparisonRow = memo(function ComparisonRow({
  product,
  rank,
  open,
  onToggle,
  metricSpecs,
  registerRow,
  category,
  suppressPartialBadge = false,
  clampVerdictLines,
}: {
  product: BariProductVM;
  rank: number;
  open: boolean;
  onToggle: (id: string) => void;
  metricSpecs: readonly MetricSpec[];
  registerRow: (id: string, el: HTMLElement | null) => void;
  /** Category slug for analytics context (anonymous — no user ID). */
  category?: string;
  /** FIX-3: when true, suppress the per-product partial confidence badge (page-level
   *  disclosure is shown instead when ≥50% of the page's products are partial). */
  suppressPartialBadge?: boolean;
  /**
   * TASK-384A: when set, clamps the rowVerdict paragraph to this many lines via
   * CSS -webkit-line-clamp. When undefined (default), behavior is unchanged —
   * no other category is affected. Use 2 for magnesium (verdicts fit 2 lines @390px).
   */
  clampVerdictLines?: number;
}) {
  const onKeyDown = (e: KeyboardEvent<HTMLButtonElement>) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      onToggle(product.id);
    }
  };

  const verdict = product.rowVerdict?.trim();
  const { isWithheld, isDemoted } = glassBoxState(product);

  return (
    <article className="bari-cmp-row" ref={(el) => registerRow(product.id, el)}>
      <button
        type="button"
        className="bari-cmp-rowhead"
        aria-expanded={open}
        aria-label={
          product.brand?.trim()
            ? `${product.name}, ${product.brand.trim()}`
            : product.name
        }
        onClick={() => onToggle(product.id)}
        onKeyDown={onKeyDown}
      >
        <span className="bari-cmp-rank bari-mono" aria-hidden>
          {rank > 0 ? rank : null}
        </span>
        <span className="bari-cmp-thumbcell">
          <BariProductThumbnail
            product={product}
            size="fill"
            blendWhite={category === "magnesium"}
          />
        </span>
        <span className="bari-cmp-namecell">
          <span className="block truncate text-[0.97rem] font-bold leading-[1.3] tracking-[-0.01em] text-[#111318]">
            {product.name}
            {product.brand?.trim() ? (
              <span
                className="ms-2 inline font-semibold tracking-normal text-[#167A58]"
                style={{ fontSize: "0.9rem" }}
              >
                <span aria-hidden>· </span>
                <span dir="auto">{product.brand.trim()}</span>
              </span>
            ) : null}
          </span>
          {product.claimShortfallFlag ? (
            <span
              className="mt-1 inline-flex items-center gap-1 rounded-full border px-1.5 py-0.5"
              style={{ backgroundColor: "#FBF8EE", borderColor: "#ECE3C8" }}
              aria-label={product.claimShortfallFlag}
            >
              <span
                className="text-[10px] leading-none"
                aria-hidden
                style={{ color: "#6B5A1E" }}
              >
                ⚠
              </span>
              <span
                className="text-[10px] font-semibold leading-none"
                style={{ color: "#6B5A1E" }}
              >
                {product.claimShortfallFlag}
              </span>
            </span>
          ) : null}
          {product.absorbedMgPill ? (
            <span
              className="mt-1 inline-flex items-center gap-1 rounded-full border px-1.5 py-0.5"
              style={{ backgroundColor: "#F0F4F1", borderColor: "#C6D4CB" }}
              title="הערכה לפי שיעורי ספיגה ממוצעים במחקרים — לא מדידה של מוצר זה."
              aria-label={product.absorbedMgPill}
            >
              <span
                className="text-[10px] font-semibold leading-none"
                style={{ color: "#3A6B50" }}
              >
                {product.absorbedMgPill}
              </span>
            </span>
          ) : null}
          {product.valueFlag ? (
            <span
              className="mt-1 inline-flex items-center gap-1 rounded-full border px-1.5 py-0.5"
              style={{ backgroundColor: "#FBF1F0", borderColor: "#E6C9C5" }}
              aria-label={product.valueFlag}
            >
              <span
                className="text-[10px] leading-none"
                aria-hidden
                style={{ color: "#843329" }}
              >
                ✕
              </span>
              <span
                className="text-[10px] font-semibold leading-none"
                style={{ color: "#843329" }}
              >
                {product.valueFlag}
              </span>
            </span>
          ) : null}
          {verdict ? (
            <p
              className={cn(
                "mt-[5px] text-[0.8rem] leading-[1.45] text-[#3C443F]",
                // TASK-384A: prop-gated clamp — only active when clampVerdictLines is set.
                // Use Tailwind line-clamp utilities (sets -webkit-line-clamp + overflow:hidden
                // as a class, not an inline style, so React does not strip it).
                // line-clamp-1 through line-clamp-6 are Tailwind core utilities.
                clampVerdictLines === 1 && "line-clamp-1",
                clampVerdictLines === 2 && "line-clamp-2",
                clampVerdictLines === 3 && "line-clamp-3",
                clampVerdictLines === 4 && "line-clamp-4",
              )}
            >
              {verdict}
            </p>
          ) : product.rowReason ? (
            <RowReason product={product} />
          ) : product.insightLine ? (
            <span className="mt-[5px] block truncate text-[0.8rem] leading-[1.45] text-[#4E5663]">
              {product.insightLine}
            </span>
          ) : null}
        </span>
        {metricSpecs.length > 0 ? (
          <span className="bari-cmp-metriccell">
            <MetricColumn specs={metricSpecs} metrics={product.metrics} />
          </span>
        ) : null}
        <span className="bari-cmp-gradecell">
          {isDemoted ? (
            // Glass Box DEMOTE: the `ניתוח חלקי` pill stands in for the confidence dot
            // (it carries the same "partial" signal, calmly). Grade chip still shows.
            <GlassBoxPartialFlag className="bari-cmp-conf" />
          ) : isWithheld ? (
            // Withhold: the `לא נוקד` chip carries the signal; no confidence dot needed.
            <span aria-hidden />
          ) : suppressPartialBadge && product.confidence === "partial" ? (
            // FIX-3: page-level disclosure is shown instead; skip the per-row badge.
            null
          ) : product.score == null || product.grade == null ? (
            // Chip is suppressed → NullScorePill renders in its footprint and carries the
            // signal itself (DESIGN-LOCK §93). No gutter dot in that case.
            <span aria-hidden />
          ) : (
            // Score Confidence Indicators (TASK-226 DESIGN-LOCK): achromatic 6px grey dot
            // in the chip's inline-start gutter for partial AND insufficient (identical
            // marker; gap type is differentiated only in the expansion). No text on the
            // row; no color encoding. verified → renders nothing. The dotted ring rides ON
            // the chip (see GradeCell).
            <ConfidenceDot
              confidence={product.confidence}
              className="bari-cmp-conf"
            />
          )}
          <GradeCell product={product} />
          <ChevronDown
            strokeWidth={1.75}
            aria-hidden
            className={cn(
              "size-[15px] shrink-0 text-[#B5BBB6] transition-transform duration-200 motion-reduce:transition-none",
              open && "rotate-180 text-[#9A9FA6]"
            )}
          />
        </span>
      </button>

      <div className={cn("bari-cmp-exp", open && "is-open")} aria-hidden={!open}>
        <div className="bari-cmp-expclip">
          <div className="bari-cmp-expbody">
            {open ? (
              <ExpansionSection
                expansion={product.expansion}
                confidence={product.confidence}
                confidenceLabelHe={product.confidence_label_he}
                confidenceTooltipHe={product.confidence_tooltip_he}
                onCollapse={() => onToggle(product.id)}
                wide
                confidencePromoted
                glassBox={
                  GLASSBOX_D5D6_ON && (isDemoted || isWithheld)
                    ? product.glassBox
                    : undefined
                }
                d4Additives={
                  GLASSBOX_D5D6_ON && product.d4_additives !== undefined
                    ? product.d4_additives
                    : undefined
                }
                d3Processing={
                  GLASSBOX_W4_ON && product.d3_processing !== undefined
                    ? product.d3_processing
                    : undefined
                }
                productId={product.id}
                category={category}
                rowVerdict={product.rowVerdict}
                bestUseCases={product.bestUseCases}
                consumerTakeaway={product.consumerTakeaway}
                bariInterpretation={product.bariInterpretation}
                rank={product.rank}
                categoryTotal={product.categoryTotal}
                magnesiumBadges={product.magnesiumBadges}
                creatineBadges={product.creatineBadges}
              />
            ) : null}
          </div>
        </div>
      </div>
    </article>
  );
});
