# Red-Team / Adversarial QA Report — Bread Comparison Page (`/hashvaot/bread`)

**Date:** 2026-07-03
**Task:** TASK-474 (F2 red-team backfill, batch 1, P1 item 9a)
**Challenger:** Adversarial QA Agent (Bari)
**Scope:** Live page as served from `bari-web/src/data/comparisons/bread_frontend_v4.json` (23 products), traced back through `C:\Bari\02_products\bread\bsip2_outputs\run_bread_conform_002\` (25 scored) and `C:\Bari\03_operations\bsip1\run_bread_conform_002\output\` (25 BSIP1 records).
**This is the category's first-ever red-team report** — none existed on disk prior to this run (confirmed by directory scan: `02_products\bread\reports\` did not exist before this task).

---

## EXECUTIVE VERDICT: **NO-GO** for continued live status as-is

Track V is **not green**: the mechanical gate suite (`run_gates.py`) returns **Overall: FAIL** against the live JSON when pointed at its own most-recent BSIP2 run. Two hard fails (G3 SCOPE, G5 GRADE-INTEGRITY) are real, reproducible, and not explained anywhere in the shipped `_meta`. Track C adds one CRITICAL (phantom-confidence scoring on an empty ingredient list, corpus-wide) and one HIGH (systemic em-dash usage against a standing owner rule). Per the D10 unified gate, a category may pass only when Track V is fully green AND Track C has zero open CRITICAL — neither condition holds.

This is a **continued-live-status** verdict, not a kill order — I raise, I do not decide whether to pull the page. Routing table is at the end.

---

## Findings, most severe first

### CRITICAL-1 — NOVA/structural-class/confidence scoring computed on an empty ingredient list, corpus-wide, while the frontend displays a fully parsed ingredient string for the same products

**What I checked:** For every product I sampled (5 of 23: `7290016245325`, `3268429`, `481203`, `2079033`, `1902325`), the BSIP1 record (`03_operations\bsip1\run_bread_conform_002\output\bsip1_<barcode>.json`) has a real, populated `ingredients_text_he` (Hebrew ingredient string, 9–15 items, `enrichment_summary.ingredient_count_parsed` = 9–15) sourced via `ingredients_raw_provenance.source: "bsip1_text_fallback"`. But the corresponding BSIP2 trace (`02_products\bread\bsip2_outputs\run_bread_conform_002\products\bsip1_bread_<barcode>\bsip2_trace.json`) records, for every one of the 5 sampled: `L1_observed_signals.ingredient_count: 0` and `ingredient_list: []`.

Concretely for `7290016245325` (לחם טחינה פרוס, the #1-ranked S-grade, score 94.8 as served):
- BSIP1: `ingredients_text_he` = "מים, קמחים 36% (פשתן, שומשום, אפונה, סויה, שקדים), טחינה, גלוטן, אינולין, מחמצת שיפון, מלח, חומץ, ויטמין C, עמילן תירס, אנזימים, חומר משמר (פוטסיום סורבט, קלציום פרפיונט), שמרים" — 13 ingredients per `enrichment_summary.ingredient_count_parsed`.
- BSIP2 trace `L1_observed_signals`: `"ingredient_count": 0, "ingredient_list": []`, `"ingredient_text_quality": "clean"` (contradictory — "clean" quality on a list of zero items).
- The trace's own `nova_uncertainty_notes` state: *"EV-030: ingredient_data_degraded... NOVA 1 fast-path suppressed"*, *"no_ingredient_list: NOVA inference unreliable"*.
- `structural_class.classification_notes` includes `"minimal_ingredients"` — a *structural_class* input directly contradicted by the 13-item ingredient string sitting one file away in the same pipeline run.
- Despite this, `confidence_level` served to the consumer is `"sufficient"` (label: "ניתוח חלקי" / partial analysis) — not the honest "insufficient" or a lower confidence tier the missing-ingredient-list condition would normally trigger. `confidence_score: 65` / `confidence_band: "medium"` in the trace itself is more honest than what reaches the page.

**Why this is CRITICAL, not HIGH:** This is not one product's data-entry slip — it is systemic across the sample (5/5 checked show the identical `ingredient_count: 0` / `ingredient_list: []` pattern despite BSIP1 having real text for all 5). The pattern reads as a BSIP1→BSIP2 hand-off bug: the trace reads the *structured* `ingredients_list` array (which is genuinely empty/null in BSIP1 — a separate field from `ingredients_text_he`) instead of the *text-fallback* string that the rest of BSIP1 and the frontend both successfully use. Whole-grain and fermentation detection (`L3_inferred_classifications.has_whole_grain`, `has_fermentation`) *do* still fire correctly (verified True for `3268429`), meaning some other part of BSIP2 keyword-matches the raw text directly — but NOVA proxy, `structural_class`, and the "confidence_reductions" bucket ("missing: ingredient_list", -25 points) do not. The category's central editorial promise — "the score reads the ingredient list, not the branding" (`breadCategoryNote`) — is being delivered by inconsistent internal paths: some engine stages honor the real ingredient text, others silently treat it as absent.

**Consumer-facing implication:** A shopper is told (category caveat, verbatim) that "the score identifies fermentation, whole grain and fiber from what's in the ingredient list — not from the label claim." For NOVA/processing-quality and structural-class purposes specifically, that claim is false for this corpus: those two engine components ran as if no ingredient list existed at all, for every product sampled.

**Evidence:** `C:\Bari\03_operations\bsip1\run_bread_conform_002\output\bsip1_7290016245325.json` (`ingredients_text_he`, `enrichment_summary.ingredient_count_parsed: 13`); `C:\Bari\02_products\bread\bsip2_outputs\run_bread_conform_002\products\bsip1_bread_7290016245325\bsip2_trace.json` (`L1_observed_signals.ingredient_count: 0`, `nova_uncertainty_notes`, `structural_class.classification_notes`); same pattern confirmed on barcodes `3268429`, `481203`, `2079033`, `1902325` (script output, not exhaustively re-quoted here — 5/5 sampled, denominator = 5 of 23 displayed products, not the full 23; **I could not verify all 23** without re-running the same check on the remaining 18, which I did not do — see Not Verified).

**Routes to:** `data-agent` (BSIP1→BSIP2 field-mapping bug: trace should read `ingredients_text_he`/parsed ingredient count, not only the structured `ingredients_list` array) and `nutrition-agent` (confidence-integrity: whether "sufficient" confidence is defensible when NOVA/structural-class were computed on a self-reported-empty ingredient list).

---

### CRITICAL-2 (mechanical, G5) — Score propagation mismatch: barcode `7290016245325` served at 94.8/S, most-recent trace computes 94.0/S

**What I checked:** Ran `03_operations\page_generator\gates\run_gates.py` directly against the live JSON and the most-recent BSIP2 run (`run_bread_conform_002`). Exit code 1, `Overall: FAIL`.

```
[FAIL] G5 GRADE-INTEGRITY
  FAIL: barcode=7290016245325: JSON score=94.8 vs trace score=94.0 (diff=0.800 > tolerance=0.05)
```

- Served (`bread_frontend_v4.json`): `score: 94.8, grade: "S"`.
- `run_bread_conform_002/run_record.json`: `score: 94.0, grade: "S"` for the same barcode.
- `run_bread_conform_002`'s own `survivor_23_drift_report` entry for this barcode: `"published_v3_score": 94.8, "new_v2_score": 94.0, "drift": -0.8"` — the pipeline's own re-score run explicitly logged this exact drift as of 2026-07-01, one day before the current gate report (`bread_frontend_v4_gates_report.md`, generated 2026-07-01T19:08:54Z) was produced — and the frontend JSON was never updated to reflect it.
- The grade (`S`) survives the drift because it's below the presumable S/A boundary either way, so this does not flip a grade — but it is a live, undisclosed, un-actioned 0.8-point score discrepancy between the shipped consumer-facing number and the category's own most recent scoring run. It also happens to be the #1-ranked "top pick" product on the page (rank 1 of 23), the one most likely to be scrutinized by a skeptical reader who cross-checks against a re-run.

**Note on the trace path bug:** the shipped `bread_frontend_v4_gates_report.md` on disk (dated 2026-07-01) shows this as WARN, not FAIL, because it was run with `--run None` (no run directory passed) — i.e., the category's own last recorded gate run **never actually checked score-vs-trace at all**; every G5 line reads "no trace found in --run dir, cannot verify score vs trace." The committed gate report is **not proof of a clean score-propagation check** — it's proof the check was skipped. Running it correctly (pointing `--run` at the actual products directory) immediately surfaces the FAIL.

**Routes to:** `data-agent` (either re-copy the 94.0 conform_002 result into the frontend JSON, or explain why 94.8 is authoritative and conform_002's re-score should be disregarded — that is a data/pipeline decision, not mine to make).

---

### CRITICAL-3 (mechanical, G3) — Two scored products silently dropped from display with zero `_meta` disclosure

**What I checked:** `run_gates.py --run <conform_002/products>` output:

```
[FAIL] G3 SCOPE
  FAIL: Scored barcode 2026 not in frontend and not explained in _meta exclusions
  FAIL: Scored barcode 7296073641568 not in frontend and not explained in _meta exclusions
```

Both barcodes carry `grade: "insufficient_data"` / `score: 50` in `run_bread_conform_002/run_record.json` (`לחם אחיד` and `לחם מחמצת אגוזים פרוס`, respectively) — consistent with the standing missing-data discard rule (memory: `missing_data_discard_rule`), which is very likely why they were dropped. **The discard itself is plausibly correct policy.** The failure is that `bread_frontend_v4.json`'s `_meta` block contains no `excluded_barcodes`, no `insufficient_data_dropped` list, no note of any kind — a reviewer (or this gate) cannot distinguish "correctly discarded per policy" from "silently lost in a JSON re-derive." `_meta.task433_membership_correction` documents the 6 cracker removals in prose detail (barcodes named explicitly) but says nothing about these 2. This is a disclosure/traceability gap, not (as far as I can verify) a scoring error — but the gate is right to fail it, because right now nothing on disk proves the two are intentional exclusions rather than a dropped-row bug.

**Routes to:** `data-agent` (add the exclusion to `_meta`, e.g. a field parallel to `task433_membership_correction` naming the 2 barcodes and citing the missing-data discard rule).

---

### HIGH-1 — Systemic em-dash usage in insightLine/rowVerdict against the standing owner phrasing rule

**What I checked:** Scanned all 23 products' `insightLine` and `rowVerdict` fields for the em-dash character (—). Result: **23 of 23 products** have at least one em-dash in `insightLine` and/or `rowVerdict` (some have 2–3 per product). Examples:
- `7290016245325` insightLine: "...הטחינה וקמחי הזרעים (פשתן, שומשום, אפונה, שקדים) — הטחינה וקמחי הזרעים... **בונים כאן פרופיל שלא קיים בשאר הקטגוריה**" (em-dash mid-sentence).
- `1902325` rowVerdict: "...חלה שבת קלאסית **— לא מוצר שנועד לערכים תזונתיים**." — this specific instance is also a textbook "X, not Y" / define-by-negation construction, itself independently banned ("BAN 'X, not Y' define-by-negation/antithesis").
- `9398281` rowVerdict: "...ציון B ריאלי **— ללא דגן מלא, ללא מחמצת**." — another antithesis-flavored em-dash construction.

The owner rule states plainly: *"MINIMIZE em dashes (Bari copy + Claude's own writing)"* and *"BAN 'X, not Y' define-by-negation/antithesis (positive declaratives only)."* Every product on this page violates the first; at least 2 of 23 sampled violate the second outright. This is not a one-off stylistic quirk — it is the dominant sentence-construction pattern across the entire category's consumer copy, suggesting the copy was authored (or the two-gate sign-off applied) before or without this standing rule being enforced as a checklist item for bread specifically.

**Why HIGH and not CRITICAL:** No consumer harm, no factual inaccuracy — this is a voice/style compliance gap against an explicit, checkable owner directive, not a defensibility-of-score problem.

**Routes to:** `content-agent` (rewrite to positive declaratives per the phrasing rule; this is exactly the class of copy governed by the two-gate sign-off — worth checking whether bread's copy actually cleared a Content + Red-Team two-gate before this page went live, since no prior red-team report existed for this category until today).

---

### MEDIUM-1 — Category caveat is well-grounded but slightly overstates measurement precision

**What I checked:** `breadCategoryNote` (rendered via the `categoryNote` prop, confirmed wired into `bread-comparison-page.tsx:22,42,54`) states two honest, engine-grounded caveats: (1) fermentation/whole-grain are read from the ingredient list not the front-of-pack claim, and (2) the engine cannot distinguish genuine slow sourdough from an industrial sourdough-powder shortcut. Both are accurate to the documented scoring nuance in `.claude/scoring.md`. This is a genuinely strong, honest caveat — better than most categories' — and I have no objection to its substance.

The friction: caveat #1's framing ("the score identifies fermentation, whole grain and fiber from what's in the ingredient list — not from the label claim") is undercut by CRITICAL-1 above — for the NOVA/structural-class dimension specifically, the ingredient list was *not* read (it was empty at that stage of the pipeline). The caveat is honest about the *intended* design; it does not (and, as a static category note, cannot) disclose the specific pipeline bug found today. I am not asking Content to add engine-internals disclosure — that would violate the leakage rule — I am flagging that CRITICAL-1's fix may also require a caveat wording review once the underlying bug is resolved.

**Routes to:** No action required now; revisit caveat wording only if/when CRITICAL-1 is fixed and the fix changes what's actually true about the pipeline.

---

## What I checked and found CLEAN (stating explicitly, per instructions)

- **OFF ban:** No Open Food Facts references anywhere in `02_products\bread\` (BSIP1, BSIP2, staging, run records) or in `bread_frontend_v4.json`. G4 gate: PASS, confirmed by direct grep + mechanical gate. Clean.
- **Leakage / jargon in consumer strings:** Scanned all 23 products' `insightLine`/`rowVerdict` for NOVA/BSIP/pillar/dimension/structural_class/matrix_integrity/cap/routing terms — zero hits. Hero, prologue, methodology lines, category note, and shelf-filter labels (`יומיומי`, `דגן מלא`, `מחמצת`, `עתיר חלבון`, `פיתות`, `מיוחד`, `לחמי בריאות`) — all clean, no framework vocabulary. G6 COPY-SAFETY gate: PASS.
- **Rank-order sanity:** Defined 3 known-better pairs from bread nutrition principles before checking scores (100% whole wheat vs. white-flour-plus-sugar challah; verified rye sourdough+seeds vs. half-white "half-whole" marketing claim; 100%-whole-rye-with-verified-fermentation vs. 40%-white-flour-dominant loaf). All 3 ranked correctly, no inversions.
- **Superlative claims vs. full corpus:** "Lowest sodium in the shelf" (barcode `7290016245325`, 126.0 mg) and "highest sodium among the rye breads" (barcode `3054183`, 500.0 mg) both checked against all 23 displayed products (not a subset) and both hold.
- **Null-data honesty:** `1902325`'s missing fiber value is disclosed in-copy ("נתוני סיבים לא בגלויה" — fiber data not on the label) rather than fabricated or silently omitted. Honest null handling, no OFF substitution.
- **Data-sanity (G8):** No impossible nutrition values, no nutrition-panel-mistaken-for-ingredients pattern. PASS.
- **Schema (G1):** Document validates against schema. PASS.

## What I could NOT verify

- I sampled 5 of 23 displayed products (barcodes `7290016245325`, `3268429`, `481203`, `2079033`, `1902325`) for the CRITICAL-1 ingredient-list discrepancy. All 5 showed the identical pattern. **I did not check the remaining 18** — the finding is stated as "5/5 sampled, denominator 5 of 23," not "23/23 confirmed." Given the consistency across the sample and that the mechanism (structured `ingredients_list` array vs. text-fallback `ingredients_text_he`) is a pipeline-level field-mapping choice rather than a per-product data quirk, I judge it highly likely to be corpus-wide, but this is a judgment call, not a verified count, and I flag it as such.
- I did not run the mobile 390px geometry checklist (no browser/DOM rendering tool used in this pass — this was a read-only data/code audit). Geometry, sticky-filter-button timing, and tap-expand behavior are **unverified** in this report and should route to Design/Frontend for a rendered-page pass (per the "done = rendered + red-teamed" standard).
- I did not run `npm run build` / `tsc --noEmit` / ESLint / the Playwright E2E or axe-core a11y suites against `bari-web` in this pass — this report is the data/score/copy track; build/route/a11y verification is a separate, still-open item if not already covered elsewhere.
- I did not check whether bread's copy previously cleared a Content-Agent + prior Red-Team two-gate sign-off, because no prior red-team report exists on disk for this category (confirmed: `02_products\bread\reports\` did not exist before this task) — meaning if the two-gate rule was already in force when this copy shipped, that gate was structurally unmet for bread until this report. I raise this; I do not know bread's copy-sign-off history beyond what's on disk.
- I did not verify `d4_additives` (E300, E202 shown on `7290016245325`) against EFSA/openfda for over-exposure flags — an adversarial evidence-weight pass on the additive tier claims ("likely-neutral" for E202) was out of scope for this pass; flagging as a possible follow-up for Nutrition/Research, not a finding here.

---

## Routing Table

| Finding | Severity | Routes to | Action needed (not prescribed by me) |
|---|---|---|---|
| CRITICAL-1: NOVA/structural-class scored on empty ingredient list corpus-wide | CRITICAL | data-agent, nutrition-agent | Fix BSIP1→BSIP2 ingredient-list hand-off; re-assess confidence labeling |
| CRITICAL-2: score propagation mismatch (94.8 vs 94.0, barcode 7290016245325) | CRITICAL | data-agent | Reconcile served score against most-recent trace; re-run G5 with correct --run path going forward |
| CRITICAL-3: 2 scored products dropped with no `_meta` disclosure | CRITICAL | data-agent | Add exclusion record to `_meta`, citing missing-data discard rule |
| HIGH-1: systemic em-dash / antithesis phrasing, 23/23 products | HIGH | content-agent | Rewrite per phrasing rule; check two-gate sign-off history for this category |
| MEDIUM-1: category caveat framing slightly ahead of pipeline reality | MEDIUM | (no action now) | Revisit only after CRITICAL-1 is resolved |

**D10 status:** BLOCKED. Track V is not green (mechanical `run_gates.py` returns FAIL, 2 hard fails: G3, G5). Track C has one open CRITICAL (CRITICAL-1). Per the unified gate, Product Agent cannot issue a go-live sign-off on this state.

---

```json
{
  "task": "TASK-474",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\bread\\reports\\red_team_bread_page_v1.md",
      "sha256_of_report_body_excluding_this_json_block": "f14eaeec2218e10ac300e521f243c8cfd9fc751c8b317ce75e81b85bd4433790"
    }
  ],
  "counts": {
    "displayed_products_live_json": 23,
    "denominator_displayed_products": "23 of 23 in bread_frontend_v4.json",
    "scored_products_run_bread_conform_002": 25,
    "denominator_scored_conform_002": "25 of 25 in run_bread_conform_002/run_record.json",
    "products_sampled_for_ingredient_list_check": 5,
    "denominator_ingredient_check": "5 of 23 displayed products (NOT exhaustive — see not_done)",
    "ingredient_list_empty_despite_bsip1_text_present": 5,
    "denominator_ingredient_bug_rate": "5 of 5 sampled (100% of sample, unverified for remaining 18)",
    "score_propagation_mismatches_found": 1,
    "denominator_score_mismatch": "1 of 23 displayed products checked against 25 conform_002 trace scores",
    "silently_dropped_scored_products": 2,
    "denominator_dropped": "2 of 25 scored in conform_002 (barcodes 2026, 7296073641568)",
    "em_dash_products": 23,
    "denominator_em_dash": "23 of 23 displayed products",
    "rank_order_pairs_checked": 3,
    "denominator_rank_order": "3 of 3 pre-defined known-better pairs, 0 inversions",
    "superlative_claims_checked": 2,
    "denominator_superlative": "2 of 2 claims checked against full 23-product corpus",
    "off_references_found": 0,
    "leakage_terms_found": 0,
    "critical_findings": 3,
    "high_findings": 1,
    "medium_findings": 1
  },
  "commands_run": [
    {
      "cmd": "python 03_operations/page_generator/gates/run_gates.py bari-web/src/data/comparisons/bread_frontend_v4.json --run 02_products/bread/bsip2_outputs/run_bread_conform_002/products --corpus 03_operations/bsip1/run_bread_conform_002/output",
      "exit_code": 1,
      "result": "Overall: FAIL (G3 SCOPE FAIL, G5 GRADE-INTEGRITY FAIL; G1/G2/G4/G6/G8 PASS; G7 SKIP no baseline)"
    },
    {
      "cmd": "python -c \"cross-check live JSON scores vs run_bread_conform_002 run_record.json for all 23 displayed barcodes\"",
      "exit_code": 0,
      "result": "1 mismatch found (7290016245325: 94.8 live vs 94.0 trace)"
    },
    {
      "cmd": "python -c \"compare BSIP1 ingredients_text_he / enrichment_summary.ingredient_count_parsed vs BSIP2 trace L1_observed_signals.ingredient_count for 5 sampled barcodes\"",
      "exit_code": 0,
      "result": "5/5 show BSIP1 text present with parsed count 9-15, BSIP2 trace ingredient_count=0 / ingredient_list=[]"
    },
    {
      "cmd": "grep -ril openfoodfacts / 'open food facts' across 02_products/bread and bread_frontend_v4.json",
      "exit_code": 1,
      "result": "no matches (grep exit 1 = no hits found = clean)"
    }
  ],
  "not_done": [
    "Did not sample remaining 18 of 23 displayed products for the ingredient-list bug (CRITICAL-1 stated as 5/5 sample rate, not full-corpus-verified)",
    "Did not run mobile 390px geometry checklist (no rendered/DOM check performed this pass)",
    "Did not run npm run build / tsc --noEmit / ESLint / Playwright E2E / axe-core a11y against bari-web",
    "Did not verify bread's prior copy sign-off history (no prior red-team report existed to check against)",
    "Did not run an adversarial evidence-weight check on d4_additives (E300/E202) against EFSA/openfda"
  ],
  "self_check": {
    "read_artifacts_directly": true,
    "accepted_builder_summary": false,
    "ran_deterministic_gate_script": true,
    "gate_script_path": "C:\\Bari\\03_operations\\page_generator\\gates\\run_gates.py",
    "gate_script_exit_code": 1,
    "gate_script_verdict": "FAIL",
    "fixture_library_touched": false,
    "scores_or_copy_or_data_modified": false,
    "acceptance_test": "D10 unified gate requires Track V green AND Track C zero open CRITICAL; neither holds; verdict = NO-GO / BLOCKED, correctly proposed as RETURNED not CLOSED"
  }
}
```
