"use client";

// GuidePageTemplateV3 — TASK-577 (magnesium guide v3, wiring phase).
//
// Assembles the owner-dictated page order (2026-07-10 readability ruling), top to
// bottom:
//   1. H1 + ONE intro sentence                              (GuideHeaderV3)
//   2. "מה גילינו" box, 4 bullets                            (GuideBulletBox, boxed)
//   3. Products immediately — 4 descriptive groups            (GuideProductGroupsV3)
//      + the market-information-gaps box (ONE occurrence, signed compact copy)
//   4. "איך לקרוא תווית מגנזיום", 3 bullets                   (GuideBulletBox, plain)
//   5. Collapsed education + sources accordion                 (native <details>)
//   6. MethodologyFooter (project-wide standard, unchanged)
//
// Purely additive — mounted only when `guide.useV3Layout` is true (see
// guide-page-template.tsx's branch). Every string rendered here is either
// owner-dictated verbatim or the signed gate-1 copy package
// (mag_guide_v3_copy_package.md), wired via magnesium-guide-data.ts /
// magnesium-guide-copy-v3.ts; this component authors none of it.

import { ChevronDown } from "lucide-react";
import { GuideHeaderV3 } from "@/components/guides/guide-header-v3";
import { GuideBulletBox } from "@/components/guides/guide-bullet-box";
import { GuideProductGroupsV3 } from "@/components/guides/guide-product-groups-v3";
import { GuideEducationSpine } from "@/components/guides/guide-education-spine";
import { MethodologyFooter } from "@/components/shared/methodology-footer";
import { comparisonWebSectionPaddingClass } from "@/lib/design/bari-comparison-tokens";
import { GUIDE_V3_DETAILS_LABEL_HE, type GuidePageVM } from "@/lib/view-models";
import { cn } from "@/lib/utils";

export function GuidePageTemplateV3({
  guide,
  methodologyLines,
}: {
  guide: GuidePageVM;
  methodologyLines?: string[];
}) {
  return (
    <div
      className="bg-[#FCFCF9]"
      data-testid="guide-page-template-v3"
      data-guide-slug={guide.slug}
    >
      <GuideHeaderV3
        h1={guide.h1}
        subtitle={guide.subtitle}
        heroImage={guide.heroImage}
        introSentenceHe={guide.introSentenceHe}
        updatedLabel={guide.updatedLabel}
        wide
      />

      {guide.whatWeFoundHe ? (
        <GuideBulletBox
          heading={guide.whatWeFoundHe.heading}
          bullets={guide.whatWeFoundHe.bullets}
          boxed
          wide
          testId="guide-what-we-found"
        />
      ) : null}

      <GuideProductGroupsV3
        products={guide.products}
        groupLabelsHe={guide.groupV3LabelsHe}
        suppressedBars={guide.suppressedBars}
        thresholdGeometry={guide.thresholdGeometry}
        marketGapsHe={guide.marketGapsCompactHe}
        expanderLabels={guide.expanderLabelsV3}
        wide
      />

      {guide.howToReadLabelHe ? (
        <GuideBulletBox
          heading={guide.howToReadLabelHe.heading}
          bullets={guide.howToReadLabelHe.bullets}
          boxed={false}
          wide
          testId="guide-how-to-read-label"
        />
      ) : null}

      {/* Collapsed education + sources accordion (dispatch item 6). Native
          <details>/<summary> — no JS required, works before hydration, and needs no
          new disclosure primitive. Folds ALL of educationSpine (REUSED-v2 per copy
          package §6 — every section confirmed unchanged/signed, none physically
          re-merged) in here: safety-load-bearing facts (UL 350 context,
          evidence_limited meaning) "survive inside disclosures/collapsed sections,
          not vanish" per structure spec §D's survival list — that prose lives only in
          these sections, so collapsing (never deleting) is what satisfies both
          constraints.

          TASK-587 (v3.2 polish, visual spec §3): findability fix, stays collapsed by
          default (Hard Rule 3 — conformance/bug-fix, not relocation or a new
          component). The `rounded-2xl border` card wrapper is DROPPED — rendered as a
          plain section instead, matching the non-boxed idiom one section above
          (GuideBulletBox boxed={false}) — the bordered-card treatment was itself part
          of why this read as "a different kind of thing" than the rest of the page.
          `<summary>`'s own content is always visible whether open or closed (only its
          sibling content toggles), so the heading + one-line teaser + expand
          affordance all live inside it: a real, findable section that still stays
          collapsed by default. `group` on <details> drives the CSS-only
          open/collapsed swap below (chevron rotation, label swap) — no JS state, same
          zero-JS/pre-hydration property the native element already had. */}
      {guide.educationSpine.length > 0 ? (
        <div className={cn("px-4 py-4", comparisonWebSectionPaddingClass())} dir="rtl">
          <details className="group" data-testid="guide-education-sources-disclosure">
            <summary
              className="cursor-pointer list-none marker:content-none [&::-webkit-details-marker]:hidden"
              data-testid="guide-education-sources-toggle"
            >
              <h2 className="text-[15px] font-extrabold tracking-[-0.02em] text-[#111318]">
                {guide.collapsedEvidenceSectionTitleHe ?? GUIDE_V3_DETAILS_LABEL_HE}
              </h2>
              {guide.collapsedEvidenceSectionTeaserHe ? (
                <p
                  className="mt-1 text-[13px] leading-[1.6]"
                  style={{ color: "#3E444A" }}
                  data-testid="guide-education-sources-teaser"
                >
                  {guide.collapsedEvidenceSectionTeaserHe}
                </p>
              ) : null}
              <span className="mt-2 flex items-center justify-between">
                <span className="text-[12px] font-semibold" style={{ color: "#4E5663" }}>
                  <span className="group-open:hidden">
                    {guide.educationExpanderLabelsV3?.collapsed ?? GUIDE_V3_DETAILS_LABEL_HE}
                  </span>
                  <span className="hidden group-open:inline">
                    {guide.educationExpanderLabelsV3?.expanded ?? GUIDE_V3_DETAILS_LABEL_HE}
                  </span>
                </span>
                {/* Byte-identical tokens to the proven product-row expander
                    (guide-product-row-v3.tsx:159-182) — same icon, size, stroke,
                    transition, and two-tone color pair, just driven by `group-open`
                    (CSS) instead of React state (this disclosure has none). */}
                <ChevronDown
                  aria-hidden
                  strokeWidth={1.75}
                  className="size-[15px] text-[#B5BBB6] transition-transform duration-200 group-open:rotate-180 group-open:text-[#9A9FA6] motion-reduce:transition-none"
                />
              </span>
            </summary>
            <div className="border-t border-black/[0.05]">
              <GuideEducationSpine sections={guide.educationSpine} wide={false} />
            </div>
          </details>
        </div>
      ) : null}

      {methodologyLines && methodologyLines.length > 0 ? (
        <MethodologyFooter lines={methodologyLines} wide />
      ) : null}
    </div>
  );
}
