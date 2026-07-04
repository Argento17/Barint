"use client";

import { Fragment, type ReactNode } from "react";
import Link from "next/link";
import { ArrowLeft, ChevronLeft } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

import { SeedOilsArticleHero } from "@/components/blog/seed-oils-article-hero";
import { SeedOilsClaimsTable } from "@/components/blog/seed-oils-claims-table";
import { SeedOilsCookiesChart } from "@/components/blog/seed-oils-cookies-chart";
import { HomeContainer } from "@/components/home/section-frame";
import { HASHVAOT_HREF, seedOilsArticle } from "@/lib/blog/seed-oils-article-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

/**
 * Renders a paragraph string with `**bold**` markers from the source draft
 * as inline emphasis, without dangerouslySetInnerHTML. Copy itself is ported
 * verbatim from the approved draft -- this only interprets the markdown-style
 * bold markers the draft already contains (e.g. "**ראשון**", "**אותו מדף**").
 */
function RichParagraph({ text, className }: { text: string; className?: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g).filter(Boolean);
  return (
    <p className={className}>
      {parts.map((part, i) => {
        if (part.startsWith("**") && part.endsWith("**")) {
          return (
            <strong key={i} className="font-extrabold text-[#111318]">
              {part.slice(2, -2)}
            </strong>
          );
        }
        return <Fragment key={i}>{part}</Fragment>;
      })}
    </p>
  );
}

function ArticleSection({
  id,
  eyebrowLabel,
  title,
  paragraphs,
  tone = "cream",
  afterContent,
  insetContent,
}: {
  id: string;
  eyebrowLabel: string;
  title: string;
  paragraphs: string[];
  tone?: "cream" | "white";
  /** Rendered after the paragraphs, inside the same max-w-3xl column (e.g. the cookies chart). */
  afterContent?: ReactNode;
  /** Rendered between paragraphs[1] and paragraphs[2] to break up a long section (e.g. the claims table). */
  insetContent?: ReactNode;
}) {
  const reduceMotion = useReducedMotion();
  return (
    <section
      id={id}
      className={cn(
        "border-t border-black/6 py-10 md:py-14",
        tone === "white" ? "bg-[#FFFFFF]" : "bg-[#F7F7F2]",
      )}
    >
      <HomeContainer>
        <div className="mx-auto max-w-3xl">
          <header className="mb-6 text-right">
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
              {eyebrowLabel}
            </p>
            <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
              {title}
            </h2>
          </header>
          <div className="space-y-4">
            {paragraphs.map((p, i) => (
              <Fragment key={i}>
                <motion.div
                  initial={reduceMotion ? false : { opacity: 0, y: 6 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, margin: "-30px" }}
                  transition={{ duration: 0.35, delay: Math.min(i, 3) * 0.03 }}
                >
                  <RichParagraph
                    text={p}
                    className="text-base leading-[1.85] text-[#111318] md:text-lg"
                  />
                </motion.div>
                {insetContent && i === 1 ? <div className="py-2">{insetContent}</div> : null}
              </Fragment>
            ))}
          </div>
          {afterContent ? <div className="mt-8">{afterContent}</div> : null}
        </div>
      </HomeContainer>
    </section>
  );
}

function RecentArticleCard({
  href,
  title,
  description,
  category,
  readTime,
  cta,
  comingSoon,
}: {
  href: string;
  title: string;
  description: string;
  category: string;
  readTime: string;
  cta: string;
  comingSoon?: boolean;
}) {
  return (
    <li className="rounded-[1.1rem] border border-black/[0.07] bg-[#FFFFFF] p-5">
      <p className="text-[0.65rem] font-bold uppercase tracking-[0.12em] text-[#7A817C]">
        {category} · {readTime}
      </p>
      <h3 className="mt-2 text-base font-extrabold leading-snug tracking-[-0.02em] text-[#111318]">
        {title}
      </h3>
      <p className="mt-2 text-sm leading-relaxed text-[#4E5663]">{description}</p>
      {comingSoon ? (
        <p className="mt-4 text-xs font-bold text-[#7A817C]">בקרוב</p>
      ) : (
        <Link
          href={href}
          className="mt-4 inline-flex items-center gap-1.5 text-xs font-bold text-[#167A58] hover:underline"
        >
          {cta}
          <ChevronLeft className="size-3.5" aria-hidden />
        </Link>
      )}
    </li>
  );
}

export function SeedOilsArticle() {
  const article = seedOilsArticle;

  return (
    <div className={cn("bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)}>
      <article>
        <SeedOilsArticleHero />

        {/* Lead */}
        <HomeContainer className="py-8 md:py-10">
          <div className="mx-auto max-w-3xl space-y-4">
            {article.lead.map((p) => (
              <RichParagraph
                key={p.slice(0, 24)}
                text={p}
                className="text-lg leading-[1.8] text-[#111318] md:text-xl"
              />
            ))}
          </div>
        </HomeContainer>

        {/* Body sections -- ported verbatim from the approved draft. The cookies
            chart (the article's proof) lands after "bari-proof"'s paragraphs; the
            claims-vs-evidence table breaks up the longer "institutions" section. */}
        {article.sections.map((section, i) => (
          <ArticleSection
            key={section.id}
            id={section.id}
            eyebrowLabel={section.eyebrowLabel}
            title={section.title}
            paragraphs={section.paragraphs}
            tone={i % 2 === 0 ? "cream" : "white"}
            afterContent={section.id === "bari-proof" ? <SeedOilsCookiesChart /> : undefined}
            insetContent={section.id === "institutions" ? <SeedOilsClaimsTable /> : undefined}
          />
        ))}

        {/* Conclusion */}
        <HomeContainer className="space-y-10 py-8 md:space-y-14 md:py-10">
          <div className="mx-auto max-w-4xl space-y-10 md:space-y-14">
            <section id="conclusion">
              <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
                {article.conclusion.title}
              </h2>
              <div className="mt-6 space-y-4">
                {article.conclusion.paragraphs.map((p) => (
                  <RichParagraph
                    key={p.slice(0, 20)}
                    text={p}
                    className="text-base leading-[1.75] text-[#4E5663] md:text-lg"
                  />
                ))}
              </div>
            </section>

            {/* Sources note */}
            <section
              id="sources"
              className="rounded-[1.15rem] border border-black/6 bg-[#FFFFFF]/60 p-6 md:p-8"
            >
              <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
                מקורות
              </p>
              <p className="mt-3 text-xs leading-relaxed text-[#7A817C]">
                {article.sourcesNote}
              </p>
            </section>

            {/* Final CTA */}
            <aside className="relative overflow-hidden rounded-[1.35rem] border border-[#1F8F6A]/22 bg-[#111318] p-7 md:p-9">
              <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
                <div className="max-w-xl space-y-2 text-right">
                  <h3 className="text-xl font-extrabold tracking-[-0.03em] text-[#F7F7F2] md:text-2xl">
                    רוצים לראות השוואות נוספות?
                  </h3>
                  <p className="text-sm leading-relaxed text-[#C8CDC9] md:text-base">
                    דגנים, גבינות, חמאה, יוגורטים, חומוס ועוד — כל קטגוריה עם ניתוח מלא ומנוע השוואה אינטראקטיבי.
                  </p>
                </div>
                <Link
                  href={HASHVAOT_HREF}
                  className="inline-flex shrink-0 items-center justify-center gap-2 rounded-full bg-[#167A58] px-6 py-3 text-sm font-bold text-[#F7F7F2] shadow-md shadow-[#1F8F6A]/25 transition-[transform,box-shadow] duration-300 hover:-translate-y-0.5"
                >
                  {article.conclusion.cta}
                  <ChevronLeft className="size-4" aria-hidden />
                </Link>
              </div>
            </aside>

            {/* Recent articles */}
            <section id="recent">
              <h2 className="mb-6 text-xl font-extrabold tracking-[-0.03em] text-[#111318]">
                {article.recentAnalyses.title}
              </h2>
              <ul className="grid gap-4 sm:grid-cols-3">
                {article.recentAnalyses.items.map((item) => (
                  <RecentArticleCard key={item.slug} {...item} />
                ))}
              </ul>
            </section>
          </div>
        </HomeContainer>

        <HomeContainer className="pb-14">
          <footer className="mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-4 border-t border-black/6 pt-8">
            <Link
              href={HASHVAOT_HREF}
              className="inline-flex items-center gap-2 text-sm font-semibold text-[#167A58] hover:underline"
            >
              כל ניתוחי המדף
              <ArrowLeft className="size-4" aria-hidden />
            </Link>
            <Link href="/blog" className="text-sm font-semibold text-[#4E5663] hover:text-[#111318]">
              חזרה לבלוג
            </Link>
          </footer>
        </HomeContainer>
      </article>
    </div>
  );
}
