---
id: TASK-593
title: verify_citations.py selftest TC-1 red: same-domain author swap not caught (corroboration parses no author/year, conservative-passes)
owner: data-agent
status: IN_PROGRESS
priority: LOW
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
summary: >
  Found during TASK-566 verification (2026-07-11, pre-existing via stash test): --selftest is 6/7 - TC-1 expects corroborated=False on a Thorning->Salas-Salvado author swap but the corroboration step finds 'no parseable author/year in context' and conservative-passes. Either the TC-1 fixture context lacks the author/year cue the parser expects, or the parser misses a real cue format. A permanently-red selftest is the 'gate error indistinguishable from success' class TASK-566 fixed elsewhere. Live PubMed connectivity check passes; the other 6 cases green.
---

# TASK-593 — verify_citations.py selftest TC-1 red: same-domain author swap not caught (corroboration parses no author/year, conservative-passes)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
