"use client";

// TASK-504A: GLP-1 / suppressed-appetite high-protein yogurt guide.
// Renders the signed-off copy (src/data/guides/yogurt_glp1_dairy_guide_v1.json, via
// src/lib/guides/yogurt-glp1-guide-data.ts) verbatim. This component authors no copy —
// every Hebrew string below is a prop passed in from the loader.
//
// Component reuse (no new visual primitives invented):
//   - ScoreChip (src/components/shared/score-chip.tsx) — the same frozen grade badge
//     used on every comparison page. Grade comes from the product VM, never hand-typed.
//   - BariProductThumbnail (src/components/comparisons/bari-product-thumbnail.tsx) — the
//     same self-hosted-via-next/image product photo tile used on every comparison page.
//   - CategoryNoteBox (src/components/comparisons/comparison-page.tsx) — the same yellow
//     "הערת קטגוריה" caveat box used on both live yogurt comparison pages.
// The howToRead cards and shortlist card frame reuse the rounded-card idiom already
// established on the site (home-guides.tsx: rounded-[1.25rem] border border-black/[0.07]
// bg-white) rather than inventing a new card style.

import Link from "next/link";

import { CategoryNoteBox } from "@/components/comparisons/comparison-page";
import { BariProductThumbnail } from "@/components/comparisons/bari-product-thumbnail";
import { ScoreChip } from "@/components/shared/score-chip";
import { shouldBlendWhiteForCategory } from "@/lib/comparisons/thumbnail-blend-white-categories";
import type { YogurtGlp1ShortlistItem } from "@/lib/guides/yogurt-glp1-guide-data";

// TASK-534: shortlist photos are cross-referenced from the yogurt_spoonable_frontend_v1.json
// corpus (see src/lib/guides/yogurt-glp1-guide-data.ts) — same source, same baked-in white
// product photography as /hashvaot/yogurt. Resolved through the single codified rule
// (thumbnail-blend-white-categories.ts) rather than a local boolean, so this call site
// tracks the category registration instead of drifting from it.
const SHORTLIST_BLEND_WHITE = shouldBlendWhiteForCategory("yogurt-spoonable");

export interface YogurtGlp1GuidePageProps {
  hero: { eyebrow: string; title: string; intro: string };
  howToRead: {
    title: string;
    intro: string;
    bars: Array<{ label: string; description: string }>;
    gradeNote: string;
  };
  shortlist: YogurtGlp1ShortlistItem[];
  fullListNote: string;
  drinkableCallout: string;
  categoryNote: string;
}

// Turns the two literal "(/hashvaot/...)" substrings inside the frozen fullListNote
// string into real Next.js <Link> elements, without altering a single character of the
// copy — the parens and path text are reconstructed exactly, just made clickable.
const ROUTE_MENTION_RE = /\((\/hashvaot\/yogurt(?:-drinks)?)\)/g;

function renderFullListNote(text: string) {
  const parts = text.split(ROUTE_MENTION_RE);
  return parts.map((part, i) =>
    i % 2 === 1 ? (
      <span key={i}>
        (
        <Link href={part} className="font-semibold text-[#167A58] hover:underline">
          {part}
        </Link>
        )
      </span>
    ) : (
      <span key={i}>{part}</span>
    )
  );
}

export function YogurtGlp1GuidePage({
  hero,
  howToRead,
  shortlist,
  fullListNote,
  drinkableCallout,
  categoryNote,
}: YogurtGlp1GuidePageProps) {
  return (
    <div className="min-h-screen bg-[#F7F7F2] text-[#111318]" dir="rtl" lang="he">
      <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 sm:py-10">
        {/* Hero */}
        <header>
          <p className="font-mono text-[0.62rem] font-bold uppercase tracking-[0.24em] text-[#1F8F6A]/80">
            {hero.eyebrow}
          </p>
          <h1 className="mt-1 text-[1.5rem] font-semibold leading-tight tracking-[-0.028em] text-[#111318] sm:text-[1.9rem]">
            {hero.title}
          </h1>
          <p className="mt-3 text-[13px] leading-[1.6] text-[#3E444A] sm:text-[14px]">
            {hero.intro}
          </p>
        </header>

        {/* How to read this guide */}
        <section className="mt-8">
          <h2 className="text-[1.1rem] font-bold text-[#111318]">{howToRead.title}</h2>
          <p className="mt-2 text-[13px] leading-[1.6] text-[#3E444A]">{howToRead.intro}</p>

          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            {howToRead.bars.map((bar) => (
              <div
                key={bar.label}
                className="rounded-[1.25rem] border border-black/[0.07] bg-white p-4"
              >
                <p className="text-[13px] font-bold text-[#167A58]">{bar.label}</p>
                <p className="mt-2 text-[12px] leading-[1.55] text-[#4E5663]">
                  {bar.description}
                </p>
              </div>
            ))}
          </div>

          <p className="mt-4 text-[12px] leading-[1.6] text-[#5E6560]">{howToRead.gradeNote}</p>
        </section>

        {/* Shortlist — visual centerpiece */}
        <section className="mt-10">
          <div className="grid gap-4 sm:grid-cols-2">
            {shortlist.map((item) => (
              <article
                key={item.barcode}
                className="flex gap-3 rounded-[1.25rem] border border-black/[0.07] bg-white p-4"
              >
                <BariProductThumbnail
                  product={item.product}
                  size="lg"
                  blendWhite={SHORTLIST_BLEND_WHITE}
                />
                <div className="min-w-0 flex-1">
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="text-[14px] font-bold leading-snug text-[#111318]">
                      {item.name}
                    </h3>
                    <ScoreChip score={item.product.score} grade={item.product.grade} />
                  </div>
                  <p className="mt-2 text-[12px] leading-[1.55] text-[#4E5663]">
                    {item.whyFeatured}
                  </p>
                </div>
              </article>
            ))}
          </div>
        </section>

        {/* Full-list note — links to the two full comparison pages */}
        <p className="mt-8 text-[12px] leading-[1.6] text-[#4E5663]">
          {renderFullListNote(fullListNote)}
        </p>

        {/* Drinkable callout — secondary/footnote weight, not a parallel section */}
        <div className="mt-4 rounded-[1rem] border border-black/[0.06] bg-[#F1F1EC] px-4 py-3">
          <p className="text-[12px] leading-[1.6] text-[#5E6560]">{drinkableCallout}</p>
        </div>

        {/* Category caveat — same yellow box as the live yogurt comparison pages */}
        <div className="mt-8">
          <CategoryNoteBox note={categoryNote} />
        </div>
      </div>
    </div>
  );
}
