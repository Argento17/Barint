---
id: TASK-147
title: Fix 2 maadanim corpus data anomalies surfaced by TASK-144 (OCR protein outlier + mis-binned cheese)
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-01
completed_at: 2026-06-02
close_reason: "oth maadanim corpus defects corrected at source; this was data hygiene only \u2014 no scoring rule or engine version changed"
depends_on: [TASK-144]
blocks: []
category_id: null
summary: >
  TASK-144 surfaced two source-data defects in the maadanim corpus (neither on the live 87 shelf): (1) יוגורט גו נטול לקטוז has source protein_g=190/100g — an OCR artifact, now correctly flagged insufficient_data by the new macro-plausibility guard; fix the source value. (2) גבינה צפתית מעודנת 5% is a צפתית CHEESE mis-binned into maadanim (false sugar signal from un-sanitized panel text) and is the lone A in the patched run — recommend excluding it from the maadanim corpus / re-routing to cheese. Data Agent to correct both at source.
---

# TASK-147 — Fix 2 maadanim corpus data anomalies surfaced by TASK-144 (OCR protein outlier + mis-binned cheese)

## Resolution (2026-06-02, data-agent) — corpus hygiene, both corrected AT SOURCE

### Defect 1 — יוגורט גו נטול לקטוז (`bsip1_maadanim_7290116932620`): OCR protein outlier
`protein_g = 190.0/100g` is physically impossible (a single macro cannot exceed 100g/100g).
Origin: panel-text OCR bleed — the scrape captured `"...100 גרם 86 קל אנרגיה 190 גרם חלבונים..."`.
The label declares **only per-cup** protein (`25 גרם חלבון בגביע, מתוכם 11.5 ... מי גבינה, 13.5 ... קזאין`)
with no package/serving weight, so a true **per-100g** value is **unrecoverable**. Per the hard rule
(do not invent nutrition data), `protein_g` set to **null** rather than substituting a number.
*(For the reviewer: energy balance — 86 kcal − 4.4g carb×4 − 2g fat×9 ≈ 12.6g — is consistent with a
high-protein dairy matrix, but it is an inference, not a label value, so it was NOT written as data.)*

Fixed at source:
- `03_operations/bsip1/run_maadanim_001/output/bsip1_7290116932620.json` — `protein_g 190.0 → null`;
  added to `missing_fields`; provenance recorded in `enrichment_warnings`.
- `02_products/maadanim/maadanim_bsip0_raw_20260528T072053.json` — upstream scrape record:
  `protein_raw "190" → ""` + `protein_raw_note` (prevents silent re-propagation on any BSIP1 rebuild).
- BSIP2 trace regenerated (engine 0.4.1, `BARI_TASK144_FIXES=on`): **75/B → 58.9/C**, confidence 50→80
  (the −40 macro-implausibility deduction and the confidence-ceiling=75 no longer apply once the bad
  value is gone). Still off-shelf.

> Note: the TASK-144 line "now correctly flagged insufficient_data by the macro-plausibility guard" was
> optimistic — the guard's −40 deduction took confidence 100→50, which is still ≥ the 40 insufficiency
> gate (`score_engine.py:1116`), so the product had been surviving as a **spurious 75/B**. The source
> fix is the real correction; the guard is a backstop, not a quarantine.

### Defect 2 — גבינה צפתית מעודנת 5% (`bsip1_maadanim_554532`): mis-binned cheese (the lone A)
A צפתית **salty cheese**, not a dairy dessert. BSIP0 `source_url` → שופרסל *מדף הגבינות › גבינות מלוחות*;
`category_raw` = cheese taxonomy `[A0104, …, A010407, A01]`. It entered maadanim via the `עדנה` brand
query matching the `עדנ` substring of `מעודנת`. It was the patched run's only A because it is a clean
high-protein/low-fat/low-carb cheese carrying a **false** added-sugar marker (the `סוכר` came from
un-sanitized panel-text bleed `"...1.5 כפיות סוכר..."`; `sugars_g` is actually null).

Excluded from the maadanim corpus at source:
- `bsip1_554532.json` moved to `03_operations/bsip1/run_maadanim_001/_excluded_misbinned/` (quarantined,
  not deleted — provenance preserved) with a `README.md` explaining the exclusion + cheese re-route.
- Its BSIP2 trace dir `…/products/bsip1_maadanim_554532/` deleted.
- Re-route to cheese is documented; actual insertion into a cheese corpus is out of scope (the cheese
  pipeline `run_cheese_001` is NON-AUTHORITATIVE / NO-GO).

### Re-derived counts (run_maadanim_001: 200 → 199 products)
| Grade | before (200) | after (199) |
|-------|---|---|
| A | 1 | **0** |
| B | 4 | **3** |
| C | 53 | **54** |
| D | 84 | 84 |
| E | 26 | 26 |
| insufficient | 32 | 32 |

A 1→0 (cheese removed); B 4→3 / C 53→54 (Go moved B→C). **No A remains in the corpus.**
Updated: `reports/run_maadanim_001_batch_summary.md` (regenerated from the 199 traces, no re-scoring of
the other 197) and `maadanim_corpus_report_v1.md` (traces 200→199, excluded 110→109, cheese line removed).
`category_config.json` `record_count: 90` (editorial scope) is unaffected — both products were already in
the 110 "excluded / no insight line" set, never in editorial scope.

### Live shelf — UNCHANGED (confirmed)
`maadanim_frontend_v2.json` = **87 products**, **0** occurrences of either product (`554532` /
`7290116932620` / both names). No frontend file was edited by this task. The live shelf is decoupled
(surgical v2 from TASK-144) and neither anomaly was ever displayed.

### 142A coordination
The cheese's false sugar signal shares root cause with TASK-142A's panel-text bleed. This fix is corpus
hygiene (exclusion + protein null) and does **not** depend on 142A's sanitization; no wait. Two related
follow-ups surfaced but left out of scope: (a) other bulgarian/צפתית cheeses still sit in the maadanim
"excluded" set (`גבינה בולגרית מעודנת 5%`, `בולגרית מעודנת 24%`×3, `קוביות/פרוסות בולגרית 5%`) — they
scored below A so never surfaced; (b) router/acquisition substring `עדנ`⊂`מעודנת` false-match.

## Disposition: propose RETURNED
Both defects corrected at source; counts re-derived; live 87-shelf verified unchanged. No scoring rule
changed (engine 0.4.1 untouched) — data hygiene only. Rollback = restore the two source values and the
quarantined file from git. Central Controller to record CLOSED.
