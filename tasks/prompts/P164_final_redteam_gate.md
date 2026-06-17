# P164 / TASK-311 — Final red-team gate on the assembled re-baseline pages (route: Red-Team Agent)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. The 7 re-baselined pages were assembled into bari-web (TASK-310, overlay-merge, orchestrator-verified). Your job = Stage-9 red_team_gate: adversarially tear the FINISHED pages apart before the owner is asked to push. You do NOT fix, NOT approve, NOT close. Produce a structured CRITICAL/HIGH/MED report. Owner-ready ONLY at zero CRITICAL.

## In scope (the assembled live JSONs + their routes)
| JSON (bari-web/src/data/comparisons/) | route(s) |
|---|---|
| cereals_frontend_v2.json | /hashvaot/breakfast-cereals |
| cakes_hard_cookies_frontend_v1.json | /hashvaot/cakes (+ /cakes-hard-cookies) |
| cookies_coffee_frontend_v2.json | /hashvaot/cookies-coffee |
| granola_frontend_v1.json | /hashvaot/granola |
| juices_frontend_v3.json | /hashvaot/juices |
| brined_cheeses_frontend_v2.json | /hashvaot/brined-cheeses |
| hummus_frontend_v5.json | /hashvaot/hummus **AND** /hashvaot/vegetable-spreads (shares this file; lenses key on _product_type) |

## Tear-down checklist (find what's broken/weak/false — assume it's wrong until proven)
1. **Build.** `cd bari-web && npx tsc --noEmit` (0 errors) + `npm run build` (capture real exit code). Any error = CRITICAL.
2. **Images resolve.** Every displayed product's `imageUrl` must be a real, resolvable asset (not a dead host, not OFF, not a 404 path). Sample broadly; list any that won't load. Dead/placeholder images on displayed products = HIGH (CRITICAL if widespread).
3. **Dropdowns / shelf filters / lenses complete.** Each page's filters populate and return products; specifically confirm /vegetable-spreads matbucha/eggplant/pepper lenses still populate from `_product_type` (10/7/5 expected) and the hummus page renders dips-only (57, no raw chickpeas). Empty/broken filter = HIGH.
4. **score == trace.** Page score must equal the AUTHORITATIVE re-baseline score = the staging rescored value (`_rescore_staging/<shelf>/<shelf>_rescored.json`), NOT the raw run `bsip2_trace.json` (shelf-relative shelves legitimately differ from raw run scores — e.g. granola 7290011131968 raw 38.3 → published 46.6 is BY DESIGN). Flag only genuine page≠staging mismatches. (Orchestrator already verified 0 page≠staging across all 7 — re-confirm independently and challenge if you find otherwise.)
5. **OFF = 0.** Zero Open Food Facts data in ANY product field (nutrition/ingredients/name/barcode/image/serving/etc.). `_meta` text that *documents* the OFF exclusion is allowed; OFF *data in a product* = CRITICAL launch blocker.
6. **Content coherence (read the Hebrew).** For grade-changed + net-new products especially: does the copy match the score/grade/real drivers? No fabricated provenance/claims; no framework leakage (NOVA/BSIP/cap/floor/penalty/dimension); grades as letters; sodium fact-only; calorie-density-first verdicts; no stale numbers (XX/Y badges, wrong gram/%/score values). Weak/incoherent/contradictory copy on a card = HIGH; fabrication = CRITICAL.
7. **Cross-page + invariants.** hummus dips-only vs vegetable-spreads coherent; milk page NOT modified; no snack-bar reaches A; no published-score regression vs intent. Anti-Immunity (RT-3 precedent): a NOVA-4 / heavy-additive product must not sit artificially high.

## Return (do NOT fix / approve / close — propose RETURNED)
- Verdict: owner-ready YES only if zero CRITICAL.
- Findings table: each finding = severity (CRITICAL/HIGH/MED) + page + barcode/field + evidence (file:line or screenshot-able description) + why it's wrong.
- Build result (tsc + npm run build exit code). Image-resolution sample results. Filter/lens results. score==trace re-confirmation. OFF result.
- End with the return contract JSON (`01_framework/operations/return_contract_v1.md`): `task` (TASK-311), `proposed_status`, `artifacts[]`, `counts{}` (with commands), `commands_run[]`, `not_done[]`, `self_check`.
- Boundaries: read/build/inspect only — do NOT modify any page, JSON, engine, or config. Do NOT push or deploy. OFF-ban absolute.
