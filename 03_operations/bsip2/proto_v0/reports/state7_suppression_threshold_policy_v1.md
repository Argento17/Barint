# State 7 Score-Suppression Threshold Policy v1

**Owner:** Nutrition Agent (methodology) · **Co-sign required:** Product Agent (visibility, D7)
**Resolves:** §8 open question #2 of `01_framework/frontend/score_confidence_indicators_spec_v1.md`
**Scope:** the `partial → insufficient` (show-caveated-score → suppress to `טרם נוקד`) boundary, plus the data fields needed to render the 7 display states. **Does NOT change scoring rules or dimension weights.**
**Date:** 2026-06-10
**Verdict:** **PASS** (see §6)

---

## 0. The governing principle

A grade is defensible only when the dimensions that *drive* it have real inputs. BSIP2 weights four load-bearing dimensions: processing quality (D3, from the ingredient list + NOVA proxy), nutrient density and calorie density (from the nutrition panel), and fat/sodium/sugar quality (from the panel). The suppression line is therefore not "is some field missing" — it is **"are enough driving inputs present that the resulting grade means something."**

The engine already computes this. `data_sufficiency` (`sufficient | insufficient`), `confidence_band` (`high | medium | low | insufficient`), and `evaluation_status` (`standard | context_limited`) are emitted on every BSIP2 trace. State 7 is the consumer-facing surface of `data_sufficiency == insufficient` / `confidence_band == insufficient`. **We are wiring display to an existing engine verdict, not inventing a new one.**

**Anchor it in the engine, not the frontend JSON.** The displayed `*_frontend_*.json` files redact `expansion.ingredients` (and, for the snacks corpus, `expansion.nutrition`) to `null` as a *packaging* choice — the scoring engine still saw the full BSIP0 panel. The threshold must read the **trace**, never the redacted display payload. (Evidence: snack-bar `bsip1_16000423534` shows `ingredients=null`/`nutrition=null` in `snacks_frontend_v2.json` but its trace carries `data_sufficiency: sufficient`, full L1 nutrition, a real `ingredient_list`, and score 51.5/C.)

---

## 1. The v1 State-7 threshold rule (decision list)

Read the BSIP2 trace, in order. First matching rule wins.

```
INPUT (per product, from the BSIP2 trace — NOT the frontend JSON):
  panel        = nutrition panel present with ≥1 of the 4 macro drivers
                 (energy_kcal, protein_g, carbohydrates_g, fat_g) non-null
  ingredients  = ingredient_list present and non-empty
  data_suff    = trace.data_sufficiency        # sufficient | insufficient
  conf_band    = trace.confidence_band          # high|medium|low|insufficient
  extract_conf = trace.ingredient_text_quality + nova_confidence_band  # see note (d)

R0  data_suff == "insufficient"  OR  conf_band == "insufficient"   → SUPPRESS (State 7)
R1  NOT panel AND NOT ingredients                                   → SUPPRESS (State 7)
R2  NOT panel (no macro driver at all)                              → SUPPRESS (State 7)
        # nutrition panel is the spine: density + calorie + fat/sodium/sugar
        # dimensions all collapse without it. A grade on ingredients alone is
        # not defensible. (Overrides spec State 4 for the TOTAL-panel-absent case.)
R3  panel present AND NOT ingredients                               → SCORE-WITH-CAVEAT (State 3)
        # D3/processing degrades to NOVA-proxy-from-name (low confidence) but
        # the panel-driven majority of the score stands. Defensible-with-caveat.
R4  ingredients present AND panel present but ONE macro driver
        missing (e.g. fiber, or sugars/sat-fat)                     → SCORE-WITH-CAVEAT (State 2)
R5  inferred category (category_confidence < CAT_CONF_MEDIUM=0.50
        AND category_instability_flag)                              → SCORE-WITH-CAVEAT (State 5)
        # category inference shifts thresholds, not the existence of a defensible
        # score; the engine already relaxes thresholds under low cat-confidence.
        # EXCEPTION → escalates to R0 only if it ALSO trips data_suff insufficient.
R6  low extraction confidence (see note d)                          → SCORE-WITH-CAVEAT (State 6)
ELSE                                                                → SCORE, complete (State 1)
```

### Which missing inputs collapse defensibility (the methodology call)

| Missing input | Effect on the grade | Disposition |
|---|---|---|
| **Entire nutrition panel** (no macro driver) | Collapses density + calorie + fat/sodium/sugar quality — the majority of the weighted score. No defensible grade. | **SUPPRESS** (R2) |
| **Ingredient list only** (panel present) | Degrades D3/processing to a name-based NOVA proxy at low confidence; the rest of the score is intact. | **CAVEAT** (R3 / State 3) |
| **Both** | Nothing left to score. | **SUPPRESS** (R1) |
| **One macro driver** (fiber, sugars, sat-fat) | A single sub-dimension softens; the grade still means something. | **CAVEAT** (R4 / State 2) |
| **Inferred category** | Thresholds shift; a defensible grade still exists (engine already relaxes). | **CAVEAT** (R5 / State 5) |
| **Low extraction confidence** | Inputs exist but are uncertain; the engine already haircuts confidence. | **CAVEAT** (R6 / State 6) |

**Combinations that MUST suppress:** any combination that satisfies R0, R1, or R2 — i.e. (a) the engine itself returned `data_sufficiency: insufficient` or `confidence_band: insufficient`, (b) both sources absent, or (c) the nutrition panel is entirely absent. Everything else caveats.

### (d) The OCR / extraction-confidence band — **engine gap, flagged for Data Agent**

State 6 ("OCR/parse confidence below threshold") **has no numeric backing in the live engine.** `signal_extractor.py` emits only `ingredient_text_quality` (categorical: `clean | corrupted | malformed | marketing_bleed`) and `nova_confidence_band` (`high | medium | low`, derived from evidence, not from a parse score). There is **no per-product OCR/extraction confidence float** in the in-house pipeline. Two of the batch loaders (`batch_run_bread_retail_003.py`, `batch_run_bread_retail_002_v2.py`) carry an `extraction_confidence` string defaulting to `"medium"` — a passthrough placeholder, not a measured value.

**Ruling (do not invent a signal):** for v1, State 6 fires on the **categorical proxy already present**, not a fabricated float:

```
extract_low  =  ingredient_text_quality in {corrupted, malformed, marketing_bleed}
                OR nova_confidence_band == "low"
```

This is honest — it uses real observability and never manufactures a differentiator that doesn't exist (cf. "never manufacture differentiation," butter-clustering memo). **If a true numeric OCR-confidence band is wanted, it is a Data-Agent/BSIP0 emission gap (new field `extraction_confidence: float ∈ [0,1]` from the scrape/parse layer), not a Nutrition deliverable.** Until that field exists, State 6 = the categorical proxy above. A numeric band that would *move the suppress/caveat line* would need EV-### + D7 co-sign.

---

## 2. Classification of the 7 spec states → 3-state VM

The spec's §6 mapping is **confirmed correct as written, with one clarification on State 4.**

| # | Spec state | VM `confidence` | Confirm / correct |
|---|---|---|---|
| 1 | Complete data | `verified` | **Confirm** |
| 2 | Partial (non-essential field absent) | `partial` | **Confirm** |
| 3 | Missing ingredient list (panel present) | `partial` | **Confirm** — panel carries the score; caveat only |
| 4 | Missing nutrition panel (ingredients present) | `partial` *if a partial panel remains*; **`insufficient` if the panel is TOTALLY absent** | **Clarify.** The spec narrates State 4 as "ingredient list present, nutrition panel absent." If "absent" means *every* macro driver is null, that product fails R2 and is **insufficient → State 7**, not partial. State 4 (`partial`) is reserved for a *thin-but-present* panel. A fully-absent panel is never a partial caveat — there is no defensible grade. |
| 5 | Inferred category | `partial` | **Confirm** (needs sub-reason flag, §5) |
| 6 | Low-confidence extraction | `partial` | **Confirm** (needs sub-reason flag, §5; fires on categorical proxy per §1d) |
| 7 | Not enough data to score safely | `insufficient` | **Confirm** |

Net: states **1→verified; 2,3,4(thin),5,6→partial; 4(panel-totally-absent),7→insufficient.** The only substantive correction is that "missing nutrition panel" splits on *thin vs. totally absent*; the totally-absent case routes to insufficient, consistent with R2.

---

## 3. Do any currently-displayed scored products move to טרם נוקד?

**Answer: NONE.**

Method: joined every scored product in the live corpora (`bari-web/src/data/comparisons/*.json`) back to its BSIP2 trace by `canonical_product_id` / `barcode`, and read the trace's `data_sufficiency` / `confidence_band` / `evaluation_status`.

- **469 scored products** across 14 live category files. **417 matched** a trace by id/barcode.
- Of the 417 matched: **336 `(sufficient, high)`, 48 `(sufficient, medium)`, 33 `(sufficient, low)` — zero `insufficient`** on either axis. The 33 `low`-band products are already shown as caveated (`partial`) scores, which is correct State-6 behavior, not suppression.
- **Butter (the highest-risk category):** 31/31 live scored products matched a trace; **0** are `data_sufficiency/confidence insufficient`. The insufficient butter traces that *do* exist in `run` (`3760088100025`, `7290105953020`, `5099460004149`, etc.) were **filtered out of the displayed corpus** — they never reached a live page. The curation layer already did what State 7 does.
- **52 unmatched** (bread 19, olive_oil 11, crackers 5, cheese 17) use a different id scheme (`shufersal_*`, `che-*`, staged). Verified directly: **every** scored row in bread/olive/crackers carries a full nutrition panel and is already classified `partial`; none has a null panel. Bread is provenance-frozen at `real_bread_retail_003` (256 scanned → 81 scored → 31 curated = 24 scored **+ 7 transparency**); the 7 transparency entries are the already-separated unscored class — bread already implements the suppress/score split.

**Conclusion:** the threshold in §1 reclassifies **no currently-displayed scored product** to State 7. Every product the engine flagged insufficient is *already* absent from display. This policy formalizes a boundary the curation layer is already honoring; it moves zero published scores.

---

## 4. Tripwire assessment & verdict routing

Tripwire #1 (touches published scores / score visibility) fires **only if a displayed score would be suppressed.** Per §3, **none would.** Therefore:

- This is **reversible display logic** (a VM-field + label mapping), not a score move. It does **not** require owner escalation and does **not** require blocking on Product approval.
- **Verdict: PASS.** Implement as reversible display wiring (Data Agent populates the fields in §5; Frontend renders per the approved visual spec).

**However — one item I surface for Product, non-blocking:** the §2 clarification that a *totally-absent* nutrition panel routes State 4 → insufficient (R2) is a methodology tightening. It changes **no live product** (none are displayed with a fully-absent panel), so it is not a tripwire today. But it is the rule that will gate *future* category go-lives. **Product should acknowledge R2 (panel-absent ⇒ suppress) as the standing pre-go-live gate** so it is applied consistently when new corpora are packaged. This is an FYI/acknowledgement, not a go/no-go block.

If at any future packaging a product currently carrying a *displayed* grade is found to fail R0/R1/R2, that **does** trip tripwire #1 and must BLOCK pending Product co-sign before suppression ships.

---

## 5. Data fields the Data Agent / Frontend Agent must populate

Emitted by the backend/VM-transformation layer (`@/lib/comparisons`), consumed read-only by the UI.

| Field | Type | Allowed values | Source |
|---|---|---|---|
| `confidence` | enum (required) | `verified \| partial \| insufficient` | from trace: `confidence_band=high & data_sufficiency=sufficient` → `verified`; insufficient per R0/R1/R2 → `insufficient`; else `partial` |
| `confidence_label_he` | string (required) | pre-rendered Hebrew badge label (spec §3 col 6) | backend-rendered |
| `confidence_tooltip_he` | string (required) | pre-rendered Hebrew tooltip sentence (spec §3 col 7) | backend-rendered |
| `confidence_sub_reason` | enum (optional) | `missing_ingredients \| missing_nutrition \| inferred_category \| low_extraction \| partial_field` (`null` for states 1 and 7) | derived from the §1 rule that fired |

**`confidence_sub_reason` value ↔ state map:** State 2 → `partial_field`; State 3 → `missing_ingredients`; State 4(thin) → `missing_nutrition`; State 5 → `inferred_category`; State 6 → `low_extraction`; States 1 & 7 → `null` (no sub-reason: complete needs none, suppressed needs none).

### Recommendation: **backend pre-renders the Hebrew strings.** Ship `confidence_label_he` + `confidence_tooltip_he` as finished strings; ship `confidence_sub_reason` **as well**, but as metadata, not as the UI's branching key.

Rationale (agrees with spec §8 rec (b) and the VM Boundary Rule): the VM contract states the UI "never computes confidence" and "backend renders Hebrew." If the UI mapped an enum → Hebrew, interpretation would leak across the VM boundary. So:
- The **label and tooltip the user sees** are backend-rendered strings (authoritative, single source of Hebrew copy — the exact strings already live in spec §3, owner-approved).
- `confidence_sub_reason` ships **only** as analytics/QA metadata and for the collapsed-row dotted-marker logic (which needs to know *that* there is a caveat, via `confidence != verified`, not *which* one). The UI must not branch Hebrew copy off it.

This keeps the UI dumb, keeps all Hebrew in one backend-owned place, and matches the existing `confidence_level → confidenceLabel` transformation already in the VM spec.

---

## 6. Verdict

**PASS** — the threshold formalizes an existing engine verdict (`data_sufficiency`/`confidence_band`), reclassifies **zero** currently-displayed scored products to `טרם נוקד`, and ships as reversible display wiring (VM fields in §5 + the Design-approved visual spec). No score moves; no tripwire fires; no Product block required.

**Two non-blocking items surfaced to Product (acknowledge, do not gate this PASS):**
1. R2 (totally-absent nutrition panel ⇒ suppress) as the standing pre-go-live gate for future categories.
2. The State-6 OCR/extraction-confidence *numeric* band is an engine/data emission gap (no per-product float exists). v1 fires State 6 on the categorical `ingredient_text_quality`/`nova_confidence_band` proxy. A future numeric band that would move the suppress/caveat line needs EV-### + D7 co-sign — routed to Data Agent, not invented here.
