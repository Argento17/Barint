import Link from "next/link";
import { ArrowRight, ExternalLink } from "lucide-react";

import { HomeContainer } from "@/components/home/section-frame";
import { NEWS_INDEX_HREF, type PoultryReportArticle } from "@/lib/news/of-poultry-report-content";

/**
 * OfPoultryReportHero — mirrors food-dyes-article-hero.tsx (back-link, eyebrow,
 * title, deck, meta line) with one addition required by the news-article spec:
 * an explicit "מקור" (source) attribution line crediting the third-party
 * investigation this piece comments on.
 *
 * Generalized in TASK-769 to take `article` as a prop (was a hard import of
 * poultryReportArticle) so the same hero renders any honest-broker news piece
 * sharing the PoultryReportArticle shape — see algimel-tahini-alert-article.tsx.
 */
export function OfPoultryReportHero({ article }: { article: PoultryReportArticle }) {
  const { hero } = article;

  return (
    <header className="relative overflow-hidden border-b border-black/6 bg-[#FFFFFF]">
      <HomeContainer className="flex flex-col py-8 md:py-12">
        <Link
          href={NEWS_INDEX_HREF}
          className="mb-2 inline-flex shrink-0 items-center gap-2 text-sm font-semibold text-[#4E5663] hover:text-[#111318]"
        >
          <ArrowRight className="size-4" aria-hidden />
          חזרה לחדשות
        </Link>

        <div className="flex max-w-3xl flex-col justify-center text-right">
          <p className="text-xs font-bold uppercase tracking-[0.24em] text-[#167A58]">
            {hero.eyebrow}
          </p>
          <h1 className="mt-3 text-balance text-3xl font-extrabold leading-[1.1] tracking-tighter text-[#111318] md:text-4xl lg:text-5xl">
            {hero.title}
          </h1>
          <p className="mt-3 max-w-2xl text-pretty text-base leading-relaxed text-[#4E5663] md:text-lg">
            {hero.deck}
          </p>
          <p className="mt-2 text-sm text-[#7A817C]">
            {hero.publishDate} · {hero.readTime}
          </p>

          <div className="mt-5 inline-flex w-fit items-center gap-2 rounded-[0.85rem] border border-black/6 bg-[#F7F7F2] px-4 py-2.5 text-sm">
            <span className="font-bold text-[#7A9450]">{hero.source.label} · </span>
            <span className="text-[#111318]">{hero.source.text}</span>
            {hero.source.url && hero.source.url !== "#" && (
              <a
                href={hero.source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 font-semibold text-[#167A58] hover:underline"
              >
                למקור המקורי
                <ExternalLink className="size-3" aria-hidden />
              </a>
            )}
          </div>
        </div>
      </HomeContainer>
    </header>
  );
}
