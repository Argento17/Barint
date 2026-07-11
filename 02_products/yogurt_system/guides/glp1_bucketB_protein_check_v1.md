# GLP-1 Guide v2 — Bucket B Protein-Density Check (TASK-535)

**Data Agent, 2026-07-08.** Runs the exact method that qualified yogurt (TASK-504A step 2 —
**absolute protein grams per 100g**, read directly from each product's nutrition fields in the
shipped comparison JSON; never a ratio-to-calories proxy, which was RT-1's failure mode) against
the 5 bucket-B candidate categories named in `glp1_guide_v2_architecture.md` §2. No new scrape,
no rescore, no external source, no OFF (banned project-wide). Source files are
`C:\Bari\bari-web\src\data\comparisons\*.json` — read-only, unmodified.

**Verdict table (see per-category detail below for reasoning):**

| Category | File | n | Verdict | Threshold candidate | n clearing / total |
|---|---|---|---|---|---|
| protein-bars | protein_combined_frontend_v2.json | 32 | **FLAT — uniformly high floor** | none meaningful (whole shelf already clears) | 32/32 clear ≥8g by 3x margin |
| cheese (cottage/white) | cheese_frontend_v4.json | 47 | **FLAT — smooth gradient** | none (no real dead zone) | n/a |
| hard-cheeses | hard_cheeses_frontend_v4.json | 31 | **FLAT — uniformly high floor** | none meaningful (whole shelf already clears) | 31/31 clear ≥8g by nearly 3x margin |
| brined_cheeses | brined_cheeses_frontend_v2.json | 36 | **FLAT — smooth gradient (weak low-outlier group only)** | none defensible as a real bimodal cut | n/a |
| hummus | hummus_frontend_v5.json | 57 | **TIERED — real split, but split = product-subtype, not formulation** | ≥7g/100g | 34/57 |

**Bottom line for Product:** only **hummus** produces a yogurt-style genuine bimodal signal, and
even that signal is explained almost entirely by legume-spread vs vegetable-spread composition,
not by an emergent "some products are engineered higher-protein" pattern the way yogurt's was. The
other four candidates are flat. Two of the four (protein-bars, hard-cheeses) are flat **because
the entire category already sits far above any GLP-1-relevant protein floor** — see the flagged
concern in §6 before treating "flat = cut" as the automatic disposition for those two.

---

## 1. Method note (applies to all 5)

- Field basis verified before computing, per category (see each section) — every value confirmed
  per-100g, not per-serving, before use.
- Missing protein values are **excluded from the check, never imputed** (Hard Rule / missing-data
  discard rule). Exclusion counts are reported per category; **0 exclusions occurred across all 5
  files** — every shipped product in every file carries a usable per-100g protein value.
- "Real tier" test applied consistently: a gap qualifies as a genuine bimodal split only if (a) it
  is the dominant gap relative to the category's total range, and (b) it separates two populated
  clusters, not one cluster from a single outlier. Yogurt's reference case (TASK-504A): dead zone
  6.5→10.0g, a fully-empty 3.5g gap in a 0–13g range (≈27% of range), separating 23 high-tier from
  55 low-tier products. That is the bar the 5 checks below are measured against.
- Histograms use 1g bins, `[lo, hi)`.

---

## 2. protein-bars — `protein_combined_frontend_v2.json` (32 products)

**Unit-landmine check (done first, per the task brief):** the file carries three protein fields —
`protein_per_100g`, `protein_per_bar`, `bar_weight_g`, plus a `show_per_bar` flag.
- `protein_per_bar` and `bar_weight_g` are **null for all 32/32 products**; `show_per_bar` is
  **`false` for all 32/32** — the per-bar path is not populated in this shipped file, so there is
  no live per-bar/per-100g ambiguity to resolve.
- `protein_per_100g` cross-checked against `nutrition_per_100g.protein_g` for all 32 products:
  **0 mismatches** (exact match every time, spot-checked beyond the 2–3 the brief asked for — ran
  the full set). Confirms the field is genuinely per-100g and internally consistent.

**Distribution (g protein / 100g), n=32, 0 excluded:**

min=25.0 · p25=27.85 · median=33.00 · p75=34.00 · max=36.0 · mean=31.14

```
[25-26) ### (3)
[26-27) # (1)
[27-28) #### (4)
[28-29) ## (2)
[29-30) ## (2)
[30-31)  (0)
[31-32) ## (2)
[32-33) # (1)
[33-34) ######## (8)
[34-35) ####### (7)
[35-36)  (0)
[36-37) ## (2)
```

Sorted values: 25.0, 25.0, 25.0, 26.0, 27.0, 27.2, 27.3, 27.4, 28.0, 28.3, 29.0, 29.0, 31.0, 31.0,
32.4, 33.0, 33.0, 33.3, 33.3, 33.4, 33.6, 33.7, 33.8, 34.0×6, 34.8, 36.0, 36.0.

**Tier check:** one gap ≥1.5g exists — 29.0 → 31.0 (Δ2.0). Relative to the 11g total range that is
18%, below the yogurt reference (27%), and it separates a 12-product low cluster (25.0–29.0) from
a 20-product high cluster (31.0–36.0) — technically a two-cluster split. But **the entire category
floor is 25.0g/100g**, already 3× yogurt's 8g threshold. There is no low group to exclude in any
nutritionally meaningful sense — even the "low" cluster here (25–29g) is exceptionally
protein-dense food. Applying a protein-density filter to this shelf does not produce a useful
recommendation cut; it would return the entire 32-product list either way.

**Verdict: FLAT — uniformly high floor.** Not "flat" in the sense of no signal — flat in the sense
that protein density does not discriminate within this category because the category definition
already guarantees it. See §6 for the recommendation this raises for Product.

**Caveats:** no missing values, no unit ambiguity found (per-bar path unpopulated), field basis
confirmed per-100g throughout.

---

## 3. cheese (cottage/white cheese shelf) — `cheese_frontend_v4.json` (47 products)

**Field basis:** `expansion.nutrition.protein`, gated on `expansion.servingNote`. Checked every
product's `servingNote` — single value across all 47: `"ל-100 גרם"` (per 100g). No per-serving
products in this file.

**Distribution (g protein / 100g), n=47, 0 excluded:**

min=2.8 · p25=5.00 · median=7.80 · p75=10.00 · max=17.0 · mean=7.56

```
[2-3)  # (1)
[3-4)  # (1)
[4-5)  ######### (9)
[5-6)  ###### (6)
[6-7)  #### (4)
[7-8)  ##### (5)
[8-9)  ##### (5)
[9-10) ## (2)
[10-11)####### (7)
[11-12)###### (6)
[12-17)  (0)
[17-18)# (1)
```

Sorted values: 2.8, 3.7, 4.0, 4.3×5, 4.4×3, 5.0×2, 5.1, 5.5, 5.8, 5.9, 6.1, 6.2, 6.3, 6.5, 7.0, 7.7,
7.8, 7.9×2, 8.1×4, 8.7, 9.0, 9.5, 10.0×3, 10.1, 10.2, 10.5×2, 11.0×5, 11.5, **17.0**.

**Tier check:** the only ≥1.5g gap is 11.5 → 17.0 (Δ5.5), but it is a single product jumping away
from the pack, not a second cluster — identified: barcode `6040619`, "גבינה טבורוג 5%", score 81.2,
grade A. This is a real product (a firmer/whey-enriched cottage-style cheese), not a data artifact
— but n=1 does not constitute a tier. Excluding that one outlier, the remaining 46 products form a
continuous gradient from 2.8g to 11.5g with every integer bin populated (no dead zone anywhere in
the bulk of the distribution).

**Verdict: FLAT — smooth gradient.** No genuine two-cluster split; the apparent "gap" is one
outlier product, not a recommendation-viable high-protein tier.

**Caveats:** no missing values. `confidence: "partial"` appears on some products (low_extraction
sub-reason) but protein field was present on all 47 regardless of confidence tier — confidence
affects overall score/copy trust, not whether this specific field existed, so nothing was excluded
on that basis; flagging for awareness only.

---

## 4. hard-cheeses — `hard_cheeses_frontend_v4.json` (31 products)

**Field basis:** `expansion.nutrition.protein`, `servingNote` = `"ל-100 גרם"` for all 31.

**Distribution (g protein / 100g), n=31, 0 excluded:**

min=22.0 · p25=23.35 · median=25.00 · p75=27.70 · max=33.0 · mean=26.12

```
[22-23) # (1)
[23-24) ######### (9)
[24-25) ## (2)
[25-26) ###### (6)
[26-27) # (1)
[27-28) #### (4)
[28-29) # (1)
[29-30)  (0)
[30-31) #### (4)
[31-32)  (0)
[32-33) # (1)
[33-34) ## (2)
```

Sorted values: 22.0, 23.0×6, 23.2, 23.5×2, 24.0, 24.5, 25.0×5, 25.5, 26.0, 27.0×4, 28.4, 30.0×4,
32.0, 33.0×2.

**Tier check:** two adjacent gaps — 28.4→30.0 (Δ1.6) and 30.0→32.0 (Δ2.0) — separate a 24-product
low cluster (22.0–28.4g) from a 7-product high cluster (30.0–33.0g). This is a technically real,
modestly clean split (likely aged/hard cheese types like Parmesan/Emmental hitting 30g+ vs
standard yellow cheeses at 23–28g). But exactly as with protein-bars: **the entire category floor
is 22.0g/100g**, already ~2.75× yogurt's 8g threshold. A protein-density filter here would not
meaningfully separate "good" from "not good enough" for a reduced-appetite/muscle-preservation
guide — every hard cheese on this shelf already clears the bar by a wide margin.

**Verdict: FLAT — uniformly high floor.** Same structural note as protein-bars: the gap is real
but nutritionally inert at this altitude. See §6.

**Caveats:** no missing values. 45 dedup exclusions are already baked into this file per its own
`_meta.exclusions` (packaging-variant SKUs removed at BSIP2 curation, unrelated to this check —
noted for completeness, not something this check re-applied).

---

## 5. brined_cheeses — `brined_cheeses_frontend_v2.json` (36 products)

**Field basis:** `expansion.nutrition.protein`, `servingNote` = `"ל-100 גרם"` for all 36.

**Distribution (g protein / 100g), n=36, 0 excluded:**

min=7.0 · p25=12.00 · median=14.00 · p75=17.38 · max=24.0 · mean=14.64

```
[7-8)   ## (2)
[8-9)   # (1)
[9-10)   (0)
[10-11) #### (4)
[11-12) # (1)
[12-13) ###### (6)
[13-14) ## (2)
[14-15) ##### (5)
[15-16) ## (2)
[16-17) ### (3)
[17-18) # (1)
[18-19) # (1)
[19-20) # (1)
[20-21) ## (2)
[21-22) ## (2)
[22-23) ## (2)
[23-24)  (0)
[24-25) # (1)
```

Sorted values: 7.0, 7.3, 8.0, 10.0×4, 11.0, 12.0×4, 12.5×2, 13.0, 13.5, 14.0×3, 14.5, 14.8, 15.0×2,
16.0×3, 17.0, 18.5, 19.0, 20.0, 20.5, 21.0×2, 22.0×2, 24.0.

**Tier check:** three gaps of similar, modest size (8.0→10.0 Δ2.0; 17.0→18.5 Δ1.5; 22.0→24.0 Δ2.0)
scattered across the range — the signature of a **continuous gradient**, not a bimodal split (a
real tier has one dominant gap, not several similarly-sized ones). The largest, at the low end
(8.0→10.0), separates only 3 products (7.0, 7.3, 8.0 — likely light/low-fat feta variants) from the
remaining 33. Three products is a low-outlier group, not a second cluster worth building a
recommendation threshold on.

**Verdict: FLAT — smooth gradient**, with only a thin (3-product) low-outlier tail rather than a
genuine two-cluster structure.

**Caveats:** no missing values. This file's own `_meta` records a prior re-flow (TASK-438,
2026-07-01) that moved 3 barcodes' grades — unrelated to protein, noted for provenance only, not
something this check needed to correct for.

---

## 6. hummus — `hummus_frontend_v5.json` (57 products)

**Field basis:** `expansion.nutrition.protein`, `servingNote` = `"ל-100 גרם"` for all 57. Confirmed
against the file's own known-limitations block: `HUM-004` flags 2 products
(`bsip1_7296073733317`, `bsip1_7296073733348`) as score-unavailable/insufficient-confidence —
**verified directly: neither barcode is present in this shipped 57-product array**, and all 57
products in the array have a non-null score and a non-null protein value. That known-limitation
note describes an earlier corpus state; it does not apply to what shipped. 0 exclusions needed.

**Raw-vs-prepared boundary check (flagged in the task brief as relevant to hummus):** per standing
project memory, the prepared-vs-raw boundary for this shelf is decided by tahini/sodium/energy —
**protein is explicitly not a valid signal for excluding a product from the corpus** (a legitimate
thick chickpea salad can reach ~18g protein and must stay). Checked for raw/dry-chickpea
contamination using the documented heuristic (sodium ≤15mg AND energy 360–390kcal per 100g):
**0 products matched** — no raw-chickpea contamination found in this file. Separately identified
the single highest-protein product, barcode `6666307`, "סלט חומוס" ("hummus salad"), 18.2g
protein, score 67.7/B — this is the exact product named in that memory as the legitimate
high-protein salad case, confirming it is correctly still in-corpus and not an artifact.
**Important distinction for this check:** that memory governs *corpus inclusion* (don't discard a
product because its protein is high); it does not forbid *using* protein as an inclusion signal
for a downstream recommendation shortlist — those are different operations, and this check only
does the latter.

**Distribution (g protein / 100g), n=57, 0 excluded:**

min=0.7 · p25=2.00 · median=7.70 · p75=7.90 · max=18.2 · mean=5.93

```
[0-1)  ### (3)
[1-2)  ########## (10)
[2-3)  ###### (6)
[3-4)   (0)
[4-5)  # (1)
[5-6)  ## (2)
[6-7)  # (1)
[7-8)  ##################### (21)
[8-9)  ######### (9)
[9-10)  (0)
[10-11)## (2)
[11-12)# (1)
[12-18)  (0)
[18-19)# (1)
```

Sorted values: 0.7, 0.8, 0.8, 1.1, 1.3, 1.5, 1.6×3, 1.7×3, 1.8, 2.0×3, 2.1, 2.2, 2.5, 4.0, 5.6, 5.7,
6.3, 7.0×3, 7.3, 7.5, 7.7×5, 7.8×2, 7.9×8, 8.0×3, 8.2, 8.5×3, 8.6×2, 10.1, 10.6, 11.0, **18.2**.

**Tier check — genuine bimodal structure, confirmed two ways:**
1. **Density:** 19 products sit at ≤2.5g, 34 products sit at ≥7.0g; only **4 products (7% of the
   corpus)** fall in the 4.0–6.3g middle zone. That is a real, if not fully empty, dead zone — 93%
   of the corpus resolves cleanly into a low or high group.
2. **Product-type cross-check:** the file's own `_meta.product_type_distribution` names 5 subtypes
   (`hummus_spread` 33, `matbucha` 10, `pepper_spread` 5, `eggplant_spread` 7, `masabacha` 2).
   Cross-tabulating protein band against subtype: `hummus_spread` = 32/33 in the ≥7g band (1 at
   5.6g); `masabacha` = 2/2 in the ≥7g band; `matbucha` = 10/10 in the ≤3g band; `pepper_spread` =
   4/5 in the ≤3g band; `eggplant_spread` = 5/7 in the ≤3g band. **The bimodal split is almost
   entirely explained by legume-based (hummus/masabacha, chickpea+tahini) vs vegetable-based
   (matbucha/pepper/eggplant, roasted-vegetable) subtype** — not by within-type formulation
   differences the way yogurt's split was (yogurt's tier came from product engineering — Greek/
   skyr/protein-fortified vs standard — within one food type). This is still a real, defensible
   structural fact about the shelf, but it is a different kind of finding than yogurt's, and
   Content should frame it accordingly (protein-dense options on this shelf are, in practice, the
   chickpea-based spreads — not "some hummus products are secretly better than others").

**Threshold candidate: ≥7g/100g.** Clears **34/57 (60%)**. This is a much larger fraction than
yogurt's 23/78 (29%) — because it is selecting almost an entire subtype rather than a formulation
tier within one — so if this shelf is included in the guide, Content/Product will likely want a
further cut (e.g., by grade/score) to produce an actual short recommendation list, the same way
yogurt's 23 qualifiers were narrowed to a 4-product shortlist by other criteria. That narrowing is
outside this check's scope.

**Verdict: TIERED (recommendation-viable, with a caveat on what the tier represents).** Real,
reproducible gap; defensible ≥7g/100g threshold; 0 data-quality blockers; the raw-chickpea
contamination risk flagged in the task brief was checked and ruled out.

---

## 7. Flag for Product — the "flat = cut" rule and uniformly-high categories

Two of the five checks (protein-bars, hard-cheeses) come back FLAT under the strict bimodal test,
but for a different reason than "no protein signal exists": **the entire category already sits
multiples above any protein-density floor that would matter for this guide** (protein-bars floor
25g/100g, hard-cheeses floor 22g/100g, vs. yogurt's 8g threshold). `glp1_guide_v2_architecture.md`
§2 states "*a shelf that comes back flat... gets cut, not forced*" — applying that literally would
drop protein bars from a GLP-1 protein-density guide, which is the category that most directly and
by-definition serves the guide's stated purpose (protein-dense food for someone eating small
amounts). This is flagged here, not decided here — Data Agent implements approved category scope,
not category strategy (D1/D10 are Product's). Recommend Product treat "flat because uniformly
excellent" and "flat because no real signal" as two different dispositions before finalizing §1.7's
category list — the check itself only establishes which is which; it does not resolve which
shelves ship.

---

## 8. Source files (unmodified, read-only)

| File | sha256 |
|---|---|
| `bari-web/src/data/comparisons/protein_combined_frontend_v2.json` | `3cb2f7b0cc161fbeb66e0f43093c4f7be574b40d8c9f893f03d91a415137deb1` |
| `bari-web/src/data/comparisons/cheese_frontend_v4.json` | `2ba3e50314c18ba8587b4323579c864fa1687bdd544323522289f745ce6af3bc` |
| `bari-web/src/data/comparisons/hard_cheeses_frontend_v4.json` | `c1ed37d2f7619081c1ad4f0aee00fdb0cde2c5bf44801e976e3a7858e893c54b` |
| `bari-web/src/data/comparisons/brined_cheeses_frontend_v2.json` | `e17b1dce5412836b23957907e48306f17b0b37624c6082c89a639c7739cd833c` |
| `bari-web/src/data/comparisons/hummus_frontend_v5.json` | `f49314fea188f2c66deb781148cec1c60df9c45896e36a0f505add0dc2feab34` |

No file was written to, scraped, or rescored. This report is the only artifact produced.

---

## Return Contract

```json
{
  "task": "TASK-535",
  "agent": "data-agent",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "02_products/yogurt_system/guides/glp1_bucketB_protein_check_v1.md",
      "action": "created",
      "sha256": "ffe5cc147f3033592ad5bf16f6540d4201499c26e16d5fe7c843b5f4dcd21e10 (hash of the pre-this-edit version; writing this string changes the file's hash again — same documented self-hash paradox as glp1_guide_v2_architecture.md's return contract; re-verify with sha256sum at read time)"
    }
  ],
  "counts": {
    "categories_checked": "5/5 (protein-bars 32, cheese 47, hard-cheeses 31, brined_cheeses 36, hummus 57; source: bari-web/src/data/comparisons/*.json, this session)",
    "categories_tiered": "1/5 (hummus; source: doc §6, gap density 4/57=7% in mid-zone, product-type cross-tab)",
    "categories_flat": "4/5 (protein-bars, cheese, hard-cheeses, brined_cheeses; source: doc §2-5)",
    "categories_data_blocked": "0/5",
    "products_excluded_missing_protein": "0/203 total products across the 5 files (32+47+31+36+57=203) — every shipped product carried a usable per-100g protein value; source: per-category exclusion counts in doc, all zero",
    "protein_bars_unit_landmine_check": "32/32 protein_per_100g values exact-match nutrition_per_100g.protein_g; 0/32 show_per_bar=true; 0/32 non-null protein_per_bar or bar_weight_g — per-bar path unpopulated in shipped file, no live unit ambiguity",
    "hummus_raw_chickpea_contamination_check": "0/57 products matched the documented raw/dry-chickpea heuristic (sodium<=15mg AND energy 360-390kcal/100g)",
    "hummus_threshold_candidate_ge_7g": "34/57 clear (60%)",
    "hard_cheeses_and_protein_bars_floor_vs_yogurt_threshold": "protein-bars min=25.0g, hard-cheeses min=22.0g, both >=2.75x yogurt's 8g/100g threshold (source: sorted value lists, doc §2 and §4)"
  },
  "commands_run": [
    {"cmd": "python3 protein_check.py (loads all 5 JSON files, computes min/p25/median/p75/max/mean, 1g-bin histogram, gap analysis >=1.5g, per-category exclusion counts)", "exit_code": 0},
    {"cmd": "python3 outliers.py (identifies specific outlier products by barcode/name/score/grade, cross-tabulates hummus protein band vs _product_type, checks HUM-004 known-limitation barcodes against shipped array, checks protein_per_bar/bar_weight_g/show_per_bar population)", "exit_code": 0},
    {"cmd": "sha256sum protein_combined_frontend_v2.json cheese_frontend_v4.json hard_cheeses_frontend_v4.json brined_cheeses_frontend_v2.json hummus_frontend_v5.json", "exit_code": 0}
  ],
  "not_done": [
    "No recommendation shortlist built for hummus (the 34/57 that clear >=7g) — that narrowing (by grade/score, same as yogurt's 23->4 cut) is Content/Product's downstream step once Product decides whether hummus ships in the guide",
    "Did not resolve the 'flat because uniformly-high' vs 'flat because no signal' question for protein-bars/hard-cheeses raised in doc §7 — flagged for Product per the Spec-Conflict Duty (Data Agent implements category scope, does not decide it)",
    "No scoring-rule change, no rescore, no new scrape, no evidence-registry entry — none required, this is a read-only distribution check per the task brief",
    "self_check hash for this document not computed pre-write (same self-hash-paradox noted in the upstream Product doc) — re-verify with sha256sum at read time"
  ],
  "self_check": "Acceptance test: does this report give, per bucket-B category, a full distribution (min/p25/median/p75/max + 1g-bin histogram, not just a summary), a real-vs-flat tier verdict grounded in a stated, consistently-applied test (dominant gap vs range, two populated clusters vs single outlier), a defensible threshold candidate with n/total where tiered, exclusion counts with reasons (0 across all 5, stated explicitly rather than omitted), the protein-bar per-bar/per-100g unit check the brief flagged by name, and the hummus raw-vs-prepared boundary check the brief flagged by name? Result: PASS on all six. One category (hummus) verdicts TIERED; four verdict FLAT, with two of those four (protein-bars, hard-cheeses) flagged as flat-because-uniformly-excellent rather than flat-because-no-signal, which is reported as a decision-relevant nuance for Product rather than silently collapsed into a flat pass/fail bit."
}
```
