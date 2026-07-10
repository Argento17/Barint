# TASK-561 — Decision: Bread live-route cutover

**Decision: Option (a).** Re-point `baseline_json` in `03_operations\page_generator\configs\bread.json`
from `bread_frontend_v3.json` to `bread_frontend_v4.json`. No other config field changes.

## Rationale

The actual defect is spine integrity, not scoring: the config's job is to describe what the
site serves, and right now it describes an orphaned file. `bread-comparison-page-data.ts`
imports `bread_frontend_v4.json` (23 products) — confirmed by direct grep
(`import rawCorpus from "@/data/comparisons/bread_frontend_v4.json"` at
`bari-web\src\lib\comparisons\bread-comparison-page-data.ts:3`) — while `bread.json` still
points `baseline_json` at `bread_frontend_v3.json` (29 products). Every day this stands, a
`spine_flip` re-flows into a file nobody serves; the live page silently goes stale relative to
whatever the pipeline believes is current. That is the HARD-3-baseline_served non-conformer
TASK-560 surfaced and deliberately declined to silently fix.

Weighed against the other two options:

- **(b) re-derive v4 through the config now** would move a published score (-0.8 pts, one
  survivor) via an unrelated post-v3 router rule that was never diagnosed, only shelved. That's
  a scoring-philosophy-adjacent change and a live-category score movement — tripwire territory
  (decision_authority_matrix tripwire 1) — not something this paper-trail task should force
  through. It also was **explicitly rejected** once already (config `_comment`, TASK-433) with
  no new evidence presented today that changes that call. Recommending it now without a
  Nutrition read on whether that router-rule drift is *correct* behavior or a bug would be
  manufacturing a scoring decision, not making a wiring one. Out of scope for today.
- **(c) accept v3 as score-of-record, keep documenting the exception** fixes nothing. It
  formalizes a config that still names a file the site does not read, so the spine_flip
  orphaning behavior TASK-560 flagged continues indefinitely. It also conflicts with two
  standing rulings this workspace already holds: the re-flow policy ("nothing is frozen... no
  category-level freeze gate") and the uniform-baseline doctrine ("ONE engine + ONE
  generate_page path; no bespoke loaders"). A permanent documented exception is a freeze wearing
  a paperwork costume. Reject.

(a) is the only option that moves the config to match reality with **zero score movement
today** — v4 is byte-identical in scores/grades to v3 for the 23 surviving products (per the
TASK-433 membership-correction build, confirmed independently here: v3 = 29 products, v4 = 23
products, difference = 6, matching the 6 crackers-split exclusions already listed in
`bread.json`'s `exclusions` array). That satisfies the 0-score-movement preference for today's
change while putting the config back in a state where the re-flow policy can do its job — the
next *real* re-score (a flag/scoring change) is expected to move numbers and should be
re-verified, not pre-emptively frozen out of the spine by an exception entry.

## Exact config-field change (for the orchestrator/Data Agent to apply, not applied here)

File: `03_operations\page_generator\configs\bread.json`

- `baseline_json`: `"C:\\Bari\\bari-web\\src\\data\\comparisons\\bread_frontend_v3.json"` →
  `"C:\\Bari\\bari-web\\src\\data\\comparisons\\bread_frontend_v4.json"`
- `corpus_dirs` / `run_products_dir`: **unchanged.** Both already point at
  `run_bread_conform_001`, the same scoring lineage v4 was membership-corrected from, and the
  config's own `exclusions` array already lists all 6 crackers-split barcodes that separate the
  29-product v3 set from the 23-product v4 set. The scoring lineage and the frontend file are
  already aligned in membership — only the `baseline_json` pointer is stale.
- `_comment`: append a short CORRECTION note (mirroring the existing 2026-06-22 v2→v3
  correction note already in this file) recording: re-pointed 2026-07-10 per TASK-561; v4 is
  the file bari-web actually imports; v3 remains superseded, not deleted; the known -0.8pt
  router-rule drift on one survivor is un-resolved and will surface at the next real re-score,
  not from this repoint.

## Expected next-`spine_flip` behavior

- **Today, with no scoring flag change:** re-pointing alone moves no scores. If a flip runs
  immediately after this repoint with flags unchanged, output should diff byte-identical to the
  current v4 scores/grades for the 23 products (self-check for whoever applies this: run the
  flip and confirm 0 movement before treating the repoint as done).
- **At the next scoring-flag change that touches bread's affected_set:** the previously-shelved
  router-rule drift (-0.8 pts, one survivor) is expected to surface. Per the re-flow policy this
  is correct behavior to **verify, not suppress** — route it to Data Agent (re-derive) and
  Nutrition Agent (confirm the router rule's effect on that product is intended, not a bug)
  before that flip is treated as clean. This decision does not resolve that drift; it only stops
  the config from actively orphaning the served file while the drift remains open.

## Follow-up recommended (not decided here, not mine to dispatch)

Open a small follow-up task for Data + Nutrition to diagnose the post-v3 router rule causing the
-0.8pt drift on one bread survivor, so option (b) can be revisited on its own merits at the next
real bread re-score instead of being permanently deferred by default.

```json
{
  "task": "TASK-561",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "tasks/returns/TASK-561_decision.md", "action": "created", "sha256": "75aa5c32540ad757218a5c0a269dfa42347d8460d0db5a7dcb3255bc60a5d222"}
  ],
  "counts": {
    "bread_frontend_v3_products": "29/29 (bari-web/src/data/comparisons/bread_frontend_v3.json, counted via python json.load)",
    "bread_frontend_v4_products": "23/23 (bari-web/src/data/comparisons/bread_frontend_v4.json, counted via python json.load)",
    "v3_minus_v4_delta": "6/6 (29-23, matches count of TASK-433 crackers-split barcodes already listed in bread.json exclusions array)",
    "config_fields_changed_by_this_task": "0/0 (decision memo only; no config edited in this task)"
  },
  "commands_run": [
    {"cmd": "python -c \"import json; print(len(json.load(open('bread_frontend_v3.json'))))\" (bari-web/src/data/comparisons)", "exit_code": 0},
    {"cmd": "python -c \"import json; print(len(json.load(open('bread_frontend_v4.json'))))\" (bari-web/src/data/comparisons)", "exit_code": 0},
    {"cmd": "grep -n bread_frontend_v bari-web/src/lib/comparisons/bread-comparison-page-data.ts", "exit_code": 0}
  ],
  "not_done": [
    "Config edit itself (baseline_json repoint + _comment update) NOT applied — this task is decision-only per instructions; orchestrator/Data Agent applies after verification.",
    "Post-repoint zero-movement spine_flip self-check NOT run here — recommended as the first verification step after the edit lands.",
    "Router-rule -0.8pt drift diagnosis NOT performed — flagged as a follow-up task, out of scope for this decision."
  ],
  "self_check": "Acceptance test: does the decision file name exactly which config field(s) change, state the option chosen with rationale, and state expected next-spine_flip behavior, per the task's DELIVERABLE spec? Yes — see 'Exact config-field change' and 'Expected next-spine_flip behavior' sections above."
}
```
