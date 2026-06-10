# TASK-239 — BSIP0 Structural Parser + Exit Gate — Audit

**Mode:** BLOCKER / HARSH VERIFICATION
**Owner:** data-agent · **Reviewers:** qa-agent, nutrition-agent
**Date:** 2026-06-10
**Verdict:** PASS WITH FIXES (all 8 findings verified; structural fix + regression tests + exit gate landed)

The defect class: a Shufersal product page can carry **two** `div.nutritionList`
panels — one per **100 g** (`subInfo` = "100 גרם"), one per **serving/cube**
(`subInfo` = "קוביה"/"מנה"). The frozen-veg scrapers selected the wrong (per-cube)
panel and the only "fix" was a **manual JSON patch** (`scope_clean_v2_1.json`). The
scraper/parser path would recreate the bug on the next run. This task converts the
defect into a structural parser fix + regression tests + a BSIP0 exit gate so it
cannot recur.

---

## Evidence table (findings #1–#8)

| # | Claim | Verdict | File | Line / function | Severity | Affects future runs? | Fix |
|---|-------|---------|------|-----------------|----------|----------------------|-----|
| 1 | First-table selection: scraper takes `soup.find("div","nutritionList")` (first match only), no per-100g preference | **CONFIRMED** | `01_scrape_shufersal_frozen_vegetables.py`; `02_scrape_shufersal_v2.py` | 01:208 `first_nutrition_list = soup.find(...)`; 02:227 same | **CRITICAL** | YES | Shared `select_nutrition_table` prefers per-100g; 01/02 refactored to call it |
| 2 | Bypass shared parser: 01/02/03 do not import `_shared/bsip0_nutrition.py`; three separate inline extractions | **CONFIRMED** | 01, 02, 03 | 01:207-220; 02:226-247; 03:31-44 | **CRITICAL** | YES | All three now `import bsip0_nutrition as bn` and call `extract_nutrition_raw` |
| 3 | Scope drift: 4 scope layers (raw→v2→v3 + 3 scope_clean files) with divergent rules | **CONFIRMED** | 01,02,03,04 + scope_clean v1/v2/v2_1 | 01:139 `SCOPE_OUT_KEYWORDS`; 02:67 `SCOPE_OUT`; 03:56-71; 04:15-23 | MEDIUM | YES (corpus membership) | Documented below + consolidation recommendation (FROZEN_VEG_SCOPE_RULES). Not built (per scope: document+recommend only) |
| 4 | Dual-table bug actually shipped the wrong values to the pipeline | **CONFIRMED** | `bsip0_*_v2.json`, `_v3.json` → `bsip1_7290018989456.json` | ginger P_7290018989456 | **CRITICAL** | YES (pre-fix) | Parser now selects per-100g; gate G2/G3 fails any non-per-100g selection |
| 5 | Inline nutrition reads `div.name` (UNIT) as the label, not `div.text` (nutrient name) | **CONFIRMED** | 01, 02 | 01:213 `label_el = item.find(class_="name") or ... text`; 02:230 same | HIGH | YES | `_rows_from_div` reads `div.text` as label, `div.name` as unit (documented in code) |
| 6 | No `ingredients_raw_source` preserved for offline ingredient re-parse | **CONFIRMED (partial)** | `_shared/bsip0_nutrition.py` | nutrition has `extract_nutrition_raw`; ingredients had none | MEDIUM | YES | Registered as follow-up; gate G8 WARNs when neither source nor reason present (see "Follow-ups") |
| 7 | Hardcoded `[:50]  # limit to 50 for now` dev cap silently truncates corpus | **CONFIRMED** | `01_scrape...` | 01:180 | HIGH | YES | Replaced with `BSIP0_SCRAPE_LIMIT` env cap defaulting to **unlimited** (0) |
| 8 | OFF contamination in frozen-veg dir | **REFUTED (clean)** | `shufersal_frozen_vegetables/` | n/a | — | N/A | No OFF tokens found; gate G1 enforces hard-fail going forward |

**Additional gap found during verification (not in #1–#8):** `nutrition_implausible`'s
inline sodium heuristic only recognised Latin `"mg"`, not the Hebrew milligram marker
`"מג"`. It therefore flagged `"10 מג"` (10 mg) as `10 g → 10000 mg implausible` — 19
false positives in the v3 corpus. Fixed by routing sodium through the canonical
`parse_sodium_mg` (which already honours `מג`). After the fix the gate flags **1**
panel, a genuine fat-overwrite signature. Severity: MEDIUM (false-fail noise that
would have masked the one real catch).

Confirmed: 6 · Confirmed-partial: 1 (#6) · Refuted: 1 (#8, OFF clean — a good refute).

---

## The dual-table bug — before/after on the REAL ginger fixture

Product **P_7290018989456 — "ג'ינג'ר קצוץ מוקפא"** (chopped frozen ginger). Two
real panels in the saved HTML:

| basis (`div.subInfo`) | energy | sodium | carbs | protein | fat |
|---|---|---|---|---|---|
| Table 0 — **100 גרם** (per 100 g) | **77 kcal** | **12 mg** | 16 g | 1.6 g | 0.7 g |
| Table 1 — **קוביה** (per cube) | 6 kcal | 1 mg | 1.3 g | 0 g | 0 g |

**Pipeline output history (the manual-patch loop, documented):**

| Artifact | Producer | energy | sodium | What it shows |
|---|---|---|---|---|
| `..._raw.json` | script 01 | label = UNIT (`{"גרם":"0","קל":"6","מג":"1"}`) | per-cube | finding #5 (unit-as-label) + #1/#4 (per-cube) |
| `..._v2.json`, `..._v3.json` | script 03 | **6 kcal** | **1 mg** | last (per-cube) table overwrote per-100g (finding #4) |
| `..._scope_clean_v2_1.json` | **manual JSON patch** | 77 kcal | 12 mg | the manual "fix" TASK-239 must replace |
| `bsip1_7290018989456.json` | BSIP1 build | 77 kcal | 12 mg | confirms the **manual patch** is what fed scoring |

**After the structural fix** (shared parser, run on the same saved HTML):
`selected_basis = per_100g`, `selected_table_index = 0`, `competing_table_count = 2`,
`insufficient = False` → **energy 77 kcal, sodium 12 mg** — produced by the parser,
no manual patch. Proven by `test_dual_table_values_match_per_100g_fixture` and by the
offline re-extraction reproduction.

---

## Structural fix (`_shared/bsip0_nutrition.py`)

- `classify_basis(subinfo)` → `per_100g` | `per_serving` | `unknown` (final-form-
  normalised Hebrew tokens; per-100g checked first).
- `extract_nutrition_tables(soup)` → every `div.nutritionList` as
  `{table_index, basis, subInfo, rows}`.
- `select_nutrition_table(tables)` → **explicitly prefers per-100g**; records
  `selected_basis`, `selected_table_index`, `selected_table_header`,
  `competing_table_count`, `insufficient`. Policy: 1 table → use it; >1 with a
  per-100g → use that; **>1 with none per-100g → `insufficient=True` (gate-fail)**.
  **Never silently selects the first table.**
- `extract_nutrition_rows` / `parse_nutrition_list` now route through the selection.
- `extract_nutrition_raw` persists **all tables + the selection metadata + concatenated
  HTML** so offline replay reproduces the exact basis decision.
- `nutrition_implausible` sodium now uses canonical `parse_sodium_mg` (Hebrew `מג` fix).

Scrapers **01 / 02 / 03** refactored: inline extraction removed; all call
`bn.extract_nutrition_raw`. Offline re-extraction (03) uses the **same** parser as
live scraping (01/02).

---

## BSIP0 exit gate (`05_bsip0_gate.py`)

Runs after scrape/post-process, before BSIP1. Exit 1 on FAIL.

| Check | Type | Catches |
|---|---|---|
| G1 OFF contamination | HARD FAIL | OFF in any field/variant (see proof below) |
| G2/G3 nutrition basis + multi-table | HARD FAIL | basis != per_100g where competing tables exist; `insufficient` |
| G4/G5 duplicate / conflicting identity | HARD FAIL | barcode dupes; one barcode → >1 name |
| G6 numeric sanity | HARD FAIL | `nutrition_implausible` (sat>fat, sodium>2000, fat-understated, kcal>900) |
| G7/G8 ingredient coverage + raw-source | WARN | low coverage; missing `ingredients_raw_source`/reason |
| G9 run-summary contract | HARD FAIL | missing run-level fields incl. `provenance.source` |

**OFF-gate proof** (all variants hard-fail; no false positives):

```
source=openfoodfacts ............ FAIL    off_url ......................... FAIL
provenance="Open Food Facts" .... FAIL    off_image ....................... FAIL
*.openfoodfacts.org image ....... FAIL    off_nutrition ................... FAIL
panel_source="source=openfood..." FAIL    off_ingredients ................. FAIL
free-text "open_food_facts" ..... FAIL    OFF in cache/trace/source field . FAIL
"cutoff coffee" (name) .......... PASS  (correctly NOT a false positive)
```

**Sample gate run** on the real (pre-fix) v3 corpus →
`gate_runs/sample_gate_run_v3.txt` / `.json`: `OVERALL: FAIL` (G1 PASS no OFF;
G6 FAIL = 1 genuine fat-overwrite panel `P_7290013994790`; G2/G3 + G8 WARN because the
legacy corpus predates the basis metadata). This is the gate correctly refusing the
manually-patched corpus.

---

## Scope debt (finding #3) — 4 drifted layers

| Layer | File | Rule | Count out | Effect on frozen-veg in/out |
|---|---|---|---|---|
| L1 | 01:139 `SCOPE_OUT_KEYWORDS` | name keyword exclude (chips, schnitzel, fruit…) | — | discovery census |
| L2 | 02:67 `SCOPE_OUT` | L1 + extras (נודלס, חזה, קלח, שמן, קפה, גמדי) | 222→174 | tightened; baby-corn/oil/coffee dropped |
| L3 | 03:56-71 | flowers + fresh-produce-not-in-frozen-cat | 174→164 | category-membership heuristic |
| L4 | 04:15-23 `EXCLUSIONS` | name-substring non-food (softener, wipes, tongue, coconut) | 164→(curation) | hard non-food removals |
| + | scope_clean v1/v2/v2_1 | separate 50/53/53-product curations | — | **divergent** parallel corpus (also where the manual nutrition patch lives) |

Drift is real: the same exclusion intent is re-expressed with different keyword sets in
four places, and a fifth parallel `scope_clean` track exists. None changed the *parser*
correctness but they change *corpus membership* run-to-run.

**Recommendation (document-only, per scope):** consolidate to a single
`FROZEN_VEG_SCOPE_RULES` module (one `SCOPE_OUT` set + one category-membership rule +
one non-food set) imported by every stage, and retire the parallel `scope_clean_*`
track. Track as a follow-up; not built here (scope said document+recommend only).

---

## Follow-ups (RETURNED to orchestrator / deferred)

- **#6 ingredients_raw_source (MEDIUM):** nutrition has offline-replay source; ingredients
  do not. Gate G8 WARNs when absent. Recommend a `capture_ingredients_raw` helper in the
  shared parser mirroring `extract_nutrition_raw`. Deferred follow-up.
- **#3 scope consolidation (MEDIUM):** single `FROZEN_VEG_SCOPE_RULES` source. Deferred.
- **Other retailer scrapers** (carrefour/victory/yohananof) still have inline nutrition
  extraction. This task fixed the shared parser (the single path) and the frozen-veg
  scrapers; migrating other retailers to `bn.extract_nutrition_raw` is a follow-up — the
  fix is now centralised so it cannot drift in the shared path.
- **Re-run frozen-veg through the fixed scrapers** to regenerate a basis-stamped corpus
  and clear the G2/G3 WARN (legacy records carry no basis). Blocked on the no-new-run
  hard rule for this task; recommend as the immediate next step.
