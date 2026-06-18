# P150 / Post-deploy smoke test — manifest-driven /hashvaot/* check (TASK-290) (route: C1-GROK)

## Repo / context
- Repo root: `C:\Bari` (you have repo access). Branch `master` (reconciled baseline).
- Read first: `C:\Bari\tasks\TASK-290.md`.
- Spine datastore: `03_operations/spine/spine.db` — rebuild with `python 03_operations/spine/ingest.py`.
  Table `live_state(data_file, category, version, run_id, product_count, generated_at, sha256)` = 17 rows,
  one per `bari-web/src/data/comparisons/*.json`.
- Existing skeleton: `03_operations/spine/smoke_test.py` — READ it and EXTEND; do not rewrite from scratch.
  Reference also the remote branch `bari/ci/prod-smoke`.
- Live site base URL: `https://bari.digital`; routes are `/hashvaot/<category>` (categories per
  `bari-web/src/lib/comparisons/registry`); milk legacy route is `/hashvaot/milk-comparison`.

## Objective
Finish `smoke_test.py` into a manifest-driven post-deploy smoke test:
1. Rebuild `spine.db`, read expected `version` + `product_count` per page from `live_state`.
2. For each live `/hashvaot/<category>` route: HTTP GET, assert HTTP 200.
3. OFF sweep: assert the served page contains ZERO OFF markers
   (`openfoodfacts|open_food_facts|off_api|off_candidate_panel`).
4. Freshness: assert the served page exposes the expected data version / product count from the manifest;
   report drift (served ≠ manifest) as a FINDING, not a crash.
5. Emit a per-route report (status · OFF count · expected vs served) and exit non-zero on any 200-fail or OFF>0.
- Runnable against prod (default) AND a local base URL (`--base-url` for `npm run dev`).
- If `bari.digital` is unreachable from your environment, still deliver the working script + a LOCAL
  dry-run (parse the committed JSON manifest) proving the logic, and document the prod wiring.

## Boundaries / guards
- READ-ONLY against the live site — HTTP GET only, never POST/deploy. This is not a deploy.
- OFF ban (TASK-238): the test DETECTS OFF; never introduce an OFF data source anywhere.
- Modify ONLY `smoke_test.py` (+ optionally one small CI/schedule wiring file under `.github/` or
  `03_operations/spine/`, clearly flagged). Do NOT touch the engine, scoring, or any comparison JSON.
- Do NOT commit, push, or close. Propose RETURNED.

## Return format
- Diff summary of `smoke_test.py` + exact run commands.
- A sample run output (prod or local dry-run) showing the per-route table.
- CI/schedule wiring (file + mechanism), if added.
- End with the machine-readable return contract (`01_framework/operations/return_contract_v1.md`, status RETURNED).
