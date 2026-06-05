---
name: feedback_cc_recommendations
description: "When operating the Command Center / registry, surface recommendations but don't offer to apply them — the user applies adjustments themselves"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9639d7d2-d382-49bc-8a0a-2b9fdecec3dc
---

When running CC Agent / Command Center work (registry, dashboard, drift, decision maps), **report findings and recommendations, then stop**. Do NOT end turns with "want me to apply X / dispatch Y / fix the tooling?" offers for command-center adjustments.

**Why:** the user reads the recommendations and makes the registry/tooling adjustments themselves (e.g. manually setting tasks to CLOSED, applying fixes). They find that faster and more token-efficient than me offering and waiting.

**How to apply:** give the analysis + concrete recommended action (file, exact change), let the user execute. Still fine to *do* work that was already approved/dispatched; this is specifically about not appending optional "shall I adjust the command center?" prompts. Relates to [[feedback_implementation]] (make changes directly when asked) — here the user prefers to apply CC adjustments themselves.
