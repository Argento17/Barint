# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(r"c:\Bari\bari-web\src")

(ROOT / "components/home/home-hero.tsx").write_text(r'''import Link from "next/link";
import { Search } from "lucide-react";

import { Button } from "@/components/ui/button";
import { HERO_COPY } from "@/lib/home/hero-copy";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

import { HeroStillLife } from "./hero-still-life";
import { HomeContainer } from "./section-frame";

export function HomeHero() {
  return (
    <section
      className={cn(
        "relative overflow-hidden border-b border-black/[0.06] bg-[#F7F7F2]",
        siteHeaderOffsetClass
      )}
    >
      <div
        className="pointer-events-none absolute inset-0 -z-10"
        aria-hidden
        style={{
          background:
            "radial-gradient(ellipse 70% 55% at 22% 45%, rgba(47,174,130,0.06) 0%, transparent 68%), radial-gradient(ellipse 50% 40% at 85% 20%, rgba(255,255,255,0.9) 0%, transparent 70%)",
        }}
      />

      <HomeContainer className="py-14 md:py-20 lg:py-24">
        <div
          className="grid items-center gap-10 md:grid-cols-2 md:gap-8 lg:gap-14"
          dir="rtl"
        >
          <div className="flex flex-col items-start gap-6 text-right md:max-w-xl">
            <h1 className="text-balance text-4xl font-extrabold leading-[1.05] tracking-[-0.04em] text-[#111318] sm:text-5xl lg:text-[3.75rem]">
              <span className="block">{HERO_COPY.headline1}</span>
              <span className="block text-[#167A58]">{HERO_COPY.headline2}</span>
            </h1>

            <p className="max-w-lg text-pretty text-lg leading-relaxed text-[#4E5663] md:text-xl">
              {HERO_COPY.subline}
            </p>

            <div className="flex w-full max-w-sm flex-col items-stretch gap-3 sm:items-start">
              <Button
                size="lg"
                className="h-[3.25rem] rounded-2xl border border-[#1F8F6A]/10 bg-[#167A58] px-8 text-base font-bold text-[#F7F7F2] shadow-[0_16px_40px_-16px_rgba(22,122,88,0.45)] transition-[box-shadow,transform,background-color] duration-500 ease-out hover:-translate-y-px hover:bg-[#1A8E64]"
                asChild
              >
                <Link href="/hashvaot" className="inline-flex items-center justify-center gap-2">
                  <Search className="size-4" aria-hidden />
                  {HERO_COPY.primaryCta}
                </Link>
              </Button>

              <p className="text-center text-sm font-semibold text-[#9A9FA6] sm:text-start">
                {HERO_COPY.secondaryCta}
              </p>
            </div>
          </div>

          <div className="flex justify-center md:justify-end">
            <HeroStillLife />
          </div>
        </div>
      </HomeContainer>
    </section>
  );
}
''', encoding="utf-8")

(ROOT / "components/home/featured-comparison-card.tsx").write_text(r'''"use client";

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
    <Link
      href={duel.href}
      className={`group block overflow-hidden rounded-[1.75rem] border border-black/[0.07] bg-[#FFFFFF] shadow-[0_20px_50px_-24px_rgba(17,19,24,0.22)] transition-[border-color,box-shadow,transform] duration-300 hover:-translate-y-0.5 hover:border-[#1F8F6A]/22 hover:shadow-[0_28px_60px_-24px_rgba(31,143,106,0.2)] ${className}`}
      dir="rtl"
    >
      <div className="flex items-start justify-between gap-4 border-b border-black/[0.05] px-6 pb-4 pt-6">
        <div className="min-w-0 space-y-1">
          <p className="text-xs font-bold tracking-wide text-[#167A58]">{duel.eyebrow}</p>
          <h3 className="text-balance text-2xl font-extrabold tracking-[-0.035em] text-[#111318]">
            {duel.title}
          </h3>
        </div>
        <span className="shrink-0 rounded-full bg-[#E8F5EF] px-3.5 py-1.5 text-[0.65rem] font-bold text-[#1F8F6A]">
          {"\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4"}
        </span>
      </div>

      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-2 px-6 py-6">
        <div className="flex flex-col items-center gap-4 text-center">
          <CarouselCardImage
            productId={vitabix.id}
            imageUrl={vitabix.imageUrl ?? CAROUSEL_PRODUCT_FALLBACK}
            imageAlt={vitabix.imageAlt}
            className="h-32 w-24 sm:h-36 sm:w-28"
            accent="#546E14"
          />
          <ScoreChip score={vitabix.score} grade={vitabix.grade} />
          <p className="text-xs font-bold leading-snug text-[#111318] line-clamp-2 max-w-[9rem]">
            {vitabix.brand}
          </p>
        </div>

        <div className="flex shrink-0 items-center justify-center px-2">
          <span className="flex h-11 w-11 items-center justify-center rounded-full border-2 border-[#D1D5D0] bg-[#F7F7F2] text-[0.65rem] font-extrabold text-[#6B7280]">
            VS
          </span>
        </div>

        <div className="flex flex-col items-center gap-4 text-center">
          <CarouselCardImage
            productId={lyon.id}
            imageUrl={lyon.imageUrl ?? CAROUSEL_PRODUCT_FALLBACK}
            imageAlt={lyon.imageAlt}
            className="h-32 w-24 sm:h-36 sm:w-28"
            accent="#8A6300"
          />
          <ScoreChip score={lyon.score} grade={lyon.grade} />
          <p className="text-xs font-bold leading-snug text-[#111318] line-clamp-2 max-w-[9rem]">
            {lyon.brand}
          </p>
        </div>
      </div>

      <div className="mx-6 mb-5 rounded-xl border-r-[3px] border-[#1F8F6A] bg-[#F7F7F2] px-4 py-3">
        <p className="text-sm font-medium leading-relaxed text-[#111318]">{duel.takeaway}</p>
      </div>

      <div className="flex items-center justify-end gap-1 px-6 pb-5 text-sm font-bold text-[#1F8F6A] opacity-75 transition-opacity group-hover:opacity-100">
        {"\u05dc\u05e6\u05e4\u05d9\u05d9\u05d4 \u05d1\u05d4\u05e9\u05d5\u05d5\u05d0\u05d4"}
        <ChevronLeft className="size-4" aria-hidden />
      </div>
    </Link>
  );
}
''', encoding="utf-8")

# Patch home-comparisons featured section
comp = (ROOT / "components/home/home-comparisons.tsx").read_text(encoding="utf-8")
old = """        {/* Featured duel card — pilot, above carousel */}
        <div className=\"reveal-up mb-8 max-w-md md:max-w-sm\" dir=\"rtl\">
          <FeaturedComparisonCard />
        </div>"""

new = """        {/* Featured duel — premium pilot card */}
        <div className=\"reveal-up mb-10\" dir=\"rtl\">
          <FeaturedComparisonCard className=\"mx-auto w-full max-w-2xl\" />
        </div>"""

if old not in comp:
    raise SystemExit("comparisons patch anchor missing")
comp = comp.replace(old, new)
(ROOT / "components/home/home-comparisons.tsx").write_text(comp, encoding="utf-8")

print("wrote hero + featured + comparisons patch")
