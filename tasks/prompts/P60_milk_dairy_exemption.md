# P60 / Implement dairy-single-token NOVA-1 exemption to restore frozen milk 85/A (route: C1-CURSOR)
Spec-complete engine fix, owner-approved + D7 co-signed (with conditions). Restore the frozen milk
invariant. Do NOT close — propose RETURNED.

## The fix (TASK-271 audit + D7 co-sign)
In `C:\Bari\03_operations\bsip2\proto_v0\src\nova_proxy.py`, the `_ingredient_data_degraded` guard
blocks the NOVA-1 fast-path for products whose `ingredients_raw_provenance.source == "bsip1_text_fallback"`.
Add a DAIRY-SINGLE-TOKEN EXEMPTION: allow the NOVA-1 fast-path when ALL hold:
  ing_count == 1  AND  additive_count == 0  AND  the single ingredient token is a bare dairy token
  in the whitelist {"חלב","חלב פרה","חלב עיזים","חלב כבשים"}.
**EXCLUDE cream/שמנת from the whitelist** (D7 condition 3 — conservative minimal scope; the frozen
trio is all חלב). The exemption overrides ONLY the text_fallback-degraded condition; all other guard
conditions (corrupted/missing/malformed ingredient data) still block. Do NOT touch W4 or any flag.

## HARD ACCEPTANCE GATES (run yourself; paste output)
1. **Exact frozen restore:** run `python batch_run_milk_005_headpin.py` → the frozen trio
   (7290000051352 whole 3.4%, 7290019790259 natural 4%, 7290102392094 goat) MUST return EXACTLY
   85/A each, nova_level=1, nova_confidence_band=high. Paste the trio scores + "Frozen invariant
   milk top 85/A" line (must read HELD/RESTORED, not BROKEN).
2. **Invariant suite:** `python C:\Bari\03_operations\shadow\engine_invariants.py` → 6/6 PASS.
3. Non-qualifying products (ing_count>1, or additives, or non-dairy) unchanged behavior.
- OFF ban absolute. No flag default changes. Engine code only in nova_proxy.py (+ a whitelist const if needed).

## Return (machine-readable contract)
Files+shas; the trio restore proof (85/A each, nova=1/high); invariant pass; confirm cream excluded;
confirm no flag/W4 changes. Do NOT close — propose RETURNED. End with the return contract.
