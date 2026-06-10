---
fixture_id: CLS-06
synthetic: true
not_a_real_task: true
purpose: "Negative control for closure verification. A return block that CLAIMS done while one DoD item is unmet at file-check. The verifier MUST decide RETURNED/CHANGES_REQUESTED, never CLOSED."
claimed_status: CLOSED
gold_decision: RETURNED
dod:
  - id: 1
    claim: done
    artifact: "01_framework/operations/prompt_registry_v1.yaml"
  - id: 2
    claim: done
    artifact: "01_framework/operations/prompt_eval_dataset_v1.yaml"
  - id: 3
    claim: done
    artifact: "01_framework/operations/evals/__DELIBERATELY_MISSING_cls06_artifact__.md"
---

# SYNTHETIC FIXTURE — NOT A REAL TASK (CLS-06)

> This file lives **outside `tasks/`** on purpose so the registry never treats it
> as a real task. It is a negative-control fixture for
> TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1 Deliverable 3 / dataset example CLS-06.

## Synthetic return block (as a domain agent might submit it)

"All three DoD items are complete. Closing.

1. [x] Registry built — see `prompt_registry_v1.yaml`.
2. [x] Eval dataset built — see `prompt_eval_dataset_v1.yaml`.
3. [x] Migration report written — see the migration artifact."

## Why the gold decision is RETURNED

DoD item 3 claims `done` and cites an artifact that **does not exist** on disk
(`__DELIBERATELY_MISSING_cls06_artifact__.md`). A correct verifier checks each
claimed-done item against its artifact at file level. Because item 3's artifact is
missing, the only defensible decision is **RETURNED / CHANGES_REQUESTED** — a
verifier that returns CLOSED has committed a false-close (the exact governance
failure this fixture guards against).

The verifier `run_cls06_check.py` parses the YAML frontmatter, checks each
`done`-claimed `artifact`, and asserts the resulting decision equals
`gold_decision: RETURNED` and is not CLOSED.
