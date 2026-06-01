import Link from "next/link";
import { ArrowRight } from "lucide-react";

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
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="flex flex-col py-8 md:py-12">
        <Link
          href="/blog"
          className="mb-2 inline-flex shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
        >
          <ArrowRight className="size-4" aria-hidden />
          חזרה לבלוג
        </Link>

        <div className="flex max-w-3xl flex-col justify-center text-right">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#1F8F6A]">
            {hero.eyebrow}
          </p>
          <h1 className="mt-3 text-balance text-3xl font-extrabold leading-[1.1] tracking-[-0.05em] text-[#111318] md:text-4xl lg:text-5xl">
            {hero.title}
          </h1>
          <p className="mt-3 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
            {hero.subtitle}
          </p>
          <p className="mt-2 text-sm text-[#7A817C]">{hero.meta}</p>

          <div className="mt-6 flex gap-8 border-t border-black/[0.06] pt-5">
            <div>
              <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">18</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                מוצרים נותחו
              </p>
            </div>
            <div>
              <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">5</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                סוגי מוצר
              </p>
            </div>
            <div>
              <p className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318]">עשרות</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                אותות תזונה
              </p>
            </div>
          </div>

          <p className="mt-4 max-w-xl text-xs leading-relaxed text-[#7A817C] md:text-sm">
            {disclaimer}
          </p>
        </div>
      </HomeContainer>
    </header>
  );
}
