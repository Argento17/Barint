"use client";

import { Fragment, useCallback, useMemo, useRef, useState } from "react";

import { ComparisonRow } from "@/components/shared/comparison-row";
import type { MetricSpec } from "@/components/shared/comparison-metric-column";
import { bandOf } from "@/lib/comparisons/comparison-bands";
import type { BariProductVM } from "@/lib/view-models";
import { cn } from "@/lib/utils";

// The unified responsive comparison table (README §4/§5). ONE row component renders
// phone + desktop via container queries on `.bari-cmp-scroll`. Carries the v2 surface
// the spec never shipped: aligned metric column, in-list band dividers, promoted
// confidence. Corpus order is law — render in array order, never re-sort (Invariant 1).
// Every product is individually visible (Invariant 2). TASK-226 removed the dashboard
// furniture (left score-distribution rail + header average score).

export function ComparisonTable({
  products,
  metricSpecs,
  showRank = true,
  initialExpandedProductId = null,
  category,
  suppressPartialBadges = false,
  clampVerdictLines,
  compactDividers = false,
}: {
  products: BariProductVM[];
  metricSpecs: readonly MetricSpec[];
  /** When false, rank numbers are not rendered (useful when ordering carries no signal). */
  showRank?: boolean;
  initialExpandedProductId?: string | null;
  /** Category slug passed through to analytics context in AdditivePanel. */
  category?: string;
  /** FIX-3: when true, per-product partial confidence badges are suppressed (≥50%
   *  of products are partial — the badge carries no signal). */
  suppressPartialBadges?: boolean;
  /**
   * TASK-384A: passed through to ComparisonRow — clamps the rowVerdict paragraph to
   * this many lines. When undefined (default), no clamp is applied; all existing
   * categories are byte-identical to before.
   */
  clampVerdictLines?: number;
  /**
   * TASK-384A: when true, reduces band-divider vertical padding from 9px to 5px so
   * an extra row fits above the fold on compact mobile viewports. Prop-gated —
   * default false leaves all other category pages byte-identical.
   */
  compactDividers?: boolean;
}) {
  const [open, setOpen] = useState<Set<string>>(
    () => new Set(initialExpandedProductId ? [initialExpandedProductId] : [])
  );
  const scrollRef = useRef<HTMLDivElement>(null);
  const rowRefs = useRef<Map<string, HTMLElement>>(new Map());

  const registerRow = useCallback((id: string, el: HTMLElement | null) => {
    if (el) rowRefs.current.set(id, el);
    else rowRefs.current.delete(id);
  }, []);

  const onToggle = useCallback((id: string) => {
    // Multiple rows may be open at once (spec §6).
    setOpen((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }, []);

  const metricHeader = metricSpecs
    .map((s) => (s.perLabel ? `${s.label} ${s.perLabel}` : s.label))
    .join(" · ");

  // Precompute the in-list band dividers in corpus order (Invariant 1). A divider is
  // shown on the first row whose score band differs from the row above it.
  //
  // TASK-365: standard competition ranking — tied products share the same rank number.
  // e.g. if three products share score 50, they all show rank N and the next distinct
  // score resumes at N+3 (not N+1). Unscored products (score === null) never get a rank.
  const rows = useMemo(() => {
    const withBand = products.map((product, index) => ({
      product,
      index,
      band: bandOf(product.score),
    }));

    // Build a score → competition rank map. Walk in corpus order (already score-sorted);
    // track the next rank slot = number of products seen so far + 1.
    const scoreToRank = new Map<number, number>();
    let nextRank = 1;
    for (const { product } of withBand) {
      if (product.score == null) continue;
      if (!scoreToRank.has(product.score)) {
        scoreToRank.set(product.score, nextRank);
      }
      nextRank++;
    }

    return withBand.map((row, i) => ({
      ...row,
      // rank: the competition rank for this product's score (0 = unscored, don't show).
      competitionRank:
        row.product.score != null ? (scoreToRank.get(row.product.score) ?? 0) : 0,
      showDivider: i === 0 || withBand[i - 1].band.id !== row.band.id,
    }));
  }, [products]);

  return (
    <div className="bari-cmp-workspace">
      <div
        className={cn(
          "bari-cmp-scroll",
          metricSpecs.length === 0 && "bari-cmp-scroll--nometric"
        )}
        ref={scrollRef}
      >
        {metricSpecs.length > 0 ? (
          <div className="bari-cmp-colhead" aria-hidden>
            <span className="bari-cmp-rank">#</span>
            <span className="bari-cmp-colhead-thumb" />
            <span className="bari-cmp-colhead-name">מוצר ותובנה</span>
            <span className="bari-cmp-colhead-metric">{metricHeader}</span>
            <span className="bari-cmp-colhead-grade">ציון</span>
          </div>
        ) : null}

        {rows.map(({ product, band, showDivider, competitionRank }) => (
          <Fragment key={product.id}>
            {showDivider ? (
              <div
                className="bari-cmp-divider"
                aria-hidden
                // TASK-384A: prop-gated compact padding — reduces divider from ~33px to
                // ~25px so an extra row fits above the fold on 390px mobile. Only active
                // when compactDividers=true (magnesium only); all other pages unchanged.
                style={compactDividers ? { paddingTop: "5px", paddingBottom: "5px" } : undefined}
              >
                <span className="bari-cmp-divider-line" />
                <span className="bari-cmp-divider-label" style={{ color: band.tone }}>
                  {band.label}
                </span>
                <span className="bari-cmp-divider-line" />
              </div>
            ) : null}
            {product.bandNote ? (
              <div
                className="px-4 py-2 text-[0.75rem] leading-[1.5] text-[#7A7A7A]"
                style={{ borderTop: "1px dashed #E0DDD5", backgroundColor: "#FAFAF8" }}
                aria-label={product.bandNote}
              >
                {product.bandNote}
              </div>
            ) : null}
            <ComparisonRow
              product={product}
              rank={showRank ? competitionRank : 0}
              open={open.has(product.id)}
              onToggle={onToggle}
              metricSpecs={metricSpecs}
              registerRow={registerRow}
              category={category}
              suppressPartialBadge={suppressPartialBadges}
              clampVerdictLines={clampVerdictLines}
            />
          </Fragment>
        ))}
      </div>
    </div>
  );
}
