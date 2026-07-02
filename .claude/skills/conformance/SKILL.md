---
name: conformance
description: Check whether live Bari categories will re-flow on a scoring switch using the real affected_set mapper, and fix or delete any non-conformer. Use to verify the spine before/after a scoring change or before go-live.
---

# /conformance — Will every category re-flow on a score flip?

**Owner lane:** Orchestrator. Enforces the **zero-different-category mandate**: after the
sweep, no live category may be structurally "different" — each conforms to the uniform spine
path or is **DELETED entirely** (page + route). Delete is the default fallback; there is no
third option. `milk` is the one no-delete carve-out.

## Use this when
- "Run conformance", "do all categories still re-flow", "check the spine", before any go-live,
  and after any engine/generator change.

## Run it
```
python 03_operations/page_generator/conformance.py --all          # every configured shelf
python 03_operations/page_generator/conformance.py --slug <cat>   # one (route slug / name / config stem)
python 03_operations/page_generator/conformance.py --slug <cat> --json
```
It runs **3 HARD checks** through the REAL `affected_set` mapper (not a stub) to prove a live
category would re-flow on a score flip. Exit 2 = a non-conformer (or milk pause).

## What "conform" means (and what it does NOT)
- Conformance proves **reachability** — that a flip would re-flow the category. It does **not**
  prove detection-fidelity, correct data, or good copy. Never report "all conform" as "all
  correct". (See `done_means_rendered_redteamed_not_gate_pass`.)

## Fixing a non-conformer
```
python 03_operations/page_generator/onboard_category.py --slug <cat>
```
Maps each HARD failure id to a concrete, copy-pasteable fix. Apply the fix, re-run
`conformance --slug <cat>` until it passes. If a category is too bespoke to conform → **delete
it** (page + route) per the mandate, rather than special-casing the spine.

## Baseline (re-verify, do NOT freeze)
As of 2026-06-18: 12 conform / 0 deferred / 0 non-conforming. Bread re-flows as
`class=published`. Milk re-flows but pauses exit-2 for owner approval if it moves. Treat these
as numbers to re-verify on each run, never as values to hold fixed.

## Return contract
State the exact command run, the pass/fail per slug, and — honestly — that this is a
reachability check, not a correctness check. Separate verified from believed.

## Related
`rescore` (the flip this guards), `build-page`, `telemetry`.
