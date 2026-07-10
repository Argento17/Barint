# Sign-off Record v1 — sha256-pinned two-gate approvals (TASK-567)

**Supersedes** the mtime-based `tasks/signoffs/<json-basename>.ok` markers (TASK-536 era).
An `.ok` marker only proved *something* was approved *sometime*; nothing tied the approval to
the bytes being committed — one changed word after sign-off went undetected. A sign-off record
pins the **sha256 of the exact approved JSON bytes**: change one byte and the approval is void.

## Location & naming

```
tasks/signoffs/<json-basename>.approval.json
e.g. tasks/signoffs/milk_frontend_v1.json.approval.json
```

Records live in the **main registry** (`C:\Bari\tasks\signoffs`) regardless of which worktree
the commit runs in — same convention as the old markers. Written by the **orchestrator only**,
after BOTH gates (Content Agent + Adversarial QA / Red-Team) pass — CLAUDE.md hard rule 2026-06-20.

## Format

```json
{
  "copy_id": "milk_frontend_v1",
  "file": "bari-web/src/data/comparisons/milk_frontend_v1.json",
  "sha256": "<hex sha256 of the exact approved JSON bytes>",
  "gates": {
    "content_agent": { "agent": "Content Agent", "date": "2026-07-10", "evidence": "<what was checked / gate ref>" },
    "red_team":      { "agent": "Adversarial QA / Red-Team", "date": "2026-07-10", "evidence": "<attack angles / report path>" }
  },
  "approved_at": "2026-07-10",
  "task": "TASK-XXX"
}
```

- `sha256` — hash of the **raw file bytes** as they will be committed (no decode, no normalization).
  Compute: `python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" <file>`.
- `evidence` — a concrete claim trail (what was diffed/attacked, report path), not "looks fine".
- Records migrated from legacy `.ok` markers additionally carry `migrated_from`,
  `migration_note`, and the full original body in `legacy_marker_text`.

## Lifecycle

Any edit to a signed-off comparison JSON — even one byte — voids the approval. Re-run BOTH
gates on the new content, then the orchestrator writes a **fresh record** with the new hash
(overwrite the old record; git history is the audit trail).

## Enforcement (both layers verify hash equality, not timestamps)

1. **Local commit hook** — `.claude/hooks/guard-two-gate-commit.ps1` calls
   `03_operations/validators/verify_signoffs.py --staged` on staged comparison JSONs: the
   **staged index blob** (what the commit will actually contain) must hash to the pinned value.
   Legacy `.ok` markers are still accepted with a printed DEPRECATION warning (transition only).
   Fails OPEN only on infra error — and then falls back to the old existence+mtime check, so the
   gate is never weaker than it was.
2. **CI** — `.github/workflows/signoff_gate.yml` runs the verifier (strict — no legacy fallback)
   on comparison JSONs **changed in the PR only** (same changed-files-only lesson as
   `c0_return_gate.yml`: whole-directory checks fail on legitimate historical drift).

## Migration

`03_operations/validators/migrate_signoffs.py` converts existing `.ok` markers: pins the sha256
of each target's HEAD content, carries the `.ok` gate text as evidence, deletes the `.ok`.
Skips (and reports) any target that is uncommitted or dirty. Safe to re-run; `--dry-run` previews.
