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
  const rows = useMemo(() => {
    const withBand = products.map((product, index) => ({
      product,
      index,
      band: bandOf(product.score),
    }));
    // TASK-365: standard competition ranking — tied products share the same rank number.
    // Walk in corpus order (already score-sorted); the first product at each distinct score
    // claims the next rank slot (= products seen so far + 1), so e.g. 12 products at score 50
    // all show the same rank and the next distinct score resumes after the tie.
    const scoreToRank = new Map<number, number>();
    let nextRank = 1;
    for (const { product } of withBand) {
      if (product.score == null) continue;
      if (!scoreToRank.has(product.score)) scoreToRank.set(product.score, nextRank);
      nextRank++;
    }
    return withBand.map((row, i) => ({
      ...row,
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
              <div className="bari-cmp-divider" aria-hidden>
                <span className="bari-cmp-divider-line" />
                <span className="bari-cmp-divider-label" style={{ color: band.tone }}>
                  {band.label}
                </span>
                <span className="bari-cmp-divider-line" />
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
            />
          </Fragment>
        ))}
      </div>
    </div>
  );
}
