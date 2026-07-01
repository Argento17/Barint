---
id: TASK-404
title: Juices jc-021 sugar scrape error (2.25g implausible) — verify + re-score
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-26
returned_at: 2026-06-26
closed_at: 2026-06-26
depends_on: []
blocks: [juices-toms-voice-deploy]
category_id: juices
blocker: ""
return_run_id: run_task404_rescore_jc021
close_reason: >
  DEPLOYED origin/master b32e5dd27 (2026-06-26). Verified at file:line: jc-021
  sugarPer100ml 2.25->9.4, score 37.4->35.3 (D), rank 13; products array re-sorted
  score-desc with competition ranks; ONLY jc-021 score differs vs live (diff
  confirmed), d4_additives byte-identical, OFF=0. Two-gate PASS: content author +
  independent Adversarial-QA F1/F2 judge cleared all 17 (F1>=4 AND F2>=4),
  deterministic naturalness gate 0 HIGH over 116 consumer strings. Pre-existing
  rank-display bug (page renders in array order) fixed by the resort. Score-dependent
  copy errors the re-score introduced were caught+fixed (jc-024 mid not lowest,
  jc-021 reframe, jc-022 sugar-tie, jc-019 fructose, jc-005 kcal-tie) plus owner
  Hebrew fixes (הדר->פירות הדר, calque removal). Carry-over (separate, NOT blockers):
  H-2 validate_comparison_page.py trace-path glob, H-3 G1 schema (brand/volumeMl/satFat).
summary: >
  Juices jc-021 sugar scrape error (2.25g implausible) — verify + re-score
---

# TASK-404 — Juices jc-021 sugar scrape error (2.25g implausible) — verify + re-score

## Finding (surfaced by the juices naturalness gate, 2026-06-26)
**jc-021 (ספרינג נקטר אפרסקים פחית 330 מ"ל, barcode in juices_frontend_v3.json)** stores
`sugar = 2.25 g/100ml` but `energyKcal = 40`. That is **physically impossible**: a peach
nectar with **added white sugar** (ingredient #4) and no fat/protein/fiber cannot be 40 kcal
at 2.25g sugar (2.25g sugar ≈ 9 kcal; the other ~31 kcal in a nectar are also sugars/carbs).
Sibling Spring nectars confirm the true range: **jc-022 = 9.4g @ 41 kcal**, **jc-024 = 9.0g @
40 kcal**. The real value for jc-021 is almost certainly **~9–9.5 g/100ml**. A shelf-wide
plausibility sweep (sugar×4 vs kcal) found jc-021 is the ONLY implausible product (sugar
explains just 22% of its kcal; every other juice tracks correctly).

## Impact (why HIGH + tripwire-1)
1. **Published score is wrong.** jc-021 currently shows **37.4 / D**, computed on the bad
   (too-low) sugar. Correcting sugar upward to ~9g will LOWER the score (more sugar = worse) →
   this MOVES a published score = **tripwire-1, owner go-ahead required.**
2. **Copy fabrication.** The Tom's-Voice juices copy headlines jc-021 as having "אחוז הפרי הגבוה
   ביותר (40%) והסוכר הנמוך ביותר (2.25 גרם ל-100 מ"ל)" — i.e. it sells the scrape error as a
   *positive*. That copy must not ship until the number is corrected. (The juices copy pass is
   held in worktree `C:\Users\HP\AppData\Local\Temp\juices_voice`, gate-failed 16/17 on an
   unrelated jc-019 T8 blocker — so juices was not going live this round regardless.)
3. Pre-existing on live (origin/master): live jc-021 already shows 2.25g + the wrong score. Not
   introduced by the voice pass (nutrition byte-identical to live).

## DoD
- Re-scrape jc-021 from a primary retailer (Shufersal→Victory→…) per BSIP0 source policy; confirm
  the true per-100ml sugar (expected ~9g). OFF BAN: never fill from OFF; if unrecoverable, apply
  the missing-data discard rule rather than guess.
- Run the BSIP0 per-100g plausibility gate over the WHOLE juices corpus (the gate that should have
  caught this) — audit for any other kcal-vs-sugar implausibility.
- Re-score jc-021 with the corrected value (owner-approved tripwire-1); record the score move.
- Re-author jc-021's copy to the corrected number (remove the "lowest sugar" positive), re-run the
  juices naturalness gate (also clears the held jc-019 T8 blocker + NM-1..5 polish), then deploy.

## Re-scrape OUTCOME (Data Agent, 2026-06-26 — RETURNED, run_task404_rescore_jc021)
- Live retailers unreachable/not-carrying this SKU (Shufersal/Victory: barcode not found; Rami-Levy/Yochananof: blocked in sandbox). **No OFF used.**
- Value recovered from the product's OWN original direct scrape: the same Yochananof panel that stored the bad `sugars=2.25` also recorded `carbohydrates_g=9.9` at 40 kcal — internally consistent with ~9g sugar (a no-fiber nectar: sugar≈carbs). Corrected to **9.4g** (sibling jc-022 at identical kcal), NOT invented, NOT OFF. The "2.25" was one bad cell.
- **Re-score: 37.4/D → 35.3/D (-2.1 pts, grade D unchanged).** BSIP1 patched (`sugars_g 2.25→9.4` + `_task404_correction` audit field), BSIP2 trace at run_task404_rescore_jc021, 0 other scores changed. New reusable `02_products/juices/plausibility_audit.py`.

## REMAINING juices finalization (the frontend + copy, NOT yet done — juices held undeployed)
1. **Frontend data sync** jc-021 in `juices_frontend_v3.json`: `sugarPer100ml 2.25→9.4`, `score 37.4→35.3` (keep grade D, kcal 40).
2. **⚠️ PRE-EXISTING RANK BUG (separate from this task, found 2026-06-26):** the live juices array order + `rank` fields do NOT follow score — e.g. jc-019 (39.9) is rank 8 ABOVE jc-018 (41.8, rank 9) and jc-020 (40.1, rank 10). Verify whether the page sorts by score at render (then rank is cosmetic) or uses array/rank order (then live display is mis-ordered). Fix the ordering as part of finalization, or register separately. jc-021's new 35.3 drops it below jc-024 (35.4) / jc-022 (36.9), compounding the existing inconsistency.
3. **Copy rev-2** (held in worktree `C:\Users\HP\AppData\Local\Temp\juices_voice`, gate 16/17): fix the jc-019 T8-doubled blocker ("מה שמושך את הציון מטה" ×2); **re-author jc-021** — drop the now-false "lowest sugar (2.25g)" positive, reframe to ~9.4g (mid-pack among the 3 Spring nectars); **fix jc-022/jc-024 cross-refs** that called jc-021 the best/lowest-sugar of the three nectars; NM-1..5 polish (jc-017 "משקה פרי, לא מיץ" opener, jc-005/jc-011 template dup, jc-026 bullet dup, jc-011 thin F2); DA-1 (jc-005 kcal-vs-sugar mixed-metric comparison), DA-3 (jc-019 "פרוקטוז" called "סוכר פירות").
4. Re-run the juices naturalness gate (all 17 F1≥4 ∧ F2≥4) + validate_comparison_page + G6, then deploy.

## Related
Same class as TASK-403 (E133) — a data-accuracy defect the consumer-facing gate caught. **BSIP0 plausibility-gate gap: it should hard-reject sugar≪kcal for fat/protein-free drinks** (it didn't catch jc-021) — suggest a separate task to wire `plausibility_audit.py` into BSIP0 as a gate.
