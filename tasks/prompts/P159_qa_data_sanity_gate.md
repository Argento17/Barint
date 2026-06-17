# P159 / TASK-301 — QA data-sanity gate (route: C1-GROK)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Full repo access. Read `tasks/TASK-301.md` first.

## Why
The canonical re-baseline (TASK-298) exposed corrupt BSIP1 source data that flowed unchecked to staging pages:
5 granola products with impossible sodium (6,000–10,000 mg/100g; real granola ~30–100) and a hummus product
whose "ingredient list" is scraped nutrition-panel text. Nothing in the pipeline caught it. Add a deterministic
gate so this class of corruption can NEVER reach a published page.

## Build — add to the page gate suite `03_operations/page_generator/gates/run_gates.py`
Add a new gate (e.g. `G_DATA_SANITY`) that FAILS (non-zero exit, like other hard gates) when a product in the
generated page carries:
1. **Physically-impossible nutrition per 100g** — at minimum: `sodium_mg > 5000`. Also add sane upper bounds for the
   other panel fields per 100g (energy_kcal > 900, any macro gram-field > 100, e.g. fat/carbs/sugars/protein/fiber > 100,
   saturated_fat_g > 100). Any breach = ERROR naming the barcode + field + value.
2. **Ingredient field that is actually a nutrition panel** — the `ingredients`/ingredient string matches a
   nutrition-panel pattern: contains 2+ of these Hebrew tokens — `ערכים תזונתיים`, `קל` (as a standalone energy unit),
   `גרם חלבונים`, `גרם פחמימות`, `גרם שומנים`, `מג נתרן`, `סיבים תזונתיים` — i.e. the panel was scraped into the
   ingredient field. Any match = ERROR naming the barcode.
Wire it so `generate_page.py`'s self-gate AND `rescore_all.py` both fail on a corrupt shelf (they already invoke
run_gates). Match the existing gate output format (PASS/WARN/FAIL lines + the report .md). Determinism preserved.

## Verify it catches the known cases
Run the gate against the staging pages and confirm it FLAGS the known-bad records:
- granola: `7290017962047` (sodium 10000), `7290017962023` (7000), `7290106771161` (8000), `7290106771369` (6000), `7290106771314` (9000)
- hummus: `7296073705505` (ingredient = nutrition panel)
Confirm it does NOT false-positive on the clean shelves (cereals/juices/cakes/cookies/brined gate still PASS on real data).

## Boundaries
- Only touch `03_operations/page_generator/gates/run_gates.py` (+ its schema/helpers if needed). Do NOT touch the engine
  (`proto_v0/src/`), the configs, or any data/page. Do NOT fix the corrupt data itself (that's TASK-300, a parallel lane) —
  your job is the GATE that catches it.
- Do NOT commit, do NOT deploy. Flag (in the return, not as code) that a BSIP1-ingest-level validator is a recommended follow-up.

## Return
- The gate code added (file:line), the exact thresholds/tokens, and the gate-run output showing it FLAGS the 6 known-bad
  records and PASSES the 5 clean shelves. **Do not close — propose RETURNED.** End with the return contract JSON
  (`01_framework/operations/return_contract_v1.md`): `task`, `proposed_status`, `artifacts[]` (path+action+sha256),
  `counts{}` (records flagged / clean shelves passing, with the command), `commands_run[]` (cmd+exit), `not_done[]`, `self_check`.
