---
id: TASK-472
title: Crackers provenance repair: wire bread-corpus BSIP1 source paths into crackers BSIP2 traces
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-03
verified_at: 2026-07-03
depends_on: []
blocks: []
category_id: crackers
summary: >
  P1 item 9b / report F3. Crackers were scraped inside the bread corpus; BSIP2 traces carry bsip1_source_path=null and empty ingredients_list while displayed data is accurate. Wire the real bread-corpus BSIP1 source paths (run_crackers_conform_001, audit_ref bsip0_real_bread_retail_003_v1) into the crackers records. Audit-trail repair ONLY — zero change to displayed data, scores, grades.
---

# TASK-472 — Crackers provenance repair: wire bread-corpus BSIP1 source paths into crackers BSIP2 traces

## Status: VERIFIED — PR #56 open, pending owner merge (non-consumer-facing)

**Deliverable (Data Agent, `tasks/returns/TASK-472_return.md`):** all 20 crackers BSIP2 trace records had `input_reference.bsip1_source_path: null`; each now wired to its real barcode-matched BSIP1 file (`run_crackers_conform_001/output/bsip1_<barcode>.json`).

**Orchestrator verification (independent, against artifacts):**
- C0 gate (`validate_return.py --json`): all 20 sha256 re-hashes PASS, all count checks PASS.
- Isolation vs origin/master (in worktree): 20 files, one JSON leaf each (20 ins / 20 del), **0 non-`bsip1_source_path` lines changed**.
- Anti-collapse (Rule-5 substance, proven directly): 20 **distinct** source paths, 0 reused, 20/20 barcode-identity match (trace barcode == source-file barcode), 0 left null.
- Not consumer-facing — trace/provenance metadata only; nothing rendered changes.
- `ingredients_list` deliberately not backfilled (BSIP2 passes BSIP1's own empty list through verbatim; separate schema decision — correctly flagged, not actioned).

**Ship:** branch `fix/task472-crackers-provenance` → **PR #56** (https://github.com/Argento17/Barint/pull/56). CLOSE on owner merge.

**Tooling notes surfaced (→ backlog):** (1) `validate_return.py` `extract_contract` mis-pairs the fence regex when a ` ```diff ` block precedes the ` ```json ` contract → LOAD ERROR on a valid contract; fix: match only `json` fences. (2) Return contract should carry a distribution marker (stdev + most_common) on full-set claims to satisfy `C5.dist` without an orchestrator hand-proof.
