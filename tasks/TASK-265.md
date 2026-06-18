---
id: TASK-265
title: Factory trust layer 4b: dual-extractor consensus (Gemini vs replay_parse)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-13
closed_at: 2026-06-13
depends_on: [TASK-264]
blocks: []
category_id: null
close_reason: >
  P48 delivered 03_operations/spine/dual_extract.py — dual-extractor consensus (rule-based
  replay_parse vs Gemini CLI on the same raw HTML). Orchestrator-verified by independent live
  re-run: Gemini genuinely subprocess-called 3× (real latency, --skip-trust, HTML via stdin),
  extracted all fields independently incl. exact Hebrew ingredient strings; compare_field has
  real AGREE/DISAGREE tolerance logic (not copied from A). 27/27 fields AGREE, 3/3 Gemini calls
  OK, zero OFF, replay_parse unmodified. Gemini prompt forbids invention/external sources (OFF
  guard); consensus check is the fabrication detector (disagreement → FLAG, never silent-win).
  CAVEAT: disagreement-detection path is logically present but UNEXERCISED on clean synthetic
  HTML (everything agreed) — messy real-shelf HTML would exercise it. First real C1-GEMINI
  consensus job. Completes the factory trust layer (4a invariants + 4b dual-extractor).
summary: >
  Build dual_extract.py: same raw HTML through rule-based replay_parse (BSIP0-A) AND Gemini CLI extraction (BSIP0-B); field-by-field consensus; agreements=high-confidence, disagreements=flagged. Gemini extracts ONLY from the HTML (null if absent, never invent, no OFF). Run on e2e synthetic fixtures. Proves independent-failure-mode cross-check.
---

# TASK-265 — Factory trust layer 4b: dual-extractor consensus (Gemini vs replay_parse)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
