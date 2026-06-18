# P91 — Merge corrected copy + fix page-data shell divergence + rebuild (route: C1 / Frontend)

**Task:** TASK-275. **Lane:** C1 Frontend (Sonnet). Land the corrected copy into the rendered page AND fix
the RT-3 root cause (page-data.ts hardcodes the shell separately from the JSON → stale copy rendered).

## Inputs
- Corrected copy (authoritative): `02_products/cookies_coffee/cookies_coffee_copy_v1.json` (58 entries:
  per-barcode insightLine + rowVerdict; pageShell = hero / prologueSentences / methodologyLines / categoryCaveat).
- Frontend data (58 products, currently ~586 PENDING_COPY): `bari-web/src/data/comparisons/cookies_coffee_frontend_v1.json`.
- Render: `cookies-coffee-page-data.ts` (HARDCODES the shell strings — the bug), `...comparison-page.tsx`,
  `...prologue-visualizations.tsx`.

## Do
1. **Merge into the JSON:** for each of the 58 products, set `insightLine` + `rowVerdict` from the corrected
   copy (by barcode). Inject the corrected pageShell (hero/prologue/methodology/caveat) into the JSON's
   page-copy location (mirror where brined keeps it). PRUNE the over-scaffolded per-product milk-depth keys
   (`consumerTakeaway`, `consumerExplanation`, `bariInterpretation`, `bestUseCases`, `expansion` if it only
   holds copy) so **0 PENDING_COPY remain**. Keep nutrition data (`expansion.nutrition`) — the charts + sugar
   metric need it; only prune the empty COPY scaffolding.
2. **Fix the divergence (RT-3 root):** refactor `cookies-coffee-page-data.ts` so the page shell — hero,
   prologueSentences, methodologyLines, categoryCaveat — is **read from the JSON** (`...page_copy`), NOT
   hardcoded. Remove the stale hardcoded Hebrew strings (the ones with "מעל 17 גרם", "61 מוצרים", "תשעה",
   "לכל אחד מהם...שחצות"). Single source of truth = the JSON.
3. **Build gate** (real exit, no tail pipe): `cd bari-web && npm run build > build_cookies3.log 2>&1; echo "EXIT:$?"`
   → EXIT:0, route present.

## Guards
- Do NOT change scores/grades/confidence/nutrition/imageUrl/d4_additives. Inject copy verbatim from the
  corrected file. Do NOT edit shared components or other categories. Scope CSS to `.cc-page`. OFF ban. No new deps.

## Return
Return contract: task=P91, proposed_status=RETURNED, artifacts (frontend JSON + page-data.ts, +sha256),
counts (verdicts merged 58/58, pageShell from JSON yes/no, hardcoded shell removed yes/no, PENDING_COPY=0,
build exit, route present, 0 score changes), commands_run (build w/ real EXIT), not_done, self_check.
Propose RETURNED — do NOT close. The orchestrator re-runs build + re-screenshots + re-red-teams.
