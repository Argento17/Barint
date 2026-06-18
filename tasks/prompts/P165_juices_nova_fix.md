# P165 / TASK-313 — Juices NOVA fix (RT-3): correct stale nova=3 on fresh-squeezed grade-A juice (route: C1-GROK)

Repo: C:\Bari. Branch: task-275-engine-fixes-abc. Edit ONLY `bari-web/src/data/comparisons/juices_frontend_v3.json`. Reversible, no commit, no deploy.

## Problem (red-team RT-3, orchestrator-verified)
On the assembled juices page, 5 grade-A products that are single-ingredient 100% **fresh-squeezed** juice carry `novaGroup: 3` (the ultra-processed-lite tier). NOVA 3 on a single-ingredient squeezed juice is definitionally wrong — these are NOVA 1. The values are stale, inherited from a legacy run; the shelf-relative rescore did NOT recompute NOVA (staging nova=None for A-grade). Peer squeezed juices on the same page already correctly show `novaGroup: 1` (e.g. `7290000525969` "מיץ תפוזים סחוט" = nova 1), so the page is internally inconsistent.

Affected barcodes (all grade=A, score=85, currently novaGroup=3):
- `7290003009640` — סחוט תפוז 1 ליטר
- `7290004030100` — 100% מיץ תפוזים ולנסיה סחוט 1 ליטר פריני
- `7290013153395` — סחוט 1 ליטר רימונים
- `7290110114886` — סחוט קלמנטינה 2 ליטר
- `7290110114893` — סחוט תפוז 2 ליטר

## Do this
1. For each of the 5 barcodes: read its `ingredients`/ingredient list + name in the JSON (and the BSIP1/BSIP2 source if present under `02_products/`). Confirm it is single-ingredient 100% squeezed juice (no additives).
2. If confirmed single-ingredient 100% juice → set `novaGroup: 1` (matches the definitionally-correct classification AND the peer squeezed juices already at 1). If a product's ingredient data shows additives/concentrate that would NOT be NOVA 1, do NOT force 1 — instead set `novaGroup: null` (never assert a class the data doesn't support) and flag it in the return. NEVER invent; NEVER use OFF.
3. Change ONLY the `novaGroup` field on these ≤5 products. Do NOT touch score, grade, copy, or any other product, or any other file. Scores/grades MUST be unchanged (NOVA is display-only here; the shelf-relative juice score is sugar-based, not NOVA-driven — confirm the score/grade are byte-identical after your edit).

## Verify / return
- For each of the 5: old nova → new nova + the ingredient evidence that justifies it.
- Confirm juices product count unchanged (21), all scores+grades byte-identical to before (diff = only novaGroup on ≤5 products).
- Confirm 0 grade-A juices still carry nova=3 (re-scan).
- Do NOT close — propose RETURNED. End with the return contract JSON (`01_framework/operations/return_contract_v1.md`): `task` (TASK-313), `proposed_status`, `artifacts[]` (path+action+sha256), `counts{}` (with command), `commands_run[]`, `not_done[]`, `self_check`. Boundaries: only juices_frontend_v3.json; OFF-ban absolute; no commit/deploy.
