# Bari Exception Registry — v1

**Status:** Active  
**Date:** 2026-05-28  
**Scope:** All deliberate deviations from frozen architecture rules across all Bari categories  
**Authority:** Any addition to this registry requires explicit approval. Undocumented exceptions are architecture violations.

---

## Purpose

The Bari comparison template architecture is frozen. Exceptions are not improvements — they are acknowledged risks that have been evaluated and approved on specific grounds. This registry documents every exception, its justification, and the constraints that prevent it from becoming a template for further drift.

A registered exception is not an invitation to repeat. It is a named deviation with defined boundaries.

---

## How to Use This Registry

**Before adding a UI element that violates a template rule:**

1. Identify which rule is being violated (cite section and item from `comparison-template-standard-v1.md` or `mobile_geometry_checklist_v1.md`)
2. State the consumer need that cannot be met without the exception
3. State why no in-template solution exists
4. Define the exact constraints that prevent the exception from multiplying
5. Submit for registry approval before shipping

If you cannot answer all four questions, the exception is not ready. Build the in-template solution instead.

---

## Active Exceptions

### EXCEPTION-001 — Bread Fermentation Filter Tooltip

**Status:** Approved  
**Category:** לחם (Bread)  
**Date approved:** 2026-05-28  
**Rule violated:** UI Stabilization Sprint 1 — "no tooltips on any UI element except EXCEPTION-001" (which this entry defines)

---

**What it is:**

A ⓘ info icon placed beside the filter option "ללא מחמצת מזוהה" in the bread category filter panel. When tapped, it displays a brief explanation (1–2 sentences maximum) of what "ללא מחמצת מזוהה" means in plain language.

It does not appear on any product row, any ingredient list, any score chip, or any other UI element. It appears only on one specific filter label.

---

**Why it is allowed:**

The filter label "ללא מחמצת מזוהה" uses the word "מחמצת," which is printed on bread packaging by manufacturers as a consumer-facing claim. It is not internal framework vocabulary. The tooltip clarifies a filter option whose words are already in use on product labels — the consumer who buys bread has already seen this word.

The need arises because a consumer may tap the filter and not understand why a bread with "שאור" in its name appears in the "ללא מחמצת מזוהה" filter. The tooltip explains that the filter reflects what was detectable in the ingredient list — not the packaging claim. This is a verification statement, not a framework disclosure.

---

**Why it does not violate the ontology-leakage policy:**

The ontology-leakage policy prohibits surfacing internal framework concepts in consumer language. The concepts at risk are: NOVA, BSIP, cap values, routing logic, structural classes, and analytical methodology.

This tooltip explains none of those. It explains the gap between a label claim and an ingredient-list signal, using words the consumer already knows: מחמצת (from packaging), שמרים (from packaging), רשימת הרכיבים (universally understood). No internal scoring variable, weight constant, or framework class is mentioned or implied.

Test: A consumer reading this tooltip learns that some breads say "שאור" on the front but use industrial yeast in the ingredients. That is a shelf observation, not a framework disclosure.

---

**Constraints preventing multiplication:**

1. **This is the only tooltip in the product.** No other filter option, score chip, ingredient item, product name, or UI element may carry a tooltip. A second tooltip anywhere in the product — regardless of category — constitutes a drift event requiring registry review and explicit re-approval.

2. **The tooltip text is fixed and reviewed.** It may not be updated without editorial review. It is not dynamically generated.

3. **Scope is bread only.** This exception was approved because מחמצת is a consumer-visible claim specific to the bread category. Other categories may not use this exception as a precedent. If מעדנים or חלב requires a tooltip, a new registry entry must be written and approved — it cannot inherit this approval.

4. **Filter context only.** The tooltip is permitted only on the filter label. If any developer or designer places a ⓘ icon on a product row, score chip, or ingredient text, it is an unauthorized exception regardless of content.

---

**Approved text (Hebrew):**

> "מחמצת לא זוהתה ברשימת הרכיבים. המוצר עשוי לציין שאור על האריזה."

Maximum 2 sentences. No additional explanation.

---

### EXCEPTION-002 — Protein-Bars Non-Conforming Pipeline Shape (No BSIP1 Trace Directory)

**Status:** Approved
**Category:** חטיפי חלבון (Protein Bars)
**Date approved:** 2026-07-03
**Rule violated:** Bari category-factory standard pipeline shape — every category is expected to have a BSIP1 enrichment trace directory (`bsip1_*.json` per product) behind its scored corpus; scoring is expected to read from that trace directory, not from a flat corpus JSON directly.

---

**What it is:**

The protein-bars category (`protein_combined_frontend_v2.json`, live route
`bari-web/src/app/hashvaot/protein-bars/`) was built and scored **inline, directly
from a flat corpus JSON** —
`02_products/snack_bars/protein_combined_corpus_task365_33_20260621_fix.json`
(33 products; corpus sha256 `469c65015bb7e5e80cd844d5d69066c53048e2f34446c917b0eb2b1b77987dc3`)
— via `batch_run_protein_bars_task365.py` / `rescore_task365_inplace.py`. There is
no BSIP1 trace directory that corresponds to this corpus. The directory the
category config points at (`02_products/snack_bars/bsip2_outputs/protein_bars_task365/`)
contains only rerank/run-record summary files, zero `bsip1_*.json` files.

Of the 33 corpus barcodes, **13 exist in NO known BSIP1 trace directory anywhere
in the repository** (confirmed by TASK-477 Phase 1 diagnosis — checked
`canonical_bsip1/run_001`, `canonical_bsip1/run_task362`, and three
`03_operations/bsip1/run_snacks_task360_*` directories; union coverage 20/33,
13/33 in none). This is not data loss — the 13 products were enriched and
scored during the original task365 corpus build without a standalone BSIP1
file ever being written for them. This is the documented shape of this
category's build, not a defect discovered after the fact.

This exception covers the TASK-477 Phase 2 surgical rescore (13 movers:
score/grade/rank/`_scoring_trace` updated in `protein_combined_frontend_v2.json`
per `03_operations/page_generator/reports/task477/protein_bars_gate_b_result.json`,
co-signed by Nutrition + Product) shipping through this non-conforming shape
rather than being blocked pending a forced conform to the standard BSIP1-directory
pipeline.

---

**Why it is allowed:**

**1. Consumer need that cannot be met without the exception:** The protein-bars
ingredient-handoff fix (an `input_loader.get_ingredients()` precedence-chain
correction, already live in every other category) needed to reach the 13
grade/score-affected protein-bar products. Blocking the rescore until all 33
products have a conforming BSIP1 trace directory would leave the category
running on a stale ingredient-handoff bug indefinitely — worse for the
consumer than shipping the corrected numbers through the category's existing
(non-conforming) pipeline shape.

**2. Why no in-template solution exists:** Re-deriving 13 missing BSIP1 records
would require re-running the original scrape/enrichment for those 13 SKUs. No
source scrape is guaranteed to reproduce byte-identically to what was captured
during the original task365 build (retailer pages change, prices/stock rotate,
scrape timing affects captured panel state). Forcing conformance here trades a
*known-reproducible* result for a *newly re-scraped, unverifiable* one — data
drift risk for zero consumer benefit, purely to satisfy directory-shape
uniformity.

**3. The reproduction guarantee that substitutes for the missing BSIP1 directory:**
`03_operations/page_generator/provenance/protein_bars_reproduce_harness.py`
scores the true 33-product corpus through the **same canonical engine modules**
every other category uses — `signal_extractor.extract_signals` →
`router_v2.classify_category` → `nova_proxy.infer_nova` →
`evaluation_scope.assign_evaluation_scope` → `score_engine.score_product` (plus
`apply_protein_bar_grade_proportionality`) — with the same published flags
(`BARI_PROTEIN_BAR_V1=on, BARI_FAT_TECH_V1=on, BARI_GLASSBOX_W4=on`, rest off).
Only the *loading* step differs (flat corpus JSON read directly vs. glob of a
BSIP1 directory); the scoring path itself is identical to every conforming
category. Run twice back-to-back for TASK-477 Phase 1: byte-identical mismatch
set both times (19/32 exact match, 13/32 move, same 13 barcodes, same deltas) —
confirming the inline-scored shape is stable and reproducible, not
non-deterministic.

**4. Constraints preventing multiplication (drift test):**

   a. **Scope is protein-bars only.** This exception documents a build-history
      fact about this specific category (task365's inline-scoring build
      choice). It is not a general license for any future category to skip
      BSIP1 enrichment. Any new category build must go through the standard
      `bari-category-factory` 7-stage pipeline including BSIP1; this exception
      does not retroactively bless skipping that stage going forward.

   b. **No forced re-conform without an explicit new decision.** `rescore_all.py
      --shelf protein_bars` will continue to hard-error on this category
      (confirmed, TASK-476b run record) because `corpus_dirs` has no
      `bsip1_*.json` files. That hard-error is intentional and stays in place —
      it is the tripwire that prevents a future automated rescore from silently
      assuming this category conforms. Any future attempt to force this
      category onto the standard path requires re-deriving the 13 missing
      records, which is a distinct, explicitly-approved future task, not a
      side effect of this exception.

   c. **The reproduction harness is the permanent substitute artifact.** Any
      future rescore of this category must go through
      `protein_bars_reproduce_harness.py` (or a direct successor covering the
      same 33-barcode corpus) — not a fresh ad hoc script — so the "same engine
      modules, same flags" guarantee holds every time, not just this once.

   d. **This exception does not extend to future data loss.** If any future
      corpus refresh for this category drops additional barcodes without the
      `missing_data_discard_rule` being explicitly invoked and logged, that is
      a new incident, not covered by this entry.

---

**Why it does not require re-deriving the corpus to be "safe":**

The TASK-477 Phase 1 diagnosis independently verified (not just trusting
self-declared metadata) that the live scores trace 1:1, by barcode, with 0
extra/0 missing records, from `rerank_table_rescore.json` to the corpus JSON's
own scraped `ingredients_full`/`nutrition_per_100g` fields — never to any
`bsip1_*.json` file, stray or otherwise. A separate stray-record risk was found
and ruled out for the *current* published scores (5 barcodes also appear,
coincidentally, in an unrelated `run_maadanim_001` deli-category BSIP1 run;
checked all 5 — same name, same nutrition, materially identical ingredients;
routed as a shared root-cause risk to TASK-409 corpus-hygiene for any *future*
tool that globs BSIP1 files by barcode without corpus-scoping, not a defect in
today's published numbers).

---

**Approved by:** Nutrition Agent + Product Agent (joint co-sign on the TASK-477
Phase 2 mover set and this exception, per the scoring-rule/pipeline-shape
co-sign requirement).

**Filed by:** Data Agent, TASK-477 Phase 2, 2026-07-03.

---

## Rejected Exception Requests

*None yet. This section will log exception requests that were reviewed and denied, with rationale, so future contributors understand the boundaries.*

---

## Governance

### Approval process

1. Write a proposed entry following the format above
2. Answer all four required questions (rule violated, consumer need, no in-template solution, multiplication constraints)
3. Present for editorial review — approved additions are merged into this registry and the relevant UI spec is updated to reference EXCEPTION-[N]
4. Unapproved exceptions shipped to production are architecture violations, not judgment calls

### Registry maintenance

- Exceptions are reviewed at each major category launch
- If an exception's consumer need disappears (e.g., bread changes its filter label), the exception is retired and the tooltip removed
- Retired exceptions remain in this document under a "Retired" section for historical reference

### The drift test

Before adding an exception, ask: if ten other teams in ten other categories saw this exception, would it spread into something that mutates the architecture? If yes, the exception is not narrow enough. Tighten the constraints or abandon the exception.

---

*This registry is governed by the same editorial authority as `comparison-template-standard-v1.md` (the canonical comparison template). Architecture rules in the template take precedence over any exception not documented here.*
