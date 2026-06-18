# P16 → Data Agent — yogurt OFF purge + dedup + clean re-run (follow-on to P13; launch path)

```
P16 / TASK-249 — Pipeline fixes from the S-grade audit, then the clean ship run.

VERIFIED FACTS (orchestrator): ALL 8/8 records in 03_operations/bsip1/
run_yogurt_yohananof_001/output carry off_candidate_panel (Open Food Facts
nutrition — banned project-wide, TASK-238). One of them (7290110565527)
duplicated a Shufersal barcode and its trace OVERWROTE the trusted Shufersal
trace in the run dir, hiding the defect.

DO:
1. In the yogurt batch runner (batch_run_yogurt_006_shipcfg.py lineage):
   add off_candidate_panel as a BLOCKING exclusion in process_corpus() —
   flagged products are excluded from scoring entirely, listed in the run
   record under "excluded_off_contaminated". No engine change, no flags change.
2. Add barcode deduplication in build_run_record(): on conflict, Shufersal
   corpus wins over Yohananof; a dedup event is recorded in the run record
   (never silent overwrite of trace files — write per-corpus trace dirs or
   suffix, your call, just no overwrites).
3. Re-run into 02_products/yogurt_system/bsip2_outputs/run_yogurt_006_shipcfg2/
   with the run record at reports/run_yogurt_006_shipcfg2_run_record.json.
   ACCEPTANCE: S_count = 1 (7290112336712 only, 92.6 — the audited honest S);
   7290110565527 = 89.9/A from its SHUFERSAL record; all 8 OFF-flagged
   Yohananof records excluded and listed.
4. Shadow backtest: python 03_operations/bsip2/proto_v0/src/shadow_backtest.py
   diff — attach verdict; frozen corpora must be untouched. Movement in yogurt
   corpora is expected (corpus exclusions) — list it.
5. Page-impact report: which products on the current v3 page lose coverage
   (expected: the 8-product Yohananof pool) — this defines the Shufersal-only
   launch scope (orchestrator ruling) for the frontend rebuild that follows.
6. Append a dated contamination record to tasks/TASK-238.md: run_yogurt_
   yohananof_001 built post-ban via the il_prices+OFF model; 8/8 records
   contaminated; excluded from scoring as of this run; re-entry only via the
   BSIP0.5 storefront fetcher (P6).

RULES: no engine/flag changes; no frontend changes; never delete the
contaminated BSIP1 records (they are evidence — exclusion, not erasure);
no Open Food Facts anywhere, including "just to compare".

RETURN BLOCK: runner diff summary; shipcfg2 grade distribution + S/A lists;
dedup + exclusion lists; Shadow verdict; page-impact list; TASK-238 entry
confirmation. Propose RETURNED.
```

---
**After you paste this to the agent:** open `tasks\DISPATCH_BOARD.md` and put an `x` in the P16 line under 📬 Signals (`- [ ]` becomes `- [x]`). That is how the orchestrator knows it's in flight.
