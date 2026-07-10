// Magnesium golden guide route — /madrichim/magnesium (TASK-504B, Wave 1).
//
// Renders GuidePageTemplate against the real magnesium GuidePageVM (bar-states from
// the Nutrition-owned validation table, copy gate-1-approved by Content). This is NOT
// the live /hashvaot/magnesium comparison page — that page is untouched, stays live,
// and is only removed in the Wave-3 migration PR (see the TODO block in
// src/app/madrichim/page.tsx). Both pages coexist during the build/verification window.
//
// noindex for now: the ported copy is gate-1 (Content) approved but has NOT yet passed
// gate 2 (Adversarial QA / Red-Team) — the standing two-gate hard rule
// (content_signoff_hard_rule) means this page is not yet consumer-ready for search
// discovery. Flip robots to index once gate 2 signs off (Frontend does not self-approve
// content — this is a reversible, non-consumer-facing technical default, not a content
// judgment).

import type { Metadata } from "next";

import { HomeContainer } from "@/components/home/section-frame";
import { GuidePageTemplate } from "@/components/guides/guide-page-template";
import { magnesiumGuide } from "@/lib/guides/magnesium-guide-data";
import { MAG_V3_METADATA_DESCRIPTION_HE } from "@/lib/guides/magnesium-guide-copy-v3";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

// TASK-577 wiring phase: meta description sourced VERBATIM from the signed v3 copy
// package, §3 (02_products/supplements/magnesium/mag_guide_v3_copy_package.md,
// sha256 668fdaee57449e8514c12d2fded3ed653a391a7cc0f5a49fd7919b622160f2dd) —
// supersedes the v2 4-criteria frame this task's dispatch says "burned us in v2
// gate-2." Scoped to "18 תוספי מגנזיום... שבדקה," no "מהמדף הישראלי"
// market-completeness claim. Not authored here.
export const metadata: Metadata = {
  title: "איך לבחור מגנזיום | Bari",
  description: MAG_V3_METADATA_DESCRIPTION_HE,
  robots: { index: false, follow: true },
};

// Content sign-off status: gate 1 (Content Agent) complete, gate 2 (Adversarial QA /
// Red-Team) PENDING — magnesium_guide_copy_v1.md header, verified at build time
// (03_operations/reports/content/magnesium_guide_copy_v1.md line 3).
const METHODOLOGY_LINES = [
  "בארי קוראת תוויות. בארי אינה בודקת במעבדה. כל המינונים המוצגים הם מה שכתוב על האריזה הישראלית. המידע כאן הוא לצורך היכרות בלבד. הוא אינו תחליף לייעוץ רפואי.",
];

export default function MagnesiumGuidePage() {
  return (
    <main
      className={cn(
        "relative min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="py-6">
        <GuidePageTemplate guide={magnesiumGuide} methodologyLines={METHODOLOGY_LINES} />
      </HomeContainer>
    </main>
  );
}
