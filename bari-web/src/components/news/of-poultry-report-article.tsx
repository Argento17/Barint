"use client";

import Link from "next/link";
import { ArrowLeft, ExternalLink } from "lucide-react";

import { ClaimStatusCard } from "@/components/news/claim-status-card";
import { OfPoultryReportHero } from "@/components/news/of-poultry-report-hero";
import { InsightBlock } from "@/components/blog/shared/insight-block";
import { RecentArticleCard } from "@/components/blog/shared/recent-article-card";
import { HomeContainer } from "@/components/home/section-frame";
import {
  HASHVAOT_HREF,
  NEWS_INDEX_HREF,
  poultryReportArticle,
} from "@/lib/news/of-poultry-report-content";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

/**
 * OfPoultryReportArticle — first חדשות (News) piece: an independent
 * honest-broker commentary on a third-party investigation (שומרים / Ynet,
 * poultry industry). TASK-521.
 *
 * Every string rendered here comes from src/data/news/of-poultry-report.json.
 * Any future edit to that data file still requires sign-off from both the
 * Content Agent and the Adversarial QA / Red-Team gate before it ships
 * (content_signoff_hard_rule).
 *
 * Architecture mirrors the blog article pattern (src/components/blog/food-dyes-article.tsx):
 * hero → lead/disclaimer → editorial insight → body sections → claim-by-claim
 * audit (this piece's spine) → practical takeaways → sources → closing CTA →
 * related reading → footer nav. Reuses the shared InsightBlock and
 * RecentArticleCard components; the claim-audit spine gets its own
 * ClaimStatusCard (mirrors shared FindingCard geometry — see that file's
 * doc comment for why it isn't a drop-in shared component: it needs a
 * verification-status chip FindingCard has no field for).
 */
export function OfPoultryReportArticle() {
  const article = poultryReportArticle;

  return (
    <div className={cn("bg-[#F7F7F2] text-[#111318]", siteHeaderOffsetClass)} dir="rtl">
      <article>
        <OfPoultryReportHero />

        {/* Honest-broker disclaimer */}
        <HomeContainer className="py-10 md:py-14">
          <div className="mx-auto max-w-3xl space-y-5">
            <p className="rounded-[0.85rem] border border-black/6 bg-[#FFFFFF]/60 px-5 py-4 text-sm leading-relaxed text-[#4E5663]">
              <span className="font-bold text-[#111318]">הבהרה · </span>
              {article.disclaimer}
            </p>
          </div>
        </HomeContainer>

        {/* מה הדוח טוען */}
        <section
          id="what-report-claims"
          className="border-t border-black/6 bg-[#F7F7F2] py-14 md:py-20"
        >
          <HomeContainer>
            <div className="mx-auto max-w-3xl">
              <header className="mb-8 text-right">
                <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
                  הדוח
                </p>
                <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
                  {article.whatReportClaims.title}
                </h2>
                <p className="mt-3 text-base leading-relaxed text-[#4E5663]">
                  {article.whatReportClaims.subtitle}
                </p>
              </header>
              <div className="space-y-5">
                {article.whatReportClaims.paragraphs.map((p, i) => (
                  <p key={i} className="text-base leading-[1.85] text-[#111318] md:text-lg">
                    {p}
                  </p>
                ))}
              </div>
            </div>
          </HomeContainer>
        </section>

        <HomeContainer className="pb-4 pt-10 md:pt-12">
          <div className="mx-auto max-w-3xl">
            <InsightBlock quote={article.editorialInsight} index={0} />
          </div>
        </HomeContainer>

        {/* מה מבוסס ומה שנוי במחלוקת — the spine of the piece */}
        <section
          id="claims-audit"
          className="border-y border-black/6 bg-[#FFFFFF] py-14 md:py-20"
        >
          <HomeContainer>
            <header className="mx-auto mb-10 max-w-3xl text-right md:mb-14">
              <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
                בדיקת אימות
              </p>
              <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
                {article.claimsAudit.title}
              </h2>
              <p className="mt-4 text-base leading-relaxed text-[#4E5663]">
                {article.claimsAudit.subtitle}
              </p>
            </header>
            <ul className="mx-auto flex max-w-3xl flex-col gap-5 md:gap-6">
              {article.claimsAudit.items.map((item, i) => (
                <ClaimStatusCard key={`${item.claim.slice(0, 24)}-${i}`} item={item} index={i} />
              ))}
            </ul>
          </HomeContainer>
        </section>

        {/* מה זה אומר עבורך */}
        <section
          id="what-it-means-for-you"
          className="border-b border-black/6 bg-[#F7F7F2] py-14 md:py-20"
        >
          <HomeContainer>
            <div className="mx-auto max-w-3xl">
              <header className="mb-8 text-right">
                <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
                  כצרכן
                </p>
                <h2 className="mt-2 text-3xl font-extrabold tracking-tighter text-[#111318] md:text-4xl">
                  {article.whatItMeansForYou.title}
                </h2>
                <p className="mt-3 text-base leading-relaxed text-[#4E5663]">
                  {article.whatItMeansForYou.subtitle}
                </p>
              </header>
              <ul className="grid gap-4 sm:grid-cols-2">
                {article.whatItMeansForYou.items.map((item) => (
                  <li
                    key={item.title}
                    className="rounded-[1rem] border border-black/[0.07] bg-[#FFFFFF] px-5 py-5"
                  >
                    <p className="text-sm font-bold leading-snug text-[#111318]">{item.title}</p>
                    <p className="mt-2 text-xs leading-relaxed text-[#4E5663]">{item.text}</p>
                  </li>
                ))}
              </ul>
            </div>
          </HomeContainer>
        </section>

        {/* מקורות */}
        <section id="sources" className="bg-[#FFFFFF] py-14 md:py-20">
          <HomeContainer>
            <div className="mx-auto max-w-3xl">
              <p className="mb-3 text-[0.65rem] font-bold uppercase tracking-[0.18em] text-[#7A817C]">
                {article.sources.title}
              </p>
              <div className="rounded-[1rem] border border-black/[0.06] bg-[#F7F7F2] px-5 py-5">
                <ol className="space-y-3">
                  {article.sources.items.map((c) => (
                    <li key={c.id} className="flex gap-3 text-right">
                      <span className="mt-0.5 shrink-0 font-mono text-[0.65rem] font-bold text-[#7A9450]">
                        [{c.id}]
                      </span>
                      <div>
                        <p className="text-xs font-semibold leading-relaxed text-[#111318]">
                          {c.short}
                        </p>
                        <p className="mt-0.5 text-[0.65rem] leading-relaxed text-[#7A817C]">
                          {c.full}
                        </p>
                        {c.url && c.url !== "#" && (
                          <a
                            href={c.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="mt-1 inline-flex items-center gap-1 text-[0.65rem] font-semibold text-[#167A58] hover:underline"
                          >
                            קישור למקור
                            <ExternalLink className="size-3" aria-hidden />
                          </a>
                        )}
                      </div>
                    </li>
                  ))}
                </ol>
              </div>
            </div>
          </HomeContainer>
        </section>

        <HomeContainer className="space-y-16 py-8 md:space-y-24 md:py-12">
          <div className="mx-auto max-w-4xl space-y-16 md:space-y-24">
            {/* Closing CTA */}
            <aside className="relative overflow-hidden rounded-[1.35rem] border border-[#1F8F6A]/22 bg-[#111318] p-7 md:p-9">
              <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
                <div className="max-w-xl space-y-2 text-right">
                  <h3 className="text-xl font-extrabold tracking-[-0.03em] text-[#F7F7F2] md:text-2xl">
                    {article.closingCta.text}
                  </h3>
                </div>
                <Link
                  href={article.closingCta.href || HASHVAOT_HREF}
                  className="inline-flex shrink-0 items-center justify-center gap-2 rounded-full bg-[#167A58] px-6 py-3 text-sm font-bold text-[#F7F7F2] shadow-md shadow-[#1F8F6A]/25 transition-[transform,box-shadow] duration-300 hover:-translate-y-0.5"
                >
                  לכל ניתוחי המדף
                  <ArrowLeft className="size-4" aria-hidden />
                </Link>
              </div>
            </aside>

            {/* Related reading */}
            <section id="related">
              <h2 className="mb-6 text-xl font-extrabold tracking-[-0.03em] text-[#111318]">
                {article.relatedReading.title}
              </h2>
              <ul className="grid gap-4 sm:grid-cols-3">
                {article.relatedReading.items.map((item) => (
                  <RecentArticleCard key={item.slug} {...item} />
                ))}
              </ul>
            </section>
          </div>
        </HomeContainer>

        <HomeContainer className="pb-14">
          <footer className="mx-auto flex max-w-3xl flex-wrap items-center justify-between gap-4 border-t border-black/6 pt-8">
            <Link
              href={NEWS_INDEX_HREF}
              className="inline-flex items-center gap-2 text-sm font-semibold text-[#167A58] hover:underline"
            >
              כל הכתבות בחדשות
              <ArrowLeft className="size-4" aria-hidden />
            </Link>
            <Link href="/blog" className="text-sm font-semibold text-[#4E5663] hover:text-[#111318]">
              לבלוג Bari
            </Link>
          </footer>
        </HomeContainer>
      </article>
    </div>
  );
}
