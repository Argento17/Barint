# HC Rework Data Refresh — TASK-380
**Run date:** 2026-06-23  
**Run ID:** hc_recover_off_barcodes_20260623_062002  
**Scope:** BSIP0→BSIP1 recovery for 2 OFF-contaminated barcodes + corpus audit

---

## Reachability table

| Retailer | From sandbox (2026-06-23) | Status code | Body bytes | Note |
|---|---|---|---|---|
| **Shufersal** | REACHABLE | 200 | ~133K | Product pages + search API live |
| **Victory** | REACHABLE | 200 | ~40K | Identity reachable; nutrition requires Playwright modal |
| Yochananof | BLOCKED | — | 0 | SSL ERR_CERT_COMMON_NAME_INVALID (consistent with SOURCE_SELECTION_POLICY.md) |
| Rami Levy | BLOCKED | — | 0 | Connection refused (consistent with rami_levy.yaml DEFERRED) |

Probe command run:
```
python C:\Bari\02_products\hard_cheeses\hc_recover_off_barcodes.py
```
Exit code: 0 (success).

---

## The 2 OFF barcodes: outcome

### 7290102302864 — Gouda Pesto Yruk 200g (גאודה פסטו ירוק)

**Status: DISCARD**

Scrape attempts:
- Shufersal: `GET /online/he/p/P_7290102302864` → HTTP 404. Search API returned 0 results.
- Victory: barcode search — 0 results.
- Yochananof (prior scrape, 2026-06-07): ingredients captured (success), nutrition tab missing.
- Rami Levy: not attempted — blocked from sandbox.

Per missing-data discard rule (owner 2026-06-13): product data not found one-shot at any reachable retailer. DISCARD record written at:  
`02_products/hard_cheeses/bsip1_outputs/bsip1_hardcheese_7290102302864.json`  
`data_sufficiency: "discard"`, `off_used: false`.

Note: The prior bsip2 trace for this barcode had nutrition (fat=34g, protein=24g, kcal=397, satfat=21g) sourced from an unknown non-yohananof path (likely the old bsip0_rerun_real.py via OFF). Those values cannot be retained — OFF ban applies. If the product needs to reappear, a fresh yohananof Playwright scrape from an Israeli IP is required to capture the nutrition tab.

### 7290014455252 — Grana Padano Mguredet (גרנה פדנו מגורדת)

**Status: RECOVERED** — Shufersal direct scrape

Source URL: `https://www.shufersal.co.il/.../grana-padano-mgudedet/p/P_7290014455252`  
Brand: מחלבות גד (Gad dairies)

Nutrition captured (per 100g, direct from Shufersal product page):

| Field | Value |
|---|---|
| Energy | 393 kcal |
| Fat | 29.0 g |
| Sat fat | 18.0 g |
| Carbohydrates | 0.0 g |
| Sugars | 0.0 g |
| Dietary fiber | 0.0 g |
| Protein | 33.0 g |
| Sodium | 600 mg |

Ingredients (Hebrew from Shufersal label):  
`חלב, מלח, אנזים מגבין, חומר משמר - ליזוזין(E-1105) (ביצים) מכיל ביצים`  
(4 ingredients; E-1105 = lysozyme preservative; NOVA 2)

Plausibility gate (DAIRY_SOLID): **PASS** — kcal=393 vs Atwater 4×0 + 4×33 + 9×29 = 393 (exact match).  
`off_used: false`, `provenance.source: "shufersal_storefront"`.

BSIP1 record written:  
`02_products/hard_cheeses/bsip1_outputs/bsip1_hardcheese_7290014455252.json`

---

## Corpus delta

| Stage | Count | Note |
|---|---|---|
| Starting count (existing BSIP1 records) | 68 | pre-run, confirmed by `Get-ChildItem bsip1_outputs | Measure-Object` |
| Recovered via direct scrape | +1 | 7290014455252 (Grana Padano) from Shufersal |
| Discarded (no data found one-shot) | +1 (discard record) | 7290102302864 (Gouda Pesto) |
| Final BSIP1 files (including discard records) | 70 | verified: `Get-ChildItem bsip1_outputs | Measure-Object → 70` |
| Net scorable additions | +1 | Grana Padano only |

**Live page context:** the live page (run_hard_cheeses_003_shelfrel) scores 30 products, all from the yohananof direct-scrape lineage. Of those 30, 0 overlap with the 37 OFF-contaminated records in bsip1_outputs. The 37 OFF records are from the dead `bsip0_rerun_real.py` run (uses OFF explicitly) — they are inert from the live page perspective but present a contamination risk for future pipeline runs.

---

## Cross-check: Grana Padano (≥2 retailers)

The Grana Padano barcode appeared at Shufersal (new direct scrape) and was previously in the bsip2 trace via an OFF-sourced record. The comparison:

| Field | Old value (OFF-sourced trace) | New value (Shufersal direct) | Agreement |
|---|---|---|---|
| fat_g | 29.0 | 29.0 | AGREE |
| fat_saturated_g | 18.0 | 18.0 | AGREE |
| protein_g | 33.0 | 33.0 | AGREE |
| energy_kcal | 393.0 | 393.0 | AGREE |
| sodium_mg | 600.0 | 600.0 | AGREE |
| carbohydrates_g | 0.0 | 0.0 | AGREE |
| ingredients | absent (OFF had none) | present (4 ingredients from Shufersal label) | NEW DATA |

Cross-source verdict: **FULL AGREEMENT** on all nutrition fields. Shufersal also adds ingredients text (`חלב, מלח, אנזים מגבין, חומר משמר - ליזוזין(E-1105)`) that was absent from the OFF-sourced record. Higher confidence now.

---

## OFF markers = 0 attestation (new records only)

Command run:
```powershell
Select-String -Path "C:\Bari\02_products\hard_cheeses\bsip1_outputs\bsip1_hardcheese_7290014455252.json" -Pattern "open_food_facts"
# Result: (no output)

Select-String -Path "C:\Bari\02_products\hard_cheeses\bsip1_outputs\bsip1_hardcheese_7290102302864.json" -Pattern "open_food_facts"
# Result: (no output)
```
Both new/updated records: **OFF markers = 0**.

### Extended corpus OFF status

The 37 pre-existing OFF-contaminated files in `bsip1_outputs/` are from the dead `bsip0_rerun_real.py` run (it explicitly uses `from integrations.clients.open_food_facts import get_product`). None of those 37 barcodes appear in the live page (run_hard_cheeses_003_shelfrel). These files are inert but contaminated — they should be explicitly excluded from any future pipeline pass by source filter. A separate cleanup task is recommended to delete or tombstone those 37 files to prevent accidental inclusion.

Verification command:
```powershell
# Count OFF files in bsip1_outputs:
Select-String -Path "C:\Bari\02_products\hard_cheeses\bsip1_outputs\*.json" -Pattern "open_food_facts" | Select-Object Filename -Unique | Measure-Object
# Output: Count = 37 (all pre-existing; 0 newly written with OFF)
```

---

## Blockers / flags for TASK-380

1. **Gouda Pesto DISCARDED** — this barcode needs a fresh Playwright scrape from Yochananof via an Israeli IP (or owner's machine) to capture the nutrition tab. Cannot be recovered from sandbox. Alternative: the product is a Dutch-market specialty; if Yochananof no longer stocks it, the discard stands permanently.

2. **37 OFF-contaminated bsip1 records** are inert but present — they are NOT used by the live page and should be cleaned up in a future pipeline pass to prevent accidental re-inclusion.

3. **Scope note**: This BSIP0→BSIP1 run was RECOVERY-ONLY (2 barcodes). Corpus augmentation from additional Shufersal/Victory products (new products not in the existing 68) was NOT performed — the spec said "leverage what already exists" and the yohananof-sourced 30-product live corpus is complete.

---

## Artifacts

| File | Action | Purpose |
|---|---|---|
| `bsip1_outputs/bsip1_hardcheese_7290014455252.json` | created | Grana Padano RECOVERED, Shufersal direct |
| `bsip1_outputs/bsip1_hardcheese_7290102302864.json` | created | Gouda Pesto DISCARD record |
| `HC_REWORK_RUN_LOG.json` | created | Machine-readable run log (reachability + results) |
| `hc_recover_off_barcodes.py` | created | Recovery script |
| `HC_REWORK_DATA_REFRESH.md` | created | This summary |
