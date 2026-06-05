---
name: feedback-agent-recommends-best
description: "For a domain decision, delegate to the owning specialist agent to RECOMMEND the single best option — don't hand the user a menu to pick from"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b6225074-158c-4f75-b996-399c426d91ef
---

When a decision sits inside a specialist agent's domain (Design/UX, Nutrition, Content, Data, Product, etc.), **delegate it to that agent and have the agent recommend the single best option with rationale — then implement it.** Do NOT present the user a list of options ("A or B?") to choose from for expert/domain calls.

**Why:** the user wants the expert agents to exercise judgment and make the call, not to be the tiebreaker on things the agents are supposed to decide. Offering a menu pushes expert work back onto the owner. (Established 2026-06-02 on the vegetable-spreads metric-bar question: the orchestrator offered "no bar vs sodium bar"; the owner said the agent should just recommend the best — "that's how it should work going forward.")

**How to apply:** identify the owning agent → dispatch with "recommend the single best X and why" → implement the recommendation → report what was decided + done (and why). The user weighs in only on genuine owner-level calls: strategy, scope, taste, and irreversible/outward-facing actions. Relates to [[feedback_agent_recommends_best]] cousin [[feedback_cc_recommendations]] (CC: surface + stop) and [[feedback_plain_english]].
