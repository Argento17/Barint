import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { milkEditorialHero } from "@/lib/comparisons/milk-editorial-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

export function MilkCinematicHero() {
  return (
    <header
      className={cn(
        "relative overflow-hidden border-b border-black/[0.06] bg-[#FFFFFF] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="flex flex-col py-8 md:py-12">
        <Link
          href="/hashvaot"
          className="mb-4 inline-flex w-fit shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
        >
          <ArrowRight className="size-4" aria-hidden />
          חזרה להשוואות
        </Link>

        <div className="max-w-3xl text-right">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">
            {milkEditorialHero.eyebrow}
          </p>
          <h1 className="mt-3 text-balance text-3xl font-extrabold leading-[1.1] tracking-[-0.05em] text-[#111318] md:text-4xl lg:text-5xl">
            {milkEditorialHero.title}
          </h1>
          <p className="mt-3 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
            {milkEditorialHero.subtitle}
          </p>
          <p className="mt-2 text-sm text-[#7A817C]">{milkEditorialHero.meta}</p>

          <div className="mt-6 flex gap-8 border-t border-black/[0.06] pt-5">
            <div>
              <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">18</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                מוצרים
              </p>
            </div>
            <div>
              <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">5</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                קטגוריות
              </p>
            </div>
            <div>
              <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">עשרות</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                אותות ניתוח
              </p>
            </div>
          </div>

          <p className="mt-5 text-sm font-semibold text-[#1F8F6A]">
            <Link href="/blog/milk-analysis" className="hover:underline">
              קראו את הניתוח העיתונאי בבלוג ←
            </Link>
          </p>
        </div>
      </HomeContainer>
    </header>
  );
}
