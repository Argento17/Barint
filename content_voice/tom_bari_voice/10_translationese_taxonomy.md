# 10 — Translationese Taxonomy (Tom / Bari Hebrew) · v0.1

**Status: v0.1 — Phase 0 baseline of Project Tom's Voice (TASK-374).**
Built 2026-06-22 from **12 owner-labeled live examples** (cereals + chocolate-tablet
shelves) + **2 owner rewrites that "really work"** (protein bars). This is the
catalogue of *naturalness* failures — Hebrew that is grammatically clean,
leakage-clean, and passes every existing gate, but still reads translated/stilted.

**Why this file exists:** none of the failures below trip any current gate
(`5_banned_phrases_and_claims.md`, the 4 NLP gates, or the 8 hard-fails in
`7_voice_match_gate.md`). They are exactly the gap the Naturalness Gate (Phase 1)
must catch. This taxonomy is the gate's calibration target.

> Transcription note: Hebrew read from owner screenshots. Owner-quoted phrases are
> verified; fuller line transcriptions are best-read and may carry minor errors —
> confirm against the source JSON before promoting any pair to `3_before_after_pairs.md`.

---

## The meta-finding (owner, 2026-06-22)
**The closer / "finish line" is the systematic failure zone.** Across the cereals
shelf the body copy is acceptable but the closing beat (`הקשר במדף`) reliably
collapses into T1/T3 calques. The Naturalness Gate must weight the final beat
hardest, and the fingerprint's closer guidance needs repair.

---

## The tells

### T1 — The "X, לא Y" contrastive — the #1 tell
A direct calque of English "it's X, not Y." Owner flags it repeatedly and deletes
it on sight in his own rewrites.

| # | Failing | Owner fix / natural form |
|---|---|---|
| #27 | `ממתק ממולא בטעם נוגט-דבש, לא טבלת קקאו` | `מדובר בסך הכל בממתק נוגט דבש` |
| #3 | `הפסד בגלל הממתיק, לא בגלל הבסיס` | (recast; drop the contrast — see T7 `הפסד`) |
| #5 | `זו התמונה הכוללת — לא רכיב אחד` | (referent unclear; recast as a positive declarative) |
| protein | `המתיקות באה ממזון שלם ולא ממלטיטול` | `המתיקות אינה מגיעה ממלטיטול` |
| protein | `זה הטוב במדף מהונדס, לא מזון חזק` | **deleted entirely** |

**Rule:** resolve a contrast with `מדובר בסך הכל ב…`, `עדיין`, or a plain positive —
never the bare `X, לא Y` parallel. Owner deletes the X-not-Y closer every time.

### T2 — "X לא תמיד אומר Y" — a calque currently blessed as a signature move
`נקי לא תמיד אומר חזק` (#2). Calque of "X doesn't always mean Y." **This sits in
`2_voice_fingerprint.md` §3 and `4_approved_phrases.md` §C as a workhorse move** —
owner's flag means a blessed move is itself translationese. Pending owner ruling:
retire or repair (natural: `מוצר נקי הוא לא בהכרח מוצר חזק`).

### T3 — Dangling `גם` / staccato fragment finish
`הפקאן שם. הסוכר גם` (#1), `כאן הוא גם לא הסיפור` (#4). Ending on `גם` mimics
English trailing "…too." — flat/incomplete in Hebrew. Primary driver of the weak
closer meta-finding.

### T4 — Calqued metaphors
`המחיר שלו ברור` (#6 — reads as literal price), `נושאים את החלבון` (protein original
→ owner: `החלבון... מקורו מ…`), `עוצרים אותו בציון D` (#2), `נתרן נמוך מאוד לזכותו`
(#10, "to its credit"). Hebrew does not carry these English figures naturally.

### T5 — Passive nominalization
`הבחירה שנעשתה היא להוסיף` (#6, "the choice that was made is to add" → `בחרו להוסיף`),
`סוכר שמוסף` (#3 → `סוכר מוסף`). The hallmark LLM-Hebrew register.

### T6 — Untranslated English loanword
`מילק` (#9) → `שוקולד חלב`.

### T7 — Wrong-register single words / compressions
`הפסד` (#3, sports/gambling register), `סיבים יפים` (protein original → `עשיר בסיבים`),
`דבש בשם, 4% דבש בפועל` (#4, calqued "honey in name, X in practice" compression).

---

## What "good" looks like (owner-validated calibration)

**#1 chocolate (kept as good):**
> `זה הצד הכי קרוב-לקפאה שיש כאן על המדף. … הקאץ' הוא הטעם: 90% מריר זה לא לכל חך, וזה עדיין מוצר עתיר שומן וקלוריות.`

Why it works: connected clauses (not staccato), a colloquial anchor (`הקאץ'`),
numbers integrated into sentences, contrast resolved with `עדיין` not X-not-Y.

**Protein-bar rewrite (owner):** plain sourcing (`החלבון במוצר מקורו מאגוזי לוז ושקדים`),
glossed jargon (`גליצרול (חומר משמר וממתיק)`), discourse connectors (`כלומר`, `וכן`),
X-not-Y deletions, weak closer deleted.

---

## RESOLVED (owner, 2026-06-22)
1. **Structure signal — RESOLVED: editing shorthand, keep prose.** The owner's
   יתרון/חיסרון labels in the protein rewrites were quick-edit shorthand, not a
   format direction. Final copy stays flowing prose (the #1-chocolate model). No
   frontend/design change. The *value* in the rewrites is the phrasing (T1/T4/T7
   deletions, jargon gloss, discourse connectors) — not the layout.
2. **T2 signature move — RESOLVED: repair the phrasing.** `X לא תמיד אומר Y` is
   repaired to **`X הוא לא בהכרח Y`** (e.g. `מוצר נקי הוא לא בהכרח מוצר חזק`).
   Applied to `2_voice_fingerprint.md` §2/§3 and `4_approved_phrases.md` §C
   (2026-06-22); logged in `8_edit_feedback_log.md`.

---

## Promotion path
Once transcriptions are confirmed: promote verified pairs into
`3_before_after_pairs.md`, add T1–T7 as a syntax sub-blacklist in
`5_banned_phrases_and_claims.md` (Phase 2), and encode T1–T7 + the closer
meta-finding as the Naturalness Gate's scoring rubric (Phase 1).
