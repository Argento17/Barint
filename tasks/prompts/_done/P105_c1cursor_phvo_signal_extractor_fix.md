# P105 — TASK-280 Phase-3: PHVO signal_extractor.py Corrections (route: C1-CURSOR)
# Spec-complete implementation of D6+D7 authorized PHVO marker corrections

**Repo:** `C:\Bari`
**Task:** `C:\Bari\tasks\TASK-280.md` (status: IN_PROGRESS)
**D6 Ruling:** `C:\Bari\tasks\returns\P103_return.md`
**D7 Co-Sign:** `C:\Bari\01_framework\bsip2_framework\phvo_governance\phvo_d7_cosign_v1.md`

---

## What to change

Target file: `C:\Bari\03_operations\bsip2\proto_v0\src\signal_extractor.py`

### Change 1: Remove מחמאה from _PHVO_MARKERS

Current (around line 1160–1169):
```python
_PHVO_MARKERS = [
    "שומן צמחי מוקשה",
    "שמן צמחי מוקשה",
    "מוקשה חלקית",
    "partially hydrogenated",
    "שומנים מוקשים",      # Fix-B: generic hardened fats (plural)
    "שומן מוקשה",         # Fix-B: generic hardened fat (singular)
    "מחמאה",              # Fix-B: margarine/shortening (Hebrew common form)
    "מרגרינה",            # Fix-B: margarine (transliteration form)
]
```

Replace with:
```python
_PHVO_MARKERS = [
    "שומן צמחי מוקשה",
    "שמן צמחי מוקשה",
    "מוקשה חלקית",
    "partially hydrogenated",
    "שומנים מוקשים",      # Fix-B: generic hardened fats (plural)
    "שומן מוקשה",         # Fix-B: generic hardened fat (singular)
    # "מחמאה" REMOVED — clarified butter (ghee), animal fat, not PHVO. D6 Q1 (TASK-280/EV-086).
    "מרגרינה",            # Fix-B: margarine (transliteration form)
]
```

### Change 2: Fix the comment at line ~1158 that misidentifies מחמאה

Find the comment block that says something like:
```python
# מחמאה-style ingredient declarations), מחמאה (margarine),
```
or any line in the comment block preceding _PHVO_MARKERS that mentions "מחמאה" as "margarine". Replace with accurate description:
```python
# (TASK-280/EV-086): מחמאה REMOVED — was misidentified as margarine; it is clarified butter (ghee),
# an animal fat. sat_fat dimension handles it correctly. See EV-086.
```

### Change 3: Add position-aware PHVO detection

Find the code that sets `has_phvo = True`. Currently it uses full-text search on `ing_text` or `full_text`.

Replace the `has_phvo` detection logic with a position-aware version:

```python
# PHVO detection: only fire if marker appears in first 8 ingredient positions (1-indexed).
# Fallback to full-text search when ingredient_order is not available.
# D6 Q2 / D7 (TASK-280/EV-086): position gate prevents trace margarine from triggering.
has_phvo = False
if ingredient_order:  # use structured list (position-aware)
    early_ingredients = " ".join(
        item.get("text", "").lower()
        for item in ingredient_order
        if item.get("position", 999) <= 8
    )
    has_phvo = any(marker in early_ingredients for marker in _PHVO_MARKERS)
else:  # fallback: full-text search (same behavior as before position gate)
    phvo_text = (ing_text or full_text or "").lower()
    has_phvo = any(marker in phvo_text for marker in _PHVO_MARKERS)
```

**NOTE:** `ingredient_order` is the structured list already built from parsing. Check the actual variable names in the code — adapt to the actual variable names used. Do NOT change the logic; only adapt to the actual variable names.

**NOTE:** The position check uses `<= 8` (1-indexed, covers first 8 ingredients). Do NOT use `<= 7`.

---

## No-regression gates (run BEFORE declaring done)

### Gate 1: Engine invariants
```
cd C:\Bari\03_operations\bsip2\proto_v0
python shadow\engine_invariants.py
```
Must PASS all 342 invariants. STOP if any FAIL.

### Gate 2: Brined cheeses byte-identical
Run brined cheeses scoring WITHOUT shelf-relative flag and compare to `run_brined_004`:
```
python proto_v0\run_scoring.py --category brined_food --output-dir ..\..\..\temp_brined_check
```
Compare scores to `02_products\brined_cheeses\bsip2_outputs\run_brined_004\products\` — every product `final_score_estimate` must match within ±0.01. If brined re-scoring is not supported with that command, run it using whatever mechanism was used for P99 (which verified 48/48 byte-identical).

### Gate 3: Milk byte-identical (frozen invariant)
Same check for milk — score output must be identical to `run_005_headpin`. Milk does not contain PHVO markers, so this gate should trivially pass, but confirm.

STOP on any gate failure. Do not proceed.

---

## Definition of Done

- [ ] מחמאה removed from _PHVO_MARKERS
- [ ] Line ~1167 comment corrected ("REMOVED — clarified butter / ghee, animal fat, not PHVO. D6 Q1 TASK-280/EV-086")
- [ ] Line ~1158 comment block fixed (no more false "margarine" reference to מחמאה)
- [ ] Position-aware has_phvo detection implemented (1-indexed `<= 8`, fallback to full-text)
- [ ] Gate 1: engine_invariants 342 PASS
- [ ] Gate 2: brined 48/48 byte-identical to run_brined_004
- [ ] Gate 3: milk byte-identical to run_005_headpin
- [ ] NO other files modified (score_engine.py UNTOUCHED, no JSON files modified)

---

## Constraints

- **Modify ONLY `signal_extractor.py`** — no other engine files
- **DO NOT modify any comparison JSON files** — no deployed scores
- **OFF ban absolute** — no Open Food Facts
- **STOP on any gate failure** — report and do not continue

---

## Return format

Write return to `C:\Bari\tasks\returns\P105_return.md`:

```json
{
  "task_id": "TASK-280",
  "phase": "Phase-3 implementation",
  "status": "RETURNED",
  "return_date": "...",
  "agent": "c1-cursor",
  "changes": {
    "mchama_removed": true,
    "comment_1167_fixed": true,
    "comment_1158_fixed": true,
    "position_gate_implemented": true,
    "position_gate_logic": "ingredient_order-based 1-indexed position <= 8, full-text fallback"
  },
  "gates": {
    "G1_invariants": {"pass": true, "count": 342},
    "G2_brined": {"pass": true, "count": 48},
    "G3_milk": {"pass": true}
  },
  "files_modified": ["03_operations/bsip2/proto_v0/src/signal_extractor.py"],
  "not_done": []
}
```

**Do not close — propose RETURNED and let the orchestrator verify.**
