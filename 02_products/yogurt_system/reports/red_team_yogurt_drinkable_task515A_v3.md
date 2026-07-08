# Red-Team Challenge Report — yogurt-drinks closing pass (TASK-515A)
Date: 2026-07-08
Scope: 20 products, /hashvaot/yogurt-drinks, yogurt_drinkable_frontend_v1.json (sha256 886656b6…4d24)
Rounds: 3 (loop-capped). Verdict: **OWNER-READY — 0 open CRITICAL, 0 open HIGH.**

---

## Round-by-round summary

**Round 1** (0 CRITICAL / 2 HIGH / 4 MEDIUM): RT-C5 (55329 copy wrongly headlined sugar instead of
the real additive/processing driver), RT-C4 (additive card e_number mismatch — showed E1422 where 4
products' labels declare E1442), RT-V1 (`validate_comparison_page.py --http` false-failed all
same-origin relative imageUrls — instrument bug, not a page defect), plus 4 MEDIUMs (all resolved or
acknowledged). All FIXED and verified.

**Round 2** (3 fixes confirmed resolved, 0 regression) surfaced a NEW HIGH, **RT-2H1**: the ingredient
classifier missed the source-qualified label "עמילן טפיוקה מעובד" (modified tapioca starch) —
contiguous-substring matching fell through to the bare "עמילן" (starch) token and mis-classified it
as native/benign, so the ECS-v1 stabilizer-complexity penalty never fired. Blast-radius measurement:
27 live-indexed products across 5 pages (drinkable 3, spoonable 13, hummus 3, cakes_hard_cookies 7,
crackers 1); orchestrator later confirmed the true count is **28** (2 additional cakes barcodes,
OCR-noise-obscured but genuinely on-label, were wrongly excluded from the original scan). Nutrition +
Product co-signed the fix (`TAPIOCA_STARCH_FIX_COSIGN.md`); C3 (P509) independently endorsed
"fix-now-split": correct the classifier and rescore the two PRE-LAUNCH yogurt pages immediately, hold
the 3 LIVE categories' regeneration+redeploy for explicit owner approval (published scores move
there — consumer-deploy tripwire).

**Round 3 (this report, FINAL/loop-capped):** verified RT-2H1 fully landed on drinkable's 3 affected
products — 7290110573737 (B→C, 62.4), 7290107938396 (C→D, 48.6, plus a priority copy fix: it had
falsely claimed "שני מייצבים טבעיים"/two natural stabilizers when a third, non-natural modified-starch
stabilizer was on-label — now honestly reads three stabilizers with the modified starch explicitly
flagged non-natural), and 7290110552244 (score moved, stayed C). All three: score==trace, additive
card counts match copy, no regression on any Round 1/2 fix. Full deterministic sweep GREEN
(`run_gates.py` exit 0, `validate_comparison_page.py --http` exit 0 all 8 gates, `rank_check.py` 0
FALSE / 7 pre-existing manual-review WARNs on unrelated barcodes). Real-DOM render verified both
375px and desktop: HTTP 200, RTL/Hebrew, 20 rows, 0 console errors, no horizontal overflow, all 20
images load, the first-ever live E-grade (barcode 55329, score 34.3) renders with the distinct
`gradePalette.E` treatment (#A52121).

**Post-round-3 fix (orchestrator-caught, self-verified, no 4th round spun):** Round 3 surfaced one
MEDIUM, RT-3M1 — barcode 55329's copy made two mutually-inconsistent "two stabilizers" claims
(row-level text said carrageenan+modified-starch; the expansion said pectin+carrageenan), both
undercounting the true 3 stabilizer-class agents on its label (pectin E440, carrageenan E407,
modified starch E1442). Content unified every mention to the honest 3-agent list. Orchestrator
independently re-verified: all stabilizer-count mentions on 55329 now agree, go-live battery still
PASS, score/grade/d4 untouched by the copy-only fix.

---

## Final state — all findings

| ID | Severity | Status |
|---|---|---|
| RT-C5 (55329 driver honesty) | HIGH | RESOLVED, verified R2+R3 |
| RT-C4 (additive-card e_number) | HIGH | RESOLVED, verified R2+R3 |
| RT-V1 (validator instrument) | MEDIUM | RESOLVED, verified R2+R3 |
| RT-2H1 (tapioca-starch classifier miss) | HIGH | RESOLVED, verified R3 |
| RT-3M1 (55329 stabilizer-count inconsistency) | MEDIUM | RESOLVED post-R3 |
| RT-C1 (55329 −4.0 derivation) | — | RESOLVED R1 (verified: genuine emulsifier-complexity penalty, not a null/missing-data artifact) |
| RT-C2 (E/D boundary is 0.9pt/noise-level) | — | ACKNOWLEDGED (inherent to banded thresholds; copy doesn't dramatize) |

**0 open CRITICAL. 0 open HIGH. 0 open MEDIUM.** Page is owner-ready.

## Score-neutral follow-ups (not blocking, logged separately)
- `trace_writer.py::assemble_trace()` omits `emulsifier_complexity_penalty` from the serialized
  `penalties_applied` ledger — benign for arithmetic (the engine's own score is correct) but
  under-discloses the mechanism behind a public grade. Recommend a trace-serialization fix + regen.
- 55329's raw trace `nova_evidence_for` field carries a copy-pasted "processed cheese archetype" note
  and mislabels its natural purple-carrot color as `artificial_color_detected` — zero score impact
  (consumer copy already correctly calls the color natural), but the trace text itself should be
  cleaned for future auditors.
- The live 3-category re-flow (hummus/cakes/crackers, 28 products, up to one grade band on 4 of
  them) is queued as an owner-approval digest item — not executed, not blocking this page.

## Verification instruments run (round 3 + post-fix)
`run_gates.py` (incl. `--run` trace verify), `validate_comparison_page.py --http`, `rank_check.py
--emit-json`, `hebrew_readability.analyze` (132 strings, 0 not-clean), Playwright real-DOM render at
375px + desktop (0 console errors both viewports), `redteam_loop_ledger.py --round 3` →
`DONE_ZERO_CRITICAL`.
