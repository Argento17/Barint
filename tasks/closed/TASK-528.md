---
id: TASK-528
title: verify_citations.py domain-word heuristic false-positives on non-food/supplement medical literature (GLP-1/incretin body-composition papers)
owner: data-agent
status: CLOSED
priority: LOW
created_at: 2026-07-08
closed_at: 2026-07-09
depends_on: []
blocks: []
category_id: null
close_reason: >
  Dispatched native-Sonnet (Data, a71e1d3) 2026-07-09 unattended; orchestrator-verified against artifacts
  before close. Fix is purely additive: 26 GLP-1/incretin/body-composition/weight-management/clinical-trial
  terms added to _FOOD_NUTRITION_WORDS + the Rule-4 generic_ok tuple (verify_citations.py:253,331-344),
  plus a reason-string update. NO change to _RED_FLAG_WORDS, Rule 1 (red-flag), Rule 3 (conservative
  fallback MISMATCH), or author/year corroboration — orchestrator read the full git diff to confirm no
  stealth weakening. Fabrication detection unweakened: independently re-ran test_verify_citations_domainword.py
  (10/10, exit 0) — 5/5 real GLP-1 PMIDs incl the bug case PMID 41877354 now consistent=True; 3/3 negative
  controls still MISMATCH (B1 leukemia Rule-1, B2 hip-arthroplasty Rule-3, B3 stroke Rule-1); 17 sentinel
  red-flag terms confirmed present. sha256 verify_citations.py=CC5065B7…; new test file 34BB96B4…
  Pre-existing --selftest TC-1 fail (6/7) unchanged, not introduced (agent proved via git stash baseline).
  Scope note: validate_return.py also shows dirty in the tree but that is a pre-existing ambient C7-containment
  change (citation-unrelated, referenced as an existing feature in orchestrate.md), re-touched by the agent's
  stash/pop cycle — NOT authored by this task and excluded from this close/commit. Non-consumer C0 tooling,
  no score/copy/deploy impact, reversible.
summary: >
  The C0 citation-fabrication gate correctly resolves real PMIDs (title/journal/year/author all match) but flags them MISMATCH when the resolved title lacks a nutrition/food domain keyword the heuristic expects -- confirmed false-positive on PMID 41877354 (real 2026 Diabetes Obes Metab paper, Eisa et al., topic = incretin/GLP-1 lean-mass, correctly resolved by the tool itself but mislabeled MISMATCH for lacking food-domain words). Surfaced during TASK-504A RT-2 evidence verification. Not a fabrication-detection failure (0 actual fabrications missed this session) -- a false-positive class on medical/pharma literature adjacent to but not strictly 'food' topically. Fix: broaden the domain-word list or add a medical/pharma-literature allowlist path.
---

# TASK-528 — verify_citations.py domain-word heuristic false-positives on non-food/supplement medical literature (GLP-1/incretin body-composition papers)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
