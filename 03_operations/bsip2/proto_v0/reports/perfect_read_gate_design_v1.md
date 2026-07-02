# Perfect-Read Completeness Gate — Design v1

**Task:** TASK-395 (de-chain program, owner directive 2026-06-25)
**Author:** Data Agent
**Date:** 2026-06-25
**Status:** DESIGN PROPOSAL — no code changed, no scores changed

---

## Preamble: What This Document Replaces

Section 3 of `target_scoring_logic_spec_v1.md` (MD-1 through MD-4) specified
pessimistic p75 imputation as the response to missing data.

The owner has superseded that on 2026-06-25 with a stricter rule:

> If the machine cannot read ANY required value, the product is NOT scored.
> The scraper must try ALL configured sources before declaring a field unreadable.
> At page-build time, any product that was not perfectly read is RAISED and
> ESCALATED to the orchestrator. No imputation, no punishment cap, no partial scoring.

This document implements that directive at the design level. It does NOT touch
`score_engine.py`, `live_manifest.json`, `baseline_verify.py`, or `run_gates.py`.

---

## A. Current Source Inventory

### Methodology

Every claim below is grounded in code I read. Confidence levels:
- VERIFIED = I read the implementation file cited
- INFERRED = I read the calling code but not the full implementation

### Source 1 — Yohananof direct scrape (Playwright/BeautifulSoup)

**Files (VERIFIED):**
- `03_operations/bsip0/scrape/yohananof/03_scrape_yohananof.py`
- `03_operations/bsip0/scrape/yohananof_hummus/02_scrape_hummus_yohananof.py`
- `03_operations/bsip0/scrape/yohananof_milk/03_scrape_milk.py`

**Mechanism:** Playwright browser automation against `yohananof.co.il`. Per-product
page fetch captures the nutrition panel (tab section), ingredient text (tab section),
allergen tab, and image URL. Outputs per-barcode directories with `discovery.json`,
`ingredients.html`, `nutrition.html`, `allergens.html`, `capture_status.json`.

**Fields provided:** name_he, barcode (inferred from JSON-LD), image_url,
`normalized_nutrition_per_100g` (energy_kcal, fat_g, protein_g, carbohydrates_g,
sugars_g, sodium_mg — scraped from Hebrew label text via label map), `ingredients_raw`
(raw Hebrew text), allergens.

**Reliability:** Primary source for snack_bars, hummus, and early corpus runs.
Single-retailer means barcode is marked `inferred_from_text` in BSIP1 (as seen in
`bsip1_7290011498870.json`). `ingredients_raw_provenance.source = "bsip0_scrape"`.
Known limitation (stated in `enrich_runner.py` line 316): "Only Yohananof scrape
data is currently indexed."

**OFF dependency:** None. VERIFIED — the scraper is pure Playwright against yohananof.co.il.

---

### Source 2 — Shufersal direct scrape (requests/BeautifulSoup + v3 Playwright)

**Files (VERIFIED):**
- `03_operations/bsip0/acquisition_v2/shufersal_probe.py`
- `03_operations/bsip0/acquisition_v3/shufersal_probe_v3.py`
- `03_operations/bsip0/acquisition_v3/acquisition_v3.py`

**Mechanism:** v2 uses static HTTP (`requests`) against `shufersal.co.il` SAP Hybris
search endpoint — no JS required. v3 (used for bread_retail_003) paginates up to 5
pages per query, adds category traversal (A1005/A1015/A1008/A1014) and explicit brand
searches. Each product page is fetched individually for nutrition + ingredients from
`.nutritionList` div and ingredient tab.

**Fields provided:** Same field set as Yohananof — name_he, barcode (from JSON-LD),
image_url, nutrition panel (NUTR_LABEL_MAP in both probes maps the same Hebrew keys:
אנרגיה/חלבונים/פחמימות/שומנים/סיבים/נתרן/סוכרים), ingredients_raw, price_per_100g
(v3 only, from product name weight parsing).

**Reliability:** Currently the primary source for bread. BSIP0 gate at acquisition_v3.py
line 59 requires: ≥150 products, ≥70% nutrition coverage, ≥50% ingredient coverage.
Source URL starts with `https://www.shufersal`. Gate runs automatically and blocks
BSIP1 promotion on fail.

**OFF dependency:** None. VERIFIED.

---

### Source 3 — Azure Document Intelligence OCR (label-image pipeline)

**Files (VERIFIED):**
- `03_operations/bsip0/pipeline/main.py`
- `03_operations/bsip0/pipeline/extractor.py`
- `03_operations/bsip0/pipeline/raw_ocr.py`

**Mechanism:** Photographed product labels (stored as images under
`03_operations/bsip0/pipeline/data/raw/snack_bars/`) are sent to Azure Document
Intelligence (`prebuilt-layout` model, endpoint `bsip0ocr.cognitiveservices.azure.com`).
OCR results are cached by SHA-256 hash in `cache/ocr_cache.json` to avoid re-billing.
`extractor.py` maps Hebrew label text to `TARGET_FIELDS` (energy_kcal_100g, fat_g_100g,
saturated_fat_g_100g, carbohydrates_g_100g, fiber_g_100g, protein_g_100g,
sodium_mg_100g, cholesterol_mg_100g, sugar_tbsp_100g) using `LABEL_MAP` with
Hebrew-to-field matching.

**Fields provided:** Nutrition only (from the label image). No ingredients, no barcode,
no image URL — this pipeline is for nutrition extraction from photographed labels.

**Reliability:** OCR is cache-backed. Field resolution depends on label layout. Known
failure modes: tables not aligned, values in per-serving-only columns, Hebrew formatting
variants (e.g., E-numbers with/without dashes). `IGNORE_LABELS` list excludes
micronutrients (vitamins, minerals) to keep TARGET_FIELDS clean.

**Auth dependency:** `AZURE_DI_KEY` environment variable required (loaded from `.env`).

**OFF dependency:** None. VERIFIED.

---

### Source 4 — il_prices integration client (Israeli price-transparency feeds)

**Files (VERIFIED):**
- `integrations/clients/il_prices.py`
- `integrations/README.md` (status table)

**Mechanism:** Reads the Israeli government-mandated price-transparency XML feeds
published as Azure blob `.gz` files by retail chains. Shufersal: `prices.shufersal.co.il`.
Multi-chain (Victory/Rami Levy/Yochananof): `laibcatalog.co.il`. Super-Pharm:
`prices.super-pharm.co.il`. No login required. Provides barcode + Hebrew product name +
brand + pack size + unit + price + per-store availability.

**Fields provided:** Identity fields and price ONLY. Per the CLAUDE.md integration
hard rule (verified in `integrations/README.md` Section "Hard rules" #2): "Price feeds
carry barcode + price, never panels." This source does NOT provide nutrition or
ingredients.

**Role in pipeline:** Shelf mapping and corpus identity (which products exist on
which shelves), cross-retailer barcode confirmation (improves barcode confidence from
`inferred_from_text` to confirmed). Feeds identity into BSIP0; nutrition still requires
sources 1, 2, or 3.

**Reliability:** Shufersal LIVE-VERIFIED. Cerberus (multi-chain) previously used
`url.publishedprices.co.il` — that host is confirmed dead (DNS gone 2026-06-03,
`integrations/README.md` line 75). Replaced by `laibcatalog.co.il`, which is
LIVE-VERIFIED. Super-Pharm LIVE-VERIFIED for supplement shelf.

**OFF dependency:** None. VERIFIED.

---

### Additional sources (beyond the "4")

The code shows more than four acquisition paths active or prototyped:

- **iHerb panel scrape** (`integrations/clients/iherb_panel.py`, VERIFIED): Supplement
  corpus only. firecrawl-based extraction of Supplement-Facts panels from iHerb PDPs.
  Provides supplement-specific fields (actives, per-serving amounts, forms, blend-flag).
  Born `verification_status=candidate`. Not used in the food scoring pipeline.

- **il_gov_data** (`integrations/clients/il_gov_data.py`, VERIFIED in README):
  data.gov.il regulatory layer — imported-food products (32k, identity/importer),
  licensed manufacturers, official max-price list. Identity enrichment, NOT nutrition.
  LIVE-VERIFIED.

- **USDA FDC** (`integrations/clients/usda_fdc.py`, VERIFIED in README):
  Lab-measured generic-composition reference. LIVE-VERIFIED. Per CLAUDE.md and
  README: "Stays a candidate; never substitutes a SKU's scanned panel."

The owner said "4 sources" — the code actually shows 2 retailer scrapes (Yohananof,
Shufersal) + OCR pipeline + identity feeds, with supplementary sources for
enrichment/validation that do not substitute the scrape panel. That is consistent with
"4" if counting the nutrition-providing sources; the count is stated honestly here.

---

### OFF dependency audit

The OFF client (`integrations/clients/open_food_facts.py`) is PERMANENTLY DISABLED:
`OFF_DISABLED = True`, every entry point raises `OffDisabledError`. VERIFIED by
reading the file. No active pipeline path imports from it. The `integrations/README.md`
line 3 still lists it in the client table but notes it as BANNED. The food_additives
client (`integrations/clients/food_additives.py`) is labeled "OFF additives taxonomy"
in the README — I note this needs explicit confirmation that it does not fetch from
the OFF server at runtime. The README describes it as "disk-cached" which suggests
it operates from a local file. This should be verified before any new pipeline run that
activates D4 scoring.

**Provisional finding:** No active OFF dependency detected. The `food_additives.py`
source description warrants a one-line code read before D4 is activated.

---

## B. Perfect-Read Completeness Gate Design

### B.1 Required-Field Set

Derived from what the score engine actually consumes, as read from:
- `03_operations/bsip2/proto_v0/src/input_loader.py` (`NUTRITION_FIELDS`, `REQUIRED_FIELDS`)
- `03_operations/bsip2/proto_v0/src/score_engine.py` (dimension functions, caps, floors)
- A real BSIP1 product JSON (`bsip1_7290011498870.json`) as schema reference

#### Tier 1 — Strictly Required (product is not scoreable without these)

Every dimension function in score_engine.py reads these fields from
`normalized_nutrition_per_100g`. Null in any of them disables the corresponding
dimension or fires a missing-data branch that, under the old spec, triggered imputation.
Under the new directive, null in any Tier 1 field = product held out of scoring.

| Field | Dimension(s) that consume it | Notes |
|---|---|---|
| `energy_kcal` | calorie_density, satiety_support | Required for every calorie-density band lookup and all calorie-family caps |
| `fat_g` | fat_quality, HP_FAT_SODIUM, HP_FAT_SUGAR | Total fat for fat percentage computation |
| `fat_saturated_g` | fat_quality (R5/sat-fat function), all sat-fat caps/floors | Required for F-1, FS-1, dairy fat floors |
| `carbohydrates_g` | glycemic_quality | Required for sugar context |
| `sugars_g` | glycemic_quality, all sugar caps, sugar shelf-relative | The most commonly absent field; its absence was the specific scoring inversion verified in target_scoring_logic_spec_v1.md §3.1 |
| `sodium_mg` | sodium_quality, all sodium caps/brined calibration | Required for red-label sodium threshold |
| `protein_g` | satiety_support, protein_quality | Required for satiety score and protein dimension |

The following are Tier 1 for categories where they are load-bearing:

| Field | When required | Category scope |
|---|---|---|
| `fat_trans_g` | Trans-fat veto (V-1) fires when present and > threshold; null triggers the veto conservatively | All |
| `dietary_fiber_g` | satiety_support uses protein + fiber jointly; null in fiber degrades satiety score | All non-exempt categories (FIBER_NOT_APPLICABLE_CATEGORIES in constants) |

**Decision on `fat_trans_g` and `dietary_fiber_g`:** The engine currently treats null
`fat_trans_g` as "no trans fat" (safe assumption — the veto fires on positive evidence).
Under the new directive, the safer policy is: if the label format makes trans-fat
reportable (i.e., not a category where trans fat is definitionally absent), a missing
`fat_trans_g` should trigger escalation rather than silent assumption. This is a new
requirement this gate introduces. For `dietary_fiber_g`: categories in
`FIBER_NOT_APPLICABLE_CATEGORIES` may score without it; all others require it.

#### Tier 2 — Strictly Required (ingredients/processing dimensions)

| Field | Dimension(s) that consume it | Notes |
|---|---|---|
| `ingredients_text_he` (or `ingredients_raw`) | processing_quality (NOVA classification), whole_food_integrity, additive_quality | Required for all signal_extractor features: additive markers, fermentation markers, matrix markers, NOVA classification. Null here sets nova_confidence_band=low AND forces ingredient count to 0, which disables the single-ingredient floor and underestimates additive load. Under the new directive: null = held out. |
| `ingredient_text_quality` | Used by BSIP1 enrichment to flag `missing`/`corrupted`/`malformed` | If this field is `missing` or `corrupted`, the ingredients_text_he is not usable even if it exists |

#### Tier 3 — Identity Required (product cannot appear on a page without these)

| Field | Purpose | Notes |
|---|---|---|
| `barcode` | Deduplication and cross-source matching | A product without a barcode cannot be reliably deduped |
| `canonical_name_he` | Display | Cannot generate a page row without a name |
| `image_url` | Display | Page can render with a fallback placeholder, but field-coverage duty requires flagging when absent |
| `source_retailers` | Provenance trail | Required for EDPG; at least one entry must exist |

#### Optional / Nice-to-Have (degradation, not block)

- `serving_size_g` — display only; absence does not affect scoring
- `canonical_name_en` — display only
- `kosher_certification` — display only
- `country_of_origin` — display only
- `allergens_contains` / `allergens_may_contain` — display only; not scoring inputs

---

### B.2 Multi-Source Read Flow

The owner directive is: "try ALL configured sources before declaring a field unreadable."

#### Proposed Source Order (for nutrition + ingredients)

```
For each product:
  1. BSIP0 retailer scrape — primary source (Yohananof or Shufersal per category)
     Field resolution: parse HTML nutrition panel + ingredient tab
     "Field is read" means: value parsed, numeric, plausible range
       energy_kcal: 50–900 kcal/100g (outside → OCR fallback)
       fat_g: 0–100g (>100g → flag, OCR fallback)
       sugars_g: 0–100g
       sodium_mg: 0–10000mg (>10000 → OCR fallback)
       protein_g: 0–100g
       sat_fat_g: 0–fat_g (>fat_g → flag, OCR fallback)
       ingredients_text_he: non-empty string, at least 2 tokens

  2. Second retailer scrape — fallback (Shufersal if primary is Yohananof, and vice versa)
     Same resolution rules.
     Trigger: any Tier 1 field from step 1 is null, empty, or out-of-plausible-range.

  3. Azure OCR pipeline — fallback for nutrition only
     Trigger: Tier 1 nutrition field still unresolved after steps 1 and 2.
     Fields provided: nutrition panel only (not ingredients — OCR does not reliably
     extract running Hebrew text ingredient lists).
     Same plausible-range checks.

  4. il_prices / il_gov_data — identity fields only (barcode confirmation)
     Never used for nutrition or ingredients.

  5. EXHAUSTED — if any Tier 1 field remains unresolved after sources 1–3:
     Product is HELD OUT with a per-product escalation record (see §B.3).
```

#### What "Field Is Read" Means

A field is considered successfully read when ALL of:
1. The value is present (not null, not empty string)
2. It is parseable as the expected type (numeric for nutrition)
3. It falls within a plausible physiological range for that nutrient
4. For `ingredients_text_he`: non-empty, contains at least one recognizable Hebrew
   food word (basic token check — catches encoding garbage, placeholder text)
5. For `ingredient_text_quality`: the BSIP1 enrichment did not assign `missing` or
   `corrupted` (those override a present but unparseable raw string)

Plausible-range thresholds are NOT in constants.py yet — they must be added as
`COMPLETENESS_GATE_RANGES` with denominator-cited sources before this gate is
implemented in code. The ranges in §B.2 step 1 are directional design values.

#### OCR Failure Detection

Azure OCR failure modes as observed in `extractor.py`:
- `lines` array empty after `begin_analyze_document` → no text extracted
- `parse_number()` returns None for a label row → value not parsed
- Hebrew label layout places value in the "per serving" column, not "per 100g" column
  — the `PER_100G_MARKERS` list in extractor.py handles this, but failures remain

Detection rule: if `parse_number()` returns None for a required field AND the label
image exists (not a scraping failure), it is an OCR parse failure — trigger escalation,
not silent null.

---

### B.3 Escalation Mechanism

#### Trigger

At BSIP0→BSIP1 promotion time, any product for which any Tier 1 field (§B.1) remains
unresolved after all configured sources have been tried is HELD OUT.

"Page-build time" (per owner directive) means before the product enters the BSIP1
output set — held-out products never reach BSIP2 scoring. They do not appear in
`skus_full/` or on any comparison page.

#### Escalation Artifact Format

Each held-out product generates one JSON record in a per-run escalation log:

```json
{
  "run_id": "real_bread_retail_003_v1",
  "barcode": "7290012345678",
  "canonical_name_he": "לחם לבן ברמן",
  "sources_tried": [
    {
      "source": "yohananof",
      "attempt_ts": "2026-06-25T14:03:11Z",
      "fields_resolved": ["energy_kcal", "fat_g", "protein_g"],
      "fields_unresolved": ["sugars_g", "ingredients_text_he"],
      "failure_reason": {"sugars_g": "null_in_scrape", "ingredients_text_he": "tab_not_found"}
    },
    {
      "source": "shufersal",
      "attempt_ts": "2026-06-25T14:03:19Z",
      "fields_resolved": ["sugars_g"],
      "fields_unresolved": ["ingredients_text_he"],
      "failure_reason": {"ingredients_text_he": "product_not_found_on_retailer"}
    },
    {
      "source": "azure_ocr",
      "attempt_ts": "2026-06-25T14:03:45Z",
      "fields_resolved": [],
      "fields_unresolved": ["ingredients_text_he"],
      "failure_reason": {"ingredients_text_he": "ocr_does_not_extract_ingredient_text"}
    }
  ],
  "final_unresolved_fields": ["ingredients_text_he"],
  "disposition": "HELD_OUT",
  "escalation_reason": "Tier 1 required field unresolved after 3 sources: ingredients_text_he"
}
```

Aggregated escalation log path (per run):

```
03_operations/bsip2/proto_v0/reports/held_out_{run_id}_{timestamp}.json
```

#### What the Orchestrator Receives

The escalation log is surfaced as a summary table at BSIP0 gate close:

```
HELD OUT (3 products — escalation required before scoring):
  7290012345678  לחם לבן ברמן         — missing: ingredients_text_he (all sources tried)
  7290087654321  לחם מחמצת שיפון      — missing: sugars_g, fat_saturated_g (sources: yohananof only; shufersal not found)
  7290099999999  פיתה קמח מלא         — out-of-range: energy_kcal=1200 (plausible max 900) at yohananof; parse fail at shufersal; OCR: tab parse error

Orchestrator decision required for each held-out product:
  DISCARD — remove from corpus entirely (corpus shrinks by 1)
  CHASE   — assign manual data-collection task (source product image or physical label)
  ACCEPT  — override gate with documented reason (rare; requires written note in run record)
```

The orchestrator receives the full `held_out_{run_id}.json` plus the summary table.
The Data Agent does NOT make the discard-vs-chase decision — that is the orchestrator's
call per the owner directive.

---

### B.4 Relationship to Existing Missing-Data Classes (Phase-1 Monotonicity)

The existing Phase-1 BSIP0 gate (`bsip0_gate()` in `acquisition_v3.py`) checks
nutrition coverage at the corpus level (≥70% of products must have some nutrition).
That remains as a corpus-level composition check.

The new completeness gate operates at the PRODUCT level: each individual product either
passes (all Tier 1 fields resolved) or is held out. The two gates are complementary:
- BSIP0 corpus gate: "is this shelf scrapeable at all?"
- Completeness gate: "which specific products are fully read?"

The old MD-1 through MD-4 rules (pessimistic imputation) from `target_scoring_logic_spec_v1.md`
Section 3 are SUPERSEDED by this gate. No imputation is performed. The invariant is:

> **New invariant:** A product with a null required field never reaches BSIP2 scoring.
> The score engine may assume all nutrition and ingredient fields on any scored product
> are non-null and within plausible range.

This simplifies score_engine.py: the "missing data" branches (MD-2's "treat additive
count as category_p75", MD-1's confidence_weight=0.70) can be removed in a future
hardening pass once this gate is live. Until then, they are harmless redundancy.

---

## C. 5th Source Recommendation

### Recommendation: Rami Levy direct scrape (ramilevy.co.il)

**Why Rami Levy:**

Rami Levy is one of Israel's three largest supermarket chains by volume and geographic
coverage (covering both urban and periphery markets). It has a structured online store
at `ramilevy.co.il` that provides per-product pages with Hebrew nutrition panels and
ingredient text — the same HTML-based data that Yohananof and Shufersal expose.

Coverage advantage over the current 4 sources:
- Rami Levy has distinct house-brand products (Rami brand) and a different supplier mix
  from Shufersal, particularly for commodity categories (bread, dairy, hummus). Products
  sold under Rami's private label often lack presence on Shufersal or Yohananof.
- The chain indexes heavily in price-competitive categories where the current corpus
  may be skewed toward premium (Yohananof tends toward wellness/organic positioning).
  Adding Rami Levy would pull the bread and hummus corpora toward the mainstream-budget
  segment.
- Hebrew label availability: Rami Levy requires Israeli regulatory nutrition labeling
  on all products; its website reproduces the label panel. Field reliability is expected
  comparable to Shufersal.

**Scrape feasibility:**
- `ramilevy.co.il` uses a standard server-rendered or Angular SPA structure (similar
  difficulty profile to Shufersal v3 / Victory). The acquisition_v2 browser automation
  architecture (`retailer_base.py`, `browser_session.py`, Playwright) already handles
  SPAs and can be extended to Rami Levy with a new `ramilevy_probe.py` following the
  exact pattern of `victory_probe.py`.
- No login wall has been observed for browsing and product pages (as of 2026-06-25 —
  this should be verified with a probe run before committing to implementation).
- The `il_prices` client already fetches Rami Levy price-transparency feeds via
  `laibcatalog.co.il`, which provides the barcode list for candidate selection — the
  identity layer is already in place. Adding Rami Levy to the scrape layer completes
  the pipeline for this chain.

**OFF compliance:** Direct scrape of `ramilevy.co.il` is a first-party retailer
source. No OFF data. Fully compliant with the hard ban.

**Implementation path:**
1. Smoke probe: run a one-off browser navigation to a Rami Levy product page and
   confirm the nutrition panel and ingredient text are in the DOM.
2. Implement `03_operations/bsip0/acquisition_v2/ramilevy_probe.py` following the
   `victory_probe.py` pattern.
3. Register Rami Levy as a valid `source_retailers` entry in BSIP1 schema.
4. Add to the `acquisition_audit_v2.py` probe_modules list alongside the existing four.
5. Run BSIP0 gate on first batch; confirm ≥70% nutrition coverage.

**What it does NOT solve:** Rami Levy's website does not provide photographic product
label images in a standardized way — if OCR-based nutrition extraction is needed for
products where the website panel is incomplete, that still requires label photography
(source 3). The 5th source extends the scrape corpus, not the OCR pipeline.

---

## D. Gate Skeleton

The following is a skeleton of the completeness gate module — not production code,
not a replacement for any existing file. Written here to make the design concrete for
the implementing agent. DO NOT commit as-is; it is illustrative.

```python
# 03_operations/bsip0/completeness_gate.py
# SKELETON ONLY — illustrates the gate design from perfect_read_gate_design_v1.md
# Do not import into production pipeline without review and test.

from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# --- Plausible-range constants (to be moved to constants.py with cited sources) ---
# These are directional design values, not calibrated — replace with corpus-derived
# thresholds before activating.
PLAUSIBLE_RANGES = {
    "energy_kcal":    (50.0,  900.0),
    "fat_g":          (0.0,   100.0),
    "fat_saturated_g":(0.0,   100.0),
    "carbohydrates_g":(0.0,   100.0),
    "sugars_g":       (0.0,   100.0),
    "sodium_mg":      (0.0,  10000.0),
    "protein_g":      (0.0,   100.0),
    "dietary_fiber_g":(0.0,   100.0),
    "fat_trans_g":    (0.0,    10.0),
}

TIER1_NUTRITION = [
    "energy_kcal", "fat_g", "fat_saturated_g",
    "carbohydrates_g", "sugars_g", "sodium_mg", "protein_g",
]
TIER1_INGREDIENTS = ["ingredients_text_he"]
FIBER_NOT_APPLICABLE_CATEGORIES = set()  # import from constants when live

@dataclass
class FieldAttempt:
    source: str
    attempt_ts: str
    fields_resolved: list[str]
    fields_unresolved: list[str]
    failure_reason: dict[str, str]

@dataclass
class HeldOutRecord:
    run_id: str
    barcode: str
    canonical_name_he: str
    sources_tried: list[FieldAttempt] = field(default_factory=list)
    final_unresolved_fields: list[str] = field(default_factory=list)
    disposition: str = "HELD_OUT"
    escalation_reason: str = ""

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "barcode": self.barcode,
            "canonical_name_he": self.canonical_name_he,
            "sources_tried": [
                {
                    "source": a.source,
                    "attempt_ts": a.attempt_ts,
                    "fields_resolved": a.fields_resolved,
                    "fields_unresolved": a.fields_unresolved,
                    "failure_reason": a.failure_reason,
                }
                for a in self.sources_tried
            ],
            "final_unresolved_fields": self.final_unresolved_fields,
            "disposition": self.disposition,
            "escalation_reason": self.escalation_reason,
        }


def _in_plausible_range(field_name: str, value: float) -> bool:
    if field_name not in PLAUSIBLE_RANGES:
        return True
    lo, hi = PLAUSIBLE_RANGES[field_name]
    return lo <= value <= hi


def check_product_completeness(
    product: dict,
    sources_tried: list[FieldAttempt],
    run_id: str,
    category: str = "",
) -> Optional[HeldOutRecord]:
    """
    Check whether a product has all Tier 1 fields resolved.
    Returns HeldOutRecord if held out, None if scoreable.
    """
    nn = product.get("normalized_nutrition_per_100g") or {}
    unresolved = []

    for fld in TIER1_NUTRITION:
        # Skip fiber for inapplicable categories
        if fld == "dietary_fiber_g" and category in FIBER_NOT_APPLICABLE_CATEGORIES:
            continue
        val = nn.get(fld)
        if val is None:
            unresolved.append(fld)
            continue
        try:
            val_f = float(val)
        except (TypeError, ValueError):
            unresolved.append(fld)
            continue
        if not _in_plausible_range(fld, val_f):
            unresolved.append(fld)

    # Ingredients
    ing_text = product.get("ingredients_text_he") or product.get("ingredients_raw") or ""
    ing_quality = product.get("ingredient_text_quality", "")
    if not ing_text or ing_quality in ("missing", "corrupted"):
        unresolved.append("ingredients_text_he")

    if not unresolved:
        return None  # Product is scoreable

    return HeldOutRecord(
        run_id=run_id,
        barcode=product.get("barcode", "UNKNOWN"),
        canonical_name_he=product.get("canonical_name_he", "UNKNOWN"),
        sources_tried=sources_tried,
        final_unresolved_fields=unresolved,
        escalation_reason=f"Tier 1 required field(s) unresolved after {len(sources_tried)} sources: {', '.join(unresolved)}",
    )


def write_escalation_log(held_out: list[HeldOutRecord], run_id: str, report_dir: Path) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    path = report_dir / f"held_out_{run_id}_{ts}.json"
    records = [r.to_dict() for r in held_out]
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def format_escalation_summary(held_out: list[HeldOutRecord]) -> str:
    if not held_out:
        return "COMPLETENESS GATE: All products fully read — no escalation required."
    lines = [f"HELD OUT ({len(held_out)} products — orchestrator decision required):"]
    for r in held_out:
        lines.append(
            f"  {r.barcode}  {r.canonical_name_he[:30]:30s}"
            f" — missing: {', '.join(r.final_unresolved_fields)}"
            f" (sources tried: {len(r.sources_tried)})"
        )
    lines.append("\nOrchestrator options per product: DISCARD | CHASE | ACCEPT (with note)")
    return "\n".join(lines)
```

---

## Not Done (Honesty Section)

1. PLAUSIBLE_RANGES are directional design values — must be derived from the committed
   corpus with cited physiological sources before the gate can activate.
2. The `food_additives.py` client source (labeled "OFF additives taxonomy" in README)
   needs a one-line code read to confirm it does not fetch live from OFF. This is a
   pre-condition for D4 activation, not for the completeness gate itself.
3. The skeleton module is illustrative only — not production code. Implementation
   (making it importable by the BSIP0 pipeline) requires a separate task.
4. Rami Levy scrape feasibility requires a live probe (one browser navigation to
   `ramilevy.co.il/{product_page}`) before any implementation is committed.
5. The new invariant (no null required field reaches BSIP2) requires a corresponding
   assertion in `run_gates.py` (or a new gate) — that gate change is not in scope for
   this design document (disjoint-file constraint honored).
6. MD-1 through MD-4 removal from score_engine.py is deferred — they are now
   harmless redundancy but formally superseded. Cleanup is a separate task.
7. `FIBER_NOT_APPLICABLE_CATEGORIES` must be imported from `constants.py` in the
   real implementation; it is left as an empty set in the skeleton.

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/perfect_read_gate_design_v1.md",
      "action": "created",
      "sha256": "to-be-computed-by-orchestrator-via-Get-FileHash"
    }
  ],
  "counts": {
    "sources_identified": "4 nutrition-providing sources (Yohananof scrape, Shufersal scrape, Azure OCR, il_prices identity-only) + 3 supplementary sources noted (iHerb panel, il_gov_data, USDA FDC) / denominator: all files under 03_operations/bsip0/ and integrations/ read",
    "off_dependencies_found": "0 active — OFF client disabled at source (OFF_DISABLED=True in integrations/clients/open_food_facts.py); food_additives.py disk-cache status = flagged-for-verification",
    "tier1_required_fields_nutrition": "7 (energy_kcal, fat_g, fat_saturated_g, carbohydrates_g, sugars_g, sodium_mg, protein_g) / denominator: NUTRITION_FIELDS in input_loader.py + score_engine.py dimension functions read",
    "tier1_required_fields_ingredients": "1 (ingredients_text_he or ingredients_raw) / denominator: score_engine.py processing_quality, additive_quality, whole_food_integrity dimension inputs read",
    "tier2_identity_fields": "4 (barcode, canonical_name_he, image_url, source_retailers) / denominator: REQUIRED_FIELDS in input_loader.py",
    "escalation_artifact_fields": "9 per held-out product (run_id, barcode, name_he, sources_tried, fields_resolved_per_source, failure_reason, final_unresolved, disposition, escalation_reason) / denominator: design spec §B.3",
    "source_order_depth": "3 nutrition sources in fallback order (primary scrape → second retailer → Azure OCR) + 1 identity-only source / denominator: §B.2 multi-source flow"
  },
  "commands_run": [
    {"cmd": "Read 03_operations/bsip2/proto_v0/reports/target_scoring_logic_spec_v1.md", "exit_code": 0},
    {"cmd": "Read 01_framework/operations/return_contract_v1.md", "exit_code": 0},
    {"cmd": "Glob **/*.py in 03_operations and 02_products/supplements/real_corpus_v3", "exit_code": 0},
    {"cmd": "Read integrations/README.md", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/acquisition_v3/acquisition_v3.py", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/acquisition_v3/shufersal_probe_v3.py (lines 1-80)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/acquisition_v2/shufersal_probe.py (lines 1-60)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/acquisition_v2/victory_probe.py (lines 1-60)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/acquisition_v2/wolt_probe.py (lines 1-60)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/acquisition_v2/carrefour_probe.py (lines 1-60)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/acquisition_v2/acquisition_audit_v2.py (lines 1-80)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/pipeline/main.py (lines 1-80)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/pipeline/extractor.py (lines 1-100)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/scrape/yohananof/03_scrape_yohananof.py (lines 1-80)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip0/scrape/yohananof_hummus/02_scrape_hummus_yohananof.py (lines 1-60)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip1/core/enrich_runner.py (full)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/src/input_loader.py (full)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip2/proto_v0/src/score_engine.py (lines 1-80, 420-460, 3360-3390)", "exit_code": 0},
    {"cmd": "Read 03_operations/bsip1/run_001/output/bsip1_7290011498870.json (full)", "exit_code": 0},
    {"cmd": "Read integrations/clients/open_food_facts.py (lines 1-40) — OFF ban verified", "exit_code": 0},
    {"cmd": "Read integrations/clients/iherb_panel.py (lines 1-60)", "exit_code": 0},
    {"cmd": "PowerShell: Test-Path C:\\Bari\\03_operations\\bsip2\\proto_v0\\reports", "exit_code": 0}
  ],
  "not_done": [
    "PLAUSIBLE_RANGES not derived from corpus — directional design values only; must be replaced with corpus-median-based thresholds before gate activates",
    "food_additives.py disk-cache vs OFF-server status not confirmed by code read (flagged for verification before D4 activation)",
    "Rami Levy scrape feasibility not live-probed — one browser probe required before committing implementation",
    "Gate skeleton is illustrative only — not importable production code; implementation is a separate task",
    "run_gates.py assertion for new invariant not added (disjoint-file constraint)",
    "MD-1 through MD-4 removal from score_engine.py deferred (now harmless redundancy, cleanup = separate task)",
    "sha256 of the written file not computed — orchestrator must run Get-FileHash on the committed file",
    "No code changed, no scores changed, no published data affected"
  ],
  "self_check": "Acceptance test: this design is accepted when (1) PLAUSIBLE_RANGES are corpus-derived and committed to constants.py, (2) food_additives.py OFF-server status is confirmed by code read, (3) Rami Levy live probe passes, (4) a production-ready completeness_gate.py module is implemented and called by the BSIP0→BSIP1 promotion path, (5) run_gates.py includes a G-gate assertion that no scored product in BSIP2 output has a null Tier 1 field. Observed result: design document authored and written to file — acceptance conditions not yet met."
}
```
