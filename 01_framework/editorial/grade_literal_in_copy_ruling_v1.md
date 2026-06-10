# Editorial Ruling — Grade Literals, Rescore Narration, and the Verified Tooltip in Consumer Copy

**Doc ID:** `grade_literal_in_copy_ruling_v1`
**Date:** 2026-06-10
**Author:** Content Agent
**Status:** RULING (policy adjudication for TASK-233C; feeds TASK-233B)
**Scope:** Reviewer pass for the TASK-233 confirmation sweep. Adjudicates the three editorial
questions in `reports/task_233_confirmation_sweep.md` §2 (QA-001..004), §4, and §6.1.
**Mode:** Policy ruling only. No product copy rewritten, no JSON changed in this pass.

This is a binding editorial ruling, not a menu. One decision per question, with the governing
standard cited. Implementation (the actual string edits) is TASK-233C/233B work, owned by Content +
Data, and must clear Nutrition (accuracy) + Product (positioning) sign-off before Frontend
integration per the publication rule.

---

## Decision 1 — Grade literals (`NN/X`) in consumer prose: **BANNED**

### Ruling

The literal composite score-with-grade token — `90/A`, `70/B:`, `82/A`, `55/C`, `56/C` — **must
not appear inside consumer prose** (insightLine, rowVerdict, bottomLine, comparisonContext, hero,
prologue, methodology). It is banned **even when the score chip already shows the same value.**
The chip already showing it is not a defense; it is the reason. Repeating the chip's value in the
sentence is at best redundant and at worst converts a *displayed finding* into a *narrated verdict*.

### Governing standard

**`score_presentation_v1.md` Rule 1 (Primary Display) governs, and it is decisive.**

> "Format: `[score] / [grade]`. Nothing else at this level. No label. No descriptor."

Rule 1 establishes exactly one consumer-facing home for the `NN/X` token: the primary score
display (the chip). The presentation philosophy treats the numeral+grade as a *structured display
object*, deliberately stripped of sentiment, shown once. The moment the same token is re-embedded
in a sentence it stops being a neutral range marker and becomes prose that asserts a verdict — the
precise drift Rule 1 exists to prevent. `score_presentation_v1.md` also states its own precedence:
"Score display rules take precedence when there is a conflict on label use." So where the verdict
model and the presentation philosophy appear to collide, **presentation wins.**

This is reinforced, not contradicted, by the other standards:

- **`insight_line_spec_v1` — Anti-pattern rule (2026-06-08, juices).** "An insight line must say
  something the column values don't... does this say something the visible metrics columns already
  show? — if yes, cut the redundant part." The score chip *is* a visible metric column. `90/A` in
  the insightLine is the textbook redundancy this rule already bans. The frozen_vegetables line
  `"קטניה קפואה טבעית — 90/A. רכיב בודד ללא תוספות, ציון מלא לקטגוריה."` fails this test directly.
- **`assertive_writing_v1` — Assertive Score Explanation.** The standard demands the explanation
  name "a specific ingredient, position, or value (observable signal → score effect)." It rewards
  *causal substance* ("רכיב בודד ללא תוספות"), never the bare numeral. The numeral adds no signal;
  the driver does.
- **`bari_editorial_intelligence` — framework invisibility / "Bari describes, never prescribes."**
  A literal `NN/X` glued into a sentence reads as the writer pronouncing a grade, edging toward the
  recommendation posture the whole editorial OS forbids.

### Reconciling `comparison_row_verdict_model` ("verdict ends on grade")

The verdict model is **not overridden — it is read correctly.** "Ends on grade" means the verdict
**lands on the earned standing and names *why* it stops there** — the canonical pattern is
`"עוצר ב-B כי…"` (stops at B because…), i.e. the *grade letter as a word in a causal clause*, not
the `NN/X` mechanic literal. The grade letter spoken in prose ("עוצר ב-B", "ציון מלא לקטגוריה") is
fine and intended. The composite *score number* (`78`, `90`, `55`) and the slashed mechanic form
(`NN/X`) are the chip's job. So:

- ALLOWED in prose: the grade *letter* in a reasoned clause — "עוצר ב-B כי מועשר בוויטמינים",
  "ציון מלא לקטגוריה" (qualitative standing, no numeral).
- BANNED in prose: the numeric score and the `NN/X` mechanic token — `90/A`, `78/B`, `55/C`.

The cereals verdict already demonstrates the correct ending ("עוצר ב-B כי…"); its violation is the
*earlier* `78/B … 55/C` clause (see Decision 2), not its closing.

### Are QA-001 / QA-002 / QA-004 launch blockers?

- **QA-001 (frozen_vegetables, 53×) — YES, blocker for this category's go-live.** Frozen_vegetables
  is still on a preview branch (pre-merge), so the literal must be stripped before merge. It is
  already on hold for the confidence contradiction (DA-005/006); fold the literal strip into the
  same pre-merge fix. No emergency to production because it is not live.
- **QA-002 (snacks) / QA-004 (bread) — confirmed defects, but NOT emergency-pause.** These are
  already live and the literal is a *pre-existing style on the oldest categories*, not a regression.
  Per the sweep §5, do not emergency-pause live pages over a style finding. Schedule the strip as
  standard TASK-233C remediation and route through the leak gate (TASK-233A) so it cannot recur.
  Severity: HIGH, not CRITICAL-emergency.
- Net: **the literal is banned everywhere; frozen_vegetables blocks at merge; live categories are
  remediated on the normal track, not paused.**

### Replacement pattern (describe standing/why without the numeral)

Drop the `NN/X` token; keep the chip carrying the number; let the prose carry the *driver and the
standing*. Pattern: **[what it is] + [the real driver] + [where it stands / why it stops].**

| BANNED (current) | REPLACEMENT (numeral removed, signal kept) |
|---|---|
| `קטניה קפואה טבעית — 90/A. רכיב בודד ללא תוספות, ציון מלא לקטגוריה.` | `קטניה קפואה, רכיב בודד ללא תוספות. ציון מלא לקטגוריה.` |
| `70/B: …` (snacks bottomLine) | open on the driver, e.g. `מוביל הקטגוריה — אך עוצר ב-B כי…` |
| `…ציון 82/A על בסיס מחמצת.` (bread) | `מחמצת אמיתית בלי שמרים תעשייתיים — מה שמעמיד אותו בראש הקטגוריה.` |

Note: the frozen_vegetables line also carries an em-dash **plus** the literal; removing the literal
and rephrasing also resolves the connector-dash style. The grade *letter* in a causal "עוצר ב-X כי"
clause remains the approved verdict ending.

---

## Decision 2 — Cereals rescore-history narration: **REMOVE, unconditionally**

### Ruling

The clause on `bsip1_cereal_5010029000061` and `5900020012814` —
`"…78/B בגרסה הקודמת עקב תקלת נתונים; הציון המתוקן הוא 55/C…"` ("78/B in the previous version due to
a data error; corrected to 55/C") — **must be removed and re-authored.** This is independent of and
prior to Decision 1: it would be a defect even if grade literals were permitted, because the
violation is not the numeral — it is the **narration of the pipeline's own history.**

### The principle

**No rescore, version, recalibration, "previous score," "data error/correction," or any pipeline
internal may appear in consumer copy.** The consumer sees the *current finding*, never the
machinery that produced it, and never the system's account of its own past mistakes. Disclosing
"the previous version was wrong" does three forbidden things at once: it exposes pipeline internals
(framework-invisibility breach), it narrates a versioning/rescore event (a system-internal that has
no consumer meaning), and it advertises that Bari published an incorrect score — directly
undermining the trust posture. The score on screen *is* the finding; its provenance is internal.

This is a clean defect under **`bari_editorial_intelligence` (framework invisibility)** and the
Hard Rule "never use framework / pipeline vocabulary in consumer-facing output." Fast-track per
sweep §5, ahead of and separate from the Decision 1 style remediation.

### Replacement

Re-author the verdict on the *current* truth only — composition, real drivers, standing — with the
existing approved ending. The strong parts of the line already comply ("95% חיטה, הרכב פשוט,
12 גרם חלבון ו-10 גרם סיבים… עוצר ב-B כי מועשר בוויטמינים… ו-342 קלוריות"). Excise the middle
rescore clause and the `78/B … 55/C` numerals entirely; keep the composition facts and the
"עוצר ב-B כי…" close. The "20 נקודות" gap-to-leader phrasing is also a raw score mechanic and should
be reworded to a qualitative standing ("הפער מ-ויטביקס ניכר") rather than a numeric point spread.

---

## Decision 3 — Verified-confidence tooltip wording: canonical line + retire the overclaim

### Ruling

**(a) Canonical wording for the verified state is:**

> `הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים`
> ("the score is based on the complete ingredient list and nutrition panel")

This is the variant already used by every other category (74× across the corpus) and it correctly
describes *what was available* (the complete label data) without asserting *where it came from*.

**(b) `כל נתוני התזונה והרכיבים היו זמינים ממקור המזון הרשמי` ("…available from the official food
source") is an inaccurate overclaim and must be retired.** It ships 53× in frozen_vegetables only
(a non-canonical variant) and it is wrong on the facts: the file's own `_meta.provenance` reads
`"Shufersal scrape (scope-clean v2_1)"` — a **retailer scrape**, not an official/authoritative food
source. Calling a supermarket scrape "the official food source" is a provenance claim Bari cannot
substantiate.

### Governing standard

**`assertive_writing_v1` — Confidence Map (Layer 1 = observation, full confidence only on what is
directly observed) + the No-Overclaim posture; reinforced by Hard Rule 2 (no claim without accuracy
sign-off) and the data-integrity rule (never assert provenance you don't have).** Bari may state
with full confidence *what data it read* ("the complete ingredient list and nutrition panel"). It
may **not** assert the *authority/source class* of that data ("official food source") when the
provenance record says otherwise. The canonical line stays inside Layer 1 (observation of data
completeness); the frozen_vegetables variant crosses into an unverifiable Layer 2 source-authority
claim.

Two compounding problems, both already flagged in the sweep, make retirement mandatory rather than
cosmetic:

1. **Accuracy:** "official source" contradicts `_meta.provenance` (Shufersal scrape). This is the
   overclaim. Retire it on accuracy grounds alone.
2. **Internal contradiction (DA-005/006):** all 53 products carry the verified "full data" framing
   *while listing data-gap `unknowns`* (missing fiber / saturated fat). A "based on complete data"
   tooltip riding on products with admitted gaps is indefensible. The wording fix (this ruling) and
   the confidence re-derivation (TASK-233B/233D, Data + Nutrition) must land together — swapping the
   wording without re-deriving confidence would still leave a "complete data" claim on incomplete
   products. **Wording is Content's call (ruled here); the verified-vs-partial state is Nutrition's
   accuracy call (TASK-233B).**

This wording decision feeds **TASK-233B** (canonical tooltip adopted system-wide) with the interim
re-derivation in **TASK-233D**.

---

## Summary of governing standards

| Question | Ruling | Governing standard |
|---|---|---|
| Grade literal `NN/X` in prose | BANNED everywhere (chip is the only home) | `score_presentation_v1` Rule 1 (precedence on label/score display) + `insight_line_spec_v1` anti-redundancy rule |
| "Verdict ends on grade" conflict | No conflict — grade *letter* in a causal clause is allowed; the *numeral/`NN/X` mechanic* is not | `comparison_row_verdict_model` read against `score_presentation_v1` Rule 1 |
| Cereals rescore narration | REMOVE unconditionally (prior to and independent of grade-literal ruling) | `bari_editorial_intelligence` framework invisibility + Hard Rule on pipeline vocabulary |
| Canonical verified tooltip | `הציון מבוסס על רשימת הרכיבים ולוח התזונה המלאים` | corpus convention (74×) + `assertive_writing_v1` Confidence Map Layer 1 |
| "ממקור המזון הרשמי" | RETIRE — inaccurate provenance overclaim | `assertive_writing_v1` no-overclaim + Hard Rule 2 (accuracy sign-off) + `_meta.provenance` evidence |

## Decision-rights note

All three are expert calls inside the Content lane (editorial policy on consumer copy) and trip no
strategic tripwire — published *scores* and scoring philosophy are untouched; this rules only on the
*words around* the scores. Decided and documented here. Implementation copy edits remain gated by
Nutrition (accuracy) + Product (positioning) before Frontend integration, per the standing
publication rule.
