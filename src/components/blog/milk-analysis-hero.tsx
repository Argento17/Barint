"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { MilkOrbitVisual } from "@/components/shared/milk-orbit-visual";
import { HomeContainer } from "@/components/home/section-frame";
import { milkAnalysisArticle } from "@/lib/blog/milk-analysis-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

export function MilkAnalysisHero() {
  const { hero, disclaimer } = milkAnalysisArticle;

  return (
    <header
      className={cn(
        "relative overflow-hidden border-b border-black/[0.06] bg-[#FFFFFF]",
        siteHeaderOffsetClass,
        "max-h-[70vh]"
      )}
    >
      <HomeContainer className="flex max-h-[70vh] flex-col pt-3 pb-5 md:pt-4 md:pb-6">
        <Link
          href="/blog"
          className="mb-2 inline-flex shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
        >
          <ArrowRight className="size-4" aria-hidden />
          חזרה לבלוג
        </Link>

        <div className="grid min-h-0 flex-1 items-center gap-4 md:grid-cols-2 md:gap-8 lg:gap-10">
          <div className="order-2 flex flex-col justify-center text-right md:order-none md:col-start-1">
            <p className="text-sm font-bold text-[#1F8F6A]">{hero.eyebrow}</p>
            <h1 className="mt-2 text-balance text-3xl font-extrabold leading-[1.12] tracking-[-0.05em] text-[#111318] md:text-4xl lg:text-[2.65rem]">
              {hero.title}
            </h1>
            <p className="mt-2 max-w-xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
              {hero.subtitle}
            </p>
            <p className="mt-2 text-sm text-[#7A817C]">{hero.meta}</p>
            <p className="mt-3 max-w-xl text-xs leading-relaxed text-[#7A817C] md:text-sm">
              {disclaimer}
            </p>
          </div>

          <div className="order-1 flex min-h-0 items-center justify-center md:order-none md:col-start-2">
            <MilkOrbitVisual
              caption="אותו מדף — סיפורים שונים"
              className="h-[clamp(9rem,20vh,11.5rem)] md:h-[clamp(10rem,24vh,13rem)]"
            />
          </div>
        </div>
      </HomeContainer>
    </header>
  );
}
