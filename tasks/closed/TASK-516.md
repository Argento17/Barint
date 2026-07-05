---
id: TASK-516
title: Crackers shelf expansion (add פריכיות + extensions) + brand extraction fix
owner: data-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-07-05
closed_at: 2026-07-05
close_reason: >
  Deliverable 1 (brand fix) SHIPPED to local task506 branch, commit 15c9ce8c (not yet
  pushed/PR'd): 17/19 -> 0/19 null, verified brand-only against origin/master (the
  correct baseline: 19/19 identical score/grade/copy, 17/19 brand populated).
  Two-gate signed off: Content Agent SIGN-OFF (agent a53a6f5f75593bf67) + Adversarial
  QA GO-WITH-CAVEAT (agent acd8d381b2b8b216a, independent live re-fetch 5/5 match).
  One non-blocking follow-up: barcode 8434165658523 ships "KRIT" (uppercase) vs the
  evidence file's literal "krit" lowercase -- doc/evidence-consistency nit for
  data-agent, not a display defect. NOTE: the orchestrator's first sign-off request
  produced a false HOLD because the Content Agent diffed against a stale local branch
  HEAD instead of origin/master -- corrected and re-verified before shipping.
  Deliverable 2 (פריכיות expansion) BSIP0->1->2 complete for 34 new products (53-product
  combined corpus), committed as backend/pipeline artifacts only -- frontend regen,
  QA gate, and content authoring intentionally NOT done, spun out to TASK-517
  (content authoring was wrongly assumed to already exist for the original 19
  products; corrected mid-task -- see TASK-517).
depends_on: []
blocks: []
category_id: crackers
summary: >
  19-product crackers corpus is too narrow; expand shelf mapping to include פריכיות (rice/corn cakes) and its line extensions, re-run BSIP1/BSIP2/QA gate, regen frontend JSON. Also fix brand_extractor.py's bread-derived 7-token allowlist which leaves 17/19 crackers brand=null.
---

# TASK-516 — Crackers shelf expansion (add פריכיות + extensions) + brand extraction fix

## Deliverable 1 — Brand extraction fix: DONE, verified

**Root cause (not what the spec assumed):** the 7-token allowlist wasn't the real gap. A brand-field
fill-rate census across every BSIP0 raw file in the repo showed the May-2026 bread-family scraper
(source of the crackers corpus) never populated the retailer's structured `brand` field at all
(0/258, 0/110), while every scraper written since reads it from the product page's schema.org
ld+json `Product.brand` block at ~100% fill (cereals 113/113, cheese 117/117, chocolate 146/146,
cookies_coffee 129/129, snack_bars 132/132). Most of the real manufacturer names
(קופסת העוגיות של רחלי, פיטנס, הדר, ARDO, ריץ, אביב אורגניק) don't even appear as substrings in the
scraped product names, so no amount of name-text token mining could have recovered them — expanding
the allowlist alone (the spec's framing) would not have fixed this.

**Fix applied:** `03_operations\bsip1\run_crackers_conform_001\fetch_brand_patch.py` — a targeted LIVE
re-scrape of the same 21 Shufersal product pages already in the corpus, reading the retailer's own
ld+json brand field (raw HTML banked to `03_operations\bsip0\raw_store\shufersal\crackers\`, 21 pages,
manifest.jsonl). Recovered 21/21 literal, retailer-attested brand strings. Added 7 new confirmed
tokens to `03_operations\bsip1\core\brand_extractor.py` (BRAND_TOKENS): קופסת העוגיות של רחלי, פיטנס,
הדר, ARDO, ריץ, אביב אורגניק, krit (lowercase variant). `build_crackers_bsip1.py` now consults
`brand_patch_v1.json` before the (always-empty, for this corpus) BSIP0 `brand` field.

**Cross-corpus safety check (Return Contract Rule 8):** `brand_extractor.py` is shared with the bread
BSIP1 builder. Checked all 25 committed bread BSIP1 records' `canonical_name_he` against the 7 new
tokens — 0 hits. Bread's published output is unaffected by this change.

**Result:** brand null-rate on the 19 displayable products: **17/19 → 0/19**. Verified against a fresh
BSIP2 re-run (score/grade byte-identical to origin/master's currently-published crackers_frontend_v1.json
for all 19 products — brand is not a scoring input). Frontend JSON patched surgically (brand field only)
and re-gated: `run_gates.py` G7 PARITY = PASS (0 grade changes, 0 products added/removed, 0 copy-length
drift vs origin/master); `validate_comparison_page.py` = PASS all hard gates (score==trace 19/19, OFF=0,
0 PENDING, 0 ingredient truncation, 19/19 imageUrl).

## Deliverable 2 — פריכיות shelf expansion: BSIP0->1->2 COMPLETE (53-product corpus scored); frontend regen intentionally HELD

**Approvals received (both dispatched in background, both responded):**
- **Nutrition Agent: GO.** Independently re-derived the Rule-5 test from raw data and confirmed 0/36
  trip the boundary flag, but corrected my draft's reasoning: the two sub-2g-fat SKUs
  (7296073161479 fat=1.8g, 7290112348999 fat=1.6g) have **3 real ingredients** (corn, salt, soy
  lecithin), not a "long list" as I'd first written — my initial comma-count was computed off
  un-cleaned raw text that still had the nutrition-table bleed attached. Also confirmed
  `router_v2.py` already has a live HARD_ANCHOR (`"פריכיות" -> category="cracker" @0.88`, line 114) so
  `CALORIE_DENSITY_TABLES["cracker"]` (250-550 kcal/100g) applies automatically — no routing fix
  needed. Found a SECOND missing-data candidate I'd missed: barcode 7296058000526 has nutrition but
  empty ingredients.
- **Product Agent: GO-WITH-CONDITIONS.** Confirmed ~53 products/page is within Bari's live range
  (cookies_coffee=117, hummus=57, cheese=47, brined_cheeses=36 — the golden reference — all pulled
  live from `bari-web/src/data/comparisons/*.json`). Conditions: (1) Rule-5 must close before BSIP1 —
  done, see above; (2) resolve the blackout SKU before admit/discard — done, see below; (3) **new copy
  for the ~34 new products must be authored in ONE pass coordinated with TASK-461's still-queued
  crackers voice-overhaul slot, not twice** — this is now the actual blocker on shipping (not
  approval); (4) standard two-gate sign-off + render/parity gate before anything reaches the owner.
  Also flagged the TASK-486 brand-null "contradiction" for Adversarial QA reconciliation (dispatched,
  see below, does not block this return).

**Corrections folded into `corpus_filter.json` before BSIP1:** fixed the false "long ingredient list"
claim (now correctly states 3 ingredients, still clears Rule-5), added the second missing-data
candidate, added the confirmed router citation. Both flagged barcodes were then re-verified with a
targeted one-shot live re-scrape (per the missing-data-discard rule) before final discard:
**7296058000519** (both nutrition and ingredients still empty on live re-check — total blackout,
discard) and **7296058000526** (nutrition present, ingredients still empty on live re-check — partial
blackout, discard per Nutrition Agent's own stated rule that ingredient text is required for
scoring). **34/36 candidates survive to BSIP1.**

**BSIP1 built:** `03_operations\bsip1\run_ricecakes_conform_001\build_ricecakes_bsip1.py` — same
schema/discipline as the crackers builder, plus a bleed-cutter adapted for this scraper's page
template (confirmed by Nutrition: no preceding sentence-period before the nutrition-table bleed, so
the crackers cleaner's regex wouldn't fire here; the ricecakes cleaner cuts at the first marker
regardless of punctuation, still never inventing — always a verbatim prefix). Brand comes directly
from this scraper's own ld+json capture (34/34, no patch needed) with a documented, narrow
pass-through for retailer-attested strings not yet in the curated token list (this scrape's brand
field is contemporaneous and direct, unlike the stale/empty field the crackers corpus's conservative
design was built to guard against). 34/34 written, 0/34 Rule-5 flags (confirms Nutrition's correction
holds across the full batch, not just the 2 spot-checked SKUs).

**BSIP2 scored:** `03_operations\bsip2\proto_v0\src\batch_run_ricecakes_conform_001.py`, same flag
vector as the existing crackers run. 34/34 scored, 0/34 router mismatches (all confirmed routed to
`category="cracker"` per Nutrition's HARD_ANCHOR citation). Score distribution: min 41.2, max 79.5,
median 70.1, stdev 9.22, grades B:27 C:4 D:3 (no A/S — plausible for a grain-snack shelf with no
standout whole-grain-dominant/minimal-ingredient product in this batch; not a collapse — spread is
healthy, matches the shape of the existing 19-product crackers distribution).

**Combined corpus ready for frontend packaging: 19 (existing, brand-fixed) + 34 (new) = 53 scored
products.** Draft `corpus_filter.json` updated to APPROVED status with both agents' rulings folded in.

**Deliberately NOT done — frontend regen, D4, FAQ, QA gate, red-team/C3 bracket:** Product Agent's
condition 3 is a real, correctly-identified blocker: the 34 new products have no authored
`rowVerdict`/`insightLine`/`expansion` copy, and the content sign-off hard rule (CLAUDE.md) forbids
anything consumer-facing shipping without Content Agent + Adversarial QA sign-off. Generating a
frontend JSON now would either ship unauthored/PENDING_COPY rows (a launch blocker per the hard rules)
or force a second authoring pass once TASK-461's crackers slot runs (exactly what Product said not to
do). This is an orchestrator-level sequencing decision (coordinate with whoever owns TASK-461's
fan-out), not mine to resolve unilaterally — surfacing it rather than guessing. Also dispatched
Adversarial QA (`qa-crackers-486-recon`) to reconcile the TASK-486 brand-null contradiction Product
flagged; response pending as of this return, does not block anything already shipped.

See the JSON return contract below for artifacts, hashes, and commands.

```json
{
  "task": "TASK-516",
  "proposed_status": "RETURNED",
  "artifacts": [
    {"path": "03_operations/bsip1/core/brand_extractor.py", "action": "modified", "sha256": "e20504ea40356de59e130f2746a7f703769098b423e25b2dddad4b6a8debeecc"},
    {"path": "03_operations/bsip1/run_crackers_conform_001/build_crackers_bsip1.py", "action": "modified", "sha256": "6ee5f5b54a911e5d3ceea685b5d41ffbd75158b8c8bf6688002f06057164f50a"},
    {"path": "03_operations/bsip1/run_crackers_conform_001/fetch_brand_patch.py", "action": "created", "sha256": "6c8dc9cca5bee0aaa7d86075309e334da3e90dae911f94f6d13d4726b153d473"},
    {"path": "03_operations/bsip1/run_crackers_conform_001/brand_patch_v1.json", "action": "created", "sha256": "24c85681e8f14f4dfd93c826273d8d6e3449bb256182fc5cc8327885ea55d20d"},
    {"path": "03_operations/bsip1/run_crackers_conform_001/run_record.json", "action": "modified", "sha256": "e0a6e2163b3cf3bcee65165846a276ab3ca6e1ffe743592e69f9e11a0c52cf40"},
    {"path": "02_products/crackers/bsip2_outputs/run_crackers_conform_001/run_record.json", "action": "modified", "sha256": "eb5920524373e2e53225d9b92ac39914523cf545f125f34574c799c6d2ff0887"},
    {"path": "bari-web/src/data/comparisons/crackers_frontend_v1.json", "action": "modified", "sha256": "9f07b85d11462b83a2056c7283bba8a7f744704d0778ce8b8d8a1b79d7cc5517"},
    {"path": "02_products/crackers/factory_run_002/shelf_map.json", "action": "created", "sha256": "2221cd9d588210abcc19bc624139c9643021909fc7453f87af55a1be033ef52a"},
    {"path": "03_operations/bsip0/scrape/shufersal_ricecakes/01_scrape_ricecakes.py", "action": "created", "sha256": "fe4c4ff1c0914ea52b1dd1d869dfa821f01d516a27f0c71c5e7027a54baaa81a"},
    {"path": "02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json", "action": "created", "sha256": "8a41a2c8938c20d780458021e3eda9e3bf1d7df0ebf4aa723e6287da534ee455"},
    {"path": "03_operations/bsip1/run_crackers_conform_001/output/bsip1_5000396021202.json", "action": "modified", "sha256": "df9f93bd884b86582e9198dc3af37f9c796a5da0f5a0f7af41fb54a161ecf688", "note": "representative of the 20-file batch; full list + brand values in run_record.json brand_hits"},
    {"path": "02_products/crackers/bsip2_outputs/run_crackers_conform_001/products/bsip1_crackers_5000396021202/bsip2_trace.json", "action": "modified", "sha256": "60ec0ddef3c5fefbf0de8333d90cf38cea92c5f50dacf8d7b1e4a399fb1461a0", "note": "representative of the 20-file batch; full list in run_record.json results; scores independently cross-checked against origin/master (see score_grade_diff_vs_origin_master count)"},
    {"path": "03_operations/bsip0/raw_store/shufersal/crackers/manifest.jsonl", "action": "created", "sha256": "3d6c54f2667aac8e0121913af922e41643100ced101600a55bd6346939edeb5e"},
    {"path": "03_operations/bsip0/raw_store/shufersal/ricecakes/manifest.jsonl", "action": "created", "sha256": "845945c942e2a6730193872d6635abe8a24a0cd19fbe57654408d7e5ae97d7e5"},
    {"path": "02_products/crackers/factory_run_002/corpus_filter.json", "action": "modified", "sha256": "30cf9b26892555bc2d91350050b691e47721887d19d2b65f4fcbd1545757ec77", "note": "post-approval revision: folds in Nutrition Agent's ingredient-count correction + second missing-data candidate + router citation; status changed DRAFT->APPROVED"},
    {"path": "03_operations/bsip1/run_ricecakes_conform_001/build_ricecakes_bsip1.py", "action": "created", "sha256": "fbb164cc2d20af16acf81b218ee3be497d5e30ae0f3208d6c91fcfd573162e29"},
    {"path": "03_operations/bsip1/run_ricecakes_conform_001/run_record.json", "action": "created", "sha256": "6ec1c329713b2851ccf9ca6cbf20bf6573baf898e1e5537d05a9f1a5b93d1309"},
    {"path": "03_operations/bsip1/run_ricecakes_conform_001/output/bsip1_7296073161479.json", "action": "created", "sha256": "637fca181051ecfcfe78a411a42dc749b815722969611ff58885cfd9c702fe89", "note": "representative of the 34-file batch (this is one of the two Nutrition-Agent-spot-checked SKUs); full list in run_record.json results"},
    {"path": "03_operations/bsip2/proto_v0/src/batch_run_ricecakes_conform_001.py", "action": "created", "sha256": "1e4601c505052ac82361ff7cd677b73582616bd1fb435ea6b1d9fec498944d6c"},
    {"path": "02_products/crackers/bsip2_outputs/run_ricecakes_conform_001/run_record.json", "action": "created", "sha256": "ca15618c015cf1fa613099f5423bf1dba8ca85236466be3abd7334b3a8e5956e"},
    {"path": "02_products/crackers/bsip2_outputs/run_ricecakes_conform_001/products/bsip1_ricecakes_7296073161479/bsip2_trace.json", "action": "created", "sha256": "fa8f283928be1ff4d59604b4b008003c9c58572bc6052edfbc2790af579fac76", "note": "representative of the 34-file batch; full list in run_record.json results"}
  ],
  "counts": {
    "brand_null_before": "17/19 null, 2/19 non-null (bari-web/src/data/comparisons/crackers_frontend_v1.json, origin/master, pre-patch); most_common=null(17), min=0/1 max=1/1 per-product has_brand flag",
    "brand_null_after": "0/19 null, 19/19 non-null (bari-web/src/data/comparisons/crackers_frontend_v1.json, post-patch); most_common=has_brand(19), stdev=0 (uniform)",
    "brand_patch_recovered": "21/21 (brand_patch_v1.json); per-product has_brand flag is 1 for all 21, stdev=0, most_common=1(21/21), min=1 max=1",
    "score_grade_diff_vs_origin_master": "0/19 (diff of final_score_estimate, fresh BSIP2 run vs origin/master); distribution of the 19 per-product deltas: min=0.0 max=0.0 median=0.0 stdev=0.0 most_common=0.0(19/19) -- confirms brand-only, no scoring drift",
    "bread_token_collision_check": "0/25 (03_operations/bsip1/run_bread_conform_002/output/bsip1_*.json canonical_name_he scanned against the 7 new tokens); most_common=no_match(25/25), stdev=0",
    "ricecakes_candidates_found": "36/36 acquired of 36 discovered (02_products/crackers/bsip0_ricecakes/ricecakes_bsip0_raw_20260705T055211.json); fat_g/100g distribution across the 35 with a parsed value: min=1.6 max=15.9 median=3.4 stdev=3.83 most_common=3.4g(8/35)",
    "ricecakes_nutrition_coverage": "35/36 (same file); missing=1 (barcode 7296058000519, total blackout candidate)",
    "ricecakes_ingredients_coverage": "34/36 (same file); missing=2 (7296058000519 total blackout + 1 additional short/empty parse)",
    "ricecakes_brand_coverage": "36/36 (same file, ld+json brand field); per-product has_brand flag stdev=0, most_common=1(36/36), min=1 max=1",
    "ricecakes_rule5_boundary_flags": "0/36 flagged, 36/36 clear (fat_g<2 AND ingredient_count<=2, computed from same file); per-product flag stdev=0, most_common=0(36/36), min=0 max=0",
    "ricecakes_off_violations": "0/36 (same file, off_source_used field); stdev=0, most_common=False(36/36)",
    "ricecakes_missing_data_discards": "2/36 (7296058000519 total blackout, 7296058000526 partial blackout; both confirmed by a targeted one-shot live re-scrape, corpus_filter.json)",
    "ricecakes_bsip1_written": "34/34 (03_operations/bsip1/run_ricecakes_conform_001/run_record.json records_written; 36 candidates minus 2 discards)",
    "ricecakes_bsip1_rule5_flags_post_bleed_clean": "0/34 (same run_record.json rule5_flags, computed from BLEED-CLEANED ingredient text per Nutrition Agent's correction, not the raw pre-parse text used in the draft)",
    "ricecakes_bsip1_brand_coverage": "34/34 (same run_record.json brand_hits)",
    "ricecakes_bsip2_scored": "34/34 (02_products/crackers/bsip2_outputs/run_ricecakes_conform_001/run_record.json scored_count)",
    "ricecakes_router_mismatches": "0/34 (same run_record.json router_mismatches; all confirmed category=cracker)",
    "ricecakes_score_distribution": "min=41.2 max=79.5 median=70.1 stdev=9.22 most_common=70(8/34) (derived from run_record.json results, python statistics module)",
    "ricecakes_grade_distribution": "B:27 C:4 D:3 of 34 (same file); no A/S grades in this batch",
    "combined_corpus_size_pending_frontend_regen": "53/53 (19 existing crackers + 34 new ricecakes, both BSIP2-scored; frontend JSON NOT yet regenerated -- see not_done)"
  },
  "commands_run": [
    {"cmd": "python 03_operations/bsip1/run_crackers_conform_001/fetch_brand_patch.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip1/run_crackers_conform_001/build_crackers_bsip1.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/batch_run_crackers_conform_001.py", "exit_code": 0},
    {"cmd": "python 03_operations/page_generator/gates/run_gates.py --config 03_operations/page_generator/configs/crackers.json --baseline <origin_master_copy> bari-web/src/data/comparisons/crackers_frontend_v1.json", "exit_code": 0},
    {"cmd": "python 03_operations/spine/validate_comparison_page.py --json bari-web/src/data/comparisons/crackers_frontend_v1.json --traces 02_products/crackers/bsip2_outputs/run_crackers_conform_001/products", "exit_code": 0},
    {"cmd": "python 03_operations/bsip0/scrape/shufersal_ricecakes/01_scrape_ricecakes.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip1/run_ricecakes_conform_001/build_ricecakes_bsip1.py", "exit_code": 0},
    {"cmd": "python 03_operations/bsip2/proto_v0/src/batch_run_ricecakes_conform_001.py", "exit_code": 0}
  ],
  "not_done": [
    "Frontend JSON regen for the combined 53-product corpus -- deliberately held per Product Agent condition 3 (single content-authoring pass coordinated with TASK-461's queued crackers voice-overhaul slot) and the content sign-off hard rule (no PENDING_COPY may ship). This is an orchestrator sequencing decision, not resolved in this return.",
    "D4 additive wiring for the 34 new products (depends on frontend packaging above)",
    "FAQ schema regen for the expanded corpus (depends on same)",
    "QA gate (G1-G8) + red-team + C3 bracket for the expanded 53-product page (depends on same; the existing 19-product page's gates were re-run and passed, but that was for the brand-only patch, not the expansion)",
    "Adversarial QA reconciliation of the TASK-486 brand-null finding (dispatched to qa-crackers-486-recon, response pending)"
  ],
  "self_check": "Acceptance test = 'null rate drops' for deliverable 1: confirmed 17/19 -> 0/19, verified score/grade byte-identical to origin/master (0/19 diff) so the fix is brand-only -- PASS. Deliverable 2 acceptance test ('expand the shelf, run the standard pipeline through QA gate + frontend JSON') is PARTIAL: BSIP0->BSIP1->BSIP2 complete for 53/53 products with both required approvals (Nutrition GO, Product GO-WITH-CONDITIONS) on record, but frontend regen/QA-gate/red-team stages are correctly held on a real, Product-Agent-identified blocker (copy-authoring sequencing + content sign-off), not skipped or worked around."
}
```
