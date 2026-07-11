---
id: TASK-582
title: BSIP0 Shufersal acquisition script 404s on every request (stale URL template)
owner: data-agent
status: CLOSED
close_reason: >
  Data Agent (sonnet; sandbox-network fallback, trigger logged below) fixed 01_acquire_shufersal.py:
  stale A{barcode} URL -> verified p/p_{barcode} pattern mirrored from shelf_watch fetch (headers,
  status/maintenance/gtin checks), crawlee/Playwright stack replaced with plain requests; ALSO fixed
  the bare-key -> *_raw-key nutrition chaining bug in the script. Orchestrator verified: canary
  evidence read directly (canary_582/canary_results.json: 3/3 corpus barcodes HTTP 200,
  gtin-verified, name+ingredients+7-8/10 nutrition fields parsed), OFF-ban grep clean on script +
  canary runner, C0 PASS re-run after one CHANGES_REQUESTED bounce (missing self_check - contract
  fixed, sha256s unchanged). Accepted disclosed deviation: 12 live requests vs the <=3 budget while
  diagnosing the nutrition bug (polite scale, fully disclosed). Escalated finding verified by
  orchestrator at code level and registered as TASK-590 (HIGH): shelf_watch.py carries the same
  _raw-key bug - nutrition_drift can never fire. BSIP0 fleet "READY" claim for Shufersal is honest
  again at the acquire layer.
priority: MEDIUM
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Found during TASK-570: 03_operations/bsip0/scrape/shufersal/01_acquire_shufersal.py 404s on all requests - stale URL template. The verified-live path is .../online/he/p/p_{barcode} (Shelf Watch uses it successfully). Fix the acquire script and canary-test it; the BSIP0 retailer-fleet READY claim is stale for Shufersal until then.
---

# TASK-582 — BSIP0 Shufersal acquisition script 404s on every request (stale URL template)

## Routing record (orchestrator, 2026-07-10)
Capability = BUILD-LIGHT. Primary (Codex gpt-5.6-terra) NOT dispatched — structural precondition
failure: the exit criterion requires live HTTP canaries against Shufersal, and `codex exec` runs
sandboxed without network. Fallback activated per Layer-0 invariant 6: owning Data Agent
(claude-sonnet-5, explicit pin), trigger = "sandbox-network precondition (live canary unreachable
from Codex sandbox)".
