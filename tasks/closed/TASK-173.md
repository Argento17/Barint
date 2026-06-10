---
id: TASK-173
title: "Bread whole-grain re-score model — fix TASK-164 ingredient non-propagation, before/after grades for owner sign-off (no live change yet)"
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
closed_by: cc-agent
depends_on: []
blocks: [TASK-172]
category_id: bread
resolution: "OWNER RULED (2026-06-03) — text-only fix, KEEP GRADES; no bread re-score. The model did its job: it proved the scores were never corrupted (bug was serialization-only, score path intact) and disproved the 'B is a depressed artifact' premise (propagation effect is mixed-sign: 10 up / 11 down / 3 unchanged; אנג'ל would DROP on additives). A real re-score would be a full engine-pinned frozen-bread rebaseline (14/24 drift on current engine, Nutrition+Product D7) — owner chose NOT to pursue it here. Frozen bread grades stand. Unblocks TASK-172 (verdict text fix, grades untouched). Model artifacts retained NOT-LIVE at 02_products/bread_retail_003/_model_task173/."
return_reason: "MODEL delivered (NOT LIVE) — and it OVERTURNS the task premise. Root cause confirmed: the bug is at the SERIALIZATION boundary (batch_run_bread_retail_003.py Step 4 lines 1099-1119 drop ingredient text + signal layer when persisting bsip2_*.json), so downstream verdict/limitingFactors authoring defaulted to a false 'refined base'. The SCORE PATH was never broken — the false signal lives only in the text layer. Therefore the TASK-164 hypothesis (bug depressed scores → B is an artifact → bump to A) is NOT supported: isolating the propagation variable moves 10 products UP, 11 DOWN, 3 unchanged (e.g. אנג'ל 7290016967074 actually DROPS 81.4→72.0 because the real ingredient list exposes 9 E-number additives the macro-only path never penalized). A clean numeric re-score is also effectively blocked: published scores = build-time engine, which has since drifted to 0.4.0 — re-running today reproduces only 6/24, with 14/24 drifting for reasons UNRELATED to this bug (a blind re-run-and-ship would repeat the recal-went-live incident). Artifacts (NOT LIVE): 02_products/bread_retail_003/_model_task173/MODEL_REPORT_NOT_LIVE.md (+ rescore_model.py, rescore_model_result.json). RECOMMENDATION: take the text-only path (TASK-172 — drop false clauses, keep frozen grades which the model confirms are NOT artifacts); treat any true numeric re-score as a separate, deliberate, engine-pinned bread rebaseline with Nutrition+Product D7 sign-off. Awaiting owner re-decision (premise changed)."
summary: >
  Owner-authorized (2026-06-03) re-score of the bread products that the TASK-164 BSIP0-to-signal ingredient non-propagation bug mis-read as refined-base. The false signal wrote bad verdict text AND likely depressed the score (B may be an artifact). Data: re-propagate the real ingredient lists (real_bread_retail_003_v1) into the signal layer for the 4 confirmed whole-grain breads (497044 / 7290016967074 / 2079927 / 3268252) + audit the rest of the bread corpus for the same pattern; re-run scoring; produce a before-after table (live grade vs corrected grade) + root-cause confirmation. MODEL ONLY — no live file or published-score change until owner signs off the grade moves (recal lesson). Bread frozen-invariant: owner-authorized unfreeze for the bug fix, signed off per-move before ship. Gates the TASK-172 verdict rewrites.
---

# TASK-173 — Bread whole-grain re-score model — fix TASK-164 ingredient non-propagation, before/after grades for owner sign-off (no live change yet)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
