// TASK-179I Wave 1 — Glass Box D5/D6 PREVIEW dataset (self-contained, NOT live).
//
// This is a flag-gated PREVIEW artifact so the owner can SEE the glass-box surface
// (a normal graded row, a `ניתוח חלקי` demoted row, a `לא נוקד` withheld row) before
// any go-live decision. It does NOT touch a live score or the published comparison JSON
// under src/data/comparisons/*.json — every product object below is authored here from
// the pilot engine output:
//   03_operations/bsip2/proto_v0/reports/glass_box/_pilot_{hummus,maadanim}_on.json
//   03_operations/bsip2/proto_v0/reports/glass_box/_pilot_summary.json
//
// The grade/score values shown are the pilot's OFF-baseline display values (what the
// product currently shows live); only the glass-box gate state + plain-language notes
// are the new D5/D6 presentation. Nothing here is wired back into the live datasets.
//
// Plain-Hebrew notes: the pilot's coded findings (proportions / missing_field /
// generic_additive / compound / protein_source) are translated to the calm, factual
// consumer phrasings from d5_d6_rule_spec_v1 §D5 / six_dimension_contract §3 (Q4 — no
// numbers, no engine terms; Q2 — "לא צוין" / "לא ניתן לאמת", never "היצרן מסתיר").

import type { BariProductVM } from "@/lib/view-models";

// Reusable placeholder expansion for the preview rows that are not the focus of a
// given card (keeps the rows realistic without fabricating nutrition we don't have).
function previewExpansion(
  partial: Partial<BariProductVM["expansion"]> = {}
): BariProductVM["expansion"] {
  return {
    nutrition: null,
    ingredients: null,
    confidenceLabel: "נתונים מלאים",
    servingNote: "ל-100 גרם",
    ...partial,
  };
}

// ─── HUMMUS preview (3 rows: normal A · normal B · withheld) ─────────────────────
// Withheld rows are the 4 plain חומוס / חומוס ענק SKUs from _pilot_summary (gate
// "withhold", d5_band "severe", panel absent). We show one as the representative.
export const glassBoxHummusPreview: BariProductVM[] = [
  {
    // Clean single-ingredient frozen chickpea — stays full grade (pilot: unconstrained).
    id: "preview_hummus_clean",
    name: "חומוס מוקפא — גרגרי חומוס",
    imageUrl: null,
    score: 85,
    grade: "A",
    insightLine:
      "מהבולטים במדף — גרגרי חומוס כרכיב יחיד. תווית שלמה, אין מה לדלל ואין מה להסתיר.",
    confidence: "verified",
    expansion: previewExpansion({
      nutrition: {
        energyKcal: 351,
        protein: 22,
        sugar: 3,
        fat: 4.5,
        fiber: 9.2,
        sodium: 23,
      },
      ingredients: "100% גרגרי חומוס",
      positiveSignals: [
        "רכיב יחיד — גרגרי חומוס בלבד",
        "חלבון גבוה לקטגוריה",
      ],
      limitingFactors: [],
    }),
    rowVerdict:
      "מהבולטים במדף — גרגרי חומוס כרכיב יחיד. תווית שלמה, אין מה לדלל ואין מה להסתיר.",
    glassBox: { gateState: "unconstrained" },
  },
  {
    // A normal graded spread with a real grade — shown for the side-by-side baseline.
    id: "preview_hummus_graded",
    name: "חומוס מסעדה",
    imageUrl: null,
    score: 72,
    grade: "B",
    insightLine:
      "ממרח סולידי — עוצר ב-B כי לצד החומוס יש מים ושמן שמדללים מעט את ההרכב.",
    confidence: "verified",
    expansion: previewExpansion({
      nutrition: {
        energyKcal: 280,
        protein: 7,
        sugar: 1,
        fat: null,
        fiber: 4,
        sodium: 410,
      },
      positiveSignals: ["רשימת רכיבים קצרה וברורה"],
      limitingFactors: ["מים ושמן מדללים את אחוז החומוס"],
    }),
    rowVerdict:
      "ממרח סולידי — עוצר ב-B כי לצד החומוס יש מים ושמן שמדללים מעט את ההרכב.",
    glassBox: { gateState: "unconstrained" },
  },
  {
    // WITHHELD — plain חומוס SKU, panel absent (_pilot_summary hummus withholds).
    id: "preview_hummus_withheld",
    name: "חומוס",
    imageUrl: null,
    score: null,
    grade: null,
    insightLine: "",
    confidence: "insufficient",
    expansion: previewExpansion({
      confidenceLabel: "נתונים חסרים",
    }),
    glassBox: {
      gateState: "withhold",
      withheld: true,
      disclosureCodes: [],
    },
  },
];

// ─── MAADANIM preview (3 rows: normal · demoted ג'לי · withheld) ─────────────────
export const glassBoxMaadanimPreview: BariProductVM[] = [
  {
    // A normal graded maadan — baseline.
    id: "preview_maadan_graded",
    name: "יופלה קלאסי",
    imageUrl: null,
    score: 69,
    grade: "B",
    insightLine:
      "מהטובים בקטגוריה — הרכב ברור עם חלבון סביר. עוצר ב-B בשל תוספת הסוכר.",
    confidence: "verified",
    expansion: previewExpansion({
      nutrition: {
        energyKcal: 95,
        protein: 3.5,
        sugar: 13,
        fat: 2.8,
        fiber: 0,
        sodium: 55,
      },
      positiveSignals: ["חלבון סביר לקטגוריה"],
      limitingFactors: ["תוספת סוכר ניכרת"],
    }),
    rowVerdict:
      "מהטובים בקטגוריה — הרכב ברור עם חלבון סביר. עוצר ב-B בשל תוספת הסוכר.",
    glassBox: { gateState: "unconstrained" },
  },
  {
    // DEMOTED — ג'לי בטעם ענבים (_pilot_summary maadanim demote, d5_band "partial",
    // findings: proportions + missing_field×5). Keeps its grade + `ניתוח חלקי` flag.
    id: "preview_maadan_demoted",
    name: "ג'לי בטעם ענבים",
    imageUrl: null,
    score: 35,
    grade: "E",
    insightLine: "",
    confidence: "partial",
    expansion: previewExpansion({
      confidenceLabel: "נתונים חלקיים",
      positiveSignals: [],
      limitingFactors: ["מבוסס ברובו על סוכר"],
    }),
    rowVerdict:
      "מבוסס ברובו על סוכר. הדירוג נשען על מידע חלקי — חלק מהפרטים לא צוינו בתווית.",
    // TASK-179N: exercise the LIVE coded path (disclosureCodes → Hebrew via the copy map),
    // the same shape the pilot JSONs emit — not authored prose.
    glassBox: {
      gateState: "demote",
      gatedScore: 35,
      gatedGrade: "E",
      disclosureCodes: ["proportions", "missing_field"],
    },
  },
  {
    // WITHHELD — a maadan with no usable panel (_pilot_summary maadanim withhold,
    // e.g. בולגרית מעודנת / המבורגר ילדים, panel absent → `לא נוקד`).
    id: "preview_maadan_withheld",
    name: "בולגרית מעודנת 24%",
    imageUrl: null,
    score: null,
    grade: null,
    insightLine: "",
    confidence: "insufficient",
    expansion: previewExpansion({
      confidenceLabel: "נתונים חסרים",
    }),
    glassBox: {
      gateState: "withhold",
      withheld: true,
      disclosureCodes: [],
    },
  },
];

// ─── W4 D3 PROCESSING preview (3 rows: NOVA-1 positive · NOVA 3–4 hedged · low-conf) ──
// TASK-181I. The three note_he strings below are the FINAL, Product-co-signed approved
// wording from d3_demoralization_spec_v1.md §3.3 (lines 466–475) — the same strings the
// engine (TASK-181G) emits verbatim. They are NOT authored or paraphrased here; this is a
// flag-gated PREVIEW so the owner can SEE the D3 surface before any go-live. No live score
// or published JSON is touched. The d3_processing object is read only when GLASSBOX_W4_ON.
//
// Candidate A (NOVA 1, high confidence, positive):
const D3_NOTE_A =
  "מוצר בעיבוד מינימלי — דפוס ההרכב שלו מתאם, במחקרים גדולים על אוכלוסיות רבות, עם תוצאות תזונתיות חיוביות.";
// Candidate B (NOVA 3–4, medium/high confidence, negative, hedged):
const D3_NOTE_B =
  "דפוס הרכב זה מתאם, במחקרים גדולים על אוכלוסיות רבות, עם צריכה תזונתית גבוהה יותר של סוכר, שומן ונתרן — לא אמירה על מוצר זה בפני עצמו.";
// Candidate C full form (low confidence, any class):
const D3_NOTE_C_FULL =
  "הרכב המוצר לא פורט במלואו — לא ניתן להעריך את דפוס העיבוד בביטחון. האומדן הנוכחי הוא זמני.";
// Candidate C mobile-compressed variant:
const D3_NOTE_C_MOBILE =
  "הרכב המוצר לא פורט במלואו — האומדן לדפוס העיבוד הוא זמני.";

export const glassBoxProcessingPreview: BariProductVM[] = [
  {
    // NOVA-1, high confidence → Candidate A (positive). A clean single-ingredient product.
    id: "preview_d3_nova1",
    name: "שיבולת שועל מלאה",
    imageUrl: null,
    score: 88,
    grade: "A",
    insightLine: "רכיב יחיד, בעיבוד מינימלי — מהבולטים במדף.",
    confidence: "verified",
    expansion: previewExpansion({
      ingredients: "100% שיבולת שועל מלאה",
      positiveSignals: ["רכיב יחיד, בעיבוד מינימלי"],
    }),
    rowVerdict: "רכיב יחיד, בעיבוד מינימלי — מהבולטים במדף.",
    d3_processing: {
      nova_class: 1,
      confidence: "high",
      note_he: D3_NOTE_A,
    },
  },
  {
    // NOVA 3–4, high confidence → Candidate B (negative, hedged "לא אמירה על מוצר זה").
    id: "preview_d3_nova4",
    name: "חטיף תירס בטעם גבינה",
    imageUrl: null,
    score: 44,
    grade: "D",
    insightLine: "דפוס הרכב מהונדס — עוצר נמוך בשל סוכר, שומן ונתרן.",
    confidence: "verified",
    expansion: previewExpansion({
      positiveSignals: [],
      limitingFactors: ["סוכר, שומן ונתרן גבוהים"],
    }),
    rowVerdict: "דפוס הרכב מהונדס — עוצר נמוך בשל סוכר, שומן ונתרן.",
    d3_processing: {
      nova_class: 4,
      confidence: "high",
      note_he: D3_NOTE_B,
    },
  },
  {
    // Low confidence → Candidate C (provisional). Full form on desktop, compressed on mobile.
    id: "preview_d3_lowconf",
    name: "מוצר מעובד — תווית חלקית",
    imageUrl: null,
    score: 58,
    grade: "C",
    insightLine: "ההרכב לא פורט במלואו — האומדן זמני.",
    confidence: "partial",
    expansion: previewExpansion({
      confidenceLabel: "נתונים חלקיים",
    }),
    rowVerdict: "ההרכב לא פורט במלואו — האומדן לדפוס העיבוד זמני.",
    d3_processing: {
      nova_class: 3,
      confidence: "low",
      note_he: D3_NOTE_C_FULL,
      note_he_mobile: D3_NOTE_C_MOBILE,
    },
  },
];
