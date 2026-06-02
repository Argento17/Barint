"use client";

import { memo, type KeyboardEvent } from "react";
import { ChevronDown } from "lucide-react";

import { BariGradeBadge } from "@/components/comparisons/bari-grade-badge";
import { BariProductThumbnail } from "@/components/comparisons/bari-product-thumbnail";
import { ConfidenceIndicator } from "@/components/shared/confidence-indicator";
import { ExpansionSection } from "@/components/shared/expansion-section";
import {
  MetricColumn,
  type MetricSpec,
} from "@/components/shared/comparison-metric-column";
import type { BariGrade, BariProductVM } from "@/lib/view-models";
import { BARI_COMPARISON_TOKENS } from "@/lib/design/bari-comparison-tokens";
import { cn } from "@/lib/utils";

const GRADE_LABELS: Record<BariGrade, string> = {
  A: "מצוין",
  B: "טוב",
  C: "בינוני",
  D: "חלש",
  E: "נמוך",
};

// Strongest +/− beneath the name on the collapsed row (spec §3.3), from rowReason.
function RowReason({ product }: { product: BariProductVM }) {
  const positive = product.rowReason?.positive ?? null;
  const limiting = product.rowReason?.limiting ?? null;
  if (!positive && !limiting) return null;

  return (
    <div className="mt-[5px] flex flex-col gap-0.5">
      {positive ? (
        <p className="truncate text-[0.8rem] leading-[1.45] text-[#3C443F]">
          <span className="font-extrabold text-[#1F8F6A]" aria-hidden>
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
  if (product.score == null || product.grade == null) {
    // Mirror the graded chip's exact box (same container + sm size) so unscored
    // products stay column-aligned and identically sized — just neutral grey.
    const rowTokens = BARI_COMPARISON_TOKENS.score.rowChip;
    return (
      <div
        className={cn(rowTokens.container, rowTokens.size.sm)}
        style={{
          backgroundColor: "#F7F7F2",
          borderColor: "rgba(17,19,24,0.10)",
        }}
        aria-label="ללא ציון"
      >
        <span
          className={cn(rowTokens.scoreClass, rowTokens.scoreSize.sm)}
          style={{ color: "#9AA09B" }}
          aria-hidden
        >
          —
        </span>
        <span
          className={cn(rowTokens.labelClass, rowTokens.labelSize.sm)}
          style={{ color: "#9AA09B" }}
          aria-hidden
        >
          ללא ציון
        </span>
      </div>
    );
  }
  return (
    <BariGradeBadge
      score={product.score}
      grade={product.grade}
      gradeLabel={GRADE_LABELS[product.grade]}
      size="sm"
      context="row"
    />
  );
}

export const ComparisonRow = memo(function ComparisonRow({
  product,
  rank,
  open,
  onToggle,
  metricSpecs,
  registerRow,
}: {
  product: BariProductVM;
  rank: number;
  open: boolean;
  onToggle: (id: string) => void;
  metricSpecs: readonly MetricSpec[];
  registerRow: (id: string, el: HTMLElement | null) => void;
}) {
  const onKeyDown = (e: KeyboardEvent<HTMLButtonElement>) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      onToggle(product.id);
    }
  };

  const verdict = product.rowVerdict?.trim();

  return (
    <article className="bari-cmp-row" ref={(el) => registerRow(product.id, el)}>
      <button
        type="button"
        className="bari-cmp-rowhead"
        aria-expanded={open}
        aria-label={product.name}
        onClick={() => onToggle(product.id)}
        onKeyDown={onKeyDown}
      >
        <span className="bari-cmp-rank bari-mono" aria-hidden>
          {rank}
        </span>
        <span className="bari-cmp-thumbcell">
          <BariProductThumbnail product={product} size="fill" />
        </span>
        <span className="bari-cmp-namecell">
          <span className="block truncate text-[0.97rem] font-bold leading-[1.3] tracking-[-0.01em] text-[#111318]">
            {product.name}
          </span>
          {verdict ? (
            <p className="mt-[5px] text-[0.8rem] leading-[1.45] text-[#3C443F]">
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
          <ConfidenceIndicator
            confidence={product.confidence}
            variant="dot"
            className="bari-cmp-conf"
          />
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
                onCollapse={() => onToggle(product.id)}
                wide
                confidencePromoted
              />
            ) : null}
          </div>
        </div>
      </div>
    </article>
  );
});
