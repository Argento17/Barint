---
id: TASK-422
title: W3: Independent verification — automated corpus-rank check + variance-flag harness
owner: qa-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-01
closed_at: 2026-07-01
depends_on: [TASK-420]
blocks: []
category_id: null
close_reason: >
  Both parts delivered + verified + wired. Part A rank_check.py (sha 5d45ca9e) — corpus-wide
  superlative gate, precision-hardened to 0 false positives across all 15 live pages, surfaced 1
  real defect (Tvorog → TASK-426, now fixed), wired as gate 6 of validate_comparison_page.py
  (cheese FAIL / milk PASS verified). Part B verify_variance.py (sha 9aef444d) — independent-lane
  variance-flag harness, selftest exit 0 (6 cases) + e2e verified (REFUTED/CONFIRMED/fail-safe).
  No published-score / consumer-facing change (no tripwire). Real Bari lane adapters (C3 + Opus
  critic) are thin wiring documented for when a claim needs live verification.
summary: >
  rank_check.py: re-derive every superlative claim vs FULL corpus (automates validate_comparison_page gate-6 manual step). verify_variance.py: sample claim N times across independent lanes (Opus critic + C3), flag on disagreement past threshold (self-consistency > debate). Additive; changes nothing published.
---

# TASK-422 — W3: Independent verification

## Part A — rank_check.py  ✅ DELIVERED + verified (2026-07-01)
`03_operations/validators/rank_check.py` (sha256 5d45ca9e8a0d…4872a). Automates the manual
step in `validate_comparison_page.py` gate 6: instead of *flagging* a fixed phrase list for a
human, it parses superlative claims from consumer copy and **re-derives each against the full
corpus** (the failure class in [[superlative_claims_need_corpus_rankcheck]] — a per-product
number-trace can't catch a false RANK claim).
- Verifies: nutrient extremums (sugar/sodium/protein/fat/fiber/energyKcal from expansion.nutrition),
  score/table-position, additive count. Plus R0 rank-field-vs-score-order integrity.
- Exit 0/1/2 (mirrors run_gates.py); `--emit-json`; `--selftest` exit 0.
- **Precision-hardened against real copy (this is the important part):** first pass produced
  100+ flags that were mostly false positives; reading the live copy revealed 3 FP classes and
  each was fixed deterministically:
  1. ambiguous score words (`מוביל`/`בראש` = "syrup leads"/"leads at 60%") → dropped;
  2. cross-clause proximity (bound `סוכר` to a `הגבוה ביותר` modifying `נתרן`) → replaced with
     ADJACENCY-bound regexes;
  3. subpool-scoped claims ("highest among the 9% cheeses / the three Spring nectars") →
     detected at SENTENCE granularity and downgraded to manual WARN (can't verify a subpool
     deterministically), never falsely failed against the whole corpus.
- **Final result across all 15 live pages: 0 false positives, true superlatives CONFIRMED
  (e.g. chocolate_bars 6/6), and exactly ONE real finding surfaced** →
  `cheese_frontend_v4 :: bsip1_cheese_6040619` (Tvorog 5%) claims "highest protein of any
  product in the category" (17g) but goat-cheese 32% (bsip1_cheese_7290108506624) has 23g —
  a live false/unscoped superlative. **Routed to Content/Nutrition (consumer-facing copy; two-gate).**

## Part B — verify_variance.py  ✅ DELIVERED + verified (2026-07-01)
`03_operations/validators/verify_variance.py` (sha256 9aef444d307a…4e238). Samples a claim across
INDEPENDENT lanes and treats DISAGREEMENT (variance) as the signal — NOT a debate (self-consistency
beats orchestrated debate, OpenReview Vusd1Hw2D9; cross-model verify ~-25% hallucination, MDPI
15/7/3676; panels <=3 to avoid false consensus). Decision rule (strict — a false CONFIRM is the
costly error): CONFIRMED = decisive votes agree at/above --confirm-agreement (default 1.0) with no
refusals; REFUTED = majority refute; FLAGGED = any split/UNSURE/lone-dissenter. Lanes are pluggable
independent shell commands (claim JSON on stdin → verdict); real adapters = C3 (dispatch.py route C3)
+ Opus critic ([[critic_lane_opus_and_c3]]); a lane error → abstain, never crashes. Exit 0/1/2;
`--selftest` exit 0 (6 cases); e2e verified (2×NO→REFUTED, 2×YES→CONFIRMED, bad-lane fail-safe).

## Wiring ✅ DONE + verified (2026-07-01, owner-approved)
`rank_check.py` is now gate 6 of `03_operations/spine/validate_comparison_page.py` (replaces the old
manual-WARN phrase scan). Runs as a decoupled subprocess; FALSE superlative → HARD fail, subpool/
uniqueness → WARN; degrades to a WARN (never crashes) if rank_check.py is absent. Verified: cheese
page → `[FAIL] superlative (1 false, 2 manual-review)`; milk page → `[PASS] superlative`.

## Follow-ups
- The Tvorog finding → **TASK-426** (Nutrition adjudicating root cause; Content reword via two-gate). Not fixed inline.
- Part B `verify_variance.py` — build next (needs live C3/Opus lane wiring).
