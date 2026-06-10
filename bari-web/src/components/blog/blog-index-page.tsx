"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ArrowRight, ChevronLeft } from "lucide-react";

import { BlogEditorialBackdrop } from "@/components/blog/blog-editorial-backdrop";
import { HomeContainer } from "@/components/home/section-frame";
import {
  articleMatchesCategory,
  blogCategories,
  blogIndex,
  featuredArticle,
  secondaryArticles,
  type BlogArticleCard,
  type BlogCategoryId,
} from "@/lib/blog/blog-index-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

function LedgerRow({ article, index }: { article: BlogArticleCard; index: number }) {
  const soon = !!article.comingSoon;
  const isFeatured = !!article.featured;
  const num = String(index + 1).padStart(2, "0");

  const metaParts = [article.categoryLabel, article.readTime, article.published]
    .filter(Boolean)
    .join(" · ");

  const rowInner = (
    <div
      className={cn(
        "relative grid border-b border-[#E2E5E2] px-[18px] py-[26px] transition-colors duration-300",
        "[grid-template-columns:40px_1fr] gap-x-[22px]",
        "sm:[grid-template-columns:54px_1fr_248px] sm:gap-x-[30px]",
        !soon && "group-hover:bg-white"
      )}
    >
      {/* Right-edge green bar */}
      {!soon && (
        <span
          className="pointer-events-none absolute inset-y-0 right-0 w-0.5 bg-[#1F8F6A] opacity-0 transition-opacity duration-300 group-hover:opacity-100"
          aria-hidden
        />
      )}

      {/* Index number */}
      <div
        className={cn(
          "font-mono font-bold leading-none pt-1",
          "text-[18px] sm:text-[22px]",
          isFeatured ? "text-[#1F8F6A]" : "text-[#AAB0AC]"
        )}
      >
        {num}
      </div>

      {/* Body */}
      <div className="min-w-0">
        {metaParts && (
          <p className="font-mono text-[0.68rem] font-medium text-[#7A817C]">{metaParts}</p>
        )}
        <h3
          className={cn(
            "mt-2 font-extrabold leading-snug tracking-[-0.03em] text-[#111318]",
            "text-[18px] sm:text-[20px]",
            isFeatured && "sm:text-[26px]",
            !soon && "transition-colors duration-300 group-hover:text-[#1F8F6A]"
          )}
        >
          {article.title}
        </h3>
        <p className="mt-2 max-w-[62ch] text-[14.5px] leading-relaxed text-[#4E5663]">
          {article.description}
        </p>
      </div>

      {/* Rail — hidden on mobile */}
      <div className="hidden sm:flex items-center">
        {article.stat ? (
          <div className="font-mono">
            <span className="block text-[27px] font-extrabold leading-none text-[#1F8F6A]">
              {article.stat.value}
            </span>
            <span className="block mt-0.5 text-[11px] text-[#7A817C]">
              {article.stat.unit}
            </span>
          </div>
        ) : soon ? (
          <span className="rounded-full border border-[#7A817C]/30 px-3 py-1 text-[0.7rem] font-semibold text-[#7A817C]">
            בקרוב
          </span>
        ) : null}
        {!soon && (
          <ChevronLeft
            className="size-[18px] text-[#1F8F6A] opacity-55 transition-all duration-300 group-hover:opacity-100 group-hover:-translate-x-[3px]"
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

function BariLabsStrip() {
  const { labs } = blogIndex;

  return (
    <section
      className="relative overflow-hidden rounded-[1.35rem] border border-[#1F8F6A]/15 bg-[#111318] px-6 py-8 text-[#F7F7F2] md:px-10 md:py-10"
      aria-labelledby="bari-labs-heading"
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_80%_60%_at_100%_0%,rgba(31,143,106,0.22),transparent_55%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.12]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(247,247,242,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(247,247,242,0.08) 1px, transparent 1px)",
          backgroundSize: "24px 24px",
        }}
        aria-hidden
      />
      <div className="relative max-w-2xl text-right">
        <p className="text-[0.65rem] font-bold uppercase tracking-[0.28em] text-[#1F8F6A]">
          Bari Labs
        </p>
        <h2
          id="bari-labs-heading"
          className="mt-3 text-2xl font-extrabold tracking-[-0.04em] md:text-3xl"
        >
          {labs.title}
        </h2>
        <p className="mt-4 text-base leading-relaxed text-[#C8CDC9]">{labs.text}</p>
        <ul className="mt-6 flex flex-wrap gap-2">
          {labs.tags.map((tag) => (
            <li
              key={tag}
              className="rounded-full border border-[#F7F7F2]/12 bg-[#F7F7F2]/[0.06] px-3 py-1 text-xs font-semibold text-[#E8EBE9]"
            >
              {tag}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export function BlogIndexPage() {
  const [activeCategory, setActiveCategory] = useState<BlogCategoryId>("all");

  const filteredArticles = useMemo(
    () =>
      [featuredArticle, ...secondaryArticles].filter((a) =>
        articleMatchesCategory(a, activeCategory)
      ),
    [activeCategory]
  );

  return (
    <main
      className={cn(
        "relative min-h-screen overflow-hidden bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <BlogEditorialBackdrop />

      <HomeContainer className="relative py-12 md:py-16 lg:py-20">
        {/* Hero */}
        <header className="max-w-3xl border-b border-black/[0.06] pb-10 md:pb-12">
          <p className="font-mono text-[0.68rem] font-bold uppercase tracking-[0.32em] text-[#1F8F6A]">
            {blogIndex.eyebrow}
          </p>
          <h1 className="mt-5 text-4xl font-extrabold tracking-[-0.055em] text-[#111318] md:text-[3.25rem] md:leading-[1.05]">
            {blogIndex.title}
          </h1>
          <p className="mt-4 text-xl font-semibold leading-snug tracking-[-0.02em] text-[#3A413D] md:text-2xl">
            {blogIndex.subtitle}
          </p>
          <p className="mt-4 max-w-xl text-base leading-relaxed text-[#4E5663]">
            {blogIndex.supporting}
          </p>
        </header>

        {/* Filters + ledger */}
        <section className="mt-10 md:mt-12" aria-labelledby="blog-articles-heading">
          <div className="mb-6 flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
            <h2
              id="blog-articles-heading"
              className="text-sm font-bold uppercase tracking-[0.2em] text-[#7A817C]"
            >
              {blogIndex.articlesSectionLabel}
            </h2>
            <div
              className="flex flex-wrap gap-2"
              role="tablist"
              aria-label="סינון לפי נושא"
            >
              {blogCategories.map((cat) => {
                const active = activeCategory === cat.id;
                return (
                  <button
                    key={cat.id}
                    type="button"
                    role="tab"
                    aria-selected={active}
                    onClick={() => setActiveCategory(cat.id)}
                    className={cn(
                      "rounded-full border px-3.5 py-2 text-sm font-semibold transition-[background-color,border-color,color,box-shadow] duration-300",
                      active
                        ? "border-[#1F8F6A]/30 bg-[#1F8F6A] text-[#F7F7F2] shadow-sm shadow-[#1F8F6A]/15"
                        : "border-black/[0.08] bg-[#FFFFFF]/80 text-[#4E5663] hover:border-[#1F8F6A]/20 hover:text-[#111318]"
                    )}
                  >
                    {cat.label}
                  </button>
                );
              })}
            </div>
          </div>

          {filteredArticles.length > 0 ? (
            <ol className="border-t border-[#E2E5E2]">
              {filteredArticles.map((article, i) => (
                <LedgerRow key={article.slug} article={article} index={i} />
              ))}
            </ol>
          ) : (
            <p className="rounded-xl border border-black/[0.06] bg-[#FFFFFF]/70 px-5 py-8 text-center text-sm text-[#4E5663]">
              אין עדיין כתבות בנושא זה — ניתוח החלב זמין בניתוח המוביל או בקטגוריית מדף ישראלי.
            </p>
          )}
        </section>

        <div className="mt-14 md:mt-16">
          <BariLabsStrip />
        </div>

        <footer className="mt-12 flex flex-col gap-4 border-t border-black/[0.06] pt-10 sm:flex-row sm:items-center sm:justify-between">
          <p className="max-w-md text-sm leading-relaxed text-[#7A817C]">
            {blogIndex.comparisonsNote}{" "}
            <Link href={blogIndex.comparisonsHref} className="font-semibold text-[#1F8F6A] hover:underline">
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
    </main>
  );
}
