---
id: TASK-287
title: Commit CI gate workflows (.github) + add OFF-string sweep job — machine-gates activation (release platform P0, gap-analysis EFF-2)
owner: frontend-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-16
closed_at: 2026-06-16
close_reason: >
  Orchestrator-verified at commit 006bfef6. `git show --name-only` = exactly 3 files, ALL under
  .github/workflows/ (barint_ci, argento_bari_ci, shadow_gate); 0 non-.github paths; 189 insertions.
  OFF-sweep job confirmed present in the COMMITTED barint_ci.yml (lines 79-92: grep -riE
  openfoodfacts|open_food_facts|off_api|off_candidate_panel|openfoodfacts.org across bari-web/src/data/,
  exit 1 + ::error:: on hit). Both barint_ci.yml + shadow_gate.yml parse as valid YAML (yaml.safe_load).
  Engine diff UNTOUCHED — score_engine.py + signal_extractor.py still ' M' (unstaged) post-commit.
  Not pushed (per spec). CI workflows are now tracked; gates run on the next PR (shadow_gate stays INACTIVE
  until an APPROVED baseline is promoted = P-BASE).
depends_on: []
blocks: []
category_id: null
summary: >
  The 3 workflow YMLs (barint_ci, argento_bari_ci, shadow_gate) are untracked and have never run. Commit them on the current branch and add an OFF-string sweep job (grep openfoodfacts|open_food_facts|off_api across bari-web/src/data/, fail on any hit). No engine edits. Reversible.
---

# TASK-287 — Commit CI gate workflows (.github) + add OFF-string sweep job — machine-gates activation (release platform P0, gap-analysis EFF-2)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
