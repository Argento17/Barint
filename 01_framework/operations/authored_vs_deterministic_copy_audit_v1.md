# Authored-vs-Deterministic Copy Audit — v1 (CORRECTED 2026-06-10)

**Task:** TASK-BARI-PROMPT-REGISTRY-CI-EVAL-V1 — Deliverable 2, Step 0
**Owners:** content-agent + qa-agent
**Date:** 2026-06-10 · **Revision:** v1.1 (corrects an inverted v1.0 finding flagged by QA)
**Purpose:** Resolve reconciliation gap #1 — classify every consumer-copy field as
deterministic-builder output vs content-agent-authored **from real builder-file
evidence (no inference)** and assign the correct eval method.

> **Correction notice.** v1.0 of this audit claimed "most insightLine / explanation
> arrays are deterministic builder output," generalizing from a single builder
> (`build_salty_snacks_frontend_v2.py`). QA review overturned this. Per-builder
> file inspection shows the **opposite**: most shipped `insightLine`s are
> **content-agent-authored and carried verbatim** by builders. The deterministic
> builder scope is **narrow**. This revision records the per-category evidence.

---

## 1. Accurate headline finding

**Most shipped `insightLine`s and explanation arrays are authored / carried-verbatim
content-agent copy.** Builders predominantly *load and pass through* authored Hebrew
(from `content_draft_v1.md`, `content_reauthor_*` reports, prior-version JSONs, or
post-build patches). **Deterministic builder scope is narrow:** only
`salty_snacks` + `snacks` (shared builder) and `butter` compute `insightLine` from
the trace; `snacks` `limitingFactors` is computed; and a *separate*
`build_cereals_multiretailer_frontend.py` path computes `rowVerdict` for
new-retailer products only. Everything else is authored.

---

## 2. Per-category provenance table (file evidence)

| Category | Field | Builder file | Producing assignment / fn | Classification | Evidence |
|----------|-------|--------------|---------------------------|----------------|----------|
| salty_snacks | insightLine | `03_operations/bsip2/proto_v0/src/build_salty_snacks_frontend_v2.py` | `build_insight_line(trace,b1)` | **computed** | line 57 fn def; line 160 `insight = build_insight_line(...)` |
| snacks | insightLine | same builder (produces `snacks_frontend_v2.json`) | `build_insight_line(trace,b1)` | **computed** | grep: builder writes `snacks_frontend_v2` |
| snacks | limitingFactors | same builder | `limiting=[]` from caps/penalties, dedup `[:4]` | **computed** | lines 146–158 |
| butter | insightLine | `02_products/butter/build_frontend_v2.py` | `build_insight_line(trace,subtype)` | **computed** | line 84 fn def |
| cereals (multiretailer) | rowVerdict | `03_operations/bsip2/proto_v0/src/build_cereals_multiretailer_frontend.py` | `row_verdict = f"{name}: {insight_line}. מקור: {retailer}."` | **computed** (new-retailer only) | line 170; line 8 "no authored copy; use trace data" |
| hummus | insightLine + positiveSignals/limitingFactors | `02_products/build_glassbox_w4_frontend.py` (v5) ← carries `build_hummus_frontend_v4.py` | "carried verbatim from live v4 JSON" | **carried-verbatim authored** | w4 line 16 "carried verbatim from v4/v2"; v4 line 91 `carried_verbatim_from_v3:[... insightLine]`, line 93 "STALE — Content Agent must rewrite" |
| cereals (008) | insightLine + rowVerdict | `03_operations/bsip2/proto_v0/src/build_cereals_008_frontend.py` | `UPDATED_COPY[pid][...]` literal strings; "carry authored verbatim" | **content-authored / patched** | line 15 "load existing authored Hebrew copy → carry forward"; lines 75/80 literal rowVerdict strings |
| bread | insightLine | `02_products/bread_retail_003/build_lechem_frontend_json.py` | `INSIGHT_LINES.get(barcode)` | **content-authored** | line 213; `INSIGHT_LINES` dict |
| yogurts | insightLine | `02_products/yogurt_system/build_yogurts_frontend_v2.py` | copied verbatim from `content_reauthor_143_run_yogurt_004.md` | **content-authored** | lines 11/18/38 "Content-authored insightLine … verbatim" |
| juices | insightLine | `03_operations/bsip2/proto_v0/src/build_juices_frontend_v3.py` | from `content_draft_v1.md` | **content-authored** | line 7 "Content Agent insight lines"; line 32 `CONTENT_MD` |
| granola | insightLine + rowVerdict | `03_operations/bsip2/proto_v0/src/patch_granola_verdicts_v2.py` | patches `p["rowVerdict"]=rv` from authored map | **patched authored** | line 3 "Patch … insightLine + rowVerdict"; line 30 `id->(insightLine,rowVerdict)` |
| cheese | insightLine | `03_operations/bsip2/proto_v0/src/build_yogurt_cheese_multiretailer_frontend.py` | "carry ALL fields verbatim from live JSONs" | **carried-verbatim authored** | line 6; line 145 `insightLine: insight_line` |
| hard_cheeses | insightLine | `02_products/hard_cheeses/build_final_frontend_v2.py` | `INSIGHT_LINES` from `content_draft_v1.md` | **content-authored** | lines 22–23, 128 |
| maadanim | insightLine | `02_products/build_glassbox_w4_frontend.py` | carried verbatim from live v4 | **carried-verbatim authored** | line 16 |
| milk | insightLine/positives/cautions/takeaway | `bari-web/src/lib/comparisons/milk-product-insights.ts` (no python builder) | literal authored TS object | **content-authored** | TS `INSIGHTS` record, literal Hebrew |
| bread | positiveSignals[] (expansion) | builder | no array assignment found in `build_lechem_frontend_json.py` | **unverified** | grep found no `positiveSignals=` in builder |
| yogurts | unknowns[]/arrays (expansion) | `build_yogurts_frontend_v2.py` | "interpretive expansion explicitly deferred by 3b" | **unverified** (v3 source unproven) | line 19 |
| all | category | `router_v2.py` | rule-based | deterministic | excluded_existing_regression |
| all | ingredients | `signal_extractor.py` | regex/taxonomy | deterministic | excluded_existing_regression |
| all | score | `score_engine.py` | deterministic | frozen invariants | excluded_existing_regression |

---

## 3. Eval-method routing rules (applied)

| Provenance | eval_method |
|------------|-------------|
| verified **computed** from trace | `golden_diff` |
| **content-authored / carried-verbatim / patched** | `pairwise_judge` (+ manual 2nd gate where flagged) |
| structural arrays (shape/banned-phrase), any provenance | `schema_validation` |
| **unverified** provenance | `manual_review` until proven |
| categorization / parsing / scoring | `excluded_existing_regression` (not in this set) |

---

## 4. Corrected eval-method distribution (verified against the dataset YAML)

| eval_method | Count (primary) |
|-------------|-----------------|
| pairwise_judge | 33 |
| golden_diff | 10 |
| schema_validation | 4 |
| manual_review | 3 |
| **Total** | **50** |

(golden_diff: CMP-01 salty_snacks, CMP-10 snacks, CMP-11 butter, EXP-06 snacks
limitingFactors, CLS-01…06 closure decisions. manual_review primary: EXP-07 bread
arrays, EXP-08 yogurt arrays, HMG-03 glass-box W1. manual_review also runs as a
2nd gate on CAV-01/02/06 and HMG-02.)

---

## 5. Conclusions

1. **Deterministic copy is the exception, not the rule** — 3 insightLine generators
   + 1 computed array + 1 computed rowVerdict path. The v1.0 headline is retracted.
2. **`rowVerdict` splits by producing run, not category** — cereals has BOTH an
   authored path (`build_cereals_008`) and a computed path (`multiretailer`). Route
   per producing run.
3. **hummus v5 arrays are carried-verbatim authored** (via `build_glassbox_w4`),
   NOT output of the deterministic `build_hummus_explanation_v1.py` — so they are
   pairwise, and the v4 lineage explicitly flags them STALE.
4. **Two surfaces remain genuinely unverified** (bread/yogurt expansion arrays) →
   `manual_review` until a builder is proven, per governance rule.
5. **No deterministic parsing/categorization/scoring added to the eval set** —
   constraint honored.
