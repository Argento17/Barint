# P84 — Re-merge FIXED cookies copy into frontend JSON (route: C2)

ROUTE: C2 (DeepSeek). MECHANICAL deterministic re-merge (the copy was corrected by P82; the frontend JSON
still holds the OLD copy). Write+run python. No wording changes. End with the return-contract JSON.

## TASK-275. Repo root: C:\Bari
- COPY (corrected, authoritative): `02_products/cookies_coffee/cookies_coffee_copy_v1.json`
  (sha should be `27304f98…`; per-barcode insightLine + rowVerdict; pageShell hero/prologueSentences/
  methodologyLines/categoryCaveat).
- DATA (re-inject into, in place; keep a .bak): `bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json`
  (already merged+pruned once by P79; structure is correct, only the copy STRINGS need updating to the fixed ones).

## Do
1. For each of the 61 products, match by barcode and OVERWRITE `insightLine` + `rowVerdict` with the
   corrected strings from the COPY file (verbatim).
2. Overwrite the page-shell copy (hero, prologueSentences, methodologyLines, categoryCaveat) with the
   corrected COPY pageShell (same location P79 used).
3. Verify 0 PENDING_COPY remain.

## Guards
- Do NOT change score/grade/confidence/barcode/imageUrl/d4_additives. Do NOT re-prune or restructure
  (already done). Inject copy verbatim — no wording edits. OFF ban. Keep product order (score desc).

## Return — end with EXACTLY this JSON
```json
{"task":"P84","proposed_status":"RETURNED",
 "artifacts":[{"path":"bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json","action":"modified","sha256":"<fill>"}],
 "counts":{"insightLine_updated":"N/61","rowVerdict_updated":"N/61","pending_copy":"N (MUST be 0)","score_grade_changed":"0","pageshell_updated":"yes"},
 "commands_run":[{"cmd":"...","exit_code":0}],
 "not_done":[],"self_check":"61 corrected verdicts re-injected verbatim, pageShell updated, 0 PENDING, 0 score changes"}
```
Do NOT close — propose RETURNED. Orchestrator verifies verdicts == fixed copy + 0 PENDING + dist unchanged.
