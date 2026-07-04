import Image from "next/image";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { seedOilsArticle } from "@/lib/blog/seed-oils-article-content";

export function SeedOilsArticleHero() {
  const { hero } = seedOilsArticle;

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

        <div className="flex flex-col-reverse items-center gap-6 md:flex-row md:items-end md:justify-between md:gap-8">
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
            <p className="mt-2 text-sm text-[#7A817C]">{hero.meta}</p>
          </div>

          {/* LUMO — The Investigator — inspects seed oils with a magnifying
              glass. Decorative hero placement per Character Bible (job-to-be-
              done: investigation -> LUMO). Visible at every breakpoint,
              scaled up progressively — no `hidden ... md:block` mobile-hide.
              `overflow-visible` wrapper + no clipping ancestor (the `<header>`
              no longer carries `overflow-hidden`) so the mascot can never be
              cropped by its container; `h-auto` preserves the source's native
              580:665 ratio so the full figure (incl. feet) always renders. */}
          <div className="shrink-0 overflow-visible py-1">
            <Image
              src="/mascots/mascot-seedoils.png"
              alt=""
              width={580}
              height={665}
              aria-hidden
              priority
              className="pointer-events-none h-auto w-32 select-none sm:w-40 md:w-48 lg:w-56"
            />
          </div>
        </div>
      </HomeContainer>
    </header>
  );
}
