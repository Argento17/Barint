---
id: TASK-244
title: "Snacks confidence inflation structural fix (DA-013): fallback must re-derive, not trust generator confidence"
owner: data-agent
status: RETURNED
priority: HIGH
created_at: 2026-06-11
depends_on: [TASK-242]
blocks: []
category_id: null
branch: task-244-confidence-structural-fix
commit: d87a625e
summary: >
  snacks_frontend_v2 shipped 4 products (snk-003/007/009/020) as verified/full-data with no
  nutrition panel. Root cause DA-013: confidence_annotation.annotate_fallback preserves inflated
  generator confidence when no trace joins. The DISPLAY hotfix shipped in TASK-242 (4-row,
  4-field copy-free patch to partial/missing_nutrition). THIS task owns the structural fix:
  fallback re-derives instead of trusting, LIVE_FILES staleness corrected, snacks regenerated,
  0 verified-with-unknowns verified corpus-wide.
---

# TASK-244 — Snacks confidence structural fix (DA-013)

## Context (2026-06-11)
- The consumer-visible symptom was fixed in **TASK-242** as an honest-display hotfix:
  snk-003/007/009/020 flipped verified→partial with the canonical `missing_nutrition`
  label/tooltip/sub_reason from `confidence_annotation.py:43-44`. That patch is NOT the fix —
  it is the disclosure. This task removes the mechanism that produced the inflation.
- data-agent reviewer return (TASK-242, 2026-06-11) confirmed the inflation set is exactly
  those 4 rows (full 18-product scan: all-null panels corpus-wide; 14 rows honest partial).

## Scope
1. **DA-013 root cause:** `confidence_annotation.annotate_fallback`
   (`03_operations/bsip2/proto_v0/src/confidence_annotation.py:235-238`) preserves the
   generator's confidence when a product does not join a trace. Change it to RE-DERIVE from
   the product's own data state (null panel ⇒ never verified). Add a regression test.
2. **LIVE_FILES staleness** in `run_confidence_annotation_pass.py`: remove dead/unshipped
   entries (`salty_snacks_v3`, `olive_oil_v1`, `crackers_staged_v1`,
   `frozen_vegetables_frontend_v1`), add the live `salty_snacks_frontend_v4.json`.
3. **Regenerate snacks** through the corrected pass (or frontend_core migration if TASK-233F
   reaches snacks first — coordinate, don't duplicate); verify the 242 hotfix values are
   reproduced by derivation, not preserved by accident.
4. **Corpus-wide assertion:** 0 products with `verified` + missing panel across all live JSONs.

## Carried findings from the TASK-242 review (park here)
- **bottomLine score drift on the 4 snacks rows** (pre-existing on master): bottomLine cites
  53/28/47/33 while top-level scores are 55/27/48/32. Copy-bearing fix — handle in the snacks
  regeneration with the banned-term/anti-redundancy filter (TASK-233F pattern).
- **Stale "OFF stays LOCAL" framing** in
  `02_products/salty_snacks/reports/run_record_salty_snacks_rescue_task241.json` purpose line —
  superseded by the project-wide ban (TASK-238 reinstated). Cosmetic root-repo artifact; fix
  alongside the regeneration commit.
- **OFF gate pattern note:** the OFF grep gate is pinned to `openfoodfacts` host/URL patterns.
  Salty v4 `_meta` drop reasons contain literal "OFF" negation tokens ("NOT backfilled from
  OFF") — acceptable; optionally reword to "any external aggregator" when next regenerated.

## DoD
- [x] `annotate_fallback` re-derives (never trusts) + regression test
- [x] LIVE_FILES corrected (no dead files, salty v4 present)
- [x] snacks regenerated; 242 hotfix values reproduced by derivation; bottomLine drift fixed
- [x] 0 verified-with-missing-panel across ALL live JSONs (scripted check output attached)
- [x] No scoring/engine change; no OFF; validation gate green

## Return block (data-agent, 2026-06-11)

**Branch:** `task-244-confidence-structural-fix` | **Commit:** `d87a625e`

### DA-013 fallback diff
`confidence_annotation.py:235-254` — `annotate_fallback(existing_confidence)` →
`annotate_fallback(product)`. New logic: checks `product["expansion"]["nutrition"]`
for any non-null value. Null panel → always `partial, missing_nutrition`; panel
present → trusts existing confidence + sub_reason. Never produces insufficient.

**Second inflation path closed:** display-panel safety override added in
`run_confidence_annotation_pass.py:133-141` — after `annotate_from_trace`, if
result is "verified" but `expansion.nutrition` is all-null, downgrades to
`partial, missing_nutrition`. Caught snk-007/009/020 which DO join traces (via
barcode) but those traces are from a stale run (score mismatch: 46/46/39 vs
display 27/48/32); the trace said verified, the display has a null panel.

### Regression test
`test_confidence_annotation_fallback.py` — 9 assertions, all pass:
- null panel + verified → partial/missing_nutrition ✓
- null dict → partial/missing_nutrition ✓
- null panel + already partial → partial/missing_nutrition ✓
- panel present + verified → stays verified ✓
- panel present + partial/partial_field → preserved ✓
- panel present + partial/low_extraction → preserved ✓
- never insufficient (×2 cases) ✓
- labels populated ✓

### LIVE_FILES diff
Removed: `crackers_staged_v1.json`, `frozen_vegetables_frontend_v1.json`,
`olive_oil_frontend_v1.json`, `salty_snacks_frontend_v3.json`.
Added: `salty_snacks_frontend_v4.json`.

### Snacks regen deltas (confidence + copy only; scores identical)
All 18 snacks → `partial` (was 18 partial already; 4 were inflated "verified"
pre-TASK-242 hotfix). 4 target products all re-derive to `partial/missing_nutrition`
via the new structural path, not by preserving the TASK-242 hotfix values.

12 stale `expansion.confidenceLabel = "נתונים מלאים יחסית"` → canonical labels
(e.g. "חסרים נתוני תזונה", "מבוסס על נתונים חלקיים", "נתונים בבדיקה").

bottomLine drift fixed for snk-003/007/009/020: 53/28/47/33 → 55/27/48/32.

All 12 live category JSONs regenerated (12/12 files written); expansion.confidenceLabel
synced with confidence_label_he corpus-wide.

### Corpus-wide assertion output
```
CORPUS-WIDE ASSERTION: verified + null expansion.nutrition
Total issues: 0
  PASS — 0 verified products with null expansion.nutrition panels
Categories with verified products:
  cereals: 3 verified, 0 verified+null_panel
  cheese: 19 verified, 0 verified+null_panel
  granola: 9 verified, 0 verified+null_panel
  maadanim: 3 verified, 0 verified+null_panel
  salty_snacks_v4: 7 verified, 0 verified+null_panel
  yogurts_v4: 19 verified, 0 verified+null_panel
```

### Guard verification
- Scores byte-identical for snacks/salty/butter/cheese (sampled): PASS
- No OFF strings introduced: PASS (annotation pass adds no content, only annotation fields)
- INVARIANT (0 flips to insufficient): PASS

### Stale OFF framing note
`run_record_salty_snacks_rescue_task241.json` is on `salty-snacks-v4` only
(not on master). Cosmetic fix deferred to `salty-snacks-v4` merge commit.
`_meta` drop reasons "NOT backfilled from OFF" are acceptable negation tokens
(task §carried-findings: "acceptable; optionally reword").

Do NOT close — RETURN for orchestrator verification.
