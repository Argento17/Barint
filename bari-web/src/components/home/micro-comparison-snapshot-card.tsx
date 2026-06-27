"use client";

import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import { motion } from "framer-motion";

import type { CarouselCard } from "@/lib/home/homepage-carousel-schema";
import { CardVisualBand } from "./carousel-card-visuals";
import { cn } from "@/lib/utils";

// ── Card shell ────────────────────────────────────────────────────────────────

const CARD_SHELL =
  "group block h-full min-h-[18rem] w-[84vw] max-w-[32rem] shrink-0 snap-center rounded-[1.5rem] border border-black/[0.08] bg-[#FFFFFF] overflow-hidden shadow-[0_20px_60px_-48px_rgba(17,19,24,0.2)] transition-[border-color,box-shadow,transform] duration-300 hover:-translate-y-0.5 hover:border-[#1F8F6A]/22 hover:shadow-[0_24px_64px_-40px_rgba(31,143,106,0.2)] sm:w-[30rem] flex flex-col";

const CONTENT_PAD = "px-4 py-3 md:px-5 flex flex-col flex-1";

// ── Eyebrow badge colours ─────────────────────────────────────────────────────

const BADGE_COLORS: Record<string, string> = {
  השוואה: "bg-[#E8F5EF] text-[#1F8F6A]",
  "מוצר מוביל": "bg-[#E8F5EF] text-[#1F8F6A]",
  "דוח קטגוריה": "bg-[#F1F5F9] text-[#475569]",
  "חקירת מרכיב": "bg-[#F0FAFA] text-[#0E7490]",
  "חקירת קטגוריה": "bg-[#FEF9EC] text-[#92400E]",
  מתודולוגיה: "bg-[#F1F5F9] text-[#475569]",
};

function badgeClass(eyebrow: string): string {
  return BADGE_COLORS[eyebrow] ?? "bg-[#F1F5F9] text-[#475569]";
}

// ── Score row (comparison only) ───────────────────────────────────────────────

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
      <span className="shrink-0 text-[0.6rem] font-extrabold text-[#5E6560]">מול</span>
      <div className="flex flex-1 items-baseline justify-end gap-1.5 min-w-0">
        <span className="truncate text-[0.65rem] font-semibold text-[#4E5663]">{right.brand}</span>
        <span className="text-xl font-extrabold tabular-nums text-[#111318]">{right.score}</span>
      </div>
    </div>
  );
}

// ── Card layout ───────────────────────────────────────────────────────────────

export function HomepageCardItem({ card }: { card: CarouselCard }) {
  return (
    <motion.div
      whileHover={{ y: -2 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="h-full"
    >
      <Link href={card.href} className={CARD_SHELL}>
        {/* Visual band — type-specific, no theme photos */}
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
            לפרטים
            <ChevronLeft className="size-3.5" aria-hidden />
          </p>
        </div>
      </Link>
    </motion.div>
  );
}

/** @deprecated Use HomepageCardItem */
export const MicroComparisonSnapshotCard = HomepageCardItem;
