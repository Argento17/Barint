# Return: TASK-586 — Align 9 governed docs to Capability Router v5

**Lane:** GENERAL (claude-sonnet-5, explicit pin per dispatch instruction).

## What this is

TASK-583 rewrote `03_operations/router/dispatch.py` to Capability Router v5 and flagged,
as known fallout, that `.claude/commands/orchestrate.md` and the 8 `.claude/agents/*.md`
files still described the retired v4.2 world (P-numbered prompt files, `(route: C1-GROK|
C1-GEMINI|C1-CURSOR|C2|C3)` tags, Grok/Cursor/DeepSeek as parallel lanes, "C1/C2/C3" used
as lane names). This task closes that fallout: read `01_framework/operations/
capability_router_v5.md` (law) and the `## Model routing` section of `CLAUDE.md`, then
edited all 9 files' routing text to the v5 truth. No agent missions, checklists, domain
content, two-gate law text, or tripwires were touched — only routing references.

## Per-file verdict

| File | Verdict | What changed |
|---|---|---|
| `.claude/commands/orchestrate.md` | **Edited (heaviest)** | Step 3 "Prepare the prompt / Lane" section: dropped the `bari_router_v4_2.md` band table (C5/C4/C3/C2.1/C2.2/C2.3/C1) and `tasks\prompts\PNN_*.md` + `(route: …)` convention; replaced with routing by the Layer-1 capability questions (`capability_router_v5.md`). Step 4 "Dispatch": replaced the "C1 BUILD HAS FOUR EXECUTORS (Sonnet+Gemini+Grok+Cursor)" model and the five lane bullets (C1-GROK/C1-GEMINI/C1/C2/C3/C1-CURSOR, each `dispatch.py PNN`) with one bullet per v5 capability (BUILD-HEAVY/LIGHT, GRUNT, CHALLENGE, EVIDENCE-RESEARCH, ENGINEERING-RESEARCH, VISION-LONGREAD, CONTENT/DOMAIN-JUDGMENT/PLANNING), naming the actual `dispatch.py` lane functions (`build_heavy`, `build_light`, `grunt_primary`, `challenge_gpt`, `evidence_research_fallback`, `engineering_research`, `vision_longread`) and the `Agent`-tool-with-explicit-pin path for Claude-lane work. Also fixed: the "Everything else... is a C1/C2 lane's job" line (→ "a routed lane's job"), the native-primitives paragraph's "multi-model lanes (Grok/Gemini/Cursor/DeepSeek/C3)" (→ "non-Claude capability lanes (Codex/GPT/Gemini via dispatch.py)"), the guardrails "C1 is four executors" bullet (→ "Route by capability (Layer 1), bind the model in Layer 2"), two stray `PNN_return.md` mentions (→ `TASK-NNN_return.md`, matching this very return's filename), and one stray "C3 consult" (→ "CHALLENGE consult"). |
| `.claude/agents/adversarial-qa-agent.md` | **Edited (frontmatter only)** | `model_routing` block: "the orchestrator may... route a purely mechanical sub-check... to a cheaper C1/C2 executor by route tag" → named the CHALLENGE capability explicitly, the cross-vendor invariant (Opus challenges Codex/GPT; gpt-5.5-pro challenges Claude/Gemini), and the GRUNT capability via `dispatch.py` for mechanical sub-checks. Rest of file (the two-track V/C mission, findings taxonomy, checklists) untouched. |
| `.claude/agents/content-agent.md` | **Edited (frontmatter only)** | `model_routing` block: "Claude C1 build lane... route a piece to another C1 executor (C1-GEMINI/C1-GROK)" → CONTENT capability (Layer 2: primary claude-fable-5, fallback claude-sonnet-5), two-gate DRAFT status, retired lanes named as killed. |
| `.claude/agents/data-agent.md` | **Edited (frontmatter only)** | Same pattern → BUILD-HEAVY/BUILD-LIGHT capability, Claude-side fallback behind Codex (`build_heavy`/`build_light`), fallback trigger stated. |
| `.claude/agents/design-agent.md` | **Edited (frontmatter only)** | Same pattern, plus the extra `C1-CURSOR` mention → VISION-LONGREAD capability, Claude-side fallback consumer behind Gemini/Antigravity (pin-gated per fn.2). No "Cursor Handoff Protocol" string exists anywhere in this file (checked — 0 matches), so the design-spec-doc carve-out in the task brief did not apply; nothing else needed touching. |
| `.claude/agents/frontend-agent.md` | **Edited (frontmatter only)** | Same pattern → BUILD-HEAVY/BUILD-LIGHT capability, named the Layer-2 pipe text "claude-sonnet-5 (Frontend/Data agent)" verbatim. |
| `.claude/agents/marketing-agent.md` | **Edited (frontmatter only)** | Same pattern → GENERAL capability (no dedicated Layer-1 row for marketing strategy), with a note that consumer-facing copy this persona drafts still routes through the CONTENT two-gate. (Note: this file also carries substantial pre-existing uncommitted changes from a prior session — TASK-505 rebuild — unrelated to this task; only the `model_routing` block is this task's edit.) |
| `.claude/agents/nutrition-agent.md` | **Edited (frontmatter only)** | Same pattern → DOMAIN-JUDGMENT capability, quoting the Layer-2 pipe text verbatim ("Nutrition/Product agents, pinned"). |
| `.claude/agents/product-agent.md` | **Edited (frontmatter only)** | Same pattern → DOMAIN-JUDGMENT capability, same pipe text. Left the unrelated "the orchestrator, C4" mention in the mission prose untouched — that names the orchestrator entity, not a v4.2 dispatch lane, and CLAUDE.md's own live text still uses "Opus/C4" for the orchestrator. |
| `.claude/agents/research-agent.md` | **Edited (frontmatter only)** | Same pattern → EVIDENCE-RESEARCH capability, Claude-side fallback behind Codex/GPT + web search, fallback trigger (API error or 120s timeout) stated. |

All 9 files edited (0 clean). Total: 10 hunks — 1 large multi-section edit in
`orchestrate.md` (5 separate `Edit` calls covering steps 3/4, the return-file naming, the
native-primitives paragraph, and the guardrails bullet) plus 8 single-block
`model_routing` rewrites, one per agent file. Verified with a final repo-wide grep across
all 9 target files for `P-[0-9]|dispatch\.py PNN|--route|Grok|Cursor|DeepSeek|C1-GEMINI|
C1-GROK|C1-CURSOR|bari_router_v4_2|Sonnet-default|four executors` — **zero matches**.

## Constraints honored

- Two-gate copy law text, tripwires, agent missions/checklists/domain content: byte-for-byte
  untouched except where a routing-lane reference was embedded inline (none were).
- No em-dash flooding beyond the codebase's existing house style; no "X, not Y" phrasing
  introduced.
- Worked directly in the local tree `C:\Bari`; nothing committed — left for orchestrator
  review, since these are governed `.claude/` files.

## Self-verification

- Ran the final grep above (see result: zero matches for retired-lane terms across all 9
  files).
- Read back every edited frontmatter block via the Edit tool's built-in diff before
  moving to the next file; no partial/garbled YAML.
- Confirmed `orchestrate.md`'s new capability-lane bullets name real functions that exist
  in `03_operations/router/dispatch.py` (checked via `grep -n "^def "` against the file:
  `build_heavy`, `build_light`, `grunt_primary`, `challenge_gpt`,
  `evidence_research_fallback`, `engineering_research`, `vision_longread` all present).

## Known caveats / not done here

- `.claude/agents/marketing-agent.md` and (per initial `git status`) several other files
  in this repo already carried unrelated pre-existing uncommitted diffs before this task
  started (a prior TASK-505 rebuild). This task's edits are additive on top of that; the
  orchestrator's review diff for those files will show more than this task's own hunk —
  flagged here so it isn't mistaken for scope creep.
- This return itself is a C7-flagged artifact by definition: it documents writes under
  `.claude/`. Per the return contract, that containment flag is expected here and the
  orchestrator should read the actual diffs (not just this table) before accepting.

## Return contract

```json
{
  "task": "TASK-586",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": ".claude/commands/orchestrate.md", "action": "modified",
     "sha256": "c6afda3ca69260b247178fa2d3b8749be44f7873945aefbb9daf0bd86f623cb5"},
    {"path": ".claude/agents/adversarial-qa-agent.md", "action": "modified",
     "sha256": "d39e41e2c5517f4d8ae1b651f5adff46c31ef6548c8571dda87bc6ffa8887585"},
    {"path": ".claude/agents/content-agent.md", "action": "modified",
     "sha256": "e687b6003f131d4bdf756d8b5afc0e8e15be49c5418caf4321c9ffa7f9eda4a2"},
    {"path": ".claude/agents/data-agent.md", "action": "modified",
     "sha256": "06eaf35bacaf7d3fa03fd508fa9bc5f7297691b11aeac5bf15c4602c5bff3f3c"},
    {"path": ".claude/agents/design-agent.md", "action": "modified",
     "sha256": "449233d020640acc423f76715bc492b41317b929330db8f92f2f161861884c20"},
    {"path": ".claude/agents/frontend-agent.md", "action": "modified",
     "sha256": "f20457a459fa20fda44600f1ce987106ffdd6f552dca2769a95e68716452d0d1"},
    {"path": ".claude/agents/marketing-agent.md", "action": "modified",
     "sha256": "50c70e29a868a58184ca17a3a11244aac1e76583b2935ff358cd113b1ed74475"},
    {"path": ".claude/agents/nutrition-agent.md", "action": "modified",
     "sha256": "db8663fb3c7152fd01a8299a053660cc6b59d9a4a3fd7140030804ca747c4190"},
    {"path": ".claude/agents/product-agent.md", "action": "modified",
     "sha256": "4d58018cfd96d939410064084a572980111f370707b4fe87060596ea03e95aad"},
    {"path": ".claude/agents/research-agent.md", "action": "modified",
     "sha256": "9585d78643e3e6d601b4c2425fee4bb6e36a12a190a9a614c4bf9c463d843b8b"}
  ],
  "counts": {
    "files_in_scope": "9/9 (1 command + 8 agent files named in the task)",
    "files_edited": "9/9 (0 reported clean — every file had at least one stale routing reference)",
    "files_clean": "0/9",
    "edit_hunks_applied": "13 total (5 in orchestrate.md covering the Lane/Dispatch sections, the C1/C2-lane phrase, the return-file naming, the native-primitives paragraph, and the guardrails bullet; 1 in adversarial-qa-agent.md's model_routing block; 1 model_routing block each in the remaining 7 agent files)",
    "stale_reference_matches_remaining": "0 (grep 'P-[0-9]|dispatch\\.py PNN|--route|Grok|Cursor|DeepSeek|C1-GEMINI|C1-GROK|C1-CURSOR|bari_router_v4_2|Sonnet-default|four executors' across all 9 files after edits)"
  },
  "commands_run": [
    {"cmd": "grep (Grep tool, output_mode content) each of the 9 files for P-[0-9]|dispatch.py|--route|Grok|Cursor|DeepSeek|C1|C2|C3|band|Gemini|Sonnet-only|route tag|prompt file|BAND=FUNCTION|opencode before editing", "exit_code": 0},
    {"cmd": "grep -n \"^def \" 03_operations/router/dispatch.py", "exit_code": 0},
    {"cmd": "grep 'P-[0-9]|dispatch\\.py PNN|--route|Grok|Cursor|DeepSeek|C1-GEMINI|C1-GROK|C1-CURSOR|bari_router_v4_2|Sonnet-default|four executors' across all 9 edited files (post-edit verification)", "exit_code": 0, "note": "0 matches, confirming clean"},
    {"cmd": "python 03_operations/validators/validate_return.py --md tasks/returns/TASK-586_return.md", "exit_code": 0}
  ],
  "not_done": [
    "No commit made — orchestrator reviews the diff and commits per this task's own instruction.",
    "marketing-agent.md's diff also contains unrelated pre-existing uncommitted changes from a prior TASK-505 session; not this task's scope to reconcile, flagged so it isn't mistaken for scope creep."
  ],
  "self_check": "Grep-surveyed all 9 target files for P-number/route-tag/Grok/Cursor/DeepSeek/C1-C2-C3-as-lane-name references before touching anything; edited each with scoped Edit-tool old_string/new_string calls confined to the model_routing frontmatter block (8 agent files) or the Lane/Dispatch/native-primitives/guardrails sections (orchestrate.md) — no mission, checklist, tripwire, or two-gate law text was in any old_string/new_string pair. Re-ran the stale-term grep across all 9 files post-edit: 0 matches. Cross-checked every dispatch.py lane function named in the new orchestrate.md text (build_heavy, build_light, grunt_primary, challenge_gpt, evidence_research_fallback, engineering_research, vision_longread) against `grep -n \"^def \" dispatch.py` — all present — and confirmed dispatch.py's main() has no --route/PNN CLI mode (only --selftest* flags), matching the claim that the router no longer reads a route tag off a prompt file. sha256 of each final file recorded above. Not committed (local-tree-only per instruction) — orchestrator reviews and commits."
}
```
