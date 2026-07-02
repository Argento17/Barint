import Image from "next/image";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { featuredArticle, secondaryArticles } from "@/lib/blog/blog-index-content";

import { HomeContainer } from "./section-frame";

export function HomeGuides() {
  const teasers = [featuredArticle, ...secondaryArticles.slice(0, 3)];

  return (
    <section className="relative overflow-hidden bg-[#F7F7F2] py-14 md:py-20" id="guides">
      <HomeContainer>
        <div className="relative mb-10 flex flex-col gap-4 md:mb-12 md:flex-row md:items-end md:justify-between">
          <div className="max-w-2xl text-right">
            <p className="text-sm font-bold text-[#167A58]">ניתוחים אחרונים</p>
            <h2 className="mt-2 text-balance text-3xl font-extrabold tracking-[-0.045em] text-[#111318] md:text-4xl">
              מהמדף ומהמעבדה
            </h2>
            <p className="mt-3 text-base leading-relaxed text-[#4E5663]">
              ניתוחים עיתונאיים ממוצרים אמיתיים — חלב, לחם, דגנים ומרכיבים. הניתוח המוביל
              מופיע כאן; שאר הקטגוריות נפתחות בהדרגה.
            </p>
          </div>
          {/* LUMO hanging from a branch beside the title, above the article batch. Decorative. */}
          <Image
            src="/mascots/lumo-tree.png"
            alt=""
            width={1100}
            height={869}
            aria-hidden
            className="pointer-events-none hidden w-44 shrink-0 self-start lg:block lg:-translate-x-10 lg:translate-y-8"
          />
          <div className="flex items-center gap-2 md:ms-auto md:flex-col md:items-center md:gap-1">
            <Link
              href="/blog"
              className="inline-flex items-center gap-1 text-sm font-bold text-[#167A58] hover:underline"
            >
              כל הניתוחים
              <ChevronLeft className="size-4" aria-hidden />
            </Link>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          {teasers.map((article) => (
            <article
              key={article.slug}
              className="flex h-full min-h-[11.5rem] flex-col rounded-[1.25rem] border border-black/[0.07] bg-[#FFFFFF]/80 p-5"
            >
              <p className="text-xs font-bold text-[#167A58]">{article.categoryLabel}</p>
              <h3 className="mt-2 text-lg font-extrabold leading-snug text-[#111318]">
                {article.title}
              </h3>
              <p className="mt-2 flex-1 text-sm leading-relaxed text-[#4E5663]">
                {article.description}
              </p>
              <p className="mt-2 text-xs text-[#5E6560]">{article.readTime}</p>
              {article.comingSoon ? (
                <span className="mt-3 text-sm font-bold text-[#5E6560]">בקרוב</span>
              ) : (
                <Link
                  href={article.href}
                  className="mt-3 inline-flex items-center gap-1 text-sm font-bold text-[#167A58] hover:underline"
                >
                  {article.cta}
                  <ChevronLeft className="size-4" aria-hidden />
                </Link>
              )}
            </article>
          ))}
        </div>
      </HomeContainer>
    </section>
  );
}
