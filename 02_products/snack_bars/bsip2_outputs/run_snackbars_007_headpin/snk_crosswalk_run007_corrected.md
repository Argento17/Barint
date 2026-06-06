# Snack Bars QA Crosswalk — run_snackbars_007_headpin (CORRECTED)

Generated: 2026-06-05  |  Task: TASK-180B  |  CC-verified via imageUrl-barcode extraction

**Note:** The original crosswalk (`snk_crosswalk_run007.md`) contained fabricated snk label
assignments. This corrected version derives mappings by extracting barcodes from
`snacks_frontend_v2.json` imageUrl fields, then matching to bsip1_pid in off.json.
The bottom-line result (zero grade-affecting moves) was correct; the per-product label
assignments were wrong. This file supersedes the original.

**Ghost product confirmed absent from frontend:**
bsip1_8423207210287 ("מרבה סלים דליס שוקולד לבן בטעם יוגורט", 69.5/B) — no snk-XXX
imageUrl contains barcode 8423207210287. The 69.5/B editorial call was about a non-displayed
product; note decision is void.

---

| snk | imageUrl barcode | bsip1_pid | run_007 score | run_007 grade | frontend_old | frontend_new | Δ |
|-----|-----------------|-----------|--------------|--------------|-------------|-------------|---|
| snk-001 | 7290011498870 | bsip1_7290011498870 | 70.0 | B | 70 | 70 | 0 |
| snk-015 | 7290011498894 | bsip1_7290011498894 | 63.0 | C | 63 | 63 | 0 |
| snk-004 | 8423207206495 | bsip1_8423207206495 | 60.4 | C | 59 | 60 | +1 |
| snk-002 | 7290011498948 | bsip1_7290011498948 | 56.7 | C | 57 | 57 | 0 |
| snk-003 | 16000548404 | bsip1_16000548404 | 55.1 | C | 53 | 55 | +2 |
| snk-016 | 8423207210928 | bsip1_8423207210928 | 52.5 | C | 51 | 53 | +2 |
| snk-009 | 8410076610379 | bsip1_8410076610379 | 47.7 | D | 47 | 48 | +1 |
| snk-005 | 5900020039590 | bsip1_5900020039590 | 47.6 | D | 46 | 48 | +2 |
| snk-010 | 8410076610386 | bsip1_8410076610386 | 46.2 | D | 46 | 46 | 0 |
| snk-018 | 8410076602251 | bsip1_8410076602251 | 45.9 | D | 44 | 46 | +2 |
| snk-011 | 7290111936784 | bsip1_7290111936784 | 43.8 | D | 44 | 44 | 0 |
| snk-012 | 7290111937262 | bsip1_7290111937262 | 42.0 | D | 42 | 42 | 0 |
| snk-017 | 8410076610508 | bsip1_8410076610508 | 40.5 | D | 39 | 41 | +2 |
| snk-019 | 7290118427896 | bsip1_7290118427896 | 39.8 | D | 40 | 40 | 0 |
| snk-020 | 7290014525306 | bsip1_7290014525306 | 31.8 | E | 33 | 32 | −1 |
| snk-007 | 5900020015174 | bsip1_5900020015174 | 26.7 | E | 28 | 27 | −1 |
| snk-006 | 7290118427858 | bsip1_7290118427858 | 17.7 | E | 17 | 18 | +1 |
| snk-013 | 4011800633516 | bsip1_4011800633516 | 16.3 | E | 17 | 16 | −1 |

## Summary
- Products changed: 11/18
- Grade-affecting moves: **0**
- Max drift: ±2pt (all cosmetic, same grade)
- snk-019 imageUrl barcode (7290118247896) differs from bsip1_pid (7290118427896) — transposition error in Yochananof image CDN; name match confirms correct product

## Corpus products not in the frontend (35 products, not displayed)
See original `snk_crosswalk_run007.md` "not in frontend" table — those 35 entries are correct.
The ghost (bsip1_8423207210287, 69.5/B) is among those 35 and is correctly NOT displayed.
