// TASK-557 — Sweetener guide (/madrichim/sweeteners). UNAPPROVED DRAFT.
//
// Pure educational prose guide (no products, no scores, no corpus counts). Copy is ported
// verbatim from the CONSUMER-COPY sentinel region of
// C:\Bari\02_products\guides\sweetener_guide_he_draft_v1.md via
// src/lib/guides/sweetener-guide-data.ts — this route authors no editorial copy. The hero
// eyebrow/title/deck and the GI table's column headers + caption are now Content-authored
// (structuralStrings, v5 re-sync) — this route renders them, it does not choose them.
//
// noindex + follow:false: this page has NOT cleared the second content gate for
// publication, is intentionally absent from src/lib/seo/sitemap-paths.ts, and is NOT
// registered in src/lib/guides/madrichim-categories.ts (so it never surfaces on the
// /madrichim hub). A visible draft banner marks it in the DOM. Flipping robots.index to
// true and adding the route to the sitemap/hub are the go-live steps, gated on content
// sign-off — a reversible, non-consumer-facing technical default, not a content judgment.
//
// VISUAL PASS (this task — owner directive: "I see only bulks of text — where are the
// visuals"): the page keeps every signed-off word exactly as authored and adds presentation
// only — a horizontal RTL bar chart for the glycemic-index table, a chocolate-bar hero card
// with a label-breakdown key, a "three groups on the shelf" card map, gradient-tile section
// icons with a subtle scroll-in reveal, three verbatim pull-quotes, and a video embed slot.
// All new visual/layout decisions (which sentence is a pull-quote, which product names tag
// which card, which icon illustrates which section) live in
// src/lib/guides/sweetener-guide-visuals.ts, which verifies every extracted string is a
// byte-identical substring of the signed-off data at import time — this route does not
// author or alter a single word. See that module's header comment for the full rationale.
//
// The two statutory package warnings still render as a distinct "label print" element
// (bordered, mono, kicker-captioned), set apart from body prose. The glycemic-index table
// itself is now a bar chart (see GlycemicBarChart) with the original real table kept in the
// DOM as an sr-only accessible/SEO fallback — no data was removed, only re-presented.
//
// The statutory-warning box's kicker caption ("נוסח האזהרה על האריזה") is still a
// frontend-authored/unsigned string — Content's structural-strings block explicitly did not
// cover this element (see the data module's block comment). Not swapped for anything, not
// re-invented here; flagged again in this task's return.

import { Fragment } from "react";
import type { Metadata } from "next";

import { GUIDE_SECTION_EYEBROW_CLASS } from "@/lib/design/bari-comparison-tokens";
import { sweetenerGuide } from "@/lib/guides/sweetener-guide-data";
import {
  SWEETENER_PULL_QUOTES,
  SWEETENER_SECTION_ICON,
  SWEETENER_VIDEO_AFTER_SECTION_ID,
  SWEETENER_VIDEO_ID,
  sectionHeadingById,
} from "@/lib/guides/sweetener-guide-visuals";
import { GlycemicBarChart } from "@/components/guides/sweetener/glycemic-bar-chart";
import { SweetenerGroupCards } from "@/components/guides/sweetener/sweetener-group-cards";
import { ChocolateBarHeroCard } from "@/components/guides/sweetener/chocolate-bar-hero-card";
import { SweetenerSectionIcon } from "@/components/guides/sweetener/section-icon";
import { SweetenerPullQuote } from "@/components/guides/sweetener/pull-quote";
import { SweetenerVideoEmbed } from "@/components/guides/sweetener/video-embed";
import { MobileActionBar } from "@/components/shared/mobile-action-bar";

export const metadata: Metadata = {
  // title mirrors structuralStrings.title (Content-authored, v5). description remains a
  // frontend-drafted placeholder — Content's structural-strings block does not cover a meta
  // description; flagged, not signed. robots noindex: unapproved draft.
  title: "מדריך הממתיקים | Bari",
  description:
    "מדריך הממתיקים של בארי מסביר, בשם שעל התווית העברית, אילו ממתיקים נמצאים באמת על המדף הישראלי ומה ידוע עליהם מהמחקר.",
  robots: { index: false, follow: false },
};

export default function SweetenersGuideRoute() {
  const { draftBanner, structuralStrings, sections, glycemicRows, sources } = sweetenerGuide;

  return (
    <div className="min-h-screen bg-[#F7F7F2] text-[#111318]" dir="rtl" lang="he">
      <MobileActionBar title={structuralStrings.title} />
      {/* Unapproved-draft banner — build-status marker, not editorial copy. Content's own
          note (source file, "מחרוזות מבניות מהפרונטאנד") confirms this string is out of
          their scope: "אינו עותק צרכני... חייב לרדת מהעמוד לפני go-live." */}
      <div
        role="status"
        className="sticky top-0 z-20 border-b border-[#C9922A]/40 bg-[#FBEFCB] px-4 py-2 text-center text-[12px] font-bold tracking-[0.01em] text-[#7A5B00]"
      >
        {draftBanner}
      </div>

      <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 sm:py-10">
        {/* Hero — eyebrow/title/deck pulled verbatim from structuralStrings (Content-authored). */}
        <header>
          <p className={GUIDE_SECTION_EYEBROW_CLASS}>{structuralStrings.eyebrow}</p>
          <h1 className="mt-2 text-[1.5rem] font-semibold leading-tight tracking-[-0.028em] text-[#111318] sm:text-[1.9rem]">
            {structuralStrings.title}
          </h1>
          {structuralStrings.deck ? (
            <p className="mt-3 text-[13px] leading-[1.6] text-[#4E5663] sm:text-[14px]">
              {structuralStrings.deck}
            </p>
          ) : null}
        </header>

        {/* Sections 1–7 */}
        <div className="mt-8 space-y-9">
          {sections.map((section) => {
            const quotesForSection = SWEETENER_PULL_QUOTES.filter(
              (q) => q.sectionId === section.id
            );
            const quoteAfterIndex = new Map(
              quotesForSection.map((q) => [q.afterParagraphIndex, q.quote])
            );

            return (
              <section key={section.id} id={section.id}>
                <div className="flex items-center gap-3">
                  <SweetenerSectionIcon icon={SWEETENER_SECTION_ICON[section.id]} />
                  <h2 className="text-[15px] font-extrabold tracking-[-0.02em] text-[#111318] sm:text-[1.05rem]">
                    {section.heading}
                  </h2>
                </div>
                <div className="mt-3 space-y-2">
                  {section.paragraphs.map((paragraph, i) => (
                    <Fragment key={i}>
                      <p className="text-[13px] leading-[1.6] text-[#3E444A]">{paragraph}</p>
                      {quoteAfterIndex.has(i) ? (
                        <SweetenerPullQuote quote={quoteAfterIndex.get(i)!} />
                      ) : null}
                    </Fragment>
                  ))}
                </div>

                {/* "Three groups on the shelf" map — introduces §§2–4, placed right after
                    the opening section (build brief item 3). */}
                {section.id === "opening" ? (
                  <div className="mt-6">
                    <SweetenerGroupCards />
                  </div>
                ) : null}

                {/* Statutory package warning — distinct "label print" element, verbatim.
                    Kicker caption remains frontend-authored/unsigned — see module header. */}
                {section.statutoryWarning ? (
                  <figure className="mt-4 rounded-md border border-dashed border-[#B7B2A6] bg-[#EFEDE6] px-4 py-3">
                    <figcaption className="text-[10px] font-semibold uppercase tracking-[0.18em] text-[#8A857A]">
                      נוסח האזהרה על האריזה
                    </figcaption>
                    <p className="mt-1.5 font-mono text-[13px] font-medium leading-[1.5] text-[#2A2A2A]">
                      {section.statutoryWarning}
                    </p>
                  </figure>
                ) : null}

                {/* Glycemic-index bar chart — replaces the flat table (build brief item 1).
                    Column headers + caption pulled verbatim from structuralStrings.giTable
                    (Content-authored, v5). The original table survives as an sr-only
                    fallback inside GlycemicBarChart. */}
                {section.showGlycemicTable ? (
                  <GlycemicBarChart
                    rows={glycemicRows}
                    columnNameLabel={structuralStrings.giTable.columnName}
                    columnGiLabel={structuralStrings.giTable.columnGi}
                    caption={structuralStrings.giTable.caption}
                  />
                ) : null}

                {/* Chocolate-bar hero card — build brief item 2, scoped to §3
                    ("high-intensity"), the section that discusses that exact bar. */}
                {section.id === "high-intensity" ? <ChocolateBarHeroCard /> : null}

                {/* Video embed slot — build brief item 6, after §2 (polyols). */}
                {section.id === SWEETENER_VIDEO_AFTER_SECTION_ID ? (
                  <SweetenerVideoEmbed
                    videoId={SWEETENER_VIDEO_ID}
                    title={sectionHeadingById(section.id)}
                  />
                ) : null}
              </section>
            );
          })}
        </div>

        {/* Sources — v5: no intro sentence (provenance leak removed); opens directly on
            the first citation. */}
        <section className="mt-10 border-t border-black/[0.08] pt-6">
          <h2 className="text-[13px] font-extrabold tracking-[-0.02em] text-[#3E444A]">
            {sources.heading}
          </h2>
          {sources.intro ? (
            <p className="mt-2 text-[11px] leading-[1.6] text-[#5E6560]">{sources.intro}</p>
          ) : null}
          <ul className="mt-3 space-y-2">
            {sources.items.map((item, i) => (
              <li key={i} className="text-[11px] leading-[1.6] text-[#5E6560]">
                {item}
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}
