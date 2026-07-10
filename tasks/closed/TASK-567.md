---
id: TASK-567
title: Tamper-proof sign-offs: sha256-pinned approval records replace mtime .ok markers
owner: qa-agent
status: CLOSED
closed_at: 2026-07-10
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
close_reason: >
  Verified against artifacts. sha256-pinned .approval.json records replace mtime .ok markers:
  verify_signoffs.py (staged-blob hashing, exit 0/1/3, legacy .ok only behind --allow-legacy-ok
  with DEPRECATION) - orchestrator re-ran selftest 6/6 exit 0 including one-flipped-byte
  tamper-detect and BOM record; 11/11 migrated local records re-verified PASS exit 0 by
  orchestrator. Hook guard-two-gate-commit.ps1 upgraded existence->hash-equality; C7 containment
  CRITICAL (a .claude/ write) adjudicated per the validator's own instruction: orchestrator read
  the hook diff personally - verifier-first with exit-1 block, infra failure falls back to the
  pre-567 existence check extended to accept .approval.json (never weaker), TASK-541/555 layers
  untouched, PS 5.1 stderr trap handled via documented cmd /c wrapper. Hook sandbox simulation
  7/7 (agent) on isolated repo. signoff_record_v1.md spec + migrate_signoffs.py shipped; CI
  signoff_gate.yml = changed-in-PR-only (c0_return_gate pattern), green-on-no-change proven.
  Origin port: branch task567-signoff-sha @ 66f5fc44 pushed (9 records for origin incl. 6
  TASK-574 records pinned to the merged PR #99 bytes), PR pending owner merge. Return C0:
  all checks PASS except the expected C7 flag (task-mandated hook edit, resolved by human read).

summary: >
  Owner-approved 2026-07-10. Replace tasks/signoffs/<json>.ok mtime markers with structured records: copy_id, sha256 of the exact approved content, gates[content_agent,red_team], approved_at. guard-two-gate-commit.ps1 and CI verify hash equality, not timestamps - one changed word voids the approval. Includes migration for existing markers and a CI job. Build pipeline only: PRODUCT DESCRIPTIONS FREEZE stays - no authoring runs.
---

# TASK-567 — Tamper-proof sign-offs: sha256-pinned approval records replace mtime .ok markers

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
