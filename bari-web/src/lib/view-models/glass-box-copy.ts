// TASK-179N — Glass Box D5/D6 code→Hebrew copy map (Content-owned strings).
//
// The pilot JSONs (hummus_frontend_v4 / maadanim_frontend_v2) emit the engine's D5/D6
// gate output in CODED form only — a `disclosureCodes: string[]` vocabulary plus the
// gate state. They carry NO prose. This module is the single place that maps each code
// to its calm, factual Hebrew line, and holds the shared labels (the `ניתוח חלקי` flag +
// tooltip, the `לא נוקד` chip + its canonical reason).
//
// It lives beside the View Model (lib/view-models) and is re-exported from the VM index
// so the canonical shared components can read it via `@/lib/view-models` only — never by
// reaching into lib/comparisons/ (legacy isolation policy).
//
// Source of truth for every string here: Content's FINAL sign-off copy,
//   C:\Bari\01_framework\glass_box\w1_disclosure_copy_v1.md  (TASK-179K).
// Register is binding (DEC-006): Q2 — disclosure, never accusation ("לא צוין"/"לא פורט",
// never "היצרן מסתיר"); Q4 — plain language only, no numbers, no engine terms. Any change
// to a consumer-facing line must route back through Content first.

import type { BariGlassBoxVM } from "./index";

// ─── Disclosure-gap codes (spec §1.2 vocabulary) → calm Hebrew line ──────────────
// Each line names WHAT the label did not state — never why, never an intent.
// Vocabulary emitted by Data: proportions | compound | generic_additive |
// protein_source | missing_field.
export const GLASS_BOX_DISCLOSURE_LINES: Record<string, string> = {
  // G1 — undisclosed ingredient proportions.
  proportions: "אחוזי הרכיבים לא צוינו בתווית.",
  // G2 — compound ingredient, no breakdown.
  compound: "חלק מהרכיבים המורכבים לא פורטו לגורמיהם.",
  // G4 — unidentified additive (generic class, no specific name / E-code).
  generic_additive: "חלק מהתוספים צוינו לפי קבוצה בלבד, ללא שם מדויק.",
  // G3 — unspecified protein source.
  protein_source: "מקור החלבון לא פורט במדויק.",
  // G5 — missing nutrition values.
  missing_field: "חלק מהערכים התזונתיים לא הופיעו בתווית.",
};

// ─── DEMOTE flag (beside the grade chip) ────────────────────────────────────────
export const GLASS_BOX_PARTIAL_LABEL = "ניתוח חלקי";
export const GLASS_BOX_PARTIAL_TOOLTIP =
  "הדירוג מבוסס על המידע שצוין בתווית. חלק מהפרטים לא פורטו.";

// ─── DEMOTE expansion section ───────────────────────────────────────────────────
export const GLASS_BOX_DISCLOSURE_HEADING = "מה לא צוין בתווית";

// ─── WITHHOLD chip + canonical reason ───────────────────────────────────────────
export const GLASS_BOX_WITHHOLD_LABEL = "לא נוקד";
export const GLASS_BOX_WITHHOLD_REASON =
  "אין מספיק מידע בתווית כדי לדרג את המוצר.";

// ─── D3 PROCESSING SIGNAL section heading (Glass Box W4, TASK-181I) ──────────────
// The calm drilldown label above the engine-emitted note_he line. The NOTE prose itself
// is NOT authored here — it is emitted verbatim by the engine (TASK-181G, spec §3.3,
// Product-co-signed). This is only the quiet section label, matching the "מה לא צוין
// בתווית" register: a neutral fact heading, never a verdict.
export const GLASS_BOX_PROCESSING_HEADING = "דפוס העיבוד";

/**
 * Resolve the ordered, de-duplicated plain-Hebrew disclosure lines for a demoted product.
 *
 * Source priority:
 *  1. coded `disclosureCodes` mapped through GLASS_BOX_DISCLOSURE_LINES (the live JSON path);
 *  2. the legacy prose fields `partialNote` / `disclosureNotes` (the self-contained
 *     /dev preview dataset, which authored prose directly).
 *
 * Unknown codes are skipped silently — a code with no approved Hebrew line is never
 * surfaced (fail-closed, never an engine token leak). Codes are mapped in their emitted
 * order; the canonical library order is not imposed.
 */
export function resolveDisclosureLines(glassBox: BariGlassBoxVM): string[] {
  const lines: string[] = [];
  const push = (line: string | null | undefined) => {
    const trimmed = line?.trim();
    if (trimmed && !lines.includes(trimmed)) lines.push(trimmed);
  };

  for (const code of glassBox.disclosureCodes ?? []) {
    push(GLASS_BOX_DISCLOSURE_LINES[code]);
  }

  // Legacy prose path (preview data only): used when no coded lines resolved.
  if (lines.length === 0) {
    push(glassBox.partialNote);
    for (const note of glassBox.disclosureNotes ?? []) push(note);
  }

  return lines;
}

/**
 * The canonical one-line reason a withheld product is unscored. Prefers an explicit
 * prose reason if one is present (preview data), otherwise the canonical Content string.
 */
export function resolveWithholdReason(glassBox?: BariGlassBoxVM): string {
  return glassBox?.withholdReason?.trim() || GLASS_BOX_WITHHOLD_REASON;
}
