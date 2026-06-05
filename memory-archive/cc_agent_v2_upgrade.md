---
name: cc-agent-v2-upgrade
description: CC Agent v2.0 — granted full closing authority (gated by independent verification) plus borrowed orchestrator best practices; what changed and the governance reconciliation
metadata: 
  node_type: memory
  type: project
  originSessionId: 9093f0b6-f985-49cc-890e-6109f9a49062
---

**CC Agent upgraded to v2.0 on 2026-06-02** (`.claude/agents/cc-agent.md`), to give CC more
responsibility as the central controller. Driven by the user; grounded in web research on Claude
orchestrator best practices (Anthropic multi-agent research system; Claude Code Agent Teams docs;
metaswarm self-improving controller framework).

**The big change — full closing authority, gated by verification.** CC v1 "proposed, never closed"
(human-Controller-only `CLOSED`). CC v2 **records `CLOSED` itself** after its **close-readiness gate**:
re-read DoD → verify each return-block claim against the actual artifact (file:line / real number, NOT
the agent's prose) → look for unstated side effects (silent drift) → risk-classify → close + cite evidence
in `close_reason`, OR escalate genuine judgement calls (accept/reject tradeoffs, prioritization, governance).
Core principle borrowed from metaswarm: **"trust nothing, verify everything"** — a return block is a claim,
not proof. (This is exactly how the maadanim editorial drift was caught.)

**Other v2 capabilities added to cc-agent.md:** 5-part delegation spec (objective / boundaries / inputs /
deliverable+return-format / guards) for every hand-off; effort & parallelism scaling rubric (trivial→inline …
cross-domain→parallel with file-ownership split, ≤3 active); adversarial review gate for high-stakes
(second different-domain agent co-signs before close); self-improvement loop (user correction → feedback
memory → propose a skill/hook if recurring).

**Enforcement (hooks, not goodwill):** see [[cc-comments-dashboard]] for the roadmap-review automation —
`roadmap_impact: true` → dashboard `ROADMAP_REVIEW` alert + PostToolUse regen/nudge; and a **PreToolUse guard**
`.claude/hooks/guard-roadmap-close.ps1` HARD-BLOCKS closing a `roadmap_impact` task until `cc_reviewed` is set
(verified: block exits 2, allow exits 0).

**Governance reconciliation (the constitutional change).** "Only the Central Controller records CLOSED"
appears across the corpus. Amended the two OPERATIVE sources to add the delegation: `CLAUDE.md` lifecycle line
+ `registry_protocol_v1.md` §1 (now: closing authority = Central Controller AND delegated CC Agent, under the
verification gate; "Central Controller" in those docs reads to include CC). **NOT yet reconciled (flagged, lower
priority — they still say Controller-only):** `registry_first_rule_v1.md`, `operating_model_v2.md`,
`task_creation_protocol_v1.md`, `tasks/_README.md`. Domain agents still NEVER write CLOSED — unchanged.

**Orchestration model + invocation (2026-06-02).** Main chat = the orchestrator (only it can spawn agents;
subagents can't spawn subagents). Default = **direct dispatch**: spawn owning agents via the Agent tool with
the 5-part delegation spec, parallel/background — NO prompts handed to the user to paste. Execution lives in
subagents (own context window; only summaries return) → keeps main context lean; start a **fresh chat per
phase** and rebuild state with `/roadmap`. Full model: `01_framework/operations/orchestration_model_v1.md`;
standing rule added to CLAUDE.md.
- **Slash commands:** `.claude/commands/roadmap.md` (`/roadmap` → live decision map) and `cc.md`
  (`/cc <q/op>` → ad-hoc CC query/close/open).
- **VERIFIED platform limit (don't re-attempt):** no Claude Code hook can spawn an agent, and `SubagentStop`
  CANNOT inject context/nudge the parent (no additionalContext; exit-2 only blocks the subagent, stderr→user).
  So "auto-invoke CC after each agent" is an **orchestrator instruction in CLAUDE.md**, NOT a hook. Backstops:
  PostToolUse dashboard regen + `ROADMAP_REVIEW` alert + the PreToolUse close-guard.
Related: [[feedback_cc_recommendations]], [[cc_v3_1_upgrade]], [[cc_comments_dashboard]].
