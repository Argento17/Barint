import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { yogurtArticle } from "@/lib/blog/yogurt-article-content";

export function YogurtArticleHero() {
  const { hero, disclaimer } = yogurtArticle;

  return (
    <header className="relative overflow-hidden border-b border-black/6 bg-[#FFFFFF]">
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
          <h1 className="mt-3 text-balance text-3xl font-extrabold leading-[1.1] tracking-tighter text-[#111318] md:text-4xl lg:text-5xl">
            {hero.title}
          </h1>
          <p className="mt-3 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
            {hero.subtitle}
          </p>
          <p className="mt-2 text-sm text-[#7A817C]">{hero.meta}</p>

          <div className="mt-6 flex flex-wrap gap-8 border-t border-black/6 pt-5">
            <div>
              <p className="text-2xl font-extrabold tracking-tight text-[#111318]">19</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                מוצרים · שתי רשתות
              </p>
            </div>
            <div>
              <p className="text-2xl font-extrabold tracking-tight text-[#7A9450]">7 / A</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                מוצרים בדרגה A
              </p>
            </div>
            <div>
              <p className="text-2xl font-extrabold tracking-tight text-[#C0392B]">56</p>
              <p className="mt-0.5 text-xs font-bold uppercase tracking-[0.12em] text-[#7A817C]">
                נקודות פער · מהטוב לגרוע
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
