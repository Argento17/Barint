"use client";

// TASK-179I Wave 1 — Glass Box D5/D6 PREVIEW route.
//
// Flag-gated visual preview so the owner can SEE the new glass-box surface before any
// go-live decision. This route does NOT go live and does NOT touch any published score
// or comparison JSON — it renders a small self-contained preview dataset
// (lib/comparisons/glass-box-preview-data.ts, authored from the pilot _on.json) through
// the real shared ComparisonPage / ComparisonRow components.
//
// View it at:  /dev/glass-box-preview   with  NEXT_PUBLIC_GLASSBOX_D5D6=on
// With the flag OFF the same rows render exactly as today (graded chip, no glass-box
// surface) — which is the point of the OFF=current-UI guarantee.

import { ComparisonPage } from "@/components/comparisons/comparison-page";
import { PROTEIN_METRIC } from "@/components/shared/comparison-metric-column";
import {
  glassBoxHummusPreview,
  glassBoxMaadanimPreview,
  glassBoxProcessingPreview,
} from "@/lib/comparisons/glass-box-preview-data";
import { GLASSBOX_D5D6_ON, GLASSBOX_W4_ON } from "@/lib/feature-flags";
import type { ComparisonShelfFilters } from "@/lib/comparisons/registry/types";
import type { BariProductVM } from "@/lib/view-models";

// No shelf lenses in the preview — an empty lens set renders no lens bar, and the
// filter is the identity (preserves corpus order, Invariant 1).
const noShelfFilters: ComparisonShelfFilters<string> = {
  lensOptions: [],
  filterProducts: (products: BariProductVM[]) => products,
};

const PREVIEW_METRICS = [PROTEIN_METRIC] as const;

// TASK-181I — separate banner for the W4 (D3) preview section, gated on its own flag.
function W4FlagBanner() {
  return (
    <div
      className="mx-auto mb-4 w-full max-w-[640px] rounded-[12px] border px-4 py-3 text-[13px] leading-[1.6] lg:max-w-[1180px]"
      style={{
        backgroundColor: GLASSBOX_W4_ON ? "#EEF6F1" : "#FBF8EE",
        borderColor: GLASSBOX_W4_ON ? "#CDE7DA" : "#ECE3C8",
        color: "#3C443F",
      }}
      dir="rtl"
    >
      <p className="font-bold">
        תצוגה מקדימה — Glass Box W4 (דפוס העיבוד / D3)
        <span className="mr-2 font-semibold text-[#6E756F]">
          {GLASSBOX_W4_ON ? "· הדגל פעיל" : "· הדגל כבוי"}
        </span>
      </p>
      <p className="mt-1 text-[#6E756F]">
        {GLASSBOX_W4_ON
          ? "פתח שורה כדי לראות את שורת דפוס העיבוד: עיבוד מינימלי (חיובי) · דפוס מהונדס (מסויג) · ביטחון נמוך (אומדן זמני, גרסה מקוצרת במובייל). תצוגה מקדימה בלבד — אינה משנה אף ציון או נתון חי."
          : "הדגל NEXT_PUBLIC_GLASSBOX_W4 כבוי — השורות מוצגות בדיוק כמו היום, ללא שכבת דפוס העיבוד. כדי לראות אותה, הפעל את הדגל."}
      </p>
    </div>
  );
}

function FlagBanner() {
  return (
    <div
      className="mx-auto mb-4 w-full max-w-[640px] rounded-[12px] border px-4 py-3 text-[13px] leading-[1.6] lg:max-w-[1180px]"
      style={{
        backgroundColor: GLASSBOX_D5D6_ON ? "#EEF6F1" : "#FBF8EE",
        borderColor: GLASSBOX_D5D6_ON ? "#CDE7DA" : "#ECE3C8",
        color: "#3C443F",
      }}
      dir="rtl"
    >
      <p className="font-bold">
        תצוגה מקדימה — Glass Box (D5/D6)
        <span className="mr-2 font-semibold text-[#6E756F]">
          {GLASSBOX_D5D6_ON ? "· הדגל פעיל" : "· הדגל כבוי"}
        </span>
      </p>
      <p className="mt-1 text-[#6E756F]">
        {GLASSBOX_D5D6_ON
          ? 'מוצג: שורה מדורגת רגילה · שורה עם "ניתוח חלקי" · שורה "לא נוקד". זוהי תצוגה מקדימה בלבד — אינה משנה אף ציון או נתון חי.'
          : "הדגל NEXT_PUBLIC_GLASSBOX_D5D6 כבוי — השורות מוצגות בדיוק כמו היום. כדי לראות את שכבת ה-Glass Box, הפעל את הדגל."}
      </p>
    </div>
  );
}

export default function GlassBoxPreviewRoute() {
  return (
    <div className="min-h-screen bg-[#EFEFEB] py-6 sm:py-8" dir="rtl">
      <div className="px-4">
        <FlagBanner />
      </div>

      <ComparisonPage
        products={glassBoxHummusPreview}
        metadataLine="תצוגה מקדימה · חומוס · 3 שורות לדוגמה"
        hero={{
          eyebrow: "Glass Box · תצוגה מקדימה",
          title: "חומוס — ניתוח חלקי / לא נוקד",
        }}
        prologueSentences={[
          'שלוש שורות לדוגמה: מוצר מדורג רגיל, מוצר עם "ניתוח חלקי", ומוצר "לא נוקד".',
        ]}
        methodologyLines={[
          "תצוגה מקדימה בלבד. אינה משנה אף ציון חי או נתון שפורסם.",
        ]}
        shelfFilters={noShelfFilters}
        metricSpecs={PREVIEW_METRICS}
      />

      <div className="h-6" />

      <ComparisonPage
        products={glassBoxMaadanimPreview}
        metadataLine="תצוגה מקדימה · מעדנים · 3 שורות לדוגמה"
        hero={{
          eyebrow: "Glass Box · תצוגה מקדימה",
          title: "מעדנים — ניתוח חלקי / לא נוקד",
        }}
        prologueSentences={[
          'שלוש שורות לדוגמה: מוצר מדורג רגיל, ג\'לי עם "ניתוח חלקי", ומוצר "לא נוקד".',
        ]}
        methodologyLines={[
          "תצוגה מקדימה בלבד. אינה משנה אף ציון חי או נתון שפורסם.",
        ]}
        shelfFilters={noShelfFilters}
        metricSpecs={PREVIEW_METRICS}
      />

      <div className="h-6" />

      <div className="px-4">
        <W4FlagBanner />
      </div>

      <ComparisonPage
        products={glassBoxProcessingPreview}
        metadataLine="תצוגה מקדימה · W4 · דפוס העיבוד · 3 שורות לדוגמה"
        hero={{
          eyebrow: "Glass Box W4 · תצוגה מקדימה",
          title: "דפוס העיבוד — עיבוד מינימלי / מהונדס / אומדן זמני",
        }}
        prologueSentences={[
          "שלוש שורות לדוגמה: עיבוד מינימלי (חיובי), דפוס הרכב מהונדס (מסויג), ואומדן בביטחון נמוך (זמני). פתח שורה כדי לראות את שורת דפוס העיבוד.",
        ]}
        methodologyLines={[
          "תצוגה מקדימה בלבד. אינה משנה אף ציון חי או נתון שפורסם.",
        ]}
        shelfFilters={noShelfFilters}
        metricSpecs={PREVIEW_METRICS}
      />
    </div>
  );
}
