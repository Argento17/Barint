---
id: TASK-583
title: LLM router redesign v5: kill Grok/Cursor/DeepSeek lanes, integrate OpenAI Codex, re-place Gemini, evaluate Qwen-via-opencode grunt lane, hard-stone architecture
owner: orchestrator
status: CLOSED
closed_at: 2026-07-10
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
close_reason: >
  Verified against artifacts. Owner approved the architecture after 3 challenge rounds
  (granular pins -> attribute routing -> Capability Router). Law written and committed:
  01_framework/operations/capability_router_v5.md (Layer 0 invariants / Layer 1 twelve
  ordered capability questions with exit criteria / Layer 2 model binding). dispatch.py
  rewritten 1574->1322 lines by build-583 (claude-sonnet-5 = BUILD-HEAVY FALLBACK, trigger
  "codex OAuth pending" - the router's first dogfooded routing decision, logged).
  Orchestrator re-ran: py_compile OK, --selftest-table PASS (code byte-matches doc, still
  green after footnote corrections), --selftest-route 14/14, grep kill-proof 0 grok/cursor/
  deepseek references, branch task583-router-v5 @ cb35627a confirmed pushed, C0 VERDICT PASS
  (validator itself re-executed all 13 claimed commands, all exit codes matched). Agent
  judgment call accepted and documented: retired the whole v4.2 P-number/route-tag flow.
  Two agent findings adjudicated: codex exec --search invalid on 0.144.1 (law footnote
  corrected, fix at pin time); gemini-cli crash root cause = UNSUPPORTED_CLIENT on this tier,
  NOT stale login - working binary is Antigravity agy.exe v1.1.0 (orchestrator found it via
  old dispatch.py; sentinel probe FAILED today so lane stays pin-gated). Follow-ups:
  TASK-585 (PIN-AT-AUTH: codex tiers post-owner-OAuth, agy revival, --search fix),
  TASK-586 (9 governed docs still describe P-number dispatch). Memory: bari_capability_
  router_v5 written, v4.2 + killed-lane index lines superseded. Owner PR merge pending.

summary: >
  Owner directive 2026-07-10: (1) kill Grok + Cursor CLI lanes; (2) Gemini subscription stays - find its right placement (currently misused); (3) OpenAI Codex subscription now available, fully trusted for tasks; (4) kill DeepSeek; evaluate Qwen models via opencode CLI as the open-source grunt lane; (5) deliver a clear hard-stoned router architecture after evaluation. Owner approves the architecture before implementation.
---

# TASK-583 — LLM router redesign v5: kill Grok/Cursor/DeepSeek lanes, integrate OpenAI Codex, re-place Gemini, evaluate Qwen-via-opencode grunt lane, hard-stone architecture

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
