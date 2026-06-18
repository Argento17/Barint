# P79 — Merge cookies copy into frontend JSON + prune to golden schema (route: C2)

ROUTE: C2 (DeepSeek). MECHANICAL deterministic JSON merge + prune. No copy writing, no judgment on
wording, no scoring. Write+run a python script. Read this whole file. End with the return-contract JSON.

## TASK-275. Repo root: C:\Bari
Two inputs:
- DATA: `bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json` (61 products; insightLine/rowVerdict
  + milk-depth fields currently = "PENDING_COPY"; + a page shell with PENDING_COPY).
- COPY: `02_products/cookies_coffee/cookies_coffee_copy_v1.json` (authored: per-barcode insightLine +
  rowVerdict; pageShell = hero / prologueSentences[3] / methodologyLines[3] / categoryCaveat).

## Do (deterministic, in-place on the DATA file — keep a .bak first)
1. **Inject row copy:** for each of the 61 products, match by `barcode` and set `insightLine` and
   `rowVerdict` from the COPY file's authored strings. (Verify all 61 barcodes match across the two files;
   report any that don't.)
2. **Inject page shell:** put the COPY pageShell (hero, prologueSentences, methodologyLines,
   categoryCaveat) into the DATA file's page-copy location — mirror where `brined_cheeses_frontend_v2.json`
   keeps its hero/prologue/methodology/caveat (inspect it; same path/keys).
3. **PRUNE to the golden schema (match brined):** the brined golden per-product copy = ONLY `insightLine`
   + `rowVerdict`. DELETE these over-scaffolded per-product keys from every product:
   `consumerTakeaway`, `consumerExplanation`, `bariInterpretation`, `bestUseCases`, `expansion`.
   (They are unused milk-depth scaffolding and hold PENDING_COPY.)
4. **Verify 0 PENDING_COPY remain** anywhere in the DATA file after the merge+prune.

## Guards
- Do NOT change any score, grade, confidence, barcode, imageUrl, nutrition, or d4_additives value.
- Do NOT alter the wording of any copy string — inject verbatim from the COPY file.
- Do NOT touch any other file. OFF ban: introduce no external data.
- Keep product array order (already sorted by score desc).

## Return — end with EXACTLY this JSON
```json
{"task":"P79","proposed_status":"RETURNED",
 "artifacts":[{"path":"bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json","action":"modified","sha256":"<fill>"}],
 "counts":{"products":"61","insightLine_injected":"N/61","rowVerdict_injected":"N/61","barcode_match":"N/61","pending_copy_remaining":"N (MUST be 0)","milk_depth_keys_pruned":"yes/no","pageshell_injected":"yes/no","score_grade_changed":"0"},
 "commands_run":[{"cmd":"...","exit_code":0}],
 "not_done":[],"self_check":"61 verdicts injected verbatim, milk-depth scaffolding pruned, 0 PENDING_COPY, 0 score/grade changes"}
```
Do NOT close — propose RETURNED. The orchestrator verifies 0 PENDING_COPY + verdicts match source + dist unchanged.
