# P73 — Nutrition ruling: cookie E-modal — honest-vs-artifact + dedicated category (route: C1 / Nutrition)

**Task:** TASK-275. **Lane:** C1 Nutrition Agent — the scoring-philosophy ruling on run_cookies_001. You own
the methodology (you authored `cookies_coffee_scoring_interpretation_v1.md`); §2.3 predicted C-modal/
B-ceiling and the real run came out E-modal. Rule on why, and what to do — grounded in the engine + the
verified evidence + the C3 outside read below.

## Verified evidence (orchestrator-checked against the 61 traces of run_cookies_001)
- Grade dist: **A0 B0 C13 D15 E33** (E-modal). Score min10 / max63.9 / median32.6 / stdev14.1.
- **25/61 bound at cap 45 = `ISRAELI_RED_LABELS_2_PLUS`** (high sugar >17.5g AND sat-fat >5g both fired).
  Real sugar runs 20–38g, sat-fat 7–10g. These are category-AGNOSTIC public-health caps.
- **Routing (NO cookie category exists):** cracker 27 · snack_bar_granola 20 · bread 7 · whole_food_fat 4 · default/cereal/dairy_protein 1 each.
- **Routing distortion (the key diagnostic):** `snack_bar_granola`-routed biscuits = **75% E (15/20)** vs
  `cracker`-routed = **40% E (11/27)** — the same class of sweet biscuit is punished much harder under the
  snack-bar lens than the cracker lens.
- Mechanically clean: OFF 0/61, brined_food 0/61, engine_invariants 6/6 PASS (342), no engine edits.

## C3 outside read (advice, already weighed — `tasks/returns/P72_return.md`)
SHIP E-MODAL AS HONEST. (1) sugar+sat-fat is a category-agnostic signal → E-heavy is directionally honest.
(2) Add a dedicated cookie category for TAXONOMY/EXPLAINABILITY ONLY, **never to lift grades** (special-
pleading); test = reroute with red-label caps INTACT — if still E/D-heavy, routing wasn't the cause.
(3) NO endemic relief — cookie sugar+fat is a *formulation choice*, not structural like brine sodium; a
bounded **C-ceiling** rule could be legit, softening the cap would not. (4) Page = explicit "least-bad", no
demoralizing language.

## Your ruling must decide (each, grounded — cite engine lines where relevant)
1. **Honest or artifact?** Given 25/61 hit the category-agnostic 2-red-label cap AND snack_bar_granola
   routing distorts (75% vs 40% E): how much of E-modal is honest vs routing artifact? Be specific.
2. **Dedicated `cookie`/`biscuit` router category — yes/no.** If yes (recommended by C3 for coherence):
   - Define the category scope + the exact **Hebrew name-keywords** to wire into the router
     (`router_v2.py` / `evaluation_scope.py`), mirroring how `brined_food` keywords were added (EV-052).
   - HARD CONSTRAINT: caps INTACT, **no endemic relief**, scored on the standard indulgence path. The
     category exists to stop semantically-wrong routing (biscuit≠snack-bar≠cracker), NOT to raise grades.
   - It must NOT match any LIVE product (no keyword overlap with snack-bars/cereals/bread/crackers live
     corpora) — zero-published-movement is mandatory (tripwire-1). List the keywords with that in mind.
3. **Grade ceiling + page framing.** Predict the post-reroute ceiling (C? B?) and give the honest Hebrew
   framing for the category caveat ("least-bad", indulgence shelf, what an A/B/C means here). Update if your
   §2.4 caveat needs revising.
4. **Update methodology §2.3** — the prediction-miss (real sugar higher than projected; routing not
   modeled). Note it for the record (a short addendum is fine; don't rewrite the whole doc).
5. **EV proposal** — draft the evidence-registry entry for the new category (EV-###: scope, keywords,
   rollback = remove keywords, no-regression proof plan = engine_invariants 342 + golden-corpus byte-
   identity on all live categories). Do NOT implement code — this is the ruling + spec; implementation is a
   separate C1-CURSOR dispatch + Product D7 co-sign.

## Guards
- No engine edits in this task (ruling + spec only). OFF ban absolute. No fabricated products/numbers.
- Frozen invariants / published scores untouchable — the new category must prove 0 live movement before any code ships.

## Return
Deliverable: `02_products/cookies_coffee/methodology/cookies_coffee_routing_ruling_v1.md` (+ §2.3 addendum).
End with the return contract: task=P73, proposed_status=RETURNED, artifacts (+sha256), counts (sections,
keywords proposed, engine cites), the honest-vs-artifact split with numbers, not_done, self_check. Propose
RETURNED — do NOT close.
