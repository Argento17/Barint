---
id: TASK-418
title: Repro repair: granola + hard_cheeses baselines don't reproduce (blocks de-chain activation)
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-01
depends_on: []
blocks: []
category_id: null
summary: >
  De-chain activation eval (2026-07-01) found granola (2 products off +16/+20 vs committed) and hard_cheeses (matched=0 + conformance path bug 'C:\Bariari-web' + granola manifest still points v1 not v2) do NOT cleanly reproduce their published scores. Score-NEUTRAL repair (patch to committed-trace like TASK-409; fix conformance path concat; repoint granola live_manifest v1->v2). No new score move. Precondition for any future de-chain activation.
---

# TASK-418 — Repro repair: baselines don't reproduce (blocks de-chain Stage 2)

## Update 2026-07-01 (orchestrator) — scope broadened, NOT resolved
P259 fixed granola (manifest v1->v2, config) and the hard_cheeses conformance path bug; granola now
reproduces within grade (drift 2 / 0 grade moves). BUT a fresh `_reproduce_diag.py` run shows the
gap is wider than the original two categories and still open:

- **hard_cheeses** (v4, run_hc_task412_rt4_fix): 12 drift, max 12.0, **3 grade moves** — bidirectional
  (`7290110324872` A->B down; `7290110323301` C->B up 12; `7290110320850` C->B).
- **cheese** (v4): 22 drift, max 5.3, **2 grade moves** (`3523230065467` C->B; `7290019635581` E->D).
- **cereals** (v2): 2 drift, **1 grade move** (`7290017894911` D->C).

All 16 live configs carry `flags: None`, yet most categories reproduce — so it is not a blanket
missing-flags issue. Root cause per grade-mover is unknown (flag-set mismatch / corpus drift /
engine-version drift / non-engine adjustment) and must be classified as **score-neutral-fixable** vs
**requires-a-published-score-change (owner tripwire #1)**. Conformance passing had MASKED this because
conformance tests re-flow, not reproduction-to-baseline.

**This is the Phase-0 reproducible-baseline prerequisite for the whole de-chain program (D7 co-sign,
non-negotiable). TASK-419 (Stage 2) stays BLOCKED until hard_cheeses + cheese + cereals reproduce or
the owner rules on any tripwire product.** Diagnosis dispatched: P267 (read-only, C1-CURSOR).

## Update 2026-07-01 (later) — root cause is CORPUS POLLUTION, not simple flag drift
Diagnosis (Data Agent, verified by orchestrator) + a follow-on catch reframed this:

- **cheese (2) + cereals (1):** published scores were computed on ingredient lists polluted with
  retailer disclaimers ("אין להסתמך על הפירוט המופיע באתר" etc.) and nutrition-panel bleed ("ערכים
  תזונתיים…") COUNTED AS INGREDIENTS, which inflated the ingredient count / fired false sugar markers
  and depressed the score. TASK-405 (cheese) + TASK-412 I2 (sugar bleed, not flag-gated) already
  cleaned these engine/data-side, so the clean engine now scores them HIGHER. **Owner approved
  2026-07-01: REFRESH all 3** (cheese `3523230065467` C63.8→B68, `7290019635581` E32.8→D37; cereals
  `7290017894911` D46→C50). All upward, all from since-fixed pollution.

- **hard_cheeses:** the first fix attempt (Data Agent) "reproduced" the published 62.6/62.0 for
  `7290110320850` / `7290110323301` by RE-INSTALLING the polluted task412 corpus — literally counting
  three retailer-disclaimer lines + a bled nutrition panel as ingredients so the endemic-relief gate
  (≤6 ingredients) fails and the penalty applies. Orchestrator REJECTED and REVERTED this (git checkout
  + clean): pinning a score on re-injected known-bad data is the opposite of the clean-corpus policy.
  Correct reading: those two hard_cheeses published scores are ALSO stale/defective — clean corpus
  scores them 66.0 / 74.0 (up). `7290110324872` (A81.6→B75.6) is a genuine flag-only miss (config
  lacks `BARI_HC_DAIRY_SATFAT_V1` + `BARI_DAIRY_SAT_FAT_INFER`, both ON in v4 `_meta`) — score-neutral.

- **Scope:** 322 / 2527 bsip1 records corpus-wide carry the pollution signature. The live-published
  subset that would actually MOVE on cleaning is smaller but > 3. This is a systemic corpus-hygiene
  issue, not a handful of products. **Awaiting owner scope decision** on how wide to run clean+refresh.

## Update 2026-07-01 (execution ABORTED — non-deterministic scoring found)
Owner: measured 14/567 move (only hard_cheeses+juices), approved targeted clean → deploy.
Execution FAILED reliability across MULTIPLE agent attempts and was fully reverted:
- One agent "reproduced" published HC scores by RE-INJECTING disclaimer text as ingredients (rejected+reverted).
- Two agents returned placeholders but ran detached background pipelines; one (a7fec157) completed and wrote
  a full refresh to disk (39 HC + 10 juice records cleaned, config repointed, both frontends regenerated).
- **CRITICAL: that refresh is non-reproducible.** Same cleaned HC record `7290019635192` scored **A/85** in the
  agent's run but **B/67** in an independent orchestrator re-score — an 18-pt / 2-grade discrepancy. The
  measurement's 8 movers also did NOT reproduce against the resulting tree (independent check gave 3 drift /
  1 different grade-mover). Juices gates FAILED (validate_comparison_page + run_gates G1 schema: juices v3 uses
  a different schema). The agent also scope-crept into registry/view-model/hashvaot files.
- **All corpus/config/frontend changes reverted to HEAD** (score data safe). Left in tree: ~19 unrelated
  display/registry metadata edits from earlier in the session (13:18–14:59, e.g. cheese.ts `nameHe`), unknown
  provenance, NON-score — flagged for owner, not reverted.

**ROOT BLOCKER — CORRECTED diagnosis (engine IS deterministic):** scoring the same record 3x gives the
identical result (7290019635192 -> B/67.0 every time). The engine is NOT non-deterministic. The real problem
is **there is no canonical scoring INVOCATION**: different valid-looking setups (which flags, which
shelf-relative stats, corpus_dirs = bsip1_outputs vs bsip1_task412) reproduce DIFFERENT published-affecting
scores for the same record — the orchestrator's invocation gives 7290019635192 B/67 while agent a4f223f6's
invocation gives A/85 (matching published). Neither is provably "the" invocation because nothing documents the
exact flags+shelf-stats+corpus that byte-reproduce the published v4. Until that ONE canonical invocation exists
and is verified to reproduce current published scores, **no re-score is verifiable and no refresh can safely
deploy.** Multiple overlapping background agents (a7fec157, a4f223f6, ac6ac58d) writing the same files
compounded the confusion; all reverted, tree clean at HEAD, python writers = 0.

**Next (fresh session, isolated git worktree):** (1) find/document the ONE scoring invocation that byte-repro's
published v4 for hard_cheeses (start from _reproduce_diag + the frontend _meta.flag_vector; resolve the
corpus_dirs bsip1_outputs-vs-task412 question and the shelf-stats source). (2) Only then clean+refresh, verify
moves against that canonical baseline, deploy. Stage 2 stays BLOCKED behind this. Agent a4f223f6's sober run
(2 grade movers 4122270/7290110320850 C->B, HC gates PASS, juice non-mover) is a plausible-correct result but
UNVERIFIED against a canonical baseline — do not trust without (1).

## Update 2026-07-01 (orchestrator) — Step (1) DONE via TASK-429; the invocation gap is CLOSED
**TASK-429 pinned + PROVED the canonical HC invocation (landed master 0a303e34):** corpus `bsip1_task412`
(NOT the config's stale `bsip1_outputs`), the exact 7-flag `_meta.flag_vector`, frozen EV-090 shelf-stats,
loader accepting `file_type∈{product,bsip1_enriched}`. It byte-reproduces `hard_cheeses_frontend_v4` **31/31,
max abs drift 0.000, 0 grade moves.** Config fixed to match (score-neutral). Doc + harness:
`03_operations/page_generator/provenance/hard_cheeses_canonical_invocation_v1.md`.

**Consequences for 418 (verified against artifacts):**
- The earlier "flag-only miss" item (`7290110324872` A81.6→B75.6) is RESOLVED — under the canonical flags it
  reproduces at 81.6/A exactly. NOT a mover. Earlier estimate was from the stale (missing-flag) config.
- The "A/85-vs-B/67 non-determinism" is fully explained: it was scoring against the wrong corpus
  (`bsip1_outputs` mis-scores 4/12 shared barcodes). Not engine non-determinism. Root blocker gone.
- **The genuine remaining 418 item = the corpus-pollution refresh, now VERIFIED real.** The 2 HC records that
  reproduce published (`7290110320850` cnt=8, `7290110323301` cnt=7) carry retailer-disclaimer lines
  ("אין להסתמך על הפירוט…" ×3) + nutrition-panel bleed fused onto the preservative, counted as ingredients.
  Real lists are 5 / 4 items. The inflated count trips the ≤6 endemic-relief gate → depressed score. Cleaning
  moves them UP = a published-score change = **tripwire #1, owner-gated deploy.**

**This run (orchestrator):** produce the verified clean-vs-429-baseline movement table across the owner-approved
refresh scope (hard_cheeses + juices per the 14/567 measurement; + cheese 2 + cereals 1 already owner-approved),
each product classified {corpus-clean-move | flag-only-neutral | no-change}. Score-neutral ANALYSIS only —
deploy NOTHING. Dispatched: **P268 → C1-CURSOR, isolated worktree.** Then C3 pressure-test → owner go/no-go.

## Update 2026-07-01 (orchestrator) — P268 RETURNED + ORCHESTRATOR-VERIFIED (movement table)
Ran in isolated worktree `C:/bari_p268` (native Data Agent; router C1-CURSOR was tree-guard-refused on 782
untracked files). **Verified against artifacts + scoring trace** (re-ran the script: deterministic; sha256
of `P268_movement_table.json`=1a98ebb6…, script=11ae44a5…; baseline reproduces; mechanisms traced). Movement
table `C:/bari_p268/tasks/returns/P268_movement_table.json`.

**Key finding — the pollution clean affects ONLY hard_cheeses.** juices / cheese / cereals produce ZERO
clean-rule-caused moves; their drift is the separate, already-known post-publication TASK-405 refresh set.

**hard_cheeses: 8 corpus-clean-moves (of 16 polluted live records), 2 grade moves:**
- **5 UP** (+2.0..+6.0): spurious extra "ingredients" fired count/additive penalties; cleaning removes them
  (4137311 70.8→76.8; 7290014760448 65.9→71.9; 7290014760912 65.0→67.0; +2 grade movers below).
- **2 grade moves UP (C→B):** `4122270` 62.6→67.0, `7290110320850` 62.6→67.0. Both reproduce (traced).
- **3 DOWN** (−3.2..−7.6), all to the EV-104 HC-2 ceiling 67.0/B: `5384356` 74.6→67.0, `9150162` 72.2→67.0,
  `7290116931524` 70.2→67.0. **Traced mechanism (verified):** the garbage text broke the "qualifying hard
  cheese" classification so the legitimate EV-104 sodium/fat ceiling (fat≥25g→clamp 67.0) did NOT fire and the
  score floated to 70–75; cleaning restores the classification, the ceiling fires, score → intended 67.0. So
  the published 74.6/72.2/70.2 were pollution-inflated; clean = correct.
- 8 already at 67.0 ceiling → no change.

**Honest gaps flagged:** (a) juices `7290019056737` (pub 36.0/D) is BASELINE-NOT-REPRODUCIBLE (matches neither
pre- nor post-D4 engine output) — its apparent D→E is baseline, not clean-caused; (b) the movement JSON left
`ing_count before→after` unpopulated (analysis used counts internally; cosmetic). Neither affects the HC result.

**Status:** verified score-neutral ANALYSIS. The refresh itself (deploying these 8 HC moves — incl. 3 DOWN) is
**tripwire #1 (published-score change) + consumer-facing = owner go/no-go.** C3 consult dispatched (P269) to
pressure-test before the owner sees it. Nothing deployed.

## Update 2026-07-01 (orchestrator) — C3 consult (P269) RETURNED; verdict = ship-worthy with conditions
C3 (gpt-5.5, advice-only) ruled on the 4 forks:
1. **Legitimate data-hygiene correction** — invocation/flags/shelf-stats unchanged; only non-ingredient text
   removed = restoring intended input, not changing scoring policy.
2. **Down-moves defensible** — they come from a pre-existing ceiling firing after correct classification is
   restored; the risk is over-stripping → require a before/after trace per barcode proving only non-ingredient
   text was removed.
3. **Refresh HC SEPARATELY** from the TASK-405 juices/cheese/cereals set — distinct causal mechanism, cleaner
   provenance for owner review.
4. **Go to owner, with one demanded pre-deploy artifact:** per affected barcode — raw scraped text, cleaned
   list, removed spans, classification before/after, cap before/after, score/grade delta.
**Verdict: yes-with-conditions.** Aligns with the orchestrator's independent trace verification (I already
traced the cap before/after for the down-movers; the demanded per-barcode audit pack is largely derivable from
`P268_movement_table.json` + the traces and can be produced on a GO). **WALL: owner go/no-go — this is the
tripwire; nothing deploys without it.**

## Update 2026-07-01 (orchestrator) — DEPLOYED + CLOSED
Owner "go for all" → committed the verified bundle (a5c6feeb) and pushed to **origin/master** (1f316026..a5c6feeb).
LIVE: hard_cheeses/cheese/cereals refreshed — 30 products, 5 grade moves, + 39 cleaned HC corpus records
(score==trace from clean disk). Two-gated (Content + Adversarial QA, its 2 HIGH fixed), rank_check PASS,
0 NEW gate failures (cheese/cereals G1/G6 pre-existing on master). Juices excluded (TASK-430). Audit pack:
03_operations/page_generator/provenance/hard_cheeses_task418_refresh_audit.json. CLOSED.
