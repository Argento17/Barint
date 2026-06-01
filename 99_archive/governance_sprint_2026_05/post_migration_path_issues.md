# Post-Migration Path Issues

**Generated:** 2026-05-17  
**Scope:** All `.py`, `.md`, `.yaml`, `.json` files under `C:\Bari\03_operations\`  
**Status:** Review required — paths not automatically fixed (fix safety left to developer)

---

## Hardcoded path issues found

### Issue 1 — `batch_run.py`: BSIP1 source path

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\batch_run.py`  
**Line:** 28  
**Old value:** `C:\Bari\bsip1_concept\batch_test_001\output`  
**New correct path:** `C:\Bari\03_operations\bsip1\run_001\output`  
**Severity:** HIGH — `batch_run.py` will fail to find BSIP1 input data when run  
**Safe to fix:** Yes — straightforward path update  

```python
# Change from:
BSIP1_SOURCE = pathlib.Path(r"C:\Bari\bsip1_concept\batch_test_001\output")
# Change to:
BSIP1_SOURCE = pathlib.Path(r"C:\Bari\03_operations\bsip1\run_001\output")
```

---

### Issue 2 — `batch_run.py`: Output and report paths

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\batch_run.py`  
**Lines:** 29–30  
**Old values:**
```python
OUTPUT_ROOT = pathlib.Path(r"C:\Bari\bsip2_proto_v0\outputs")
REPORT_ROOT = pathlib.Path(r"C:\Bari\bsip2_proto_v0\reports")
```
**New correct paths:**
```python
OUTPUT_ROOT = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\outputs")
REPORT_ROOT = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\reports")
```
**Severity:** HIGH — batch runner will write outputs to non-existent path  
**Safe to fix:** Yes — straightforward path update  

---

### Issue 3 — `generate_review.py`: Trace and review paths

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\generate_review.py`  
**Lines:** 13–14  
**Old values:**
```python
TRACE_ROOT  = pathlib.Path(r"C:\Bari\bsip2_proto_v0\outputs\products")
REVIEW_ROOT = pathlib.Path(r"C:\Bari\bsip2_proto_v0\review")
```
**New correct paths:**
```python
TRACE_ROOT  = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\outputs\products")
REVIEW_ROOT = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\review")
```
**Severity:** HIGH — generate_review.py will fail to locate trace files  
**Safe to fix:** Yes — straightforward path update  

---

### Issue 4 — `generate_visuals.py`: Trace and visual output paths

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\generate_visuals.py`  
**Lines:** 26–27 (plus docstring comment on line 6)  
**Old values:**
```python
TRACE_ROOT  = pathlib.Path(r"C:\Bari\bsip2_proto_v0\outputs\products")
VISUAL_ROOT = pathlib.Path(r"C:\Bari\bsip2_proto_v0\visuals")
```
**New correct paths:**
```python
TRACE_ROOT  = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\outputs\products")
VISUAL_ROOT = pathlib.Path(r"C:\Bari\03_operations\bsip2\proto_v0\visuals")
```
**Severity:** HIGH — generate_visuals.py will fail when run  
**Safe to fix:** Yes — straightforward path update  

---

### Issue 5 — `diagnose_positive_structure.py`: Trace path

**File:** `C:\Bari\03_operations\bsip2\proto_v0\src\diagnose_positive_structure.py`  
**Line:** 8  
**Old value:** `C:\Bari\bsip2_proto_v0\outputs\products`  
**New correct path:** `C:\Bari\03_operations\bsip2\proto_v0\outputs\products`  
**Severity:** MEDIUM — diagnostic script only; not on critical path  
**Safe to fix:** Yes  

---

### Issue 6 — `batch_test_001.py`: BSIP0 source path

**File:** `C:\Bari\03_operations\bsip1\run_001\batch_test_001.py`  
**Lines:** 18 (comment), 38 (active code)  
**Old values:**
```python
# cd C:\\Bari
BSIP0_ROOT = Path(r'C:\Bari\bsip0_scrape')
```
**New correct path:**
```python
BSIP0_ROOT = Path(r'C:\Bari\03_operations\bsip0\scrape')
```
**Severity:** HIGH — BSIP1 batch runner will fail to locate BSIP0 scraped data  
**Safe to fix:** Yes — straightforward path update. Also update the comment on line 18.  

---

### Issue 7 — `azure_test.py`: Image path

**File:** `C:\Bari\03_operations\bsip0\pipeline\azure_test.py`  
**Line:** 12  
**Old value:** `C:\Bari\bsip0_pipeline\data\raw\snack_bars\product_001\nutrition1.png`  
**New correct path:** `C:\Bari\03_operations\bsip0\pipeline\data\raw\snack_bars\product_001\nutrition1.png`  
**Severity:** MEDIUM — azure_test.py is a test script, not production; image is confirmed present at new path  
**Safe to fix:** Yes  

---

### Issue 8 — Report `.md` files: Stale path references (non-breaking)

**Files:**
- `C:\Bari\03_operations\bsip1\run_001\reports\batch_report.md` line 4: references `C:\Bari\bsip0_scrape`
- `C:\Bari\03_operations\bsip2\proto_v0\reports\batch_summary.md` line 4: references `C:\Bari\bsip1_concept\batch_test_001\output`

**Severity:** LOW — documentation only; no code execution affected  
**Safe to fix:** Yes — update path references in these reports to reflect new locations  

---

## Summary

| # | File | Severity | Breaks on run? |
|---|---|---|---|
| 1 | `batch_run.py` L28 | HIGH | Yes — BSIP1 input not found |
| 2 | `batch_run.py` L29-30 | HIGH | Yes — outputs written to wrong location |
| 3 | `generate_review.py` L13-14 | HIGH | Yes — trace files not found |
| 4 | `generate_visuals.py` L26-27 | HIGH | Yes — trace files not found |
| 5 | `diagnose_positive_structure.py` L8 | MEDIUM | Yes — diagnostic only |
| 6 | `batch_test_001.py` L18,38 | HIGH | Yes — BSIP0 source not found |
| 7 | `azure_test.py` L12 | MEDIUM | Yes — test script only |
| 8 | Report `.md` files | LOW | No — documentation only |

**All HIGH severity issues are straightforward path string replacements.** No logic changes required.

---

## Recommended approach

Fix all HIGH severity issues before running any scripts. Each fix is a one-line string replacement. The pattern is consistent: replace `C:\Bari\{old_dir_name}\` with `C:\Bari\03_operations\{new_path}\`.

Consider refactoring hardcoded paths to use `pathlib.Path(__file__).parent.parent` relative resolution to prevent this class of issue in future restructuring.
