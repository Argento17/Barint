import Image from "next/image";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";

import { featuredArticle, secondaryArticles } from "@/lib/blog/blog-index-content";
import { cn } from "@/lib/utils";

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
              className={cn(
                "relative flex h-full min-h-[11.5rem] flex-col overflow-hidden",
                "rounded-2xl border border-[rgba(17,19,24,0.09)] bg-white p-5 pt-[calc(1.25rem+0.4rem)]",
                "shadow-[0_1px_2px_rgba(17,19,24,0.05)]",
                !article.comingSoon && [
                  "transition-[transform,box-shadow] duration-200",
                  "hover:-translate-y-[3px] hover:shadow-[0_22px_48px_-28px_rgba(17,19,24,0.3)]",
                  "motion-reduce:transition-none motion-reduce:hover:translate-y-0",
                ]
              )}
            >
              <div className="absolute inset-x-0 top-0 h-[0.4rem] bg-[#1F8F6A]" aria-hidden />
              <p className="text-xs font-bold text-[#167A58]">{article.categoryLabel}</p>
              <h3
                className="mt-2 text-lg font-extrabold leading-snug text-[#111318]"
                style={{ fontFamily: "var(--font-heading, var(--font-sans))" }}
              >
                {article.title}
              </h3>
              <p className="mt-2 flex-1 text-base leading-relaxed text-[#4E5663]">
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
