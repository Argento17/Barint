"use client";

import { Fragment, useCallback, useMemo, useRef, useState } from "react";

import { ComparisonRow } from "@/components/shared/comparison-row";
import type { MetricSpec } from "@/components/shared/comparison-metric-column";
import { bandOf, railBandsFor } from "@/lib/comparisons/comparison-bands";
import type { BariProductVM } from "@/lib/view-models";
import { cn } from "@/lib/utils";

// The unified responsive comparison table (README §4/§5). ONE row component renders
// phone + desktop via container queries on `.bari-cmp-scroll`. Carries the v2 surface
// the spec never shipped: aligned metric column, in-list band dividers, scroll-only
// band rail, promoted confidence. Corpus order is law — render in array order, never
// re-sort (Invariant 1). Every product is individually visible (Invariant 2).

export function ComparisonTable({
  products,
  metricSpecs,
  /** Desktop page hosts the side band rail; phone-frame pages omit it. */
  showRail = false,
  showRank = true,
  initialExpandedProductId = null,
  category,
  suppressPartialBadges = false,
}: {
  products: BariProductVM[];
  metricSpecs: readonly MetricSpec[];
  showRail?: boolean;
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

  // Rail jump: scroll the list container only — never scrollIntoView (it yanks long
  // lists, §7). Honor reduced-motion.
  const onJump = useCallback((id: string) => {
    const el = rowRefs.current.get(id);
    const scroll = scrollRef.current;
    if (!el || !scroll) return;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    scroll.scrollTo({ top: el.offsetTop - 8, behavior: reduce ? "auto" : "smooth" });
  }, []);

  const metricHeader = metricSpecs
    .map((s) => (s.perLabel ? `${s.label} ${s.perLabel}` : s.label))
    .join(" · ");
  const railBands = showRail ? railBandsFor(products) : [];

  // Average Bari score of the products currently in view (recomputes under shelf filters).
  // The header's score column used to show the product COUNT after "ציון ·", which read like
  // a score sitting directly above the score chips. The count already lives in the page's
  // metadata line; the column now shows a clearly-labelled average instead.
  const scored = products.filter((p) => typeof p.score === "number");
  const averageScore =
    scored.length > 0
      ? Math.round(scored.reduce((sum, p) => sum + (p.score as number), 0) / scored.length)
      : null;

  // Precompute the in-list band dividers in corpus order (Invariant 1). A divider is
  // shown on the first row whose score band differs from the row above it.
  const rows = useMemo(() => {
    const withBand = products.map((product, index) => ({
      product,
      index,
      band: bandOf(product.score),
    }));
    return withBand.map((row, i) => ({
      ...row,
      showDivider: i === 0 || withBand[i - 1].band.id !== row.band.id,
    }));
  }, [products]);

  return (
    <div className={cn("bari-cmp-workspace", showRail && "bari-cmp-workspace--wide")}>
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
            <span className="bari-cmp-colhead-grade">
              ציון
              {averageScore != null ? (
                <>
                  {" · ממוצע "}
                  <b className="bari-cmp-colhead-avg">{averageScore}</b>
                </>
              ) : null}
            </span>
          </div>
        ) : null}

        {rows.map(({ product, index, band, showDivider }) => (
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
              rank={showRank ? index + 1 : 0}
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

      {showRail && railBands.length > 0 ? (
        <aside className="bari-cmp-rail" aria-label="ניווט לפי טווח ציון">
          <p className="bari-cmp-rail-title">טווחי ציון</p>
          {railBands.map((band) => (
            <button
              key={band.id}
              type="button"
              className="bari-cmp-rail-band"
              onClick={() => onJump(band.firstProductId)}
            >
              <span className="bari-cmp-rail-row">
                <span className="bari-cmp-rail-label">{band.label}</span>
                <span className="bari-cmp-rail-count bari-mono">{band.count}</span>
              </span>
              <span className="bari-cmp-rail-bar">
                <i
                  style={{
                    width: `${(band.count / products.length) * 100}%`,
                    background: band.tone,
                  }}
                />
              </span>
            </button>
          ))}
        </aside>
      ) : null}
    </div>
  );
}
