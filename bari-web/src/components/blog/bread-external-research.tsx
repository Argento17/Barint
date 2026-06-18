"use client";

import { ExternalLink } from "lucide-react";

import { breadArticle } from "@/lib/blog/bread-article-content";

/**
 * BreadExternalResearch — key finding card from Lancet 2019 Reynolds et al.
 * Data: breadArticle.externalResearch.
 */
export function BreadExternalResearch() {
  const { externalResearch } = breadArticle;
  const { keyFinding } = externalResearch;

  return (
    <div>
      <header className="mb-6 text-right">
        <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#7A9450]/85">
          מחקר בינלאומי
        </p>
        <h2 className="mt-2 text-2xl font-extrabold tracking-tighter text-[#111318] md:text-3xl">
          {externalResearch.title}
        </h2>
        <p className="mt-2 text-sm leading-relaxed text-[#4E5663]">
          {externalResearch.subtitle}
        </p>
      </header>

      {/* Key finding card */}
      <div className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] p-6 md:p-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:gap-8" dir="rtl">
          {/* Stat */}
          <div className="shrink-0 text-right">
            <p className="text-4xl font-extrabold tracking-[-0.04em] text-[#7A9450] md:text-5xl">
              {keyFinding.headline}
            </p>
            <p className="mt-1 max-w-[12rem] text-xs font-bold uppercase tracking-[0.1em] text-[#7A817C]">
              {keyFinding.headlineLabel}
            </p>
          </div>

          {/* Description */}
          <div className="flex-1 text-right">
            <p className="text-sm leading-relaxed text-[#111318] md:text-base">
              {keyFinding.description}
            </p>

            <blockquote className="mt-4 border-r-2 border-[#7A9450]/40 pr-4 text-sm italic leading-relaxed text-[#4E5663]">
              {keyFinding.quote}
              <cite className="mt-1 block not-italic text-[0.65rem] font-bold text-[#7A817C]">
                {keyFinding.quoteAttribution}
              </cite>
            </blockquote>

            <p className="mt-4 text-xs leading-relaxed text-[#7A817C]">{keyFinding.caveat}</p>

            <a
              href={keyFinding.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-3 inline-flex items-center gap-1.5 text-xs font-semibold text-[#1F8F6A] hover:underline"
            >
              {keyFinding.source}
              <ExternalLink className="size-3" aria-hidden />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
