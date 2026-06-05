---
name: feedback-plain-english
description: "In ALL explanations, reports, and questions to the user, use plain English — no jargon, no internal field/file names"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b6225074-158c-4f75-b996-399c426d91ef
---

In EVERYTHING you say to the user — explanations, status reports, summaries, AND questions/choices — write in plain, everyday English. Do NOT use internal jargon, code identifiers, field names (`unknowns[]`, `metricSpecs`, `aria`, `rowReason`), task-chain shorthand, or git/engineering terms without explaining them in human language first. The user repeatedly could not understand questions phrased this way (2026-06-02, during TASK-161 roadmap), and on 2026-06-04 said the explanations were STILL too heavy with unnecessary jargon — so this applies to all prose, not only questions.

**Why:** the user is the product owner/decision-maker, not reading the code. A question they can't parse is a question they can't answer — it stalls the work and wastes a turn.

**How to apply:** Before asking, strip every technical term. Say what the thing IS and why it matters to the product/user, not what it's called in the code. Example: not "fix the vegetable-spreads aria unit" → instead "the protein bar's screen-reader label says the wrong unit (ml vs grams)." If a choice is just engineering housekeeping with no product impact, say so plainly or just pick the sensible default and proceed. Relates to [[feedback_cc_recommendations]] and [[feedback_implementation]].
