"use client";

// GuidePageTemplateV3 — TASK-577 (magnesium guide v3 STRUCTURAL rebuild).
//
// Assembles the owner-dictated page order (2026-07-10 readability ruling), top to
// bottom:
//   1. H1 + ONE intro sentence                              (GuideHeaderV3)
//   2. "מה גילינו" box, 4 bullets                            (GuideBulletBox, boxed)
//   3. Products immediately — 4 descriptive groups            (GuideProductGroupsV3)
//      + the market-information-gaps box (ONE occurrence)
//   4. "איך לקרוא תווית מגנזיום", 3 bullets                   (GuideBulletBox, plain)
//   5. Collapsed education + sources accordion                 (native <details>)
//   6. MethodologyFooter (project-wide standard, unchanged)
//
// Purely additive — mounted only when `guide.useV3Layout` is true (see
// guide-page-template.tsx's branch). Every string rendered here is either
// owner-dictated verbatim or an existing gate-2-approved v2 string carried through
// unchanged (see magnesium-guide-data.ts for the per-field provenance comments); this
// component authors none of it.

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
        suppressedBarsDisclosureHe={guide.suppressedBarsDisclosureHe}
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
          new disclosure primitive. Folds ALL of educationSpine (not only the
          citation list) in here: the owner's own dispatch requires safety-load-bearing
          facts (UL 350 context, evidence_limited meaning) to "survive inside
          disclosures/collapsed sections, not vanish" — that prose lives only in these
          sections, so collapsing (never deleting) is what satisfies both constraints
          without inventing new copy. Reuses the SAME `לפרטים` toggle label as the
          per-product disclosure for one consistent vocabulary on the page. */}
      {guide.educationSpine.length > 0 ? (
        <div className={cn("px-4 pb-2", comparisonWebSectionPaddingClass())} dir="rtl">
          <details
            className="rounded-2xl border border-black/[0.06]"
            data-testid="guide-education-sources-disclosure"
          >
            <summary
              className="cursor-pointer list-none px-4 py-3 text-[13px] font-bold text-[#111318] marker:content-none [&::-webkit-details-marker]:hidden"
              data-testid="guide-education-sources-toggle"
            >
              {GUIDE_V3_DETAILS_LABEL_HE}
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
