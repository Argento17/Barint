import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { upfArticle } from "@/lib/blog/upf-article-content";

export function UpfArticleHero() {
  const { hero } = upfArticle;

  return (
    <header className="relative border-b border-black/6 bg-[#FFFFFF]">
      <HomeContainer className="flex flex-col py-8 md:py-12">
        <Link
          href="/blog"
          className="mb-2 inline-flex shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
        >
          <ArrowRight className="size-4" aria-hidden />
          חזרה לבלוג
        </Link>

        <div className="flex max-w-3xl flex-col justify-center text-right">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#167A58]">
            {hero.eyebrow}
          </p>
          <h1 className="mt-3 text-balance text-3xl font-extrabold leading-[1.1] tracking-tighter text-[#111318] md:text-4xl lg:text-5xl">
            {hero.title}
          </h1>
          <p className="mt-3 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
            {hero.subtitle}
          </p>
          <p className="mt-2 text-sm text-[#5E6672]">{hero.meta}</p>
        </div>
      </HomeContainer>
    </header>
  );
}
