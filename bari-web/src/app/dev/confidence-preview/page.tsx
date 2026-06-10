"use client";

// DEV-ONLY harness for the Score Confidence / Data-Completeness Indicators (spec v1).
// Proves all 7 consumer states — including State 7 (`insufficient` → טרם נוקד null pill),
// which has NO live product (live distribution: verified 74 / partial 395 / insufficient 0).
// These are local fixtures; no fake product is written into the live comparison JSON.
// Renders through the REAL ComparisonTable → ComparisonRow → ConfidenceMarker path so the
// preview reflects production rendering exactly. Not linked from any nav.

import { ComparisonTable } from "@/components/shared/comparison-table";
import type { BariProductVM } from "@/lib/view-models";

function expansion(over: Partial<BariProductVM["expansion"]> = {}) {
  return {
    nutrition: {
      energyKcal: 250,
      protein: 9,
      sugar: 4,
      fat: 12,
      satFat: 7,
      fiber: null,
      sodium: 320,
    },
    ingredients: "חלב, מלח, תרבית.",
    confidenceLabel: "נתונים מלאים",
    servingNote: "ל-100 גרם",
    positiveSignals: ["חלבון סביר מול שומן מתון"],
    limitingFactors: ["שומן רווי גבוה יחסית"],
    bottomLine: "מוצר סולידי בקטגוריה.",
    ...over,
  } satisfies BariProductVM["expansion"];
}

// Fixtures map onto the 8 regression cases. States 1–6 mirror the real backend field
// shapes (confidence_label_he / confidence_tooltip_he prerendered verbatim); States 7a/7b
// carry score=null + confidence "insufficient" to trigger chip suppression.
const FIXTURES: BariProductVM[] = [
  {
    id: "fx-1-complete",
    name: "1 · נתונים מלאים (verified)",
    imageUrl: null,
    score: 85,
    grade: "A",
    insightLine: "מבוסס על תווית מלאה — אין סימון.",
    confidence: "verified",
    confidence_label_he: "מבוסס על נתונים מלאים",
    confidence_tooltip_he: "הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים.",
    confidence_sub_reason: null,
    expansion: expansion(),
  },
  {
    id: "fx-2-partial",
    name: "2 · נתונים חלקיים (partial)",
    imageUrl: null,
    score: 70,
    grade: "B",
    insightLine: "טבעת מנוקדת + נקודה אפורה.",
    confidence: "partial",
    confidence_label_he: "מבוסס על נתונים חלקיים",
    confidence_tooltip_he:
      "הציון מבוסס על נתונים חלקיים. חלק מהפרטים לא היו זמינים.",
    confidence_sub_reason: "partial_field",
    expansion: expansion({ confidenceLabel: "נתונים חלקיים" }),
  },
  {
    id: "fx-3-missing-ingredients",
    name: "3 · חסרים נתוני רכיבים (partial)",
    imageUrl: null,
    score: 68,
    grade: "C",
    insightLine: "לוח תזונה קיים, רשימת רכיבים חסרה.",
    confidence: "partial",
    confidence_label_he: "חסרים נתוני רכיבים",
    confidence_tooltip_he:
      "רשימת הרכיבים לא הייתה זמינה — הציון מבוסס על נתוני התזונה בלבד.",
    confidence_sub_reason: "missing_ingredients",
    expansion: expansion({ ingredients: null, confidenceLabel: "נתונים חלקיים" }),
  },
  {
    id: "fx-4-thin-nutrition",
    name: "4 · חסרים נתוני תזונה (partial)",
    imageUrl: null,
    score: 71,
    grade: "B",
    insightLine: "לוח תזונה דק אך קיים.",
    confidence: "partial",
    confidence_label_he: "חסרים נתוני תזונה",
    confidence_tooltip_he:
      "חלק מנתוני התזונה לא היו זמינים — הציון מבוסס על הנתונים שכן היו זמינים.",
    confidence_sub_reason: "missing_nutrition",
    expansion: expansion({
      nutrition: {
        energyKcal: 250,
        protein: 9,
        sugar: null,
        fat: 12,
        satFat: null,
        fiber: null,
        sodium: null,
      },
      confidenceLabel: "נתונים חלקיים",
    }),
  },
  {
    id: "fx-5-inferred-category",
    name: "5 · קטגוריה משוערת (partial)",
    imageUrl: null,
    score: 52,
    grade: "C",
    insightLine: "הקטגוריה זוהתה באופן משוער.",
    confidence: "partial",
    confidence_label_he: "קטגוריה משוערת",
    confidence_tooltip_he:
      "הקטגוריה זוהתה באופן משוער. הציון עשוי להתעדכן כשיתווספו נתונים.",
    confidence_sub_reason: "inferred_category",
    expansion: expansion({ confidenceLabel: "נתונים חלקיים" }),
  },
  {
    id: "fx-6-low-extraction",
    name: "6 · נתונים בבדיקה (partial)",
    imageUrl: null,
    score: 64,
    grade: "C",
    insightLine: "OCR מתחת לסף — הנתונים בבדיקה.",
    confidence: "partial",
    confidence_label_he: "נתונים בבדיקה",
    confidence_tooltip_he:
      "חלק מהנתונים בבדיקה. הציון עשוי להתעדכן כשיתווספו נתונים מאומתים.",
    confidence_sub_reason: "low_extraction",
    expansion: expansion({ confidenceLabel: "נתונים חלקיים" }),
  },
  {
    id: "fx-7a-insufficient",
    name: "7a · טרם נוקד (insufficient — fully absent panel)",
    imageUrl: null,
    score: null,
    grade: null,
    insightLine: "המוצר נמצא על המדף — טרם התקבלו נתונים לניתוח.",
    confidence: "insufficient",
    confidence_label_he: "טרם נוקד",
    confidence_tooltip_he:
      "המוצר טרם נוקד — הנתונים לא היו זמינים לניתוח. הציון יתווסף כשיתווספו נתונים.",
    confidence_sub_reason: "no_panel",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "נתונים חסרים",
      servingNote: "",
    },
  },
  {
    id: "fx-7b-insufficient",
    name: "7b · טרם נוקד (insufficient — both absent)",
    imageUrl: null,
    score: null,
    grade: null,
    insightLine: "המוצר נמצא על המדף — טרם התקבלו נתונים לניתוח.",
    confidence: "insufficient",
    confidence_label_he: "טרם נוקד",
    confidence_tooltip_he:
      "המוצר טרם נוקד — הנתונים לא היו זמינים לניתוח. הציון יתווסף כשיתווספו נתונים.",
    confidence_sub_reason: "both_absent",
    expansion: {
      nutrition: null,
      ingredients: null,
      confidenceLabel: "נתונים חסרים",
      servingNote: "",
    },
  },
];

export default function ConfidencePreviewPage() {
  return (
    <main dir="rtl" className="mx-auto max-w-[420px] px-3 py-6">
      <h1 className="mb-1 text-lg font-extrabold text-[#111318]">
        תצוגת מצבי ביטחון (dev)
      </h1>
      <p className="mb-4 text-[12px] leading-relaxed text-[#6E756F]">
        7 מצבים — verified / partial (4 וריאציות) / insufficient. State 7 הוא fixture
        (אין מוצר חי insufficient). הקש על שורה לפתיחת ההרחבה ולתווית/טולטיפ המלאים.
      </p>
      <ComparisonTable
        products={FIXTURES}
        metricSpecs={[]}
        showRank={false}
      />
    </main>
  );
}
