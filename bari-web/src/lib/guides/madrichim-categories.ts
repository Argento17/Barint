/**
 * Madrichim (מדריכים) hub registry — TASK-504B Wave 1.
 *
 * Reuses the existing `HashvaotCategory` type + `HashvaotCategoryBox` component
 * verbatim (src/lib/hashvaot/hashvaot-categories.ts, src/components/hashvaot/
 * hashvaot-category-box.tsx) rather than forking a parallel type — the shape already
 * generalizes cleanly to a second hub.
 *
 * Wave 1: magnesium is a real, built guide (/madrichim/magnesium) — content gate-1
 * approved (Content Agent); gate 2 (Adversarial QA / Red-Team) passed with the
 * TASK-504B fix commits; the guide route stays `noindex` pending owner robots
 * approval (see src/app/madrichim/magnesium/page.tsx).
 *
 * The TASK-504A yogurt-glp1 guide (owner-ready) is listed with title/description
 * reused VERBATIM from its signed metadata (src/app/madrichim/yogurt-glp1/page.tsx)
 * — not newly authored.
 *
 * DEFERRED: the creatine guide (TASK-504 Wave 2) is NOT listed here. Its rebuilt
 * 26-domestic corpus carries "TODO owner-description-pass (freeze)" placeholders on
 * the 8 new products (owner product-descriptions freeze) — it ships only after the
 * owner's description pass replaces those placeholders.
 */

import type { HashvaotCategory } from "@/lib/hashvaot/hashvaot-categories";

// Title/description below are ported verbatim from the gate-1-approved copy
// (magnesium_guide_copy_v1.md H1 + intro first sentence) — not newly authored.
// ctaLabel reuses the live blog CTA string "מדריך קנייה" verbatim.
export const MADRICHIM_CATEGORIES: HashvaotCategory[] = [
  {
    id: "magnesium-guide",
    title: "איך לבחור מגנזיום",
    status: "live",
    href: "/madrichim/magnesium",
    description:
      "בדקנו 18 תוספי מגנזיום מהמדף הישראלי לפי שישה דברים שבאמת קובעים אם תוסף מגנזיום שווה את הכסף.",
    accent: "#1F8F6A",
    heroStat: { value: "18", label: "מוצרים נבדקו" },
    ctaLabel: "מדריך קנייה",
  },
  {
    id: "yogurt-glp1-guide",
    // Title + description reused VERBATIM from the TASK-504A signed metadata
    // (src/app/madrichim/yogurt-glp1/page.tsx) — not newly authored.
    title: "יוגורט עתיר חלבון: מדריך לבחירה",
    status: "live",
    href: "/madrichim/yogurt-glp1",
    description:
      "מדריך לבחירת יוגורט עתיר חלבון מתוך המדף הישראלי, ממוין לפי חלבון, נתרן וסוכר, מבוסס על הציונים שכבר פורסמו בהשוואת היוגורט.",
    accent: "#6E9C88",
    heroStat: { value: "78", label: "מוצרים נבדקו" },
    ctaLabel: "מדריך קנייה",
  },
];
