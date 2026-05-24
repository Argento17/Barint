"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { ArrowRight, ChevronLeft, Clock } from "lucide-react";

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

function FeaturedArticleCard({ article }: { article: BlogArticleCard }) {
  return (
    <Link
      href={article.href}
      className="group relative block overflow-hidden rounded-[1.5rem] border border-[#1A1D24]/[0.09] bg-[#FFFFFF] shadow-[0_40px_120px_-72px_rgba(17,19,24,0.45)] ring-1 ring-black/[0.04] transition-[transform,box-shadow,border-color] duration-500 ease-out hover:-translate-y-1 hover:border-[#1F8F6A]/22 hover:shadow-[0_48px_140px_-64px_rgba(31,143,106,0.28)]"
    >
      <div
        className="pointer-events-none absolute inset-0 bg-gradient-to-bl from-[#E8F5EF]/50 via-transparent to-transparent opacity-80 transition-opacity duration-500 group-hover:opacity-100"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute -left-24 top-1/2 h-64 w-64 -translate-y-1/2 rounded-full bg-[#1F8F6A]/6 blur-3xl transition-all duration-700 group-hover:bg-[#1F8F6A]/10"
        aria-hidden
      />

      <div className="relative p-7 md:p-10 lg:p-12">
        <div className="min-w-0 text-right">
          <span className="inline-flex rounded-full border border-[#1F8F6A]/18 bg-[#F7F7F2]/90 px-3 py-1 text-[0.7rem] font-bold tracking-wide text-[#1F8F6A]">
            {article.categoryLabel}
          </span>
          <h2 className="mt-5 font-heading text-3xl font-extrabold leading-[1.12] tracking-[-0.045em] text-[#111318] transition-colors duration-300 group-hover:text-[#1F8F6A] md:text-[2.15rem] lg:text-[2.35rem]">
            {article.title}
          </h2>
          <p className="mt-4 max-w-2xl text-base leading-[1.75] text-[#4E5663] md:text-[1.05rem]">
            {article.description}
          </p>
          {article.metaLine ? (
            <p className="mt-5 font-mono text-[0.72rem] font-medium tracking-wide text-[#7A817C] md:text-xs">
              {article.metaLine}
            </p>
          ) : null}
          <span className="mt-8 inline-flex items-center gap-2 rounded-full bg-[#1F8F6A] px-6 py-3 text-sm font-bold text-[#F7F7F2] shadow-md shadow-[#1F8F6A]/20 transition-[transform,box-shadow] duration-300 group-hover:shadow-lg group-hover:shadow-[#1F8F6A]/28">
            {article.cta}
            <ChevronLeft
              className="size-4 transition-transform duration-300 group-hover:-translate-x-0.5"
              aria-hidden
            />
          </span>
        </div>
      </div>
    </Link>
  );
}

function SecondaryArticleCard({ article }: { article: BlogArticleCard }) {
  const soon = article.comingSoon;

  const content = (
    <>
      <div className="flex items-center justify-between gap-3">
        <span className="rounded-md border border-black/[0.06] bg-[#F7F7F2]/80 px-2 py-0.5 text-[0.65rem] font-bold text-[#4E5663]">
          {article.categoryLabel}
        </span>
        <span className="inline-flex items-center gap-1 text-[0.7rem] font-medium text-[#7A817C]">
          <Clock className="size-3" aria-hidden />
          {article.readTime}
        </span>
      </div>
      <h3
        className={cn(
          "mt-4 text-lg font-extrabold leading-snug tracking-[-0.03em] text-[#111318]",
          !soon && "transition-colors duration-300 group-hover:text-[#1F8F6A]"
        )}
      >
        {article.title}
      </h3>
      <p className="mt-2.5 text-sm leading-relaxed text-[#4E5663]">{article.description}</p>
      <div className="mt-5 flex items-center justify-between border-t border-black/[0.05] pt-4">
        <span
          className={cn(
            "text-sm font-semibold",
            soon ? "text-[#7A817C]" : "text-[#1F8F6A]"
          )}
        >
          {soon ? "בקרוב" : article.cta}
        </span>
        {!soon ? (
          <ChevronLeft
            className="size-4 text-[#1F8F6A] opacity-0 transition-all duration-300 group-hover:opacity-100 group-hover:-translate-x-0.5"
            aria-hidden
          />
        ) : null}
      </div>
    </>
  );

  if (soon) {
    return (
      <div className="rounded-[1.2rem] border border-dashed border-black/[0.1] bg-[#FFFFFF]/55 p-5 md:p-6">
        {content}
      </div>
    );
  }

  return (
    <Link
      href={article.href}
      className="group block rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF]/95 p-5 shadow-[0_12px_40px_-28px_rgba(17,19,24,0.2)] transition-[border-color,box-shadow,transform] duration-300 ease-out hover:-translate-y-0.5 hover:border-[#1F8F6A]/18 hover:shadow-[0_20px_56px_-24px_rgba(31,143,106,0.18)] md:p-6"
    >
      {content}
    </Link>
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

  const showFeatured = articleMatchesCategory(featuredArticle, activeCategory);

  const filteredSecondary = useMemo(
    () => secondaryArticles.filter((a) => articleMatchesCategory(a, activeCategory)),
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

        {/* Featured */}
        {showFeatured ? (
          <section className="mt-10 md:mt-12" aria-labelledby="blog-featured-heading">
            <div className="mb-5 flex items-end justify-between gap-4">
              <h2
                id="blog-featured-heading"
                className="text-sm font-bold uppercase tracking-[0.2em] text-[#7A817C]"
              >
                {blogIndex.featuredSectionLabel}
              </h2>
              <span className="hidden h-px flex-1 max-w-xs bg-gradient-to-l from-[#1F8F6A]/25 to-transparent sm:block" />
            </div>
            <FeaturedArticleCard article={featuredArticle} />
          </section>
        ) : null}

        {/* Filters + grid */}
        <section className="mt-14 md:mt-16" aria-labelledby="blog-articles-heading">
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

          {filteredSecondary.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2 lg:gap-5">
              {filteredSecondary.map((article) => (
                <SecondaryArticleCard key={article.slug} article={article} />
              ))}
            </div>
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
