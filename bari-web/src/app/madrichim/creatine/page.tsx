// Creatine guide route — /madrichim/creatine (TASK-504 Wave 2).
//
// Mirrors src/app/madrichim/magnesium/page.tsx exactly in structure. This is NOT
// the live /hashvaot/creatine comparison page — that page is untouched, stays live,
// and is only removed in the Wave-3 migration PR.
//
// noindex for now: TWO gaps stand between this page and go-live, both stronger than
// magnesium's single gap at its own Wave-1 ship point —
//   1. The tier-layer copy (creatine_guide_tier_copy_v1.md) is gate-1 (Content)
//      approved only; gate 2 (Adversarial QA / Red-Team) is PENDING, same as
//      magnesium.
//   2. UNLIKE magnesium, per-product oneLinerHe and the buyingRule bar explanations
//      have NO guide-specific gate-1 copy at all (see creatine-guide-data.ts header)
//      — this build reuses the existing (also-draft) rowVerdict strings and ships
//      short Frontend-authored structural placeholders for the bar explanations.
// Flip robots to index once both gaps close — Frontend does not self-approve
// content, this is a reversible, non-consumer-facing technical default.

import type { Metadata } from "next";

import { HomeContainer } from "@/components/home/section-frame";
import { GuidePageTemplate } from "@/components/guides/guide-page-template";
import { creatineGuide } from "@/lib/guides/creatine-guide-data";
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

// Meta description: structural facts only (counts + the four checked parameters),
// mirroring the register of the magnesium guide's own metadata line. Not yet
// two-gate signed off — see the file-header note above.
export const metadata: Metadata = {
  title: "איך לבחור קריאטין | Bari",
  description:
    "בארי בדקה 39 תוספי קריאטין — 26 שזמינים בישראל ו-13 מותגי ייחוס עולמיים — לפי מינון, צורה כימית, בדיקת צד שלישי והוגנות מחיר, כדי להראות מה לחפש על התווית לפני שקונים.",
  robots: { index: false, follow: true },
};

// Content sign-off status: gate 1 (Content Agent) complete for the tier layer only
// (creatine_guide_tier_copy_v1.md); gate 2 (Adversarial QA / Red-Team) PENDING for
// everything on this page, including the per-product and buying-rule strings that
// have no gate-1 pass at all yet (creatine-guide-data.ts header).
const METHODOLOGY_LINES = [
  "בארי מבססת את ההשוואה על קריאת תוויות ודפי מוצר. כל המינונים והמחירים המוצגים הם מה שכתוב על האריזה או בדף המוצר בעת הבדיקה. המחירים המוצגים נכונים לתאריך הבדיקה (יולי 2026) ועשויים להשתנות. המידע כאן הוא לצורך הכרה בלבד, ואינו תחליף לייעוץ רפואי.",
];

export default function CreatineGuidePage() {
  return (
    <main
      className={cn(
        "relative min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="py-6">
        <GuidePageTemplate guide={creatineGuide} methodologyLines={METHODOLOGY_LINES} />
      </HomeContainer>
    </main>
  );
}
