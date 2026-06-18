---
id: TASK-324
title: Omega-6:3 / specific-lipid extraction METHOD + label-coverage DATASET (EV-011 Na:K pattern), NO scoring
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-18
closed_at: 2026-06-18
close_reason: >
  P175/C1-GROK delivered + ORCHESTRATOR-VERIFIED. method_omega_lipid_extract.py (standalone) extracts
  omega-3/6 + specific lipids from in-house BSIP0 rows / BSIP1 panel (OFF-sourced panels skipped),
  EV-011 contract (absent -> declared:false, not zero/insufficient). DECISIVE POSITIVE-CASE TEST run by
  orchestrator: synthetic declared omega (1200/3600) -> omega3=1200, omega6=3600, ratio=3.0, declared=True;
  absent -> declared=False. So the headline 0% coverage is a REAL finding, not a broken-method false
  negative. Coverage reconciled independently: 979 evaluated / 0 declaring quantitative omega3 / 0 omega6 /
  0 ratio-computable / 186 qualitative oil signals (recorded separately, never converted to mg). SCOPE GUARD
  VERIFIED: git diff on score_engine/constants/configs/bari-web = EMPTY (exit 0). FINDING for the later
  governance step: an omega-6:3 EV-### is NOT viable on the current corpus (0% label coverage) — method is
  built + parked exactly like EV-011 Na:K (apply-only-when-declared); validates the label-derivability
  firewall. Activation/governance out of scope. Not committed, not pushed.
depends_on: [TASK-322]
blocks: []
category_id: null
summary: >
  Build a standalone extraction method that parses omega-6 / omega-3 / specific-lipid declarations from Hebrew labels where present, normalizes to per-100g fields, and measures live label coverage. Models the EV-011 present-when-declared / no-op-when-absent contract. Extraction + coverage data ONLY; no ratio applied to any score, no engine-path edit.
---

# TASK-324 — Omega-6:3 / specific-lipid extraction METHOD + label-coverage DATASET (EV-011 Na:K pattern), NO scoring

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
