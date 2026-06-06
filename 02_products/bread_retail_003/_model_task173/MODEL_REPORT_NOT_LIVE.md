# TASK-173 — Bread Re-Score MODEL — NOT LIVE — DO NOT SHIP

**Status:** MODEL ONLY. No live file, published score, grade, or frontend JSON changed.
**Author:** data-agent | **Date:** 2026-06-03 | **Run:** real_bread_retail_003_v1
**Artifacts:** `_model_task173/rescore_model.py`, `_model_task173/rescore_model_result.json`

---

## 1. Root cause — CONFIRMED (file/stage)

The ingredient list is present and high-confidence in the BSIP0 raw scrape for all 24
displayed products (`real_bread_retail_003_v1_20260525T194532_bsip0_raw.json`,
field `ingredients_raw`, `extraction_confidence: high`).

**The propagation does NOT break inside the BSIP2 scoring pipeline.** The runner
`batch_run_bread_retail_003.py` DOES carry ingredients into scoring:
`normalize_to_bsip1()` populates `ingredients_text_he`/`ingredients_raw` (lines 147–148),
and `run_pipeline()` calls `extract_signals(prod)` (line 181) on the full product. The
signal extractor detects whole grain from those ingredients
(`WHOLE_GRAIN_MARKERS_HE` → `has_whole_grain`, `signal_extractor.py` lines 150–158, 726).

**The break is at the SERIALIZATION boundary (Step 4, lines 1099–1119).** The persisted
`bsip2/bsip2_shufersal_*.json` deliberately drops the ingredient text and the entire
signal layer; it keeps only `final_score`, `final_grade`, `nutrition`, and a boolean
`has_ingredients`. Every downstream consumer therefore had no ingredient-derived signal:

- `build_lechem_frontend_json.py` re-reads ingredients from BSIP0 for the `expansion`
  block, but takes `score`/`grade` straight from the BSIP2 flat file (lines 231–232).
- The limitingFactors authoring (`limiting_factors_v1.json`, TASK-129C) worked off the
  flat file's confidence label, not the raw ingredients, so it defaulted to the false
  "אין רשימת רכיבים זמינה / בסיס קמח מזוקק" framing.

**So the false 'refined base / fiber-source unclear' signal lives in the VERDICT/
limitingFactors layer, not in the score path.** The score itself was computed by an
engine that *did* see the ingredients at build time.

## 2. Re-score feasibility — BLOCKED (engine drift), modelled isolation instead

A clean corrected re-score is NOT cleanly re-runnable today. The published bread scores
(= the stored BSIP2 `final_score`, verified equal to the live frontend score for all 24
products — see §4) were produced by the **build-time engine (pre-0.4.0)**. The engine has
since drifted (TASK-133 named-additive identity, protein-matrix awareness, weight re-sync;
RECAL_P0 / TASK-144 flags exist but default OFF, matching the bread build).

Re-running the current engine reproduces the stored score for only 6/24 products; 14/24
"drift" — i.e. today's engine would move scores for reasons UNRELATED to the propagation
bug. Forcing a current-engine re-score and shipping it is exactly the "staged recal scores
went live un-reconciled" incident the owner flagged. **Recommend NOT doing a blind
re-run-and-ship.**

What IS cleanly modellable is the **isolated propagation variable**: run the same
(current) engine twice per product — once WITH the genuine ingredients, once with them
stripped — so the delta is purely the bug's effect, with engine drift held constant.

## 3. Audit of the propagation pattern across all 24 — and the surprise

With ingredients propagated, **21/24 products detect whole grain**; with ingredients
stripped (bug simulation), **0/24** do. So the non-propagation pattern is corpus-wide,
not limited to the 4 named products (those 4 are confirmed whole-grain in the audit).

**But the isolated score effect is MIXED-SIGN, not depressive** (this contradicts the
TASK-164 hypothesis that the bug depressed the score):

| Direction (corrected − nonprop) | Count |
|---|---|
| Ingredients RAISE the score (wg bonus + NOVA help dominate) | 10 |
| Ingredients LOWER the score (additive/emulsifier/sugar/isolate-fiber penalties dominate) | 11 |
| No change | 3 |

Example: `shufersal_7290016967074` (אנג'ל חיטה מלאה, 9 E-numbers) — WITH ingredients the
engine sees the additive load and scores it **lower** (72.0) than the macro-only path
(81.4). Propagating ingredients does not uniformly help whole-grain breads; for additive-
heavy ones it hurts.

## 4. Before/after MODEL table (live vs isolated-propagation re-run)

`live` = published score (verified == stored BSIP2 final_score, build-time engine).
`corrected` = current engine WITH genuine ingredients. `nonprop` = current engine,
ingredients stripped (bug sim). `Δprop` = corrected − nonprop (pure bug effect, same engine).
`stored↔` = which re-run the stored/live score matches (~CORR / ~NONP / drift).

| id | name | live | corrected | nonprop | Δprop | wg(corr) | stored↔ |
|---|---|---|---|---|---|---|---|
| 7290016967074 | אנג'ל חיטה מלאה | 72/B | 72.0/B | 81.4/A | −9.4 | yes | ~CORR |
| 2079927 | דגנים מלא | 75/B | 81.5/A | 81.1/A | +0.4 | yes | drift |
| 3268252 | חיטה מלא לילדים | 75/B | 82.0/A | 79.2/B | +2.8 | yes | drift |
| 497044 | ברמן אקטיב | 72/B | 80.7/A | 80.1/A | +0.6 | yes | drift |
| 3268429 (anchor) | ירוק מקמח מלא | 80/A | 82.0/A | 79.8/B | +2.2 | yes | ~NONP |
| 481203 | מחמצת קמח מלא | 77/B | 82.0/A | 76.9/B | +5.1 | yes | ~NONP |
| 3054183 | שיפון מלא סטמכר | 76/B | 82.0/A | 75.9/B | +6.1 | yes | ~NONP |
| 481197 | מחמצת גרעינים | 76/B | 82.0/A | 75.9/B | +6.1 | yes | ~NONP |
| 574370 | שיפון קל | 75/B | 82.0/A | 82.0/A | 0.0 | yes | drift |
| 2079996 | אחיד פרוס קל | 73/B | 79.6/B | 81.1/A | −1.5 | yes | drift |
| 7290018500460 | אנג'ל חצי מלא | 67/B | 72.0/B | 76.1/B | −4.1 | yes | drift |
| 4685027 | מחמצת+חיטה מלאה קל | 70/B | 72.0/B | 79.7/B | −7.7 | yes | drift |
| 2079217 | מחמצת שיפון+אגוזים | 61/C | 67.4/B | 76.3/B | −8.9 | yes | drift |
| 2079477 | אחיד פרוס | 67/B | 74.1/B | 72.9/B | +1.2 | no | drift |
| 7290016245325 | טחינה פרוס | 82/A | 82.0/A | 82.0/A | 0.0 | no | ~CORR |
| 7290018500316 | כוסמין לבן | 68/B | 76.1/B | 73.3/B | +2.8 | yes | drift |
| 6451507 | מחמצת מכוסמין | 66/B | 69.0/B | 78.5/B | −9.5 | yes | drift |
| 6451484 | מחמצת אגוזים צימוקים | 60/C | 68.8/B | 72.6/B | −3.8 | yes | drift |
| 2079033 | דגנים לייט | 74/B | 80.2/A | 81.7/A | −1.5 | yes | drift |
| 96086000966 | קרקר כוסמין מלא+שומשום | 82/A | 81.5/A | 81.5/A | 0.0 | yes | ~CORR |
| 96086000577 | קרקר כוסמין אורגני | 78/B | 77.7/B | 81.7/A | −4.0 | yes | ~CORR |
| 7296073134459 | קרקר שוודי | 72/B | 72.2/B | 76.2/B | −4.0 | yes | ~CORR |
| 7296073134442 | קרקר שיפון | 71/B | 71.4/B | 75.4/B | −4.0 | yes | ~CORR |
| 8434165658523 | קרם קרקר | 59/C | 67.4/B | 66.2/B | +1.2 | no | drift |

Evidence for the 4 named whole-grain products (raw ingredient head, all conf=high):
- 497044: `קמח חיטה מלא (100% מסך הקמחים, 53% ממשקל המוצר)`
- 7290016967074: `קמח חיטה מלא (נטחן מגרעין החיטה בשלמותו)(100% ממשקל הקמחים)`
- 2079927: `קמח חיטה מלא (83% ממשקל הקמחים)`
- 3268252: `קמח חיטה מלא (100% מהקמח, 66% ממשקל הלחם)`

## 5. Blast radius vs the frozen-bread ruling

- **Nothing is live.** All numbers above are staged in `_model_task173/`. Live
  `bread_frontend_v2.json` was NOT touched by this task (its only pending git diff is the
  pre-existing TASK-172 limitingFactors edit — zero score/grade/insightLine drift).
- The simple "B is a depressed artifact → bump to A" story is **not supported**. Under a
  current-engine corrected re-run, 11 products would move UP (incl. several B→A) and 11
  would move DOWN — but that table is confounded by post-build engine drift and must not
  be read as a ship-ready re-score.
- A genuine corrected re-score requires a decision the data agent cannot self-make:
  either (a) freeze/pin the build-time engine and re-run with ingredients (isolates the
  bug, but reopens whole-grain B→A moves on a frozen category), or (b) accept a full
  current-engine rescore of bread (re-baselines the whole category, large blast radius).
  Both need owner + Nutrition (D7 co-sign) before any number moves.

## Recommended next step (for owner)
Treat the score question as **open but not auto-correctable**. The cheap, safe, already-
scoped win is TASK-172's text fix: drop the demonstrably-false "refined base / fiber
unclear" limitingFactors + verdict clauses on the 21 confirmed whole-grain products and
keep the frozen grades — no score movement. A numeric re-score should be a separate,
explicitly-owner-authorized engine-pinning exercise, not folded into this bug fix.
