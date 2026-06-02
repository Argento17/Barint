import type { Metadata } from "next";

import { buildConsumerExplanationView } from "@/lib/comparisons/consumer-explanation-view";
import { milkProducts } from "@/lib/comparisons/milk-page-data";
import { shortenReason } from "@/lib/comparisons/row-surface";
import {
  filterMilkProducts,
  MILK_SHELF_LENS_OPTIONS,
  type MilkShelfFilterId,
} from "@/lib/comparisons/milk-shelf-filters";
import type { ComparisonShelfFilters } from "@/lib/comparisons/registry/types";
import type { BariProductVM } from "@/lib/view-models";

// IMP-3 — fold milk onto the shared ComparisonPage. Milk is website=LEGACY: scores and
// copy are preserved verbatim; only the rendering path changes. Everything that made milk
// "special" (its 4-cell grid, framer row, bespoke expansion taxonomy, pillars panel) was
// layout, not data — this layer reshapes the bespoke MilkComparisonProduct into the
// universal BariProductVM so the one responsive table can render it.
//
// Expansion remap (MILK_RECOMMENDATION §2, verbatim strings):
//   whatToKnow + takeawayLine → rowVerdict      (the 2-sentence collapsed-row description —
//                                                authored analysis + verdict, matching the
//                                                maadanim row treatment, NOT terse +/− lines)
//   raisesScore     → expansion.positiveSignals (מה עובד לטובת המוצר?)
//   lowersScore     → expansion.limitingFactors (מה מגביל את הציון?)
//   relativeToPeers → expansion.comparisonContext (הקשר במדף)
//   tradeoffNote    → expansion.caveats         (הערות)
// All 18 milk products are curated (milk-product-insights), so whatToKnow/takeawayLine are
// per-product authored strings — composing them into a row verdict surfaces "what we saw in
// the analysis" on the row, the way maadanim's authored rowVerdict does. No fabrication.
//
// GOVERNED OMISSION (flagged for Content/Nutrition re-approval): the bespoke "advanced —
// פירוט לפי היבטים" pillars panel (BariInterpretationPanel) is NOT ported. It is a
// per-dimension score-bar + strength-label (חזק/בינוני/חלש) surface — both are deprecated
// Gen-0 patterns (Architecture Generations Registry) and the strength labels are
// explicitly forbidden by the Score Presentation rules. No other category exposes it, and
// adding a slot for it to the shared expansion would re-introduce the category-specific
// divergence this unification exists to remove. The two textual metric cells the grid
// carried (תוספים label, רכיב עיקרי) are likewise dropped — they are textual, not the
// numeric metrics the aligned column renders, and their content is already narrated in the
// positive/limiting signal lines.

function buildMilkProductVM(): BariProductVM[] {
  return milkProducts.map((product) => {
    const view = buildConsumerExplanationView(product, milkProducts);
    // Analysis sentence + verdict, composed into the collapsed-row description.
    const rowVerdict = [view.whatToKnow, view.takeawayLine]
      .map((s) => s?.trim())
      .filter(Boolean)
      .join(" ");
    return {
      id: product.barcode,
      name: product.displayTitle ?? product.shortName,
      imageUrl: product.image_url,
      score: product.score,
      grade: product.grade,
      insightLine: "",
      // All milk rows are fully-scored products with an ingredient panel and label
      // nutrition — verified. No bespoke per-product confidence signal exists to gate
      // partial/insufficient, and we do not fabricate one.
      confidence: "verified",
      expansion: {
        nutrition: null,
        ingredients: null,
        confidenceLabel: "נתונים מלאים",
        servingNote: "ל-100 מ״ל",
        positiveSignals: view.raisesScore,
        limitingFactors: view.lowersScore,
        comparisonContext: view.relativeToPeers,
        caveats: view.tradeoffNote ? [view.tradeoffNote] : undefined,
      },
      metrics: {
        protein_g: product.proteinPer100ml,
        sugar_g: product.sugarPer100ml,
      },
      // rowReason added for hummus-format parity (TASK-161A). Milk rows render rowVerdict
      // (the authored 2-sentence description) first; rowReason is the +/− fallback derived
      // from the same raisesScore/lowersScore signals, matching the other categories.
      rowReason: {
        positive: shortenReason(view.raisesScore?.[0]),
        limiting: shortenReason(view.lowersScore?.[0]),
      },
      rowVerdict,
    } satisfies BariProductVM;
  });
}

export const milkVmProducts: BariProductVM[] = buildMilkProductVM();

export const milkMetadataLine = `${milkVmProducts.length} מוצרים בדירוג · מדגם מדף (תוויות), 2026 · ממוין לפי ציון Bari`;

export const milkHero = {
  eyebrow: "חלב ותחליפים",
  title: "השוואת חלב ותחליפי חלב",
} as const;

// Preserved verbatim from the bespoke milk page prologue paragraph.
export const milkPrologueSentences = [
  "חלב נראה כמו קטגוריה פשוטה, אבל המדף מספר סיפור קצת יותר מורכב.",
  "חלק מהמוצרים נשענים על הרכב בסיסי וקצר יחסית, בעוד אחרים משתמשים בתוספות שונות כדי להשפיע על מרקם, חיי מדף או ערכים תזונתיים.",
  "בבדיקה ראינו שמוצרים שנראים דומים מאוד מבחוץ יכולים להיות שונים בהרכב, ברמת העיבוד ובאופן שבו הם משתלבים בשימוש יומיומי.",
  "לכן ההשוואה כאן לא מסתכלת רק על מספר אחד, אלא על התמונה הרחבה של המוצר כפי שהוא מופיע על המדף.",
] as const;

// Preserved verbatim from the bespoke milk page methodology section.
export const milkMethodologyLines = [
  "ההשוואה מבוססת על מוצרי חלב שנאספו ונבדקו מתוך מידע גלוי לצרכן במדף הישראלי.",
  "לכל מוצר נבחנים הרכב הרכיבים, הערכים התזונתיים, רמת העיבוד וההקשר הקטגורי שלו.",
  "ההשוואה אינה נשענת רק על קלוריות, חלבון או סוכר, אלא מנסה להבין את איכות המוצר כמכלול.",
  "הדירוג נועד לעזור בהשוואה בין מוצרים דומים באותה קטגוריה, ולא לשמש כהמלצה רפואית או תזונתית אישית.",
] as const;

// Category caveat (cheese gold-standard format), rendered once in the header. Grounded in
// the frozen milk run_004 outcome (CLAUDE.md invariant: top = whole/4%/goat dairy at 85/A;
// plant drinks are scored on the same category-relative scale, not penalized for being
// non-dairy). Two reader nuances: (1) "low-fat" is not automatically a higher score;
// (2) plant and dairy are compared on the same shelf, by composition — not by type.
export const milkCategoryNote = [
  "הערת קטגוריה — 'דל שומן' אינו אוטומטית ציון גבוה יותר\n\nהציון משקלל את הרכב המוצר כולו — חלבון, סוכר, תוספים ורמת עיבוד — ולא את אחוז השומן לבדו. חלב מלא או 3% עשוי לקבל ציון גבוה מגרסת דל-שומן של אותו מותג, כשהבסיס שלו פשוט יותר.",
  "הערת קטגוריה — חלב פרה ותחליפים צמחיים נמדדים על אותו מדף\n\nמשקה שקדים, סויה או שיבולת שועל אינו מקבל ציון נמוך רק משום שאינו חלב. כל מוצר נמדד מול דומיו לפי ההרכב שעל האריזה — אך שימו לב שתחליפים צמחיים רבים מועשרים ומיוצבים, וזה משתקף בציון.",
]
  .join("\n\n");

export const milkBlogLink = {
  href: "/blog/milk-analysis",
  label: "קראו את הניתוח העיתונאי בבלוג ←",
} as const;

export const milkComparisonMetadata: Metadata = {
  title: "השוואת חלב ואלטרנטיבות | Bari",
  description:
    "השוואת מוצרים אמיתיים ממדפי סופרים — ציון Bari, חלבון, סוכר, תוספים ופרשנות מוצר. מידע, לא המלצה.",
};

function isMilkShelfFilterId(filter: string): filter is MilkShelfFilterId {
  return MILK_SHELF_LENS_OPTIONS.some((option) => option.id === filter);
}

export const milkShelfFilters: ComparisonShelfFilters<MilkShelfFilterId> = {
  lensOptions: MILK_SHELF_LENS_OPTIONS,
  filterProducts: (products: BariProductVM[], activeFilters: MilkShelfFilterId[]) =>
    filterMilkProducts(products, activeFilters.filter(isMilkShelfFilterId)),
};
