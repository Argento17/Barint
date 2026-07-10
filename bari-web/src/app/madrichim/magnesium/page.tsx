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
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

// Meta description sourced VERBATIM from the gate-1 v2 copy package, Slot 10b
// (02_products/supplements/magnesium/mag_guide_v2_copy_package.md) — TASK-575
// gate-2 CRITICAL-1 fix: the prior v1 string carried the retired model (named
// third-party testing + price as assessed criteria) and the unscoped
// "מהמדף הישראלי" market claim. Not authored here.
export const metadata: Metadata = {
  title: "איך לבחור מגנזיום | Bari",
  description:
    "בארי בדקה 18 תוספי מגנזיום הנמכרים בישראל לפי מינון מגנזיום יסודי, צורה כימית, בטיחות ושקיפות תיוג, כדי להראות מה לחפש על התווית לפני שקונים.",
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
