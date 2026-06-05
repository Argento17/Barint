---
name: decision-authority-matrix
description: Autonomy-default decision law — agents/orchestrator/CC/Product act by default; owner makes only the 5 strategic-tripwire calls
metadata: 
  node_type: memory
  type: project
  originSessionId: d33fa356-0a99-43d0-b5d3-f0f0c920a9ef
---

Owner directive (2026-06-04): **be more autonomous across all agents; owner makes extremely strategic decisions only.** Confirmed the boundary = exactly **5 escalation tripwires** and chose "write the law + update everything."

**The law:** `01_framework/governance/decision_authority_matrix_v1.md` (authoritative). Core rule = **default to autonomous action; if unsure whether a wire fires, it didn't — act, keep reversible, log.** Escalate to owner ONLY if a decision: (1) touches a **frozen invariant** / published scores / scoring philosophy; (2) ships something **irreversible AND consumer-facing** (category go-live, public claim, brand/positioning); (3) **starts or kills a major program**; (4) creates **external commitment / spend / legal exposure**; (5) **redefines strategy, target user, or what Bari is.** Triage = Reversibility × Blast radius; only the one-way+whole-product cell is the owner's. Mid-tier (beyond a lane, no wire) routes to Product / Orchestrator / CC — never the owner.

**Wired in:** CLAUDE.md got a new "## Decision authority (autonomy default)" section + the old broad escalation line in §Tasks narrowed ("judgement calls resolve autonomously by default"). All 10 agent files got an identical "## Autonomy Mandate" section before "## Escalation Rules" (Product + CC variants note they absorb the mid-tier).

**Why:** keeps owner out of expert/mid-tier calls; safe because reversibility is the default (flag-gating à la `BARI_RECAL_*`, CC close-readiness gate, registry audit log, PR-not-direct-to-main). Builds on [[feedback_agent_recommends_best]] (no A/B menus for expert calls) and [[cc_agent_v2_upgrade]] (CC closing authority).

**How to apply:** before asking the owner anything, check the 5 wires; if none fire, decide and act. Reserve AskUserQuestion for genuine wire-trips (strategy/scope/irreversible/spend).
