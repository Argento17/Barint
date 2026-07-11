"use client";

// Reusable Guide page template (TASK-504, Wave 0 skeleton).
// Assembles the plan's three layers (§3): buying rule → product bar-state table →
// education spine. Driven entirely by the typed GuidePageVM contract — no per-guide
// branching lives here. The magnesium and creatine guides (Wave 1/2) will each supply
// their own GuidePageVM and render through this same template unchanged.
//
// Not yet reviewed by the Design Agent (that conformance pass is plan §6, scheduled
// after this spike). Structure and token reuse only — treat pixel-level styling here
// as provisional until that gate runs.

import { GuideBuyingRule } from "@/components/guides/guide-buying-rule";
import { GuideProductTable } from "@/components/guides/guide-product-table";
import { GuideEducationSpine } from "@/components/guides/guide-education-spine";
import { MethodologyFooter } from "@/components/shared/methodology-footer";
import { MobileActionBar } from "@/components/shared/mobile-action-bar";
import type { GuidePageVM } from "@/lib/view-models";

export function GuidePageTemplate({
  guide,
  methodologyLines,
}: {
  guide: GuidePageVM;
  /** Optional — the category-caveat / methodology standard applies project-wide.
   *  Pass Content-authored lines once the golden guide (magnesium) ships; omitted in
   *  this skeleton since no real methodology copy exists yet. */
  methodologyLines?: string[];
}) {
  return (
    <div
      className="bg-[#FCFCF9]"
      data-testid="guide-page-template"
      data-guide-slug={guide.slug}
    >
      <MobileActionBar title={guide.h1} />
      <GuideBuyingRule
        h1={guide.h1}
        subtitle={guide.subtitle}
        heroImage={guide.heroImage}
        buyingRuleIntro={guide.buyingRuleIntro}
        bars={guide.buyingRule}
        wide
      />
      <GuideProductTable
        products={guide.products}
        buyLinkDisclosureLine={guide.buyLinkDisclosureLine}
        headlineFinding={guide.headlineFinding}
        suppressedBars={guide.suppressedBars}
        suppressedBarsDisclosureHe={guide.suppressedBarsDisclosureHe}
        bandExcludedBars={guide.bandExcludedBars}
        domesticBandsDisclosureHe={guide.domesticBandsDisclosureHe}
        benchmarkProducts={guide.benchmarkProducts}
        benchmarkSectionHeadingHe={guide.benchmarkSectionHeadingHe}
        recommendationTierCaptions={guide.recommendationTierCaptions}
        veryRecommendedEmptyStateHe={guide.veryRecommendedEmptyStateHe}
        cannotAssessSectionIntroHe={guide.cannotAssessSectionIntroHe}
        expanderLabels={guide.expanderLabels}
        thresholdGeometry={guide.thresholdGeometry}
        wide
      />
      <GuideEducationSpine sections={guide.educationSpine} wide />
      {methodologyLines && methodologyLines.length > 0 ? (
        <MethodologyFooter lines={methodologyLines} wide />
      ) : null}
    </div>
  );
}
