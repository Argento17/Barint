---
id: TASK-420
title: W1: Deterministic return-contract gate (validate_return.py) — C0 on 100% of agent returns
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-01
closed_at: 2026-07-01
depends_on: []
blocks: [TASK-421, TASK-423]
category_id: null
close_reason: >
  Built + self-verified 03_operations/validators/validate_return.py (sha256
  c62f58726a30…489a7e). `--selftest` exits 0: passing contract → PASS, failing contract →
  FAIL(correct). Verified 3 input paths (--json, --md fenced-block extraction with Hebrew
  copy, stdin) and --emit-json. Live-tested the 6 checks: C2 sha mismatch + missing-file,
  C3 sourceless count, C5 full-set-without-distribution (rank claims correctly downgraded to
  WARN, not a false block), C6 fabricated PMID '31douchebag' caught HARD. Wired into
  /orchestrate step 5 (deterministic first pass, exit!=0 → auto CHANGES_REQUESTED) and
  referenced from return_contract_v1.md. UTF-8 stdout forced (cp1252 crash fixed).
summary: >
  Composable C0 validator over return_contract_v1.md JSON: schema, sha256 re-check, count re-derivation, citation gate, distribution presence. Runs on every RETURNED block; exit!=0 -> auto CHANGES_REQUESTED. Foundation for W2-W4.
---

# TASK-420 — W1: Deterministic return-contract gate (validate_return.py)

## Problem
Bari's C0 gates (`run_gates.py`, `validate_comparison_page.py`, `verify_citations.py`) fire at
page-ship time. But the highest-frequency failures happen upstream at agent RETURN time —
self-reported counts that were wrong (`0/48` when it was `48/48`; "4/4 pairs pass" masking a
31-product collapse), fabricated PMIDs, and superlatives with no artifact. The orchestrator
checked the return contract by hand. This makes that check deterministic and universal.

## Deliverable
- `03_operations/validators/validate_return.py` — composable "Guard" over the
  `return_contract_v1.md` JSON. Runs on every RETURNED block. Six checks:
  - **C1 SCHEMA** — valid JSON, 7 required keys, valid status/action/types.
  - **C2 ARTIFACTS** — sha256 re-hash of every artifact; deleted files gone; created/modified exist.
  - **C3 COUNTS-FORM** — every count carries a number AND a named denominator/source (Rule 1/6).
  - **C4 COMMANDS** — commands_run well-formed; `--run-commands` re-executes and checks exit codes (Rule 6).
  - **C5 DISTRIBUTION** — full-set claims ("N/N", large N) or distribution-keyed claims must carry
    stdev/median/most_common (Rule 5); rank/ratio claims → soft WARN only (no false block).
  - **C6 CITATIONS** — flags any malformed/fabricated PMID token; hands off to `verify_citations.py` if present.
- Exit codes mirror `run_gates.py`: 0 PASS · 1 FAIL · 2 load-error. `--emit-json` for machine consumption.
- Inputs: `--json`, `--md` (extracts last ```json fence), or stdin. UTF-8 stdout (handles Hebrew copy).

## Integration
- `/orchestrate` (`.claude/commands/orchestrate.md`) step 5: deterministic first pass; exit!=0 → auto CHANGES_REQUESTED.
- `01_framework/operations/return_contract_v1.md`: documents the gate as this contract's enforcer.

## Verification
- `python 03_operations/validators/validate_return.py --selftest` → exit 0 (passing→PASS, failing→FAIL).
- Governance: changes no published score, no scoring philosophy, no consumer-facing artifact. No tripwire.

## Follow-ups (not in W1)
- Optional: a pre-commit / router hook that runs the gate on every `tasks/returns/*.md` automatically.
- Depends-on-this: TASK-421 (W2 golden regression), TASK-423 (W4 orchestrator durability).
