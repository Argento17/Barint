# Adversarial QA / Red-Team — Magnesium Guide Content Gate-2 (TASK-504 Wave 1)

**Date:** 2026-07-05 · **Gate:** ELEVATED (supplement / health-adjacent) · **Challenger:** adversarial-qa-agent
**Target (integrated):** `C:\bari_wt_t504\bari-web\src\lib\guides\magnesium-guide-data.ts`
**Instrument:** `integrations\clients\hebrew_readability.py::analyze().is_clean` (run per-field, not eyeballed)
**Supersedes for the tier track:** `magnesium_guide_tier_copy_redteam_v2.md` (verdict of record NO-GO / RT-8).

This is the persisted two-gate (Content + Adversarial QA) sign-off record. Data-file comments must
cite THIS artifact rather than "this task's return."

---

## Verdicts

| Component | Verdict | Basis |
|---|---|---|
| **Tier copy (re-gate RT-8)** | **GO** | RT-8 + RT-6 resolved; 11/11 tier strings `is_clean=True` |
| **Full-body copy (fresh gate-2)** | **GO** | RT-9 resolved (3/3 reworded strings `is_clean=True`); Wave-0 must-fixes PASS; grammar flag = non-blocking false-positive |
| **Gate-status comment audit** | **CORRECTIONS LISTED** | 6 comments cite "this task's return" → repoint to this file; 1 stale "body[3] UNCHANGED" |

Page-level go-live is **still gated by** the standing non-blocking monitors RT-5 (EXCEPTION-003 carve-out
unwired in `hebrew_readability.py`) and RT-7 (disclosure-adjacency), both frontend/gate-owner code items,
plus RT-10/11/12 below. No open CRITICAL.

---

## RT-9 — RESOLVED (was the full-body blocker)

Content dropped the substring "מומלץ" from the 3 flagged consumer strings; meaning + UL numbers preserved.
Re-run of `analyze().is_clean`:

| String | Line | Before | After | is_clean |
|---|---|---|---|---|
| headlineFinding.body[3] (Supherb) | 491 | "…שמומלץ לתשומת לב…" | "…**המצריך** תשומת לב…" | **True** |
| educationSpine "בטיחות" | 594 | "הסף העליון **המומלץ**…" | "הסף העליון **שנקבע**…" | **True** |
| educationSpine "מינון ובטיחות" | 621 | "הסף העליון **המומלץ**…" | "הסף העליון **שנקבע**…" | **True** |

Safety semantics survive on 594 + 621 (asserted programmatically): 350 mg/day (IOM/NASEM) hard line;
250 mg/day soft line; SCF 2001 + EFSA 2015 reaffirmation; NO "2021"; GI-tolerance-not-toxicity framing
("אין כאן רעילות" / "שלשול קל, זמני"). All other body strings (18 oneLinerHe, 6 buyingRule, headline
title/body[0-2,4-8], remaining spine sections, disclosure, captions) were `is_clean=True` on the prior
pass and are unchanged.

## Wave-0 must-fixes (full-body) — PASS
- **No "EFSA 2021" fabrication:** 0 occurrences in consumer copy; "2021" appears only in a code comment
  describing the avoided legacy defect. Consumer strings use SCF 2001 / EFSA 2015.
- **Bisglycinate hedged weaker-than-citrate:** 4 hedges (body[4], spine "צורה כימית וספיגה", forms-recap-2,
  sources-5); the 3 weak PMIDs disclosed as reviewed-and-insufficient (2024 COI, 2019 mouse-only, 1994
  4-of-12 subgroup), never cited as proof. Matches rubric `citation_gaps` disposition.
- **No "דירוג"/grade-letter forms:** 0 in consumer copy; `bandExcludedBars=[]` is structural only.

## Tier re-gate — GO (detail)
- **RT-8 (sole prior blocker) RESOLVED:** integrated body[2] names zero tier words; `is_clean=True`.
- **RT-6 RESOLVED:** the retired "הרשימה המעשית להתחיל ממנה" shortlist framing is absent; body[8] uses
  descriptive "בקבוצות שלמעלה".
- 11/11 tier strings `is_clean=True`: body[0/2/8], 4 tier captions, empty-state, cannot-assess intro,
  2 expander labels. Captions scoped to displayed bars, no "meets every bar" over-claim, no hardcoded counts.

---

## Grammar-gate adjudication (`hebrew_grammar_gate.analyze()`, strings 594/621)

Flag: `noun_adj_gender_mismatch`, **medium confidence**, on "המכון הלאומי לבריאות האמריקאי" (NIH).

- **(a) False-positive — NOT a genuine error.** "האמריקאי" (Masc Sing) correctly modifies "המכון"
  (Masc Sing), the true phrase head. DictaBERT-morph mis-anchors it to the intervening "בריאות" (Fem)
  inside the prepositional phrase "לבריאות". This is exactly the module's own documented limit
  (`hebrew_grammar_gate.py` HONEST LIMITS: loanword/ambiguous gender mislabeling; reference noun several
  tokens away across prepositional/relative constructions; "flags are CANDIDATES for human review, not
  hard verdicts"). Content confirmed it fires on the pre-edit text too — pre-existing, not introduced by
  the RT-9 reword.
- **(b) NOT in the deterministic go-live battery.** `run_gates.py` and
  `03_operations\spine\validate_comparison_page.py` contain zero references to grammar / readability /
  is_clean / leak. `hebrew_grammar_gate` is imported only by `copy_evals/run_evals.py`, two snack-bar
  one-offs, `naturalness_gate.py`, and `hebrew_grammar_autofix.py` — none of which is the go-live battery.
  It also requires a ~440MB DictaBERT download + torch, so it is not a deterministic offline gate. It
  therefore **cannot red go-live**, even were the flag genuine.
- **(c) Recommendation: NO reword. Ship as-is.** The phrase is correct standard Hebrew; contorting correct
  copy to satisfy a mis-anchoring parser that is not in the go-live path is the wrong trade. If the team
  later wants the ad-hoc `copy_evals` grammar scan to go green, the minimal OPTIONAL reorder is
  "המכון הלאומי האמריקאי לבריאות" (adjacency) — optional, not a blocker, and would require its own
  `is_clean` re-check.

Ruling: grammar flag = **non-blocking false-positive** → full-body verdict is **GO**, not CONDITIONAL.

---

## Comment-correction list (Deliverable 3)

Truthful as of this GO, but repoint from "this task's return" to this artifact:

| Line | Field | Action |
|---|---|---|
| 505–510 | suppressedBarsDisclosureHe | cite `magnesium_guide_content_gate2_v1.md` (slot-copy Slot 2 QA GO) instead of "this task's return" |
| 472–484 | headlineFinding | (1) cite this artifact; (2) **fix stale claim** "body[3]-body[7] … UNCHANGED" — body[3] WAS reworded for RT-9 (L491) |
| 513–522 | recommendationTierCaptions | cite this artifact |
| 530–535 | veryRecommendedEmptyStateHe | cite this artifact |
| 542–544 | cannotAssessSectionIntroHe | cite this artifact |
| 547–549 | expanderLabels | cite this artifact |
| ~433 | heroImage.alt | cite the slot-copy QA GO record for the alt text rather than "this task's return" |

Routes to: **orchestrator** (comment truthfulness — QA raises, does not self-edit source).

---

## Residual MEDIUM findings (non-blocking; not go-live blockers)
- **RT-10:** gate-status comments cite "this task's return" (a conversation, not an artifact); resolved by
  the correction list above once repointed to this file.
- **RT-11:** the two slot-copy "both gates passed" comments (alt, disclosure) reference
  `magnesium_guide_slot_copy_v1.md`, which self-labels a Content gate-1 draft ("Gate 2 not sought"); the
  QA gate-2 GO record for slot copy should be the citation for auditability.
- **RT-12 (cross-check, routes to nutrition-agent):** rubric `safety` bar boundary is off-by-one —
  PASS = "dose ≤ 250", FLAG = "250 < dose ≤ 350", yet the FLAG rationale + `per_product_result` table +
  integrated data all treat the two **250 mg** products (Supherb, Altman Bisglycinate) as FLAG. Copy
  follows FLAG intent; the defect is the rubric inequality, not the copy.
- **Advisory (non-blocking):** all 18 oneLinerHe + spine use em-dashes; `em_dash` is ADVISORY in the
  instrument (owner rule = minimize, not ban).

---

## Verdict
**Tier copy: GO · Full-body copy: GO · Comment audit: corrections listed.** No open CRITICAL. Content
sign-off (gate 1) + this Adversarial QA sign-off (gate 2) together satisfy the two-gate hard rule for the
tier and body copy. Page go-live remains subject to RT-5/RT-7 (frontend/gate-owner) and the comment repoint.
Proposed status: RETURNED (QA raises + routes; does not fix or close).
