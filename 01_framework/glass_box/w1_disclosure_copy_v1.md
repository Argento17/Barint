**Task:** TASK-179K

# Bari Glass Box — D5/D6 Consumer Disclosure Copy (FINAL, v1)

**Author:** Content Agent · **Date:** 2026-06-04 · **Wave:** TASK-179, Wave 1 (editorial sign-off)
**Status:** FINAL WORDING — editorial sign-off on the consumer-facing strings for the D5 (DEMOTE)
and D6 (WITHHOLD) glass-box states. Presentation copy only; no score, threshold, or engine
behavior is defined or changed here. Ships behind `BARI_GLASSBOX_D5D6` (default OFF) with the rest
of the wave. **RETURNED** for Nutrition (accuracy) + Product (positioning) co-sign before any
go-live; Frontend integrates the approved strings.

**Reads-first:**
- `d5_d6_rule_spec_v1.md` §1.2 (the five disclosure-gap types) — the source of WHAT each line names.
- `six_dimension_contract_v1.md` §5.0 (DEC-006 Q2/Q4) — the binding register rules.
- Existing comparison-page voice: `hummus-comparison-page-data.ts`, `maadanim-page-data.ts`
  (calm, declarative, "רשימת הרכיבים / הערכים התזונתיים", no jargon).

---

## Register rules honored (DEC-006, binding)

- **Q2 — disclosure, never accusation.** Opacity is a confidence/disclosure *condition*. Use
  **"לא צוין" / "לא ניתן לאמת" / "לא פורט"**. **NEVER** "היצרן מסתיר", never any implication that the
  maker concealed something or that the product is unhealthy. The grade is unchanged by these notes.
- **Q4 — plain language only.** No numbers, no engine/internal terms (no "D5", "band", "confidence",
  "ceiling", "additive class"). A shopper-in-a-supermarket reads these, not a data analyst.
- **Voice.** Calm, factual, short, mobile-readable. Consistent with the existing comparison pages.
  No exclamation, no ALL CAPS, RTL phrasing, ends with a full stop.

---

## 1. The DEMOTE flag (beside the grade chip)

The grade still shows; a small muted-gold pill sits next to it.

| Item | FINAL string | Render context |
|---|---|---|
| Flag label | **`ניתוח חלקי`** | inline 10px pill, `glass-box-flag.tsx` `PARTIAL_LABEL` |
| Flag tooltip (optional, on tap/hover) | **`הדירוג מבוסס על המידע שצוין בתווית. חלק מהפרטים לא פורטו.`** | one line; see §4 placement note |

Notes: `ניתוח חלקי` is **approved as-is** — two words, calm, fits the pill, says exactly what it is
(a partial analysis), not an accusation. The tooltip is **new** (no draft existed); it states the
condition in one breath and is the consumer-facing one-liner of "the grade stands; some detail was
not stated." It deliberately avoids "חסר" (which reads as a fault) in favor of "לא פורטו".

---

## 2. The WITHHOLD chip + reason

`לא נוקד` shows where the grade chip would be (neutral box, no number, no error color); the
expansion leads with a one-line reason.

| Item | FINAL string | Render context |
|---|---|---|
| Withhold chip label | **`לא נוקד`** | grade-cell box, `comparison-row.tsx` (`labelText`) |
| Withhold reason (one line) | **`אין מספיק מידע בתווית כדי לדרג את המוצר.`** | leads the expansion, `expansion-section.tsx` |

Notes: `לא נוקד` is **approved as-is** — it already matches the snack page's `insufficient` chip
(`snack-page-data.ts`), so it reads as a known, neutral state, not a new alarm. The reason is the
existing preview-data string, **approved as canonical**. See §3 for the de-dup fix.

---

## 3. The expansion disclosure section (DEMOTE)

The "what wasn't stated" block inside a demoted product's expansion.

| Item | FINAL string | Render context |
|---|---|---|
| Section heading | **`מה לא צוין בתווית`** | `expansion-section.tsx` `LABEL_DISCLOSURE` |

**One calm line per disclosure-gap type** (spec §1.2). One sentence, no number, names *what*
was not stated, never *why* and never an intent:

| Gap type (spec §1.2) | FINAL Hebrew line |
|---|---|
| **G1 — undisclosed proportions** | **`אחוזי הרכיבים לא צוינו בתווית.`** |
| **G2 — compound ingredient, no breakdown** | **`חלק מהרכיבים המורכבים לא פורטו לגורמיהם.`** |
| **G4 — unidentified additive (generic class, no name/E-code)** | **`חלק מהתוספים צוינו לפי קבוצה בלבד, ללא שם מדויק.`** |
| **G3 — unspecified protein source** | **`מקור החלבון לא פורט במדויק.`** |
| **G5 — missing nutrition values** | **`חלק מהערכים התזונתיים לא הופיעו בתווית.`** |

These are a **library** — only the lines whose gap actually fired are shown for a given product
(Frontend already renders `disclosureNotes[]` as a list). Keep each product to the gaps the engine
actually found; do not show the whole list on every row.

---

## 4. Diffs from the existing drafts (what I changed and why)

| Location | Draft string | FINAL | Why |
|---|---|---|---|
| `expansion-section.tsx` withhold fallback (L411) | `אין מספיק נתונים לאריזה זו כדי להציג פירוט.` | `אין מספיק מידע בתווית כדי לדרג את המוצר.` | **Unify** the withhold reason to one canonical sentence. The shopper should read the *same* reason whether it comes from the data or the fallback. "מידע בתווית… כדי לדרג" is more precise than "נתונים… להציג פירוט" and ties the reason to the label, not to our pipeline. |
| New | (none) | flag tooltip `הדירוג מבוסס על המידע שצוין בתווית. חלק מהפרטים לא פורטו.` | A one-liner was requested; none existed. Explains the pill in plain words without a number. |
| New (G2) | (none) | `חלק מהרכיבים המורכבים לא פורטו לגורמיהם.` | No draft existed for the compound-ingredient gap. "מורכבים … לגורמיהם" = a compound item not broken into its parts; plain, no intent. |
| New (G4) | partial precedent `רכיב לא זוהה בתווית` | `חלק מהתוספים צוינו לפי קבוצה בלבד, ללא שם מדויק.` | "רכיב לא זוהה" is ambiguous (sounds like *we* failed to identify it). The final names the real condition: an additive given by its **class** (e.g. "מייצב") with no specific name — factual, Q2-clean. |
| New (G3) | (none) | `מקור החלבון לא פורט במדויק.` | No draft existed. Mirrors the hummus page's "מקור החלבון" phrasing for cross-page consistency. |
| `glass-box-preview-data.ts` G1/G5 lines | `אחוזי הרכיבים לא צוינו בתווית.` · `חלק מהערכים התזונתיים לא הופיעו בתווית.` | **unchanged** | Already correct in voice and register. Approved as-is. |
| `glass-box-flag.tsx` label | `ניתוח חלקי` | **unchanged** | Approved as-is. |
| `comparison-row.tsx` chip | `לא נוקד` | **unchanged** | Approved as-is; matches existing snack page. |
| `expansion-section.tsx` heading | `מה לא צוין בתווית` | **unchanged** | Approved as-is. |

**Endemic flavorings (spec §1.4):** the spec excludes bare `חומרי טעם וריח` from the band and from
D6, so by design it does **not** trigger a demote line. If Product later decides to *surface* it as a
neutral note (not a demote), the approved calm phrasing is **`הרכב הטעמים לא פורט בתווית.`** — held in
reserve, not wired now.

---

## 5. Length / placement recommendations for Design + Frontend

1. **Flag tooltip** — the pill itself shows only `ניתוח חלקי`. The tooltip line is ~7 words; on
   mobile a tap-to-reveal (not hover) is needed. If a tooltip surface isn't available on the row,
   the same sentence can live as the **first** line of the expansion disclosure section instead.
   Design call on the surface; the words don't change.
2. **G4 line length** — `חלק מהתוספים צוינו לפי קבוצה בלבד, ללא שם מדויק.` is the longest line (~8
   words). It wraps to two lines in the 12px `NoteList` on a 280px width. That's acceptable (the list
   already wraps), but flag for Design if a single-line fit is wanted — a shorter variant
   `חלק מהתוספים צוינו לפי קבוצה בלבד.` is approved as a fallback if length is a problem.
3. **Withhold reason unification** — the fallback string in `expansion-section.tsx` L411 should be
   updated to the canonical reason (§4). One-line Frontend edit; no logic change.
4. **No line carries a number** — confirmed across all strings (Q4). If any future engine-derived
   note tries to inject a count or field name, it must route back through Content first.

---

## 6. Return summary

- **File:** `C:\Bari\01_framework\glass_box\w1_disclosure_copy_v1.md`
- **Approved as-is:** `ניתוח חלקי` flag · `לא נוקד` chip · `מה לא צוין בתווית` heading · the G1 and
  G5 preview lines · the withhold reason `אין מספיק מידע בתווית כדי לדרג את המוצר.`
- **New/changed (need co-sign):** flag tooltip; G2/G3/G4 lines; the withhold-fallback unification.
- **All strings checked:** Q2 (no accusation/intent), Q4 (no number, no engine term), RTL, calm,
  mobile-readable. Leakage check: no NOVA/BSIP/cap/floor/dimension/confidence-term in any consumer line.

*End of disclosure copy v1. Editorial sign-off pending Nutrition + Product co-sign.*
