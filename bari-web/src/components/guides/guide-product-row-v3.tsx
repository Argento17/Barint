"use client";

// GuideProductRowV3 — TASK-577 (magnesium guide v3 STRUCTURAL rebuild).
//
// Owner-dictated card contract (dispatch item 4): exactly 4 visible lines — elemental
// mg, chemical form, labelled servings/day, and one "מה חשוב לדעת: …" line.
// EVERYTHING else this guide can show about a product (bar-state badges, the
// classifier pill, the full 4-bar threshold-gauge stack) moves under the row's own
// `לפרטים` disclosure, collapsed by default.
//
// This is a deliberate, owner-directed departure from the v2 row's C3 guardrail P508
// ("the compact badge row is ALWAYS visible, un-gated by the expander") — that
// guardrail is superseded for v3 by this task's explicit dispatch instruction. Not
// silently dropped: documented here so a future reader does not "fix" this back.
//
// Reuses the identical `.bari-cmp-exp`/`.bari-cmp-expclip` grid-motion + ChevronDown
// idiom already shipped on GuideProductRow (v2) — same disclosure mechanism, not a
// new one, per the dispatch's "reuse existing disclosure components if present".

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
  GUIDE_V3_DETAILS_LABEL_HE,
  type GuideBarKey,
  type GuideThresholdGeometry,
  type GuideProductVM,
} from "@/lib/view-models";
import { cn } from "@/lib/utils";

function GuideProductThumbnailV3({ imageUrl, name }: { imageUrl?: string | null; name: string }) {
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

export function GuideProductRowV3({
  product,
  rank,
  suppressedBars,
  thresholdGeometry,
}: {
  product: GuideProductVM;
  /** 1-based position within its group — zebra tone only, never a rank number. */
  rank: number;
  suppressedBars?: GuideBarKey[];
  thresholdGeometry?: Partial<Record<GuideBarKey, GuideThresholdGeometry>>;
}) {
  const [open, setOpen] = useState(false);
  const facts = product.visibleFactsV3;
  const barByKey = new Map(product.bars.map((b) => [b.bar, b] as const));
  const visibleBars = GUIDE_BAR_ORDER.filter((barKey) => !suppressedBars?.includes(barKey));
  const detailId = `guide-row-v3-${product.id}-detail`;

  return (
    <article
      className={cn("rounded-2xl border border-black/[0.06] p-4", comparisonRowStripeClass(rank))}
      dir="rtl"
      data-testid="guide-product-row-v3"
    >
      <div className="flex items-start gap-3">
        <GuideProductThumbnailV3 imageUrl={product.imageUrl} name={product.name} />
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
          </div>

          {/* ── The 4 owner-dictated visible lines (dispatch item 4) ──────────────── */}
          {facts ? (
            <dl className="mt-2 space-y-1" data-testid="guide-row-v3-facts">
              <div className="flex gap-1.5 text-[13px] leading-[1.5]">
                <dt className="sr-only">מגנזיום יסודי</dt>
                <dd className="font-bold text-[#111318]">{facts.elementalDoseLabel}</dd>
              </div>
              <div className="flex gap-1.5 text-[12.5px] leading-[1.5]">
                <dt className="sr-only">צורה כימית</dt>
                <dd className="font-semibold text-[#3E444A]">{facts.formLabel}</dd>
              </div>
              {facts.servingsPerDayLabel ? (
                <div className="flex gap-1.5 text-[12px] leading-[1.5]">
                  <dt className="sr-only">מנה יומית מצוינת</dt>
                  <dd className="text-[#5A6168]">{facts.servingsPerDayLabel}</dd>
                </div>
              ) : null}
              <div className="text-[12.5px] leading-[1.55] text-[#3E444A]">
                <span className="font-semibold text-[#111318]">מה חשוב לדעת: </span>
                {facts.whatMattersHe}
              </div>
            </dl>
          ) : null}

          {/* ── `לפרטים` disclosure — everything else (badges, classifier pill,
              full threshold-gauge stack) lives here, collapsed by default. ────────── */}
          <button
            type="button"
            aria-expanded={open}
            aria-controls={detailId}
            onClick={() => setOpen((prev) => !prev)}
            data-testid="guide-row-v3-expander"
            className="mt-2.5 flex min-h-[40px] w-full items-center justify-center gap-1 border-t text-[12px] font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-[-2px] focus-visible:outline-[#167A58]"
            style={{ borderColor: "rgba(17,19,24,0.05)", color: "#4E5663" }}
          >
            <span>{GUIDE_V3_DETAILS_LABEL_HE}</span>
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

          <div id={detailId} aria-hidden={!open} className={cn("bari-cmp-exp", open && "is-open")}>
            <div className="bari-cmp-expclip">
              {open ? (
                <div className="pt-2.5">
                  {product.classifierHe ? (
                    <p className="mb-2">
                      <span
                        className="inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-semibold"
                        style={{
                          backgroundColor: "#F3F4F2",
                          color: "#5A6168",
                          border: "1px solid rgba(17,19,24,0.08)",
                        }}
                        data-testid="guide-row-v3-classifier"
                      >
                        {product.classifierHe}
                      </span>
                    </p>
                  ) : null}

                  <div className="flex flex-wrap gap-1.5" data-testid="guide-row-v3-badge-row">
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

                  <div className="mt-2.5">
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
