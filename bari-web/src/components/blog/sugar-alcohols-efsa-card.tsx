"use client";

import { ExternalLink } from "lucide-react";

import { efsaCard } from "@/lib/blog/sugar-alcohols-article-content";

/**
 * EFSA Independent-Source Credibility Card — TASK-379
 *
 * Card-only (no YouTube/video block).
 * Strings: S-40..S-46 verbatim from sugar_alcohols_blog_copy_v1.md.
 * Design: institutional quote-card treatment modelled on OliveOilExternalResearch,
 * adapted to card-only geometry: eyebrow → title → lead → finding blockquote
 * (with EN verbatim sub-line) → amber caveat box → external source link.
 */
export function SugarAlcoholsEfsaCard() {
  return (
    <section className="space-y-0">
      {/* Card */}
      <div className="rounded-[1.2rem] border border-black/[0.07] bg-[#FFFFFF] px-6 py-7 md:px-8 md:py-8">
        {/* Eyebrow + title + lead */}
        <div className="mb-6 text-right">
          <p className="font-mono text-[0.65rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/85">
            {efsaCard.eyebrow}
          </p>
          <h2 className="mt-2 text-2xl font-extrabold tracking-[-0.04em] text-[#111318] md:text-3xl">
            {efsaCard.title}
          </h2>
          <p className="mt-3 text-base leading-relaxed text-[#4E5663] md:text-lg">
            {efsaCard.lead}
          </p>
        </div>

        {/* EFSA finding blockquote — quotedText (S-43a) only; authorNote (S-43b) is outside */}
        <blockquote className="mb-4 border-r-4 border-[#1F8F6A]/40 pr-5 text-right">
          <p className="text-base leading-relaxed text-[#111318] md:text-lg">
            {efsaCard.quotedText}
          </p>
          {/* English verbatim sub-line */}
          <p
            className="mt-3 text-xs leading-relaxed text-[#7A817C] italic"
            dir="ltr"
          >
            {efsaCard.verbatimEn}
          </p>
          <cite className="mt-2 block text-xs font-bold uppercase tracking-[0.1em] text-[#7A817C] not-italic">
            EFSA Journal 2011;9(4):2076
          </cite>
        </blockquote>

        {/* Bari author note (S-43b) — OUTSIDE the blockquote; Bari commentary, not EFSA */}
        <p className="mb-6 text-right text-base leading-relaxed text-[#4E5663] md:text-lg">
          {efsaCard.authorNote}
        </p>

        {/* Amber caveat box */}
        <p className="mb-6 rounded-[0.75rem] border border-amber-200/60 bg-amber-50/60 px-4 py-3 text-right text-xs leading-relaxed text-[#7A6A00]">
          <span className="font-bold">הגבלת הממצאים · </span>
          {efsaCard.caveat}
        </p>

        {/* External source link */}
        <div className="flex justify-end">
          <a
            href={efsaCard.sourceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#167A58] hover:underline"
          >
            {efsaCard.ctaLabel}
            <ExternalLink className="size-3.5" aria-hidden />
          </a>
        </div>
      </div>
    </section>
  );
}
