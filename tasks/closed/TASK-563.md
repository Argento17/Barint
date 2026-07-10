---
id: TASK-563
title: Published pages are not re-derivable from the traces their configs reference (14/16 live shelves)
owner: data-agent
status: CLOSED
closed_at: 2026-07-10
close_reason: >
  Orchestrator-verified 2026-07-10. Data Agent census + remediation: 2 shelves RE-POINTED to the real persisted trace runs (hard_cheeses -> run_hc_task418_clean 31/31 exact; snacks -> snacks_task413_staging 21/21 exact) - orchestrator independently re-ran G5 on both = PASS, committed d187a92c; 5 shelves already conformed; bread handled under TASK-561. 8 shelves NOT RECOVERABLE by construction: _task409_rederive_v2.py scored in-memory and wrote into live JSON without persisting traces (brined_cheeses, cakes, cereals, cheese, chocolate_bars, chocolate_tablets, cookies_coffee, protein_bars). Published numbers presumed correct; per-product provenance for those 8 does not exist on disk. OWNER DECISION PENDING (digest): uniform re-derive (moves published numbers = tripwire, movement table first) OR formally accept published-JSON-as-record; forward-protection already live (conformance_gate 16/16 + G5 wired for the 11 recoverable). First return failed C0 (malformed contract keys) -> CHANGES_REQUESTED -> agent fixed; validator now exit 0, re-verified by orchestrator. Bonus finding routed: granola consumerExplanation-as-string crashes run_gates (folded into TASK-574 lane). Paper-trail state: 11/16 shelves auditable, 8... see above.
priority: CRITICAL
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Found while probing run_gates for CI (TASK-565). Read-only census of all 16 live shelves: the served frontend JSON's _meta.run_id disagrees with the run_products_dir its page_generator config points at on 14/16 shelves; 12/16 carry bespoke re-score markers (reflow / deanchor_meta_regenerated / p461_construction). brined_cheeses _meta records method='live_json_score_grade_swap_rerank' -- scores were written straight into the live JSON on 2026-07-02 (TASK-442/395 de-anchor, BARI_REDLABEL_CONTINUOUS_V1=on) while run_brined_005 traces date from 2026-06-17. Consequence: run_gates G5 GRADE-INTEGRITY fails on 10/16 shelves with published score != trace score (e.g. brined_cheeses barcode 7290019635826: page 76.1 / grade B vs trace score_after_penalty 85.42; hard_cheeses 4137311: 76.8 vs 70.8). The engine arithmetic in the trace is internally consistent (score_after_cap 97.42 - penalty 12.0 = 85.42), so this is NOT the TASK-552 ledger gap. NO SCORE WAS CHANGED and none should be without owner direction: the published numbers may well be correct and the TRACES stale. What is established is that published scores currently cannot be audited against the trace their own config names. Directly implicates the uniform-baseline doctrine (bespoke live-JSON swap paths) and the corpus-traceability program (TASK-405). Decide: re-generate traces to match published pages, re-point configs at the runs that actually produced them, or re-derive pages through the uniform path (score-moving -> owner tripwire).
---

# TASK-563 — Published pages are not re-derivable from the traces their configs reference (14/16 live shelves)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
