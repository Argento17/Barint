---
id: TASK-630
title: Wire re-scored traces (bread/crackers/cheese) into PD read-path so calc becomes derivable + fix parity_gate cp1252 print bug
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-07-11
depends_on: []
blocks: []
category_id: null
origin_task: TASK-629
lesson_trigger: correction
lesson_outcome: immediate_fix
lesson_artifact: 03_operations/product_dossier/parity_gate.py
lesson_validator: python 03_operations/product_dossier/parity_gate.py --selftest
lesson_evidence: main-tree build_dossiers rebuild flipped 52 calc-FAILs to PASS (bread 23/23, crackers 0 fail, cheese 45/47, protein_bars 32/32); parity_gate diverge=0 (matched=704 agree=704); parity_gate --selftest PASS; scores byte-identical to served.
close_reason: >
  VERIFIED + committed (traces 8f706b0c; config-order fix aa05de42). Surgical trace-backfill of the 52
  TASK-629-corrected barcodes (bread 18 / crackers 17 / cheese 17) emitted at new run dirs, appended to
  each shelf config's run_products_dir. Main-tree build_dossiers rebuild confirmed the flip: bread 23/23
  calc PASS, crackers 0 calc fail (19 pass + 34 warn), cheese 45/47 pass, protein_bars 32/32. Aggregate
  calc fail 111 -> 61 (-50). parity_gate diverge=0 (matched=704 agree=704); the 6 gaps are legacy
  bread_frontend_v3.json (deferred v3 retirement, not a regression). Scores UNCHANGED (backfill asserts
  score-identity vs served; served JSON untouched). parity_gate.py cp1252 print crash fixed (hasattr
  reconfigure guard) + selftest PASS. CORRECTION codified: my dispatch spec told Codex 'later dir
  overrides earlier' but build_dossiers.py L349 is FIRST-dir-wins (traces.setdefault) -- backfill dir
  was placed second and did not override until I swapped it first. RESIDUAL (out of 630 scope): 2 cheese
  products (7290019635383, 56272) have a pre-existing 0.2pt JSON-vs-trace rounding mismatch, NOT in the
  629-corrected set -- a separate micro-derivability gap.
summary: >
  TASK-629 re-scored bread/crackers/cheese (scores correct, parity diverge=0) but calc check FAILS (18+17+17) because the new BSIP2 traces (task629_corrected/output) aren't wired into the shelf configs' run_products_dir that build_dossiers reads -> served-new vs trace-old mismatch. Repoint configs at the re-scored traces (same trace-backfill pattern as protein_bars 32/32 pass) -> calc flips pass. Also fix parity_gate.py UnicodeEncodeError on cp1252 (Hebrew print).
---

# TASK-630 — Wire re-scored traces into PD read-path

Trace-wiring gap fix. See close_reason. Backfill dir MUST be FIRST in run_products_dir (build_dossiers is first-dir-wins, L349).
