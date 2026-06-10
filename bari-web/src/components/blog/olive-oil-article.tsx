"use client";

import Link from "next/link";
import { ArrowLeft, ChevronLeft, ExternalLink } from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";

import { OliveOilArticleHero } from "@/components/blog/olive-oil-article-hero";
import { OliveOilExternalResearch } from "@/components/blog/olive-oil-external-research";
import { OliveOilOriginChart } from "@/components/blog/olive-oil-origin-chart";
import { OliveOilTransparencyMatrix } from "@/components/blog/olive-oil-transparency-matrix";
import { HomeContainer } from "@/components/home/section-frame";
import { HASHVAOT_HREF, oliveOilArticle } from "@/lib/blog/olive-oil-article-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

function InsightBlock({ quote, index = 0 }: { quote: string; index?: number }) {
  const reduceMotion = useReducedMotion();
  return (
    <motion.blockquote
      initial={reduceMotion ? false : { opacity: 0, x: 12 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.5, delay: index * 0.05 }}
      className="relative border-r-4 border-[#7A9450] bg-[#FFFFFF] px-6 py-5 md:px-8"
    >
      <p className="text-lg font-semibold leading-snug tracking-[-0.02em] text-[#111318] md:text-xl">
        {quote}
      </p>
    </motion.blockquote>
  );
}

function FindingCard({
  title,
  finding,
  whyItMatters,
  index,
}: {
  title: string;
  finding: string;
  whyItMatters: string;
  index: number;
}) {
  const reduceMotion = useReducedMotion();
  return (
    <motion.li
      initial={reduceMotion ? false : { opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }}
      className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] px-6 py-6 md:px-8 md:py-7"
    >
      <h3 className="text-xl font-extrabold tracking-[-0.03em] text-[#111318] md:text-2xl">
        {title}
      </h3>
      <p className="mt-3 text-base leading-relaxed text-[#111318]">{finding}</p>
      <p className="mt-4 text-sm leading-relaxed text-[#4E5663]">
        <span className="font-bold text-[#7A9450]">למה זה משנה · </span>
        {whyItMatters}
      </p>
    </motion.li>
  );
}

function BuyingGuideCard({
  signal,
  what,
  availability,
}: {
  signal: string;
  what: string;
  availability: string;
}) {
  return (
    <li className="rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF] px-5 py-5">
      <p className="text-xs font-bold uppercase tracking-[0.12em] text-[#7A9450]">{signal}</p>
      <p className="mt-2 text-sm font-semibold leading-snug text-[#111318]">{what}</p>
      <p className="mt-2 text-xs leading-relaxed text-[#7A817C]">
        <span className="font-bold">זמינות: </span>
        {availability}
      </p>
    </li>
  );
}

/**
 * ScienceSection — renders the polyphenol/freshness narrative with formal citations.
 * Template note: any article with a "science" section in its content object
 * can render this component pattern. Props are the typed science object from
 * the content file.
 */
function ScienceSection({
  science,
}: {
  science: typeof oliveOilArticle.science;
}) {
  const reduceMotion = useReducedMotion();
  return (
    <section id="science" className="border-t border-black/6 bg-[#FFFFFF] py-14 md:py-20">
      <HomeContainer>
        <div className="mx-auto max-w-3xl">
          <header className="mb-8 text-right">
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
              מדע הרעננות
            </p>
            <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
              {science.title}
            </h2>
            <p className="mt-3 text-base leading-relaxed text-[#4E5663]">
              {science.subtitle}
            </p>
          </header>

          <div className="space-y-5">
            {science.paragraphs.map((p, i) => (
              <motion.p
                key={i}
                initial={reduceMotion ? false : { opacity: 0, y: 8 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-30px" }}
                transition={{ duration: 0.45, delay: i * 0.04 }}
                className="text-base leading-[1.85] text-[#111318] md:text-lg"
              >
                {p}
              </motion.p>
            ))}
          </div>

          {/* Formal citations */}
          <div className="mt-10 rounded-[1rem] border border-black/[0.06] bg-[#F7F7F2] px-5 py-5">
            <p className="mb-3 text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
              מקורות
            </p>
            <ol className="space-y-3">
              {science.citations.map((c) => (
                <li key={c.id} className="flex gap-3 text-right">
                  <span className="mt-0.5 shrink-0 font-mono text-[0.65rem] font-bold text-[#7A9450]">
                    [{c.id}]
                  </span>
                  <div>
                    <p className="text-xs font-semibold leading-relaxed text-[#111318]">
                      {c.short}
                    </p>
                    <p className="mt-0.5 text-[0.65rem] leading-relaxed text-[#7A817C]">
                      {c.claim}
                    </p>
                    <a
                      href={c.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-1 inline-flex items-center gap-1 text-[0.65rem] font-semibold text-[#1F8F6A] hover:underline"
                    >
                      קישור למקור
                      <ExternalLink className="size-3" aria-hidden />
                    </a>
                  </div>
                </li>
              ))}
            </ol>
          </div>
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
          className="mt-4 inline-flex items-center gap-1.5 text-xs font-bold text-[#1F8F6A] hover:underline"
        >
          {cta}
          <ChevronLeft className="size-3.5" aria-hidden />
        </Link>
      )}
    </li>
  );
}

export function OliveOilArticle() {
  const article = oliveOilArticle;

  return (
    <main className={cn("bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)}>
      <article>
        <OliveOilArticleHero />

        {/* Lead */}
        <HomeContainer className="py-10 md:py-14">
          <div className="mx-auto max-w-3xl space-y-5">
            {article.lead.map((p) => (
              <p key={p.slice(0, 24)} className="text-lg leading-[1.8] text-[#111318] md:text-xl">
                {p}
              </p>
            ))}
          </div>
        </HomeContainer>

        {/* Science of freshness — polyphenols, IOC standard, citations */}
        <ScienceSection science={article.science} />

        {/* Extra virgin guarantees — what the grade means and doesn't mean */}

        <section id="extra-virgin" className="border-t border-black/6 bg-[#F7F7F2] py-14 md:py-20">
          <HomeContainer>
            <div className="mx-auto max-w-3xl">
              <header className="mb-8 text-right">
                <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
                  מה הדרגה אומרת
                </p>
                <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
                  {article.extraVirginGuarantees.title}
                </h2>
                <p className="mt-3 text-base leading-relaxed text-[#4E5663]">
                  {article.extraVirginGuarantees.subtitle}
                </p>
              </header>
              <div className="space-y-5">
                {article.extraVirginGuarantees.paragraphs.map((p, i) => (
                  <p
                    key={i}
                    className="text-base leading-[1.85] text-[#111318] md:text-lg"
                  >
                    {p}
                  </p>
                ))}
              </div>
            </div>
          </HomeContainer>
        </section>

        <HomeContainer className="pb-4 pt-10 md:pt-12">
          <div className="mx-auto max-w-3xl">
            <InsightBlock quote={article.editorialInsights[0]} index={0} />
          </div>
        </HomeContainer>

        {/* What we checked — methodology (up front so readers know the basis before findings) */}
        <HomeContainer className="py-10 md:py-12">
          <section
            id="methodology"
            className="mx-auto max-w-3xl rounded-[1.15rem] border border-black/6 bg-[#FFFFFF]/60 p-6 md:p-8"
          >
            <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
              מה בדקנו
            </p>
            <h2 className="mt-2 text-lg font-extrabold text-[#111318]">
              {article.methodology.title}
            </h2>
            <ol className="mt-4 grid gap-3 md:grid-cols-3">
              {article.methodology.steps.map((step, i) => (
                <li key={step.title} className="list-none text-sm">
                  <span className="font-mono text-xs font-bold text-[#7A9450]">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <p className="mt-1 font-bold text-[#111318]">{step.title}</p>
                  <p className="mt-1 leading-relaxed text-[#7A817C]">{step.text}</p>
                </li>
              ))}
            </ol>
            <p className="mt-4 text-xs leading-relaxed text-[#7A817C]">
              {article.methodology.footnote}
            </p>
          </section>
        </HomeContainer>

        {/* Findings */}
        <section
          id="findings"
          className="border-y border-black/6 bg-[#FFFFFF] py-14 md:py-20"
        >
          <HomeContainer>
            <header className="mx-auto mb-10 max-w-3xl text-right md:mb-14">
              <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
                מה מצאנו
              </p>
              <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
                {article.findings.title}
              </h2>
              <p className="mt-4 text-base leading-relaxed text-[#4E5663]">
                {article.findings.subtitle}
              </p>
            </header>
            <ul className="mx-auto flex max-w-3xl flex-col gap-5 md:gap-6">
              {article.findings.items.map((item, i) => (
                <FindingCard
                  key={item.title}
                  title={item.title}
                  finding={item.finding}
                  whyItMatters={item.whyItMatters}
                  index={i}
                />
              ))}
            </ul>
          </HomeContainer>
        </section>

        {/* Origin chart */}
        <div className="bg-[#F7F7F2] py-14 md:py-20">
          <HomeContainer>
            <div className="mx-auto max-w-3xl">
              <OliveOilOriginChart />
            </div>
          </HomeContainer>
        </div>

        <HomeContainer className="pb-4">
          <div className="mx-auto max-w-3xl">
            <InsightBlock quote={article.editorialInsights[1]} index={1} />
          </div>
        </HomeContainer>

        {/* Transparency matrix */}
        <HomeContainer className="py-10 md:py-14">
          <div className="mx-auto max-w-4xl">
            <OliveOilTransparencyMatrix />
          </div>
        </HomeContainer>

        <HomeContainer className="pb-4">
          <div className="mx-auto max-w-3xl">
            <InsightBlock quote={article.editorialInsights[2]} index={2} />
          </div>
        </HomeContainer>

        {/* External research */}
        <div className="bg-[#F7F7F2] py-14 md:py-20">
          <HomeContainer>
            <div className="mx-auto max-w-3xl">
              <OliveOilExternalResearch />
            </div>
          </HomeContainer>
        </div>

        <HomeContainer className="space-y-16 py-8 md:space-y-24 md:py-12">
          <div className="mx-auto max-w-4xl space-y-16 md:space-y-24">
            {/* Buying guide */}
            <section id="buying-guide">
              <header className="mb-8 text-right">
                <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
                  מדריך קנייה
                </p>
                <h2 className="mt-1 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
                  {article.buyingGuide.title}
                </h2>
              </header>
              <ul className="grid gap-4 sm:grid-cols-2">
                {article.buyingGuide.items.map((item) => (
                  <BuyingGuideCard
                    key={item.signal}
                    signal={item.signal}
                    what={item.what}
                    availability={item.availability}
                  />
                ))}
              </ul>
              <p className="mt-5 rounded-[0.85rem] border border-black/6 bg-[#FFFFFF]/60 px-5 py-4 text-right text-sm leading-relaxed text-[#4E5663]">
                <span className="font-bold text-[#111318]">הערה · </span>
                {article.buyingGuide.caveat}
              </p>
            </section>

            {/* Conclusion */}
            <section id="conclusion">
              <h2 className="text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
                {article.conclusion.title}
              </h2>
              <div className="mt-6 space-y-4">
                {article.conclusion.paragraphs.map((p) => (
                  <p
                    key={p.slice(0, 20)}
                    className="text-base leading-[1.75] text-[#4E5663] md:text-lg"
                  >
                    {p}
                  </p>
                ))}
              </div>
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
                  className="inline-flex shrink-0 items-center justify-center gap-2 rounded-full bg-[#1F8F6A] px-6 py-3 text-sm font-bold text-[#F7F7F2] shadow-md shadow-[#1F8F6A]/25 transition-[transform,box-shadow] duration-300 hover:-translate-y-0.5"
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
              className="inline-flex items-center gap-2 text-sm font-semibold text-[#1F8F6A] hover:underline"
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
    </main>
  );
}
