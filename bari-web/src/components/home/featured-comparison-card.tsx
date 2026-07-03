"use client";

import Image from "next/image";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import { getFeaturedCerealDuel } from "@/lib/home/featured-cereal-duel";
import { ScoreChip } from "@/components/shared/score-chip";
import { CarouselCardImage } from "@/components/home/carousel-card-image";
import { CAROUSEL_PRODUCT_FALLBACK } from "@/lib/home/homepage-carousel-schema";

export function FeaturedComparisonCard({ className = "" }: { className?: string }) {
  const duel = getFeaturedCerealDuel();
  if (!duel) return null;

  const { vitabix, lyon } = duel;

  return (
    /* Shell provides the outer frame and shadow -- card itself stays clean */
    <Link
      href={duel.href}
      className={`group block w-full overflow-hidden rounded-[1.5rem] bg-white transition-opacity duration-200 hover:opacity-95 ${className}`}
      dir="rtl"
    >
      {/* === Top grid: story | product A | VS | product B === */}
      <div className="grid grid-cols-1 md:grid-cols-[minmax(0,1fr)_auto_auto_auto]">

        {/* Story column */}
        <div className="flex flex-col justify-between gap-4 border-b border-black/[0.05] px-6 py-6 md:border-b-0">
          <div className="space-y-2">
            <p className="text-[11px] font-bold uppercase tracking-widest text-[#167A58]">
              {duel.eyebrow}
            </p>
            <h3 className="text-2xl font-extrabold leading-tight tracking-[-0.035em] text-[#111318]">
              {duel.title}
            </h3>
            <p className="text-sm leading-relaxed text-[#4E5663]">
              {duel.matchupLine}
            </p>
          </div>
          <p className="text-sm font-medium leading-relaxed text-[#111318]">
            {duel.verdict}
          </p>
          <div className="flex items-center gap-1 text-sm font-bold text-[#1F8F6A] opacity-75 transition-opacity group-hover:opacity-100">
            {"לצפייה בהשוואה"}
            <ChevronLeft className="size-4" aria-hidden />
          </div>
        </div>

        {/* Product A -- vitabix */}
        <div className="flex flex-col items-center gap-3 border-b border-black/[0.05] px-5 py-6 text-center md:border-b-0">
          <div className="relative">
            {/* OLI in boxing gloves beside the winning pack, fully clear of it. Decorative.
                Mobile: smaller + tighter offset so it stays clear of the pack without
                overflowing the narrow single-column card. */}
            <Image
              src="/mascots/oli-boxing.png"
              alt=""
              width={820}
              height={900}
              aria-hidden
              className="pointer-events-none absolute bottom-0 -start-14 w-14 sm:-start-16 sm:w-16 md:-start-28 md:w-24"
            />
            <CarouselCardImage
              productId={vitabix.id}
              imageUrl={vitabix.imageUrl ?? CAROUSEL_PRODUCT_FALLBACK}
              imageAlt={vitabix.imageAlt}
              className="h-32 w-24 sm:h-36 sm:w-28"
              accent="#546E14"
            />
          </div>
          <ScoreChip score={vitabix.score} grade={vitabix.grade} />
          <p className="max-w-[7rem] text-xs font-bold leading-snug text-[#111318]">
            {vitabix.brand}
          </p>
        </div>

        {/* VS divider */}
        <div className="hidden items-center justify-center px-2 md:flex">
          <span className="flex h-10 w-10 items-center justify-center rounded-full border-2 border-[#D1D5D0] bg-[#F7F7F2] text-[0.6rem] font-extrabold text-[#6B7280]">
            VS
          </span>
        </div>

        {/* Product B -- lyon */}
        <div className="flex flex-col items-center gap-3 border-b border-black/[0.05] px-5 py-6 text-center md:border-b-0">
          <CarouselCardImage
            productId={lyon.id}
            imageUrl={lyon.imageUrl ?? CAROUSEL_PRODUCT_FALLBACK}
            imageAlt={lyon.imageAlt}
            className="h-32 w-24 sm:h-36 sm:w-28"
            accent="#8A6300"
          />
          <ScoreChip score={lyon.score} grade={lyon.grade} />
          <p className="max-w-[7rem] text-xs font-bold leading-snug text-[#111318]">
            {lyon.brand}
          </p>
        </div>
      </div>

      {/* === Bottom: insight strip + bullets === */}
      <div className="px-6 py-4">
        <div className="mb-3 rounded-xl border-r-[3px] border-[#1F8F6A] bg-[#F7F7F2] px-4 py-2.5">
          <p className="text-sm font-bold text-[#167A58]">{duel.insightStrip}</p>
        </div>
        <ul className="space-y-1.5">
          {duel.bullets.map((bullet, i) => (
            <li key={i} className="flex items-start gap-2 text-xs text-[#4E5663]">
              <span className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[#1F8F6A]" />
              {bullet}
            </li>
          ))}
        </ul>
        <p className="mt-3 text-[0.65rem] leading-relaxed text-[#5E6560]" dir="rtl">
          <span className="font-semibold">נתונים חלקיים</span>
          {" — "}
          חלק מנתוני הרכיבים עדיין בבדיקה — ההשוואה משקפת את מה שפורסם, והציונים עשויים להתעדכן.
        </p>
      </div>
    </Link>
  );
}
