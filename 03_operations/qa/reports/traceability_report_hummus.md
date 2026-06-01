# Bari Traceability Validation Report — hummus

**Generated:** 2026-05-30 21:03:36  
**Category:** hummus  
**Overall verdict:** PASS ✅

---

## TRC-002 — BSIP0 Backlink Check

> Every canonical `bsip1_{barcode}.json` must have a matching BSIP0 source.

| Metric | Value |
|--------|-------|
| Verdict | **PASS ✅** |
| Total BSIP1 files checked | 69 |
| Matched to BSIP0 source | 69 |
| Unmatched (no BSIP0 found) | 0 |

All 69 BSIP1 files have a confirmed BSIP0 source.

---

## CAN-004 — Exclusion Leak Check

> Products rejected in `candidate_review.csv` must not appear in `canonical_bsip1/`.

| Metric | Value |
|--------|-------|
| Verdict | **PASS ✅** |
| CSV files scanned | 1 |
| Rejected products checked | 90 |
| Leaked into canonical | 0 |

All 90 rejected products are absent from `canonical_bsip1/`.

---

## Summary

| Check | Verdict | Key metric |
|-------|---------|------------|
| TRC-002 — BSIP0 backlink | PASS ✅ | 69/69 matched |
| CAN-004 — Exclusion leak | PASS ✅ | 0 leaked / 90 rejected |

**Overall: PASS ✅**

Category `hummus` passed both traceability checks. Clear to proceed to BSIP2.

---

*Bari Traceability Validator v1 — [TRC-002 + CAN-004 per category_factory_qa_v1.md]*