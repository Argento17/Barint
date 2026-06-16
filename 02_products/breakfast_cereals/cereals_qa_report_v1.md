# Cereals Comparison Page — Full QA Report v1

- **Date:** 2026-06-12
- **Auditor:** QA Agent
- **Scope:** All 34 products in `bari-web/src/data/comparisons/cereals_frontend_v2.json`
- **Ground truth:** `run_cereals_008` + `run_cereals_008_reconstruction` + `run_cereals_multiretailer_001(_reconstruction)` traces; BSIP1 corpus `run_cereals_002`, `run_cereals_carrefour_001`
- **Verdict:** **FAIL (go-live blocker present)** — not a score-integrity failure, but an **OFF-data-source hard-rule violation** affecting 8/34 products, plus one grade-propagation defect and a confirmed stale deployment.

---

## BOTTOM LINE (one line)

The 7/10 is **mostly stale-deployment + data-completeness**, with **NO systemic score-integrity problem** — BUT there is one true launch blocker that is neither: **8 of 34 products are sourced entirely from Open Food Facts (nutrition, ingredients, name, image), violating the project-wide OFF ban (TASK-238).** Scores themselves propagate correctly (1 grade-boundary rounding defect aside), and the corrupt-ingredient products are sugar-capped from the nutrition panel, so their grades are safe.

---

## CRITICAL FINDINGS

### C1 — OFF data-source contamination on 8/34 products (HARD-RULE / LAUNCH BLOCKER)
- **What:** 8 products draw their **nutrition panel, ingredients, product name, and image all from Open Food Facts** (`panel_source: open_food_facts` in BSIP1).
- **Products (barcodes):** 7613037686906, 7613033548192, 3560071016074, 42400108153, 5900020046833, 5900020041142, 7290116537351, 4005528115218.
- **Root cause:** All 8 originate from `03_operations/bsip1/run_cereals_carrefour_001/output/` where `source.panel_source = "open_food_facts"`, `panel_found: true`. The identity came from `il_prices` (Carrefour feed) but the **panel content came from OFF**. By contrast, the 26 Shufersal-pool products (`run_cereals_002`) have `panel_source: None` (direct Shufersal scrape) — OFF-free.
- **Layer:** DATA (source) — propagates into scoring (OFF nutrition fed the score) and display.
- **Why blocker:** CLAUDE.md / `off_ban_hard_rule` / TASK-238 — "any OFF dependency is a launch blocker," banned for nutrition, ingredients, names, images, scoring traces. These 8 scores are computed on OFF panels.
- **Note on `_meta`:** JSON `_meta` claims `retailer_breakdown: {carrefour: 1}` and "1 net-new Carrefour product." This is **wrong** — 8 Carrefour/OFF-sourced barcodes are present. All 8 are also **mislabeled `"retailer": "shufersal"`** in the JSON.
- **Recommended owner action:** Remove the 8 OFF-sourced products from the corpus, OR re-source their panels from a real Shufersal/direct scrape before any go-live. Do not ship OFF-fed scores. (Owner decision — strategic tripwire #2, consumer-facing + #1 touches data integrity.)

---

## HIGH FINDINGS

### H1 — Stale deployment: remediated copy never merged to master (CONFIRMED)
- **What:** The owner saw `"ערכים שלא הועברו לגרסה הקודמת"` on the Lion row. That string does **not** exist in the current committed JSON (count=0), but **does** exist on `master` (count=2).
- **Root cause:** The copy remediation commit `d7224ed8` (TASK-254, "34/34 insightLine + rowVerdict", 2026-06-12 13:45) lives **only on branch `task-244-confidence-structural-fix`**. `git merge-base --is-ancestor d7224ed8 master` → exit 1 (**NOT merged**). master HEAD is `8eacb083`. If prod builds from master, prod is pre-remediation.
- **Layer:** DEPLOYMENT.
- **Recommended owner action:** Merge TASK-254 to master and redeploy. The owner's copy complaint is fixed-but-undeployed, exactly as the orchestrator hypothesized. CONFIRMED.

### H2 — Ingredient field = marketing promo, not declaration (3 fully-corrupt) — DISPLAY BUG, score safe
- **What:** Three products show front-of-pack promo bullets as the "ingredients," with no real declaration:
  - 5900020036407 (Lion): `"מס' 1 חיטה מלאה • 9 ויטמינים ומינרלים • מקור לברזל... • ללא צבעי מאכל • ללא חומרים משמרים"`
  - 5900020012814 (Nesquik): same `• `-bullet pattern
  - 72968 (Cini Minis): same pattern
- **Score impact — SAFE (verified in trace):** The engine already flags these as `ingredient_text_quality: "marketing_bleed"` and **did not derive any false signal**:
  - `additive_quality: 100`, `penalties_applied: []` — zero ingredient-derived penalties fired.
  - Binding cap = `ISRAELI_RED_LABEL_1_SUGAR` (cap **55**), driven by the **nutrition-panel sugar** (Lion 24.7g, Nesquik 22.4g, Cini 25.0g), **independent of the ingredient text**.
  - NOVA proxy = 3 from `additive_categories: 0, added_sugars: 1` (sugar panel), capping at 94.8 (non-binding).
  - Lion: `weighted_dimension_score 61.39` → capped to 55. Grade C is correct and panel-driven.
  - `explanation_drivers: "DOMINANT: Binding cap=55 from ISRAELI_RED_LABEL_1_SUGAR"`.
- **Conclusion:** This is a **display/data-completeness bug, NOT a score bug.** Grades are safe.
- **Layer:** DATA (display field) — the real declaration was never scraped; promo text leaked into the ingredients slot.
- **Recommended owner action:** Re-scrape the real ingredient declaration for these 3, OR show the "data could not be retrieved" state for ingredients rather than promo text. (Data Agent.)

### H3 — Grade-propagation defect: 884912126115 (Great Grains Dates) shows D, trace says E
- **What:** Trace `final_score_estimate = 34.7` in **both** run_008 and reconstruction; `grade_estimate = E` in both. JSON shows `score: 35, grade: "D"`.
- **Root cause:** 34.7 was rounded up to 35 at JSON generation, crossing the **D/E boundary (cutoff = 35.0; 33.3/34.7 = E, 35.1/36.0 = D, confirmed by neighbor scan)**. The displayed grade D contradicts the engine's E.
- **Score delta:** +0.3 (rounding); **grade impact: E→D** (one full grade).
- **Layer:** SCORING propagation (grade derivation from rounded vs raw score).
- **Recommended owner action:** Escalate to Nutrition/Data — decide whether grade is derived from the raw trace score (→ E) or the displayed rounded score. Current state displays an E-grade product as D. (This is the only genuine grade-integrity discrepancy in 34.)

---

## MEDIUM FINDINGS

### M1 — 5 English product names on a Hebrew RTL site
- **Products:** 7613037686906 "Fitness almond honey", 7613033548192 "Nestle Fitness Dark Chocolate", 3560071016074 "Corn flakes", 42400108153 "Cereal", 5900020046833 "Cheerios".
- **Root cause:** BSIP1 `name` field is `null` for all (Carrefour/OFF records). The English strings are **OFF-derived product names** leaking through as the display fallback. No clean Hebrew name exists in BSIP1 or the trace for these 5 (the corpus never captured a Hebrew name). The other 3 Carrefour products got Hebrew names downstream (manual/other), these 5 did not.
- **Layer:** DATA. Subsumed by C1 — these are 5 of the 8 OFF products. Removing/ re-sourcing per C1 resolves this.
- **Recommended owner action:** Same as C1. If any of the 8 are kept, a real Hebrew name must be sourced (not OFF).

### M2 — 8/34 missing images (empty imageUrl)
- **Products:** the same 8 OFF barcodes (7613037686906, 7613033548192, 5900020041142, 3560071016074, 7290116537351, 4005528115218, 42400108153, 5900020046833).
- **Root cause:** Every one had an `images.openfoodfacts.org` image in BSIP1; these were **correctly nulled** by commit `6a6bc14d` (TASK-245A, "null 21 OFF imageUrls — cereals 9"). **No real product-scrape image exists** for these 8 — OFF was the only image source, and OFF images are banned.
- **Layer:** DATA. The null is TASK-238-correct behavior, not a bug; the underlying problem is C1 (OFF-only products).
- **Recommended owner action:** Same as C1. The 26 Shufersal products all have valid Cloudinary/Shufersal images.

### M3 — Ingredient field = real list + promo tail ("מאפיינים נוספים…") on many Shufersal products
- **What:** Numerous products append a marketing tail after the real declaration, e.g. `…מלח. מאפיינים נוספים ללא צבעי מאכל,` (הרדוף 7290017325910), `…מלח. מאפיינים נוספים עשיר בדגנים מלאים,` (7290116535371), שוגי 7290107647854, of-alufim 7290112494351, etc. Also OCR artifacts: stray `n`/`rn` newline tokens, RTL digit reversal (`(%94`), embedded nutrition tables (7297488199590, 7290017894911, Cheerios).
- **Score impact:** None — these are MARKETING-APPENDED (real list present); the engine parses the real ingredients. Classification per the orchestrator's taxonomy: **CLEAN** (most), **MARKETING-APPENDED** (the "מאפיינים נוספים" group), **FULLY-CORRUPT** (only the 3 in H2).
- **Layer:** DATA (display cleanliness / OCR).
- **Recommended owner action:** Strip the "מאפיינים נוספים…" tail and OCR noise from the displayed ingredient string (cosmetic; not score-affecting). (Data/Content.)

---

## CLEAN / PASS ITEMS (verified)

- **Score → grade propagation (33/34):** JSON `score`/`grade` matches the source run (run_008 original) within rounding for 33 of 34 products. The 9 "mismatches" vs the *reconstruction* run resolve cleanly against the *original* run_008 (the JSON's actual source); only 884912126115 (H3) is a true defect. The reconstruction run is a divergent re-score (systematically ~2–3 pts lower) and is **not** the JSON source — do not use it as the propagation baseline.
- **Copy / leakage (current JSON):** ZERO T4 / framework vocabulary (NOVA, BSIP, cap, floor, dimension, proxy, run_, "הגרסה הקודמת") in any `insightLine` or `rowVerdict`. ZERO raw-score mechanics (no "68.2"-style decimals). Sodium is **never causal** — all 13 sodium mentions are fact-only values ("X מ\"ג נתרן ל-100 גרם"); the named limiter is always sugar/fiber/processing. (3 regex hits manually cleared as false positives.)
- **Corrupt-ingredient scores (H2 trio):** Verified sugar-capped from the nutrition panel; grades safe.
- **Confidence labels:** Coherent with data state — `verified`/"מבוסס על נתונים מלאים" for full-data products (8445291638839, 3387390525960, 884912126115); `missing_ingredients`/"חסרים נתוני רכיבים" for the 6 empty-ingredient products; `missing_nutrition`/"חסרים נתוני תזונה" for null-fiber products (שוגי, קורנפלקס דבש). `source_traceability_status: resolved` on all 34.
- **Additive enrichment (d4_additives):** Correct and well-explained where present (E471, E322 functional; BHT/E321 contested; synthetic dyes dose-dependent on טריקס and the US "Cereal"). No false additives on the marketing-bleed trio (correctly empty).

---

## SEVERITY SUMMARY

| ID | Severity | Finding | Products | Layer | Owner action |
|----|----------|---------|----------|-------|--------------|
| C1 | CRITICAL | OFF-sourced nutrition/ingredients/name/image | 8 Carrefour barcodes | DATA→scoring/display | Remove or re-source (OFF ban) |
| H1 | HIGH | Remediation not merged to master; prod stale | page-wide copy | DEPLOYMENT | Merge TASK-254, redeploy |
| H2 | HIGH | Promo text as ingredients (score SAFE) | 5900020036407, 5900020012814, 72968 | DATA (display) | Re-scrape ingredients |
| H3 | HIGH | Grade shows D, trace says E (35 vs 34.7) | 884912126115 | SCORING propagation | Nutrition: fix grade derivation |
| M1 | MEDIUM | English names on RTL site (OFF names) | 5 of the 8 | DATA | Subsumed by C1 |
| M2 | MEDIUM | 8 missing images (OFF stripped) | 8 of the 8 | DATA | Subsumed by C1 |
| M3 | MEDIUM | Promo tail + OCR noise in ingredients | ~12 Shufersal | DATA (cosmetic) | Strip tail (not score-affecting) |

---

## RED-TEAM GATE (Hard Rule 9)

No red-team challenge report found at `02_products/breakfast_cereals/reports/red_team_*.md`. Per QA Hard Rule 9, a QA **PASS** verdict for go-live cannot be issued until a red-team report exists for this corpus version with no open CRITICAL findings. Independent of the red-team gate, **C1 alone blocks PASS.**

## VERDICT

**FAIL.** Blocker = C1 (OFF data source on 8/34). Then H1 (deploy stale copy), H3 (one E-shown-as-D grade). The page's underlying scoring engine is sound — the 7/10 is driven by data-completeness (OFF gap-fill, missing images/names) and a stale deployment, not by score-integrity failure. Fix C1 + H3, merge/deploy H1, re-run red-team gate, then re-QA.
