"use client";

import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

import type { CarouselCard } from "@/lib/home/homepage-carousel-schema";
import { CardVisualBand } from "./carousel-card-visuals";
import { cn } from "@/lib/utils";

// -- Card shell — unified to the /hashvaot hub finding-card language
// (owner-approved 2026-07-09): rounded-2xl, neutral border, soft shadow,
// hover-lift handled by the outer motion.div (below) so this shell only
// owns the static chrome + hover shadow. ────────────────────────────────

const CARD_SHELL =
  "group block h-full min-h-[20rem] w-[92vw] max-w-[44rem] shrink-0 snap-center overflow-hidden rounded-2xl border border-[rgba(17,19,24,0.09)] bg-white shadow-[0_1px_2px_rgba(17,19,24,0.05)] transition-[box-shadow] duration-200 hover:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)] sm:w-[42rem] flex flex-col";

const CONTENT_PAD = "px-4 py-3 md:px-5 flex flex-col flex-1";

// -- Eyebrow badge colours ─────────────────────────────────────────────────────

const BADGE_COLORS: Record<string, string> = {
  "\u05D4\u05E9\u05D5\u05D5\u05D0\u05D4": "bg-[#E8F5EF] text-[#1F8F6A]",
  "\u05DE\u05D5\u05E6\u05E8 \u05DE\u05D5\u05D1\u05D9\u05DC": "bg-[#E8F5EF] text-[#1F8F6A]",
  "\u05D3\u05D5\u05D7 \u05E7\u05D8\u05D2\u05D5\u05E8\u05D9\u05D4": "bg-[#F1F5F9] text-[#475569]",
  "\u05DE\u05DE\u05E6\u05D0 \u05E7\u05D8\u05D2\u05D5\u05E8\u05D9\u05D4": "bg-[#FEF3C7] text-[#92400E]",
  "\u05D7\u05E7\u05D9\u05E8\u05EA \u05DE\u05E8\u05DB\u05D9\u05D1": "bg-[#F0FAFA] text-[#0E7490]",
  "\u05D7\u05E7\u05D9\u05E8\u05EA \u05E7\u05D8\u05D2\u05D5\u05E8\u05D9\u05D4": "bg-[#FEF9EC] text-[#92400E]",
  "\u05DE\u05EA\u05D5\u05D3\u05D5\u05DC\u05D5\u05D2\u05D9\u05D4": "bg-[#F1F5F9] text-[#475569]",
};

function badgeClass(eyebrow: string): string {
  return BADGE_COLORS[eyebrow] ?? "bg-[#F1F5F9] text-[#475569]";
}

// -- Score row (comparison only) ───────────────────────────────────────────────

function CompactScoreRow({ card }: { card: CarouselCard }) {
  if (!card.leftProduct || !card.rightProduct) return null;
  const left = card.leftProduct;
  const right = card.rightProduct;

  return (
    <div className="flex items-center gap-2 rounded-lg bg-[#F7F7F2]/70 px-3 py-2" dir="rtl">
      <div className="flex flex-1 items-baseline gap-1.5 min-w-0">
        <span className="text-xl font-extrabold tabular-nums text-[#111318]">{left.score}</span>
        <span className="truncate text-[0.65rem] font-semibold text-[#4E5663]">{left.brand}</span>
      </div>
      <span className="shrink-0 text-[0.6rem] font-extrabold text-[#5E6560]">{"\u05DE\u05D5\u05DC"}</span>
      <div className="flex flex-1 items-baseline justify-end gap-1.5 min-w-0">
        <span className="truncate text-[0.65rem] font-semibold text-[#4E5663]">{right.brand}</span>
        <span className="text-xl font-extrabold tabular-nums text-[#111318]">{right.score}</span>
      </div>
    </div>
  );
}

// -- Card layout ───────────────────────────────────────────────────────────────

export function HomepageCardItem({ card }: { card: CarouselCard }) {
  const reduceMotion = useReducedMotion();

  return (
    <motion.div
      whileHover={reduceMotion ? undefined : { y: -3 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="h-full"
    >
      <Link href={card.href} className={CARD_SHELL}>
        {/* accent top-bar — reference hub card language */}
        <div className="h-[0.4rem] w-full shrink-0" style={{ background: card.accent }} aria-hidden />
        {/* Visual band -- type-specific, no theme photos */}
        <CardVisualBand card={card} />

        {/* Card body */}
        <div className={CONTENT_PAD}>
          {/* Header: eyebrow badge + category + title */}
          <div className="flex items-start justify-between gap-3 border-b border-black/[0.05] pb-3">
            <div className="min-w-0 flex-1 text-right" dir="rtl">
              <p className="text-[0.65rem] font-bold text-[#4E5663]">{card.category}</p>
              <h3 className="mt-1 line-clamp-2 text-base font-extrabold leading-tight tracking-[-0.03em] text-[#111318] md:text-lg">
                {card.title}
              </h3>
            </div>
            <span
              className={cn(
                "shrink-0 rounded-full px-2.5 py-1 text-[0.6rem] font-bold",
                badgeClass(card.eyebrow)
              )}
            >
              {card.eyebrow}
            </span>
          </div>

          {/* Body: compact score row (comparison) or evidence block */}
          <div className="mt-3 flex flex-1 flex-col gap-2.5">
            {card.type === "comparison" && <CompactScoreRow card={card} />}

            <div
              className="rounded-lg border-r-[3px] border-[#1F8F6A] bg-[#F7F7F2]/80 px-3 py-2"
              dir="rtl"
            >
              <p className="text-[0.75rem] font-medium leading-relaxed text-[#111318]">
                {card.evidence}
              </p>
            </div>

            {card.metric && (
              <p
                className="text-[0.65rem] font-bold tabular-nums text-[#1F8F6A]"
                dir="rtl"
              >
                {card.metric}
              </p>
            )}
          </div>

          {/* Footer link */}
          <p className="mt-3 flex items-center justify-end gap-1 text-xs font-bold text-[#1F8F6A] opacity-70 transition-opacity group-hover:opacity-100">
            {"\u05DC\u05E4\u05E8\u05D8\u05D9\u05DD"}
            <ChevronLeft className="size-3.5" aria-hidden />
          </p>
        </div>
      </Link>
    </motion.div>
  );
}

/** @deprecated Use HomepageCardItem */
export const MicroComparisonSnapshotCard = HomepageCardItem;