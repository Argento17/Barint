# TASK-143 — Yogurt Reconciliation: run_yogurt_004 (clean, EV-029-corrected)

**Date:** 2026-06-02 · **Engine:** proto_v0 / 0.4.0 **UNMODIFIED** · **Run:** run_yogurt_004
**Supersedes:** run_yogurt_003 (AFFECTED by the EV-029 fat-overwrite; fat now corrected)

## Why this run exists
TASK-142A confirmed run_yogurt_003 was scored on EV-029-corrupt fat (the shared `nutritionList` parser
overwrote total fat with the trans sub-row → fat=0.5 on 47/97; saturated never captured). TASK-143 was
BLOCKED on that fix. The parser is now fixed (shared `_shared/bsip0_nutrition.py`) and the yogurt scraper
imports it (and persists `nutrition_raw_source` per TASK-151). This is the clean re-scrape → re-build →
re-score, engine untouched.

## Data integrity (the fix is validated)
- Re-scrape 2026-06-02: 93 products; corrupt 2026-06-01 raw **replaced/deleted**. BSIP0 gate PASS.
- BSIP1 `run_yogurt_004/output`: 86 included (= run_003 corpus), ingredients 100%.
- fat=0.5 collapsed **47/97 → 1** (the 1 is a genuine 0% product). `nutrition_raw_source` persisted on 93/93.
- QA: COV-001 95.3%, COV-002 100%, COV-003 100%, COV-005 100%, **COV-006 0.0% implausible (PASS)**.

## Reconciliation A — run_yogurt_004 (clean) vs run_yogurt_003 (affected)  [machine→machine, 84 common barcodes]
**The EV-029 impact on yogurt is MILD** — the key finding.

| Metric | Value |
|---|---|
| Grade changes | **5 / 84** |
| Score delta | median **0.0**, mean **-0.2**, range **-14.1 … +12.0** |
| Score moves | 35 down · 25 up · 24 ~unchanged |
| Grade dist run_003 | C 32 / B 29 / D 24 / E 1 |
| Grade dist run_004 | C 28 / **B 30** / D 27 / E 1 |

The 5 grade changes:
- C→D יוגורט יווני צזיקי 10% (59.1→45.0)
- C→D מולר פרוטאין יוגורט תות (51.9→49.0)
- C→D יופלה GO תות (52.0→49.2)
- C→B יוגורט בסגנון יווני 6.5% (64.5→65.4)
- C→B דנונה פרו 20ג חלבון תות (55.0→67.0)

**Why mild (vs cheese/maadanim, which shifted hard):** yogurt fat is genuinely small (0% / 1.5% / 3%), so the
fat-overwrite distortion (fake 0.5 vs real ~1.5–3 g) is numerically minor for the score. Contrast cream-cheese,
where 0.5 g masked real 25–32 g. So run_yogurt_003's grades were *invalid in provenance* but, by luck of the
category's low fat, *close in value*. run_yogurt_004 is the clean, citable baseline.

## Reconciliation B — run_yogurt_004 (machine) vs LIVE DEC-005 manual shelf  [for the go-live decision]
The live shelf (`bari-web/src/data/comparisons/yogurts_frontend_v1.json`, 13 curated products) is **A-heavy and
manually scored**; the machine shelf is **B-capped**. Best-name-match:

| Live (manual) | Machine run_004 (closest) |
|---|---|
| yog-001 **A/88** יוגורט מלא 3% תנובה | B/74.9 |
| yog-002 **A/87** יוגורט ביו 1.5% תנובה | B/73.3 |
| yog-004 **A/85** יוגורט יווני 5% שטראוס | B/71.5 |
| yog-003 **A/82** יוגורט 0% שומן | B/74.4 |
| yog-005 **A/80** יוגורט יווני 0% שטראוס | C/62.0 |
| yog-006 B/78 אקטיביה טבעית | B/74.4 |
| yog-012 B/69 יופלה GO פירות יער | C/50.9 |
| yog-007 C/62 יופלה בטעמי פירות | C/50.9 |

- **Live grade dist:** A 5 / B 5 / C 3. **Machine max:** 78.7 → **B** (zero A's).
- **Expected downward correction CONFIRMED.** The manual A's (80–88) are NOT supported by the engine on real
  scraped data; the cleanest plain bio yogurts top at ~74–75/B. The **A-ceiling ruling (139A) does NOT restore
  A** here — plain live-culture yogurts are macro-capped at B and/or lack the confirmed-culture + clean-matrix
  combination A requires.
- **Caveat:** the live manual shelf includes non-dairy items (יוגורט סויה / קוקוס) that the dairy_protein scrape
  doesn't cover 1:1; those rows have weak matches and need a plant-pool decision at re-author time.

## DoD status (TASK-143)
- ✅ Re-run full BSIP0→BSIP2 on calibrated engine (run_yogurt_004; engine UNMODIFIED).
- ✅ Reconcile vs live DEC-005 — every delta documented (Reconciliation B); downward correction justified.
- ✅ QA hard-fail-free + COV-006 plausibility PASS; clean baseline ready to freeze.
- ⏳ Content/Design re-author insight lines/prologue to the new (B-capped) shelf — **separate, downstream**.
- ⏳ **Product Owner go-live**: accept retiring DEC-005 + the corrected (A→B) shelf — **human gate, blocks the swap**.
- ⏳ Replace live `yogurts_frontend_v1.json` + retire DEC-005 — **only after PO go-live**.

## Recommendation
The data cycle is done and clean. **Do NOT swap the live shelf yet** — it overwrites DEC-005 (hard to reverse)
and drops 5 A's to B. That needs explicit Product Owner go-live + a Content/Design re-author pass. Propose
TASK-143 **RETURNED** with the live swap held on those two human gates.
