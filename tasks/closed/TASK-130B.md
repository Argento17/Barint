---
id: TASK-130B
title: Implement validate-corpus MVP
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "The MVP validator is implemented, preserves shipped pages via WARN mode, blocks new handoffs via ERROR mode, and clearly documents remaining non-MVP gaps."
depends_on: [TASK-130]
blocks: [TASK-132]
category_id: null
summary: >
  Implement the validate-corpus MVP that enforces the Category Module Contract v1
  (category_module_contract_v1.md §2/§3). MVP scope: schema/count/coherence/
  explanation-completeness/unknowns/ordering checks against BariProductVM, exit-coded,
  per-product diagnostics. WARN mode for already-LIVE categories, ERROR mode for new
  handoffs (mitigates contract risk R1). Does not modify datasets.
---

# TASK-130B — Implement validate-corpus MVP

Parent: TASK-130 (Operating-Model Hardening). Spec: `01_framework/operations/category_module_contract_v1.md` §6–§7.

## Scope (MVP)
- Single exit-coded command over comparison datasets, validating against the real
  `BariProductVM` contract.
- Rules: §2.1 schema, §2.2 counts/dupes, §2.3 score⇔grade coherence, §2.4 explanation
  completeness (bread limitingFactors gap), §2.5 unknowns-when-null, §2.6 no-score
  explicit, §2.7 ordering, §2.8 prohibited vocabulary (heuristic).
- WARN for LIVE categories, ERROR for new handoffs.
- Per-product diagnostics (id + rule + offending value).
- Do NOT modify datasets.

## Out of scope (MVP)
- Baseline snapshots / regression diff (§6.4) — stub/deferred.
- Shared-corpus post-filter validation (§6.6) — flagged as gap.
- Build/eslint/git preconditions of `--handoff` (§3.6, §6.7) — deferred.
- Image-resolution (§2.9) — best-effort/deferred.

## Outcome (2026-06-01) — proposed RETURNED
Implemented `bari-web/scripts/validate-corpus.mjs` + `npm run validate-corpus`
(dependency-free Node ESM; no new packages). Modes: `[<id>|--all] [--handoff]`.
- DEV `--all` over 7 datasets → exit 0, 233 warnings (LIVE failures are non-blocking →
  preserves shipped state, contract R1).
- HANDOFF promotes failures to ERROR (bread --handoff → 32 errors, exit 1).
- Deprecated orphans (hummus v1/v2) → SKIP + §4.3 warning, not deep-validated.
Rules implemented: §2.1–§2.8, §1.3, §4.3. Datasets NOT modified.
Confirmed the contract's stated gaps in real data: bread 24/24 missing limitingFactors
+ 24/24 unknowns gap; unknowns gap widespread (yog 13, snk 18, maad 87); hummus_v3 clean
on unknowns. Gaps vs contract: §6.4 baselines, §6.6 shared-corpus post-filter, §3.6
build/git handoff preconditions, §6.5 runtime-schema-from-type, §2.9 image-resolve — all
deferred. Awaiting Central Controller to record CLOSED.
