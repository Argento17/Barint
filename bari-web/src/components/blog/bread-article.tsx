"use client";

import Link from "next/link";
import { ArrowLeft, ChevronLeft } from "lucide-react";

import { BreadArticleHero } from "@/components/blog/bread-article-hero";
import { BreadExternalResearch } from "@/components/blog/bread-external-research";
import { BreadKeyProductMatrix } from "@/components/blog/bread-key-product-matrix";
import { BreadScoreDistribution } from "@/components/blog/bread-score-distribution";
import { BuyingGuideCard } from "@/components/blog/shared/buying-guide-card";
import { FindingCard } from "@/components/blog/shared/finding-card";
import { InsightBlock } from "@/components/blog/shared/insight-block";
import { RecentArticleCard } from "@/components/blog/shared/recent-article-card";
import { ScienceSection } from "@/components/blog/shared/science-section";
import { HomeContainer } from "@/components/home/section-frame";
import { BREAD_HASHVAOT_HREF, BREAD_BLOG_HREF, breadArticle } from "@/lib/blog/bread-article-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

export function BreadArticle() {
  const article = breadArticle;

  return (
    <main className={cn("bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)}>
      <article>
        {/* Hero */}
        <BreadArticleHero />

        {/* Lead paragraphs */}
        <HomeContainer className="py-10 md:py-14">
          <div className="mx-auto max-w-3xl space-y-5">
            {article.lead.map((p) => (
              <p key={p.slice(0, 24)} className="text-lg leading-[1.8] text-[#111318] md:text-xl">
                {p}
              </p>
            ))}
          </div>
        </HomeContainer>

        {/* Science section — fermentation and whole grain */}
        <ScienceSection science={article.science} eyebrow="מדע התסיסה והדגן" />

        {/* Whole grain label — what it does and does not guarantee */}
        <section
          id="whole-grain-label"
          className="border-t border-black/6 bg-[#F7F7F2] py-14 md:py-20"
        >
          <HomeContainer>
            <div className="mx-auto max-w-3xl">
              <header className="mb-8 text-right">
                <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
                  מה הכיתוב אומר
                </p>
                <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
                  {article.wholeGrainLabel.title}
                </h2>
                <p className="mt-3 text-base leading-relaxed text-[#4E5663]">
                  {article.wholeGrainLabel.subtitle}
                </p>
              </header>
              <div className="space-y-5">
                {article.wholeGrainLabel.paragraphs.map((p, i) => (
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

        {/* Insight block 1 */}
        <HomeContainer className="pb-4 pt-10 md:pt-12">
          <div className="mx-auto max-w-3xl">
            <InsightBlock quote={article.editorialInsights[0]} index={0} />
          </div>
        </HomeContainer>

        {/* Methodology box */}
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

        {/* Score distribution chart */}
        <BreadScoreDistribution />

        {/* Insight block 2 */}
        <HomeContainer className="pb-4">
          <div className="mx-auto max-w-3xl">
            <InsightBlock quote={article.editorialInsights[1]} index={1} />
          </div>
        </HomeContainer>

        {/* Key product matrix */}
        <BreadKeyProductMatrix />

        {/* Insight block 3 */}
        <HomeContainer className="pb-4">
          <div className="mx-auto max-w-3xl">
            <InsightBlock quote={article.editorialInsights[2]} index={2} />
          </div>
        </HomeContainer>

        {/* External research */}
        <div className="bg-[#F7F7F2] py-14 md:py-20">
          <HomeContainer>
            <div className="mx-auto max-w-3xl">
              <BreadExternalResearch />
            </div>
          </HomeContainer>
        </div>

        {/* Buying guide + conclusion + CTA + recent articles */}
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

            {/* CTA — links to the bread comparison page */}
            <aside className="relative overflow-hidden rounded-[1.35rem] border border-[#1F8F6A]/22 bg-[#111318] p-7 md:p-9">
              <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
                <div className="max-w-xl space-y-2 text-right">
                  <h3 className="text-xl font-extrabold tracking-[-0.03em] text-[#F7F7F2] md:text-2xl">
                    רוצים לראות את כל הלחמים?
                  </h3>
                  <p className="text-sm leading-relaxed text-[#C8CDC9] md:text-base">
                    24 מוצרים, ציונים, רכיבים ופרטי מחמצת — כל המדף בעמוד ההשוואה האינטראקטיבי.
                  </p>
                </div>
                <Link
                  href={BREAD_HASHVAOT_HREF}
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

        {/* Footer */}
        <HomeContainer className="pb-14">
          <footer className="mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-4 border-t border-black/6 pt-8">
            <Link
              href={BREAD_HASHVAOT_HREF}
              className="inline-flex items-center gap-2 text-sm font-semibold text-[#1F8F6A] hover:underline"
            >
              לניתוח הלחם המלא
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
