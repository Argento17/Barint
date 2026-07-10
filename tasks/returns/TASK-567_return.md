# TASK-567 Return — Tamper-proof sign-offs: sha256-pinned approval records

Date: 2026-07-10 · Builder: subagent (C1) · Branch: task567-signoff-sha (worktree C:/bari_wt_567 off origin/master) · Local build tree: C:\Bari (uncommitted, per spec)

## What was built

1. **Record format + spec** — `tasks/signoffs/<json-basename>.approval.json` with
   `copy_id, file, sha256 (exact approved JSON bytes), gates.{content_agent,red_team}.{agent,date,evidence}, approved_at, task`
   (+ `migrated_from` / `migration_note` / `legacy_marker_text` on migrated records).
   Spec: `01_framework/operations/signoff_record_v1.md`.
2. **Verifier** — `03_operations/validators/verify_signoffs.py`. Hashes the exact bytes
   (working tree, or the STAGED index blob with `--staged` — precisely what a commit ships) and
   exits 1 on missing record OR sha256 mismatch. Exit 0 pass / 1 violation / 3 infra (so callers
   never confuse "verifier broken" with "approved"). CRLF-smudge aware: pinned hashes are of the
   git blob; a clean-vs-HEAD file whose raw disk bytes differ only by autocrlf smudge re-hashes the
   HEAD blob (git-confirmed clean only — a truly edited file stays a mismatch, no weakening).
   Legacy `.ok` accepted ONLY behind `--allow-legacy-ok`, with a printed DEPRECATION warning.
   utf-8-sig reads, `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`, stdlib only.
   `--selftest` = 6 checks proving both directions (see evidence).
3. **Hook** — `.claude/hooks/guard-two-gate-commit.ps1` (LOCAL registry only; origin does not
   track this file) now calls the verifier with `--staged --allow-legacy-ok` on staged comparison
   JSONs: exit 1 → block (exit 2) with the mismatch detail; exit 0 → pass (DEPRECATION/WARN lines
   surfaced). Verifier unavailable/infra → printed warning + fallback to the pre-567 existence
   check (extended to accept `.approval.json` existence), so the gate is never weaker than the old
   one under any failure. TASK-541 copy-authored layer and TASK-555 `git -C` scoping untouched.
   PS 5.1-safe (no `&&`, no ternary).
4. **Migration** — `03_operations/validators/migrate_signoffs.py`: pins sha256 of
   `git show HEAD:<file>` (current committed content), carries the `.ok` gate text verbatim into
   `gates.*.evidence` (full body under `legacy_marker_text`), deletes the `.ok`. Skips + reports
   uncommitted/dirty targets (content-filter-aware `git diff --quiet HEAD`). Ran in BOTH trees:
   local 11/11 migrated, worktree 9/9 (see counts).
5. **CI** — `.github/workflows/signoff_gate.yml` (new workflow; c0_return_gate.yml pattern):
   runs verifier `--selftest`, then verifies ONLY comparison JSONs changed in the PR
   (`git diff --name-only --diff-filter=ACMR base.sha...HEAD -- 'bari-web/src/data/comparisons/*.json'`).
   Empty diff → explicit exit 0. Strict mode (no legacy fallback) — the same PR migrates every
   origin `.ok`, so nothing depends on the fallback.

## Test evidence

**Selftest (both trees, exit 0):** matching-record-passes · one-flipped-byte-fails ·
missing-record-fails · legacy-ok-without-flag-fails · legacy-ok-with-flag-passes (DEPRECATION
printed) · bom-record-passes — 6/6 behaved as expected.

**Real-file pass case:** all 11 local records verify against the real comparison JSONs
(disk mode exit 0; staged mode spot-check exit 0). Worktree: all 9 records PASS, exit 0.

**Tamper case (scratchpad copy, repo untouched):** copied `chocolate_bars_frontend_v1.json` to
the scratchpad, flipped ONE byte (offset 500, `data[500] ^= 0x01`) → verifier exit 1:
`approved: df69ebe37d03…  current: af9ce28fd643…` — one byte voids the approval, as specified.

**Hook simulation (isolated sandbox: scratch CLAUDE_PROJECT_DIR + scratch git repo with a staged
comparison JSON; the live hook file exercised via piped PreToolUse payloads, real state never
touched):**

| Case | Setup | Expected | Got |
|---|---|---|---|
| A | staged bytes match pinned sha256 | exit 0 | 0 |
| B | staged bytes tampered | exit 2 + mismatch detail | 2, both hashes printed |
| C | legacy `.ok` only | exit 0 + DEPRECATION on stderr | 0, warning printed |
| D1 | verifier absent, record exists | exit 0 (fallback existence) | 0 |
| D2 | verifier absent, no record/marker | exit 2 (fallback blocks) | 2 |
| E | non-commit git command | exit 0 | 0 |
| F | commit with no comparison JSON staged | exit 0 | 0 |

**CI provably green on a no-change PR:** (a) the gate step's file list comes from
`git diff base...HEAD` limited to `bari-web/src/data/comparisons/*.json` — on this PR that list is
empty (verified in the worktree: count=0) → the step prints "nothing to gate" and exits 0;
(b) the only other step is `--selftest`, which exits 0 (run in the worktree); (c) a PR touching
none of the `on.paths` doesn't even trigger the workflow. Workflow YAML parses
(`yaml.safe_load` OK, jobs: verify-signoffs, on: pull_request + workflow_dispatch).

**Migration distribution (full set, no sampling):** local run over 11 `.ok`: statuses
{MIGRATED: 11, SKIPPED: 0, ERROR: 0}; task ids {TASK-574: 6, TASK-551: 2, TASK-515: 2, none: 1
(crackers EV-104 legacy)}. Worktree run over 9 `.ok` (origin's 3 committed + 6 TASK-574
reconstructed verbatim from the registry's preserved marker text; origin HEAD = merged PR #99 =
the exact TASK-574-signed-off bytes): {MIGRATED: 9, SKIPPED: 0, ERROR: 0}. The 2
`*_redteam_ledger.json` sign-offs exist only locally — origin has no such target files, so no
records were fabricated for it. Yogurt record hashes are identical local vs worktree
(e6ea823a122b / c571ae356df1) — the two trees agree on those bytes.

## Worktree / PR

- Commit: `66f5fc44` on `task567-signoff-sha` (16 files: workflow, spec, 2 validators,
  9 records added, 3 `.ok` deleted), pushed.
- PR URL (no gh CLI — open to create): **https://github.com/Argento17/Barint/pull/new/task567-signoff-sha**
- The hook edit is NOT in the PR: origin/master does not track `guard-two-gate-commit.ps1`
  (local-brain artifact), and the task's port list is workflow + verifier + spec + migration outputs.

## Freeze compliance

No comparison JSON content, no consumer copy touched — verified: the worktree commit and the
local diff contain only signoff records, validators, hook, workflow, spec, and this return.
Gate strictly stronger: existence+mtime → existence + sha256 equality of the staged blob.

```json
{
  "task": "TASK-567",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/validators/verify_signoffs.py", "action": "created", "sha256": "c094dbcf8013671fcf8be5459e47bc42e69da7047c3a279bbff036bba58367df"},
    {"path": "03_operations/validators/migrate_signoffs.py", "action": "created", "sha256": "bccb1b02f694a5fc935df57bb4cd3793953920bfee55e25e08178a7d3ce52de2"},
    {"path": "01_framework/operations/signoff_record_v1.md", "action": "created", "sha256": "a3f2d81116576520ec728054b483ac6a6d8ea0907fdf161ab2d2f9956e382624"},
    {"path": ".github/workflows/signoff_gate.yml", "action": "created", "sha256": "f02d8d927929107bd2d1f4636b3f6d34c1d43cbe02daec9fd11d2d8f92e28d90"},
    {"path": ".claude/hooks/guard-two-gate-commit.ps1", "action": "modified", "sha256": "b7c0999308d96a974b924184424c9189664946b0a027e2edcd1b32a4d72e5b3e"},
    {"path": "tasks/signoffs/chocolate_bars_frontend_v1.json.approval.json", "action": "created", "sha256": "13ff688385ab72141301c6507c98560bd6e9a86d9c9eddd22fbc1e4862b46e8c"},
    {"path": "tasks/signoffs/chocolate_bars_frontend_v1.json.ok", "action": "deleted"},
    {"path": "tasks/signoffs/chocolate_tablets_frontend_v1.json.approval.json", "action": "created", "sha256": "2b0b42efe9bfe6617c13a33380ab90f9a3734db5e82152189924a942c30d0f7b"},
    {"path": "tasks/signoffs/chocolate_tablets_frontend_v1.json.ok", "action": "deleted"},
    {"path": "tasks/signoffs/cookies_coffee_frontend_v2.json.approval.json", "action": "created", "sha256": "a98f2c27f7af8931fcc4ff9aa9ee2b92da00e9d179c30b9241d55edd8f0341dd"},
    {"path": "tasks/signoffs/cookies_coffee_frontend_v2.json.ok", "action": "deleted"},
    {"path": "tasks/signoffs/crackers_frontend_v1.json.approval.json", "action": "created", "sha256": "185d90b1b49eb45652d3a21d2aeb334444a6a9575ab04377dbcf7cde4819ad61"},
    {"path": "tasks/signoffs/crackers_frontend_v1.json.ok", "action": "deleted"},
    {"path": "tasks/signoffs/juices_frontend_v3.json.approval.json", "action": "created", "sha256": "eee5e490eb651f6f155902a0f6c1f2a7b0cf02e103537c453529263f3865b82f"},
    {"path": "tasks/signoffs/juices_frontend_v3.json.ok", "action": "deleted"},
    {"path": "tasks/signoffs/protein_combined_frontend_v2.json.approval.json", "action": "created", "sha256": "8be37f935bf6b8171233aa3fa52d2eaf1d6b105b39ec2443b1f743bc1aaea8e8"},
    {"path": "tasks/signoffs/protein_combined_frontend_v2.json.ok", "action": "deleted"},
    {"path": "tasks/signoffs/snacks_frontend_v5.json.approval.json", "action": "created", "sha256": "47d2c8c926d12f7a613956573f8956e63c2c9d24a734781f0d38a3430626f233"},
    {"path": "tasks/signoffs/snacks_frontend_v5.json.ok", "action": "deleted"},
    {"path": "tasks/signoffs/yogurt_drinkable_frontend_v1.json.approval.json", "action": "created", "sha256": "23db12da1a78e2b70bea786408f041ba03098debdaa0c975de370cc5d125e565"},
    {"path": "tasks/signoffs/yogurt_drinkable_frontend_v1.json.ok", "action": "deleted"},
    {"path": "tasks/signoffs/yogurt_drinkable_frontend_v1_redteam_ledger.json.approval.json", "action": "created", "sha256": "d679a2f2b72b2f5c9543ae4baac3c2bd39bd0698e78227d6afc414785db6f9fc"},
    {"path": "tasks/signoffs/yogurt_drinkable_frontend_v1_redteam_ledger.json.ok", "action": "deleted"},
    {"path": "tasks/signoffs/yogurt_spoonable_frontend_v1.json.approval.json", "action": "created", "sha256": "fb6a3a6a105639921827fbea10539e0f1558cc114e7233fc15be4590c69ff4ae"},
    {"path": "tasks/signoffs/yogurt_spoonable_frontend_v1.json.ok", "action": "deleted"},
    {"path": "tasks/signoffs/yogurt_spoonable_frontend_v1_redteam_ledger.json.approval.json", "action": "created", "sha256": "d22cee623232049d901452dd3bc7b99565001b1923f95d478e5c1679efbfe306"},
    {"path": "tasks/signoffs/yogurt_spoonable_frontend_v1_redteam_ledger.json.ok", "action": "deleted"},
    {"path": "tasks/returns/TASK-567_return.md", "action": "created"}
  ],
  "counts": {
    "selftest_checks_passed": "6/6 (verify_signoffs.py --selftest, both trees)",
    "local_ok_markers_migrated": "11/11 (ls tasks/signoffs/*.ok before run; migrate_signoffs.py summary; status dist {MIGRATED:11, SKIPPED:0, ERROR:0}, most_common=MIGRATED(11), stdev=0.0 on the binary outcome set; task-id dist {TASK-574:6, TASK-551:2, TASK-515:2, none:1})",
    "local_records_verified_pass": "11/11 (verify_signoffs.py over all records' target JSONs, exit 0; per-file dist {PASS:11, FAIL:0, SKIP:0}, most_common=PASS(11), stdev=0.0 on the binary outcome set)",
    "worktree_ok_markers_migrated": "9/9 (3 committed on origin + 6 reconstructed TASK-574; migrate summary MIGRATED=9 SKIPPED=0 ERROR=0)",
    "worktree_records_verified_pass": "9/9 (verify_signoffs.py in C:/bari_wt_567, exit 0)",
    "tamper_detection": "1/1 flipped-byte copy detected (exit 1, hashes df69ebe37d03 vs af9ce28fd643)",
    "hook_simulation_cases_correct": "7/7 (A,B,C,D1,D2,E,F table above)",
    "comparison_jsons_changed_in_pr": "0/20 (git diff origin/master...HEAD in worktree, comparisons dir has 20 committed .json) -- CI gate step exits 0"
  },
  "commands_run": [
    {"cmd": "python 03_operations/validators/verify_signoffs.py --selftest", "exit_code": 0},
    {"cmd": "python 03_operations/validators/migrate_signoffs.py --dry-run", "exit_code": 0},
    {"cmd": "python 03_operations/validators/migrate_signoffs.py", "exit_code": 0},
    {"cmd": "python 03_operations/validators/verify_signoffs.py --repo C:/Bari --signoffs C:/Bari/tasks/signoffs <11 record targets>", "exit_code": 0},
    {"cmd": "python 03_operations/validators/verify_signoffs.py --repo <scratchpad tamper copy> ... chocolate_bars_frontend_v1.json", "exit_code": 1},
    {"cmd": "<PreToolUse payload> | powershell -NoProfile -File .claude/hooks/guard-two-gate-commit.ps1  (cases A/C/D1/E/F)", "exit_code": 0},
    {"cmd": "<PreToolUse payload> | powershell -NoProfile -File .claude/hooks/guard-two-gate-commit.ps1  (cases B/D2)", "exit_code": 2},
    {"cmd": "python C:/bari_wt_567/03_operations/validators/migrate_signoffs.py --repo C:/bari_wt_567", "exit_code": 0},
    {"cmd": "python -c \"import yaml; yaml.safe_load(open('.github/workflows/signoff_gate.yml', encoding='utf-8-sig'))\"", "exit_code": 0},
    {"cmd": "git -C C:/bari_wt_567 commit -F msg567.txt  (commit 66f5fc44)", "exit_code": 0},
    {"cmd": "git -C C:/bari_wt_567 push -u origin task567-signoff-sha", "exit_code": 0}
  ],
  "not_done": [
    "Hook edit not ported to origin: origin/master does not track .claude/hooks/guard-two-gate-commit.ps1 (local-brain artifact); the task's port list is workflow + verifier + spec + migration outputs",
    "2 redteam_ledger approval records are local-only: origin has no *_redteam_ledger.json target files, so no origin records were created for them",
    "PR not opened (no gh CLI per policy) -- branch pushed, create at https://github.com/Argento17/Barint/pull/new/task567-signoff-sha",
    "Local C:/Bari changes intentionally left uncommitted per spec (build tree only)"
  ],
  "self_check": "Acceptance: a matching record passes and one flipped byte in a copy fails. Observed: verify exit 0 on all 11 real files (approved df69ebe37d03... == current), then exit 1 on the scratchpad copy with byte 500 XOR'd (current af9ce28fd643... != approved), and the live hook blocked the same tamper at commit boundary with exit 2 in sandbox simulation."
  }
```
