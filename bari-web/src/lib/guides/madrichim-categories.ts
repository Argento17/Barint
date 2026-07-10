/**
 * Madrichim (מדריכים) hub registry — TASK-504B Wave 1.
 *
 * Reuses the existing `HashvaotCategory` type + `HashvaotCategoryBox` component
 * verbatim (src/lib/hashvaot/hashvaot-categories.ts, src/components/hashvaot/
 * hashvaot-category-box.tsx) rather than forking a parallel type — the shape already
 * generalizes cleanly to a second hub.
 *
 * Wave 1: magnesium is a real, built guide (/madrichim/magnesium) — content gate-1
 * approved (Content Agent); gate 2 (Adversarial QA / Red-Team) still PENDING per the
 * standing two-gate hard rule, which is why the guide route itself is `noindex` for
 * now (see src/app/madrichim/magnesium/page.tsx).
 *
 * Wave 2: creatine is now also a real, built guide (/madrichim/creatine) — 31
 * products (18 Israeli + 13 worldwide). The tier-layer copy is gate-1 approved
 * (creatine_guide_tier_copy_v1.md); per-product and buying-rule copy has NO
 * guide-specific gate-1 pass yet (see creatine-guide-data.ts header) — gate 2 is
 * PENDING for the whole page, same noindex treatment as magnesium.
 *
 * Supplements stay on /hashvaot/supplements until the Wave-3 migration PR (see the
 * TODO block in src/app/madrichim/page.tsx) — both hubs coexist during this window.
 */

import type { HashvaotCategory } from "@/lib/hashvaot/hashvaot-categories";

// Title/description below are ported verbatim from the gate-1-approved copy
// (magnesium_guide_copy_v1.md H1 + intro first sentence) — not newly authored.
// countLabel replaces the retired heroStat field (hashvaot finding-card redesign,
// b0c3ed53): splitCountLabel renders "N מוצרים נבדקו" as value + label.
export const MADRICHIM_CATEGORIES: HashvaotCategory[] = [
  {
    id: "magnesium-guide",
    title: "איך לבחור מגנזיום",
    status: "live",
    href: "/madrichim/magnesium",
    countLabel: "18 מוצרים נבדקו",
    description:
      "בדקנו 18 תוספי מגנזיום מהמדף הישראלי לפי שישה דברים שבאמת קובעים אם תוסף מגנזיום שווה את הכסף.",
    accent: "#1F8F6A",
    ctaLabel: "מדריך קנייה",
  },
  {
    id: "creatine-guide",
    title: "איך לבחור קריאטין",
    status: "live",
    href: "/madrichim/creatine",
    countLabel: "39 מוצרים נבדקו",
    // UNSIGNED Frontend structural placeholder (no gate-1 card-copy slot exists for
    // creatine yet — creatine-guide-data.ts header gap (b)) — a factual count-based
    // description, not narrative Content voice.
    description:
      "בדקנו 39 תוספי קריאטין — 26 שזמינים בישראל ו-13 מותגי ייחוס עולמיים — לפי מינון, צורה כימית, בדיקת צד שלישי והוגנות מחיר.",
    accent: "#2F7A4F",
    ctaLabel: "מדריך קנייה",
  },
  {
    id: "yogurt-glp1-guide",
    // Title + description reused VERBATIM from the TASK-504A signed metadata
    // (src/app/madrichim/yogurt-glp1/page.tsx) — not newly authored.
    title: "יוגורט עתיר חלבון: מדריך לבחירה",
    status: "live",
    href: "/madrichim/yogurt-glp1",
    countLabel: "78 מוצרים נבדקו",
    description:
      "מדריך לבחירת יוגורט עתיר חלבון מתוך המדף הישראלי, ממוין לפי חלבון, נתרן וסוכר, מבוסס על הציונים שכבר פורסמו בהשוואת היוגורט.",
    accent: "#6E9C88",
    ctaLabel: "מדריך קנייה",
  },
];
