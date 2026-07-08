# Red-Team Challenge Report — yogurt-spoonable closing pass (TASK-515)
Date: 2026-07-08
Scope: 78 products, /hashvaot/yogurt, yogurt_spoonable_frontend_v1.json (sha256 2bb1e85d…c108ad)
Rounds: 3 (loop-capped). Verdict: **OWNER-READY — 0 open CRITICAL, 0 open HIGH.**

---

## Round-by-round summary

**Round 1** (0 CRITICAL / 1 HIGH / 2 MEDIUM): HIGH-1 — barcode 7290112336712 (S, 92.6) rowVerdict
claimed processing was "clean" while the engine flags `processing_quality`=64/medium and
`LOW_NOVA_CONFIDENCE` (the confidence chip was already honestly hedged "נתונים בבדיקה," so this was
HIGH not CRITICAL). MEDIUM-1: false "THE simplest" superlative (7 products tie at ≤2 ingredients).
MEDIUM-2: leader/ceiling framing on a 2.0pt (noise-level) gap between two S-grade products. All FIXED.

**Round 2** (3 findings resolved, 0 regression) surfaced a NEW HIGH, **RT-R2-1**: the fix for MEDIUM-2
had named the literal grade letter "S" in consumer copy on the 2 flagship products, but the frozen
ScoreChip folds every score ≥80 to an "A" chip site-wide (no S slot exists) — a visible chip/copy
contradiction. FIXED (round 3: literal "S" removed from all copy, replaced with co-equal
"highest-scoring" framing; the data `grade` field correctly stays "S," only prose changed). A
follow-up superlative false-claim (565527 claiming "the highest score" when 336712 holds the actual
single max) was also caught and fixed via the go-live battery's rank-check gate.

Separately, a scoring-engine bug (**RT-2H1**) was found on the sibling drinkable page and its blast
radius included 13 spoonable products: the ingredient classifier missed the source-qualified label
"עמילן טפיוקה מעובד" (modified tapioca starch), mis-classifying it as native/benign starch and
skipping the ECS-v1 stabilizer-complexity penalty. Nutrition + Product co-signed the fix
(`TAPIOCA_STARCH_FIX_COSIGN.md`); C3 (P509) endorsed "fix-now-split." The classifier was corrected,
all 13 spoonable products re-scored (3 crossed a grade boundary: 7290010471669 D→E, 7290110578572
C→D, 7290119377404 B→C), each product's additive card was corrected to include the newly-detected
stabilizer, and affected copy was re-authored — including barcode 7290119386642, which had been
naming entirely the wrong additives (flavor-agent+stabilizer instead of the actual
phosphates+modified-starch).

**Round 3 (this report, FINAL/loop-capped):** verified RT-2H1 fully landed on all 3 spoonable
grade-crossers (score==trace, grade==trace, additive counts consistent with copy) and re-confirmed
all Round 1/2 fixes hold with 0 regression: 0 literal "S" in prose, all 4 corpus-wide superlatives
re-checked TRUE against the full 78, the honest processing hedge on 7290112336712 intact, no phantom
confidence. Full deterministic sweep GREEN: `run_gates.py` G1–G8 exit 0, `rank_check.py` 0 FALSE
superlatives, score/grade vs trace 0 mismatches on all 78, 0 grade-monotonicity violations, 0 OFF
markers, 0 PENDING. Real-DOM render verified at 375px: HTTP 200, RTL/Hebrew, 78 rows, 0 console
errors, 0 broken images, no horizontal overflow, row expansion/collapse works.

---

## Final state — all findings

| ID | Severity | Status |
|---|---|---|
| HIGH-1 (336712 processing over-claim) | HIGH | RESOLVED, verified R2+R3 |
| MEDIUM-1 (false "THE simplest") | MEDIUM | RESOLVED, verified R2+R3 |
| MEDIUM-2 (leader/ceiling on noise gap) | MEDIUM | RESOLVED, verified R2+R3 |
| RT-R2-1 (literal "S" vs frozen A-chip) | HIGH | RESOLVED, verified R3 |
| (superlative false-max, 565527) | — | RESOLVED, verified via go-live battery |
| RT-2H1 (tapioca-starch classifier miss, 13 products) | HIGH | RESOLVED, verified R3 |

**0 open CRITICAL. 0 open HIGH.** Page is owner-ready.

## Open, non-blocking MEDIUMs (pre-existing, untouched by this session's work — routed, not fixed)
- **RT-R3-M1** — `d4_additives` display array under-counts vs the honest "4 additives" copy claim on
  3 products (7290102393169, 7290102393176, 7290102393947). The copy is TRUTHFUL (trace
  `additive_marker_count=4`, matching the expansion's ingredient-string disclosure); the curated
  `d4_additives` chip array simply omits non-E-numbered additive categories (flavor agent, acidity
  regulator). Not new this session; not touched by the tapioca fix. Routes to data-agent (populate
  the array) or content-agent (align the count language to the displayed chips).
- **RT-R3-M2** — minor "X, ולא Y" phrasing + 2 advisory em-dashes in the mandatory category-caveat
  copy (relative-scoring disclosure box). Style-only, pre-existing, no scoring-dimension leakage.
  Routes to content-agent.

## Verification instruments run (round 3)
`run_gates.py` (G1–G8, `--run`/`--corpus`), `rank_check.py --emit-json` (0 FALSE, 2 confirmed TRUE),
score/grade-vs-trace census (0/78 mismatch), grade-monotonicity check (0 violations), Hebrew
leakage gate (0 genuine Tier-4 terms; 17 is_clean=False flags reviewed and confirmed decimal-nutrition
false positives, not score-mechanic leakage), Playwright real-DOM render at 375px (200, rtl/he, 78
rows, 0 console errors, 0 broken images, expand/collapse verified), `redteam_loop_ledger.py --round 3`
→ `DONE_ZERO_CRITICAL`, loop cap reached cleanly at 3/3.
