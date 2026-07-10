"use client";

import Image from "next/image";
import Link from "next/link";
import { ArrowRight, ChevronLeft } from "lucide-react";

import { BlogEditorialBackdrop } from "@/components/blog/blog-editorial-backdrop";
import { HomeContainer } from "@/components/home/section-frame";
import { newsArticles, newsIndex, type NewsArticleCard } from "@/lib/news/news-index-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

/**
 * NewsIndexPage — חדשות index/hub.
 *
 * Mirrors the blog index ledger-row pattern (src/components/blog/blog-index-page.tsx)
 * for architectural consistency (uniform-baseline doctrine, TASK-521): same
 * backdrop, same HomeContainer/siteHeaderOffsetClass, same numbered-ledger-row
 * list styling. Left out on purpose vs. the blog index: the category filter
 * tabs and the "Bari Labs" strip — both blog-specific features that don't
 * apply to a single-category news list. Not a redesign, a proportional subset.
 */
function LedgerRow({ article, index }: { article: NewsArticleCard; index: number }) {
  const soon = !!article.comingSoon;
  const num = String(index + 1).padStart(2, "0");

  const metaParts = [article.published, article.readTime].filter(Boolean).join(" · ");

  const rowInner = (
    <div
      className={cn(
        "relative grid border-b border-[#E2E5E2] px-[18px] py-[26px] transition-colors duration-300",
        "[grid-template-columns:40px_1fr] gap-x-[22px]",
        "sm:[grid-template-columns:54px_1fr_120px] sm:gap-x-[30px]",
        !soon && "group-hover:bg-white"
      )}
    >
      {!soon && (
        <span
          className="pointer-events-none absolute inset-y-0 right-0 w-0.5 bg-[#167A58] opacity-0 transition-opacity duration-300 group-hover:opacity-100"
          aria-hidden
        />
      )}

      <div className="font-mono text-[18px] font-bold leading-none text-[#AAB0AC] pt-1 sm:text-[22px]">
        {num}
      </div>

      <div className="min-w-0">
        {metaParts && (
          <p className="font-mono text-[0.68rem] font-medium text-[#7A817C]">{metaParts}</p>
        )}
        <h3
          className={cn(
            "mt-2 text-[18px] font-extrabold leading-snug tracking-[-0.03em] text-[#111318] sm:text-[20px]",
            !soon && "transition-colors duration-300 group-hover:text-[#167A58]"
          )}
        >
          {article.title}
        </h3>
        <p className="mt-2 max-w-[62ch] text-[14.5px] leading-relaxed text-[#4E5663]">
          {article.description}
        </p>
      </div>

      <div className="hidden items-center sm:flex">
        {soon ? (
          <span className="rounded-full border border-[#7A817C]/30 px-3 py-1 text-[0.7rem] font-semibold text-[#7A817C]">
            בקרוב
          </span>
        ) : (
          <ChevronLeft
            className="size-[18px] text-[#167A58] opacity-55 transition-all duration-300 group-hover:opacity-100 group-hover:-translate-x-[3px]"
            style={{ marginInlineStart: "auto" }}
            aria-hidden
          />
        )}
      </div>
    </div>
  );

  if (soon) {
    return <li className="opacity-[0.62]">{rowInner}</li>;
  }

  return (
    <li>
      <Link href={article.href} className="group block">
        {rowInner}
      </Link>
    </li>
  );
}

export function NewsIndexPage() {
  return (
    <div
      className={cn(
        "relative min-h-screen overflow-hidden bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
      dir="rtl"
    >
      <BlogEditorialBackdrop />

      <HomeContainer className="relative py-12 md:py-16 lg:py-20">
        <header className="relative border-b border-black/[0.06] pb-10 md:pb-12">
          {/* OLI as news reporter, top-left of the header (RTL: opposite the text block).
              Decorative — same idiom as the homepage LUMO (home-guides.tsx). */}
          <Image
            src="/mascots/mascot-oli-news-reporter.webp"
            alt=""
            width={800}
            height={800}
            aria-hidden
            className="pointer-events-none absolute left-0 top-0 hidden w-40 lg:block xl:w-48"
          />
          <div className="max-w-3xl">
            <p className="font-mono text-[0.68rem] font-bold uppercase tracking-[0.32em] text-[#167A58]">
              {newsIndex.eyebrow}
            </p>
            <h1 className="mt-5 text-4xl font-extrabold tracking-[-0.055em] text-[#111318] md:text-[3.25rem] md:leading-[1.05]">
              {newsIndex.title}
            </h1>
            <p className="mt-4 text-xl font-semibold leading-snug tracking-[-0.02em] text-[#3A413D] md:text-2xl">
              {newsIndex.subtitle}
            </p>
            <p className="mt-4 max-w-xl text-base leading-relaxed text-[#4E5663]">
              {newsIndex.supporting}
            </p>
          </div>
        </header>

        <section className="mt-10 md:mt-12" aria-labelledby="news-articles-heading">
          <h2
            id="news-articles-heading"
            className="mb-6 text-sm font-bold uppercase tracking-[0.2em] text-[#7A817C]"
          >
            {newsIndex.articlesSectionLabel}
          </h2>

          {newsArticles.length > 0 ? (
            <ol className="border-t border-[#E2E5E2]">
              {newsArticles.map((article, i) => (
                <LedgerRow key={article.slug} article={article} index={i} />
              ))}
            </ol>
          ) : (
            <p className="rounded-xl border border-black/[0.06] bg-[#FFFFFF]/70 px-5 py-8 text-center text-sm text-[#4E5663]">
              אין עדיין כתבות חדשות.
            </p>
          )}
        </section>

        <footer className="mt-14 flex flex-col gap-4 border-t border-black/[0.06] pt-10 sm:flex-row sm:items-center sm:justify-between md:mt-16">
          <p className="max-w-md text-sm leading-relaxed text-[#7A817C]">
            {newsIndex.blogNote}{" "}
            <Link href={newsIndex.blogHref} className="font-semibold text-[#167A58] hover:underline">
              בלוג
            </Link>
            {" · "}
            {newsIndex.comparisonsNote}{" "}
            <Link
              href={newsIndex.comparisonsHref}
              className="font-semibold text-[#167A58] hover:underline"
            >
              השוואות
            </Link>
            .
          </p>
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-sm font-semibold text-[#4E5663] transition-colors hover:text-[#111318]"
          >
            <ArrowRight className="size-4" aria-hidden />
            דף הבית
          </Link>
        </footer>
      </HomeContainer>
    </div>
  );
}
