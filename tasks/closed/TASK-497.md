---
id: TASK-497
title: Hygiene small-fixes batch — protein rerank grade-floor tie-bug (intermediate file) + hebrew_readability word-boundary false-positive
owner: data-agent
status: CLOSED
priority: LOW
created_at: 2026-07-03
closed_at: 2026-07-03
close_reason: "MERGED LIVE PR #73 (squash, origin/master 22d85ea4; guard on master verified). (A) protein rerank_table_rescore.json 2 sub-floor barcodes C→D (49.8/49.7<50); live frontend confirmed already D, untouched. (B) hebrew_readability.py Hebrew word-boundary guard + brand allowlist + regression tests — תנובה clean, standalone נובה still flags. Barcode/diff-verified: only 2 internal files, 0 consumer/score touched. Internal non-consumer → orchestrator-merged."
depends_on: []
blocks: []
category_id: null
summary: >
  Two internal, non-consumer hygiene fixes surfaced by red-teams this session. (A) protein
  rerank_table_rescore.json mislabels 2 sub-floor products (7290019766230, 7290019401544, score<50 → policy D)
  as grade C in the INTERMEDIATE artifact — the LIVE frontend already shows correct D, so consumers are NOT
  affected; fix the intermediate file for internal consistency. (B) hebrew_readability.py leakage gate
  substring-matches "נובה" (NOVA framework token) inside the brand name "תנובה" (Tenuva) → false-positive
  leak flag on truthful copy; add a word-boundary / brand-allowlist guard. Neither touches published scores
  or consumer copy.
---

# TASK-497 — hygiene small-fixes batch (internal, non-consumer)

## Fix A — protein rerank tie-bug (intermediate file only)
- File: the protein rerank_table_rescore.json intermediate artifact (locate under 02_products/snack_bars/ or
  the protein rescore run dir). Barcodes 7290019766230 + 7290019401544 (score < 50) are labeled grade C but
  policy floor (grade_boundary_policy_v1: C floor=50, D floor=35) makes them D. LIVE frontend
  (protein_combined_frontend_v2.json) already shows the correct D → NO consumer impact; this is intermediate-
  artifact consistency only. Fix the 2 grade labels in the intermediate file. Confirm live is already correct
  (do NOT touch the live JSON — it's right).

## Fix B — hebrew_readability word-boundary false-positive
- File: the hebrew_readability leakage gate (hebrew_readability.py). It flags "NN.N" score-mechanic + framework
  tokens; "נובה" (NOVA) substring-matches inside "תנובה" (Tenuva, a dairy brand). Add a word-boundary guard
  and/or a brand allowlist so brand names containing a framework substring don't trip the gate. Add a
  regression test if the module has a test harness. Do NOT loosen the gate's real detection.

## Guards
- ZERO published-score change, ZERO consumer-copy change (both fixes are internal artifacts/tooling).
- Base off origin/master (not local HEAD — F1 divergence). Isolated worktree. Internal → orchestrator may
  merge (non-consumer, non-tripwire) after verify, or PR.

## Return: 5-part + before/after per fix + machine-readable Return Contract. Propose RETURNED.
