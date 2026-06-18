---
id: TASK-250
title: Yogurts scoring methodology rulings from red-team v4 — A-grade eligibility with null sugar (RT-6), rounding at grade boundaries (RT-4/RT-13), null satFat silence (RT-9), sweetener signal absence (RT-10), ceiling compression disclosure (RT-11)
owner: nutrition-agent
status: RETURNED
priority: HIGH
created_at: 2026-06-11
depends_on: []
blocks: [TASK-249]
category_id: null
summary: >
  Red-team yogurts v4 raised 6 methodology questions that must be ruled on BEFORE run_yogurt_006 regenerates scores. Central question - can a product hold 90/A when its sugar value is null and the sugar cap cannot fire. Any scoring change needs D7 co-sign + owner tripwire sign-off. Deliverable is a ruling pack consumed by TASK-249 regen.
phase2_status: COMPLETE — run_yogurt_006 generated; staging JSON at yogurts_frontend_v006_staging.json; owner sign-off pending on Ruling 3 grade corrections before live publish
---

# TASK-250 — Yogurts scoring methodology rulings from red-team v4 — A-grade eligibility with null sugar (RT-6), rounding at grade boundaries (RT-4/RT-13), null satFat silence (RT-9), sweetener signal absence (RT-10), ceiling compression disclosure (RT-11)

## Return Block — Phase 1 (Ruling Pack)

**Status:** RETURNED (phase 1 complete; phase 2 complete)
**Date:** 2026-06-11
**Ruling file:** `02_products/yogurt_system/reports/yogurts_v4_methodology_rulings_v1.md`

### Phase 1 Deliverable

Five rulings issued, one per RT finding in scope. Summary:

| Ruling | RT Finding | Decision | Owner Tripwire |
|--------|-----------|----------|----------------|
| 1 | RT-6 null sugar / A-grade | A allowed; add −10 confidence reduction for null sugar_g → confidence_band becomes partial | No |
| 2 | RT-9 null satFat silence | Same disclosure principle; add −5 confidence reduction for null satFat; flag 2 Greek products for re-scrape | No |
| 3 | RT-4 + RT-13 grade-boundary rounding | Grade-before-round is correct policy; fix builder to use raw score for grade assignment; owner sign-off required before live publish | Yes — owner sign-off before go-live |
| 4 | RT-10 sweetener signal absence | Detection bug, not missing rule; sweetener cap is already wired; fix sweetener_tier null gap in signal_extractor | No |
| 5 | RT-11 ceiling compression | Intentional; no score change; add disclosure to category caveat copy; exclude barcode 7290116932620 pending corruption fix | No |

---

## Return Block — Phase 2 (Implementation)

**Status:** RETURNED
**Date:** 2026-06-11
**Implemented by:** nutrition-agent (Data Agent scope; no Product Agent co-sign yet — see gate)

### Phase 2 Deliverable

run_yogurt_006 generated with all applicable rulings. Staging JSON produced.

**Score movement table (run_005 → run_006):**

| Barcode | Name | Score | Grade 005 | Grade 006 | Conf 005 | Conf 006 | Ruling |
|---------|------|-------|-----------|-----------|----------|----------|--------|
| 7290114313070 | יוגורט מוקצף אפרסק | 35 | D | **E** | high | high | R3 grade-before-round (raw=34.8) |
| 7290102399819 | מולר פרוטאין יוגורט.פירות | 50 | C | **D** | high | high | R3 grade-before-round (raw=49.6) |
| 7290110321031 | יופלה GO מועשר בחלבון | 90 | A | A | high (eng=85) | medium (eng=70) | R1+R2 null sugar+satFat confidence |
| 7290116935614 | יוגורט GO חלבון 25 גרם | 90 | A | A | high (eng=85) | medium (eng=70) | R1+R2 null sugar+satFat confidence |
| 7290112336712 | דנונה פרו 21 חלבון | 90 | A | A (after 89.9 cap) | high (eng=85) | high (eng=80) | R2 null satFat only (sugar present) |
| All other products | — | unchanged | unchanged | unchanged | — | — | No ruling impact |

**Notes:**
- Scores are identical between run_005 and run_006 for all products (rulings touch confidence only + grade assignment fix).
- Frontend confidence label was already "partial" for the A-grade products in run_005 due to annotation logic (single-source). The engine confidence band changes are correctly recorded in traces.
- Ruling 4 (sweetener cap): NOT APPLICABLE. Investigation found that BSIP1 sweetener_count=1 for the three flagged products (7290102395231, 7290114311069, 7290112336712) is from honey or table sugar appearing in nutrition table text — not non-nutritive sweeteners. BSIP2's SWEETENER_TIER_*_HE lists are correctly scoped to non-nutritive sweeteners only. The sweetener cap should not and does not fire. No vocabulary fix needed.
- Ruling 2 re-scrape: NOT NEEDED. Both full-fat Greek products (7290017065588 10%, 7290014890589 8%) have satFat available in BSIP1 (6.6g and 4.8g respectively). The Ruling 2 re-scrape flag does not apply.
- 7290116932620 excluded from run_006 corpus (protein=190 corruption, RT-1, Ruling 5).

### Pre-conditions for go-live (OWNER TRIPWIRE — Ruling 3)

Frontend JSON is staged at:
`C:\Bari\02_products\yogurt_system\yogurts_frontend_v006_staging.json`

It must NOT be written to `bari-web/src/data/` until the owner signs off on the two grade corrections:
- 7290114313070: 35/D → 35/E (raw=34.8, builder was rounding before grading)
- 7290102399819: 50/C → 50/D (raw=49.6, same builder bug)

### Artifacts

- `C:\Bari\02_products\yogurt_system\reports\yogurts_v4_methodology_rulings_v1.md` — ruling pack
- `C:\Bari\03_operations\bsip2\proto_v0\src\batch_run_yogurt_006.py` — run_006 batch runner (BARI_TASK250_CONF=on)
- `C:\Bari\03_operations\bsip2\proto_v0\src\score_engine.py` — TASK-250 flag + confidence reductions (lines ~135–150, ~865–880)
- `C:\Bari\02_products\yogurt_system\build_yogurts_frontend_v006.py` — run_006 frontend builder (grade-before-round fix + staging-only output)
- `C:\Bari\02_products\yogurt_system\yogurts_frontend_v006_staging.json` — STAGED frontend JSON (not live)
- `C:\Bari\02_products\yogurt_system\bsip2_outputs\run_yogurt_006\` — 88 product traces
- `C:\Bari\02_products\yogurt_system\reports\run_yogurt_006_run_summary.json` — run summary
