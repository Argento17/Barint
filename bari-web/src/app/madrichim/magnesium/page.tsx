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
// MAG_V3_METADATA_DESCRIPTION_HE (the prior three-dimension metadata description) is
// intentionally not imported -- TASK-580 gate-2 RT-4: it contradicted the page's own
// visible intro ("ארבעה דברים", v3.1-SLOT-2) by still saying "שלושה דברים". See the
// `metadata.description` comment below for the fix. Still exported from
// magnesium-guide-copy-v3.ts for rollback/provenance; just unused at this call site.
import { siteHeaderOffsetClass } from "@/lib/site-layout";
import { cn } from "@/lib/utils";

// TASK-577 wiring phase (HISTORICAL — superseded for `description` by the TASK-580
// gate-2 RT-4 comment at the field itself, below): meta description sourced VERBATIM
// from the signed v3 copy package, §3 (02_products/supplements/magnesium/
// mag_guide_v3_copy_package.md, sha256
// 668fdaee57449e8514c12d2fded3ed653a391a7cc0f5a49fd7919b622160f2dd) — supersedes the
// v2 4-criteria frame this task's dispatch says "burned us in v2 gate-2." Scoped to
// "18 תוספי מגנזיום... שבדקה," no "מהמדף הישראלי" market-completeness claim. Not
// authored here. `title` below is still governed by this paragraph, unchanged.
//
// TASK-577 fix round (2026-07-10): title corrected to the owner-dictated H1
// ("איך לבחור תוסף מגנזיום") — the copy package has no H1/title slot (package gap),
// so the owner's own dictated text wins over the leftover v2 string this carried.
// No openGraph/twitter override exists on this route (checked — the root layout's
// openGraph.title is a generic, site-wide string, unrelated to this page).
export const metadata: Metadata = {
  title: "איך לבחור תוסף מגנזיום | Bari",
  // description: TASK-580 gate-2 RT-4 fix -- restores intro/metadata consistency.
  // The visible intro now reads "ארבעה דברים" (v3.1-SLOT-2, TASK-580 commit
  // 9223fb69), but this metadata description still said "שלושה דברים" -- a page
  // contradicting its own <meta> tag. Fix: reuse the ALREADY two-gate-signed
  // four-dimension description from mag_guide_v2_copy_package.md SLOT 10b (sha256
  // of that package unchanged by this task -- REUSED-v2 signed string, not new
  // copy), extracted programmatically from its fenced block, byte-exact. Part of
  // the same שלושה→ארבעה bundle as the SLOT-2 intro -- pending owner acceptance
  // of that numeral change (Content's SLOT-2 addendum return: "requires the
  // owner's explicit acceptance before it ships -- proposed here, not settled").
  // Not pushed past this local branch pending that acceptance + Red-Team gate-2.
  description:
    'בארי בדקה 18 תוספי מגנזיום הנמכרים בישראל לפי מינון מגנזיום יסודי, צורה כימית, בטיחות ושקיפות תיוג, כדי להראות מה לחפש על התווית לפני שקונים.',
  robots: { index: false, follow: true },
};

// Content sign-off status: gate 1 (Content Agent) complete, gate 2 (Adversarial QA /
// Red-Team) PENDING — magnesium_guide_copy_v1.md header, verified at build time
// (03_operations/reports/content/magnesium_guide_copy_v1.md line 3).
//
// TASK-577 fix round (2026-07-10): the page-level `methodologyLines` pass to
// GuidePageTemplate is REMOVED — it rendered the exact same disclaimer sentence
// ("בארי קוראת תוויות. בארי אינה בודקת במעבדה...") a second time, byte-identical to
// the string already at the top of the guide's own "מקורות" section
// (magnesium-guide-data.ts, educationSpine[5].body[0]), which is REUSED-v2 signed
// content living inside the v3 collapsed education+sources accordion. The fix
// instruction is explicit: keep exactly the one occurrence at the top of מקורות,
// remove the other render. `GuidePageTemplate`'s `methodologyLines` param stays
// optional/project-wide (its own doc comment already frames it that way) — this is a
// per-guide decision not to double-render a fact this guide's own copy package
// already places elsewhere, not a change to the canonical MethodologyFooter
// component itself.
export default function MagnesiumGuidePage() {
  return (
    <main
      className={cn(
        "relative min-h-screen bg-[#F7F7F2] text-[#111318]",
        siteHeaderOffsetClass
      )}
    >
      <HomeContainer className="py-6">
        <GuidePageTemplate guide={magnesiumGuide} />
      </HomeContainer>
    </main>
  );
}
