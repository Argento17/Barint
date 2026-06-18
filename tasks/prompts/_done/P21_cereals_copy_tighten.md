P21 / TASK-254 — Cereals copy: one tightening pass (cheap lane, bounded)

CONTEXT: The cereals remediation draft passed the claim gate with 0 hard
failures (P17) and the orchestrator read it. Facts are clean. This pass fixes
TONE only — no facts, numbers, grades, or drivers change. After this pass the
file is re-gated, then integrated live.

FILE (edit in place, produce v2 alongside):
- Input:  02_products/breakfast_cereals/cereals_copy_remediation_draft_v1.json
- Output: 02_products/breakfast_cereals/cereals_copy_remediation_draft_v2.json
- Edit ONLY the `new_insightLine` and `new_rowVerdict` string fields. Touch
  nothing else — not badge, not trace_drivers_cited, not notes, not _meta.

DO:

1. DE-TEMPLATE THE SUGAR CLAUSE. ~18 D/E cards currently end the "why" with the
   identical phrase "...כי הסוכר גבוה ומחיל/מחילה/מחילים מגבלה על הציון". Two
   fixes:
   (a) KILL THE JARGON: "מחיל מגבלה על הציון" is engine-speak. Replace with plain
       consumer Hebrew that still names SUGAR as the driver. Allowed varied
       phrasings (rotate, don't reuse one): "הסוכר הגבוה מושך את הציון מטה",
       "רמת הסוכר היא מה שעוצר את הציון", "הסוכר הגבוה הוא הגורם המגביל",
       "הסוכר הגבוה קובע את הציון כאן", "הסוכר הגבוה הוא מה שמוריד".
   (b) VARY ACROSS CARDS: no two consecutive cards (by score order) may use the
       same phrasing. The reader scrolls these in a row.
   HARD CONSTRAINT: sugar must remain the named driver wherever the trace shows a
   sugar cap fired (ISRAELI_RED_LABEL_1_SUGAR / HIGH_SUGAR_25G_PLUS in
   trace_drivers_cited). Do NOT introduce any NEW driver, do NOT name sodium as a
   cause, do NOT change which factor is blamed.

2. THREE SPECIFIC NITS:
   - הרדוף (7290017325910): delete "נתוני חלבון וסיבים חלקיים" from new_rowVerdict.
     Protein (8g) and fiber (4g) exist — "partial" is misleading. Just end on the
     sodium fact.
   - ויטביקס (5010029000061): in new_rowVerdict, drop the defensive
     "לא תוצאת השלמה מלאכותית אלא" construction. State plainly why it stops at B
     (profile not yet at the category's A minimum). No reference to a prior error.
   - Any verdict that repeats "ל-100 גרם" 2–3 times: state the basis once, drop
     the repeats. Read naturally.

RULES (hard): no number, percentage, grade letter, calorie, or sodium value may
change. No new factual claim. No sodium/BHT/vitamin causation. No prior-run
references. Every claim must stay entailed exactly as v1 was — you are only
rephrasing the *why* clause and removing the 3 nits. If a rephrase would change
meaning, keep v1's wording.

RETURN BLOCK: v2 file path; count of cards whose sugar clause was reworded; confirm
no two consecutive-by-score cards share a phrasing; confirm the 3 nits fixed;
confirm zero numeric/grade changes (diff badge + numbers v1 vs v2 = identical).
Propose RETURNED. (Orchestrator then re-runs the claim gate before integration.)

---
After you send this to the agent: open tasks\DISPATCH_BOARD.md and put an `x` in
the P21 line under 📬 Signals.
