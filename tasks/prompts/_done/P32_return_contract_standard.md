# P32 / TASK-257-adjacent (process hardening) — Machine-readable Return Contract standard (route: C2)

ZERO-JUDGMENT MECHANICAL TASK. You will create one standard file and insert one
identical section into 11 agent definition files. Do not rephrase, do not improve,
do not reorganize anything else in those files.

WHY (context only): twice in one day, agent return blocks contained numeric claims
that failed verification ("47/47 replay proof" = a build stat; "v2 differs from v1"
= byte-identical files). Prose claims cannot be machine-checked. From now on every
return block ends with a JSON contract the orchestrator verifies mechanically.

STEP 1 — create: 01_framework/operations/return_contract_v1.md
Exact content:

---START FILE---
# Return Contract v1 (mandatory for all agent return blocks)

Every return block MUST end with a fenced JSON block:

```json
{
  "task": "<TASK-ID or P-number>",
  "proposed_status": "RETURNED | BLOCKED",
  "artifacts": [
    {"path": "<repo-relative path>", "action": "created|modified|deleted",
     "sha256": "<hash of final file>"}
  ],
  "counts": {"<claim_name>": "<N>/<M> with M = denominator source named, e.g. 'products_with_image: 80/80 (BSIP1)'"},
  "commands_run": [{"cmd": "<exact command>", "exit_code": 0}],
  "not_done": ["<anything in the spec you did not do, or empty list>"],
  "self_check": "<the one acceptance test from your spec and its observed result>"
}
```

Rules:
1. Every numeric claim in the prose MUST appear in `counts` with its denominator
   and source. A number with no artifact behind it is not a claim — omit it.
2. `artifacts` lists EVERY file touched. sha256 = `Get-FileHash` / `sha256sum` of
   the final state.
3. `not_done` is mandatory honesty: empty list means "spec fully done" and you
   will be held to that.
4. The orchestrator verifies the JSON against the filesystem before acceptance.
   A return block without this JSON is automatically CHANGES_REQUESTED.
---END FILE---

STEP 2 — insert into EACH of these 11 files, immediately BEFORE the line
"## Autonomy Mandate" (every file has it; if a file does not, append at the end):
.claude/agents/cc-agent.md, content-agent.md, data-agent.md, design-agent.md,
frontend-agent.md, marketing-agent.md, nutrition-agent.md, product-agent.md,
qa-agent.md, red-team-agent.md, research-agent.md

Exact section to insert (identical in all 11):

## Return Contract (mandatory — 2026-06-12)

Every return block ends with the JSON contract defined in
`01_framework/operations/return_contract_v1.md`: artifacts+sha256, counts with
named denominators, commands_run with exit codes, `not_done`, and the spec's
acceptance test result. Prose numbers not present in `counts` are treated as
unverified. A return without the JSON block = CHANGES_REQUESTED automatically.

STEP 3 — bump each agent file's frontmatter `version:` by +0.1 and add a
changelog entry: `Return Contract v1 wired (P32).` (match each file's existing
changelog format; if a file has no changelog list, add one matching qa-agent.md's
format).

STEP 4 — append ONE line to C:\Bari\CLAUDE.md at the end of the
"## Tasks & registry (Agent OS — all agents)" section:
- **Return Contract.** Every agent return block ends with the machine-readable JSON contract (`01_framework/operations/return_contract_v1.md`); returns without it are auto-`CHANGES_REQUESTED`.

RULES: touch ONLY the 13 files named above. No other edits. No reformatting of
untouched sections. Preserve file encodings (UTF-8).

RETURN BLOCK: list of 13 files with action; confirm the inserted section is
byte-identical across the 11 agent files (state the sha256 of the inserted text);
confirm CLAUDE.md line added; AND end with the JSON contract from STEP 1 itself —
you are its first user. Propose RETURNED.

---
After you send this to the agent: open tasks\DISPATCH_BOARD.md and tick the P32 line.
