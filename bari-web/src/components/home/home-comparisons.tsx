"use client";

import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { FeaturedComparisonCard } from "@/components/home/featured-comparison-card";
import { HERO_COPY } from "@/lib/home/hero-copy";

import { HomeContainer } from "./section-frame";

export function HomeComparisons() {
  return (
    <section className="relative overflow-hidden bg-[#F7F7F2] py-14 md:py-20" id="comparisons">
      <HomeContainer>
        {/* Centered section head per v5 spec */}
        <div className="reveal-up mb-10 flex flex-col items-center gap-3 text-center" dir="rtl">
          <p className="text-sm font-bold text-[#167A58]">{HERO_COPY.comparisonsEyebrow}</p>
          <h2 className="text-balance text-3xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-4xl">
            {HERO_COPY.comparisonsTitle}
          </h2>
          <p className="max-w-xl text-pretty text-base leading-relaxed text-[#4E5663]">
            {HERO_COPY.comparisonsSubtitle}
          </p>
          <Link
            href="/hashvaot"
            className="mt-1 inline-flex items-center gap-1 text-sm font-semibold text-[#1F8F6A] hover:underline"
          >
            כל ההשוואות
            <ChevronLeft className="size-4" aria-hidden />
          </Link>
        </div>

        {/* Featured comparison card owns its own chrome (hub finding-card
            language) -- this wrapper only centers/constrains width. */}
        <div className="reveal-up mx-auto" style={{ maxWidth: "1180px" }} dir="rtl">
          <FeaturedComparisonCard />
        </div>
      </HomeContainer>
    </section>
  );
}
