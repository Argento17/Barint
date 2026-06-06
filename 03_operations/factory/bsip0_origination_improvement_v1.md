# BSIP0 Origination Improvement v1 — acquire clean, gate at the door (TASK-183)

**Status:** PROPOSED (evaluation + ranked plan) · **Owner:** data-agent · **Date:** 2026-06-05
**Origin:** TASK-140 breakfast-cereals (run_cereals_002/004, shipped live) · **Blocks:** TASK-184
**Related:** `corpus_purity_gates_v1.md`, `category_factory_v1.md` (Stages 3–6), EV-045/EV-045b

> This is an **evaluation + plan**, not a pipeline rewrite. It changes no published scores and
> no engine code. It specifies upgrades for TASK-184 (and later) to apply. The contaminant +
> energy pre-scan in §4 is specified concretely enough to be lifted into the BSIP0 gate as-is.

---

## 0. Problem in one line

BSIP0 acquires by **Hebrew name-substring queries with no food-class gate** (`01_scrape_cereals.py`
`INCLUDE_SIGNALS`/`EXCLUDE_SIGNALS`). Adjacent products on adjacent shelves — ptitim pasta, bread,
baking flour, chocolate confections, an oat drink — match a cereal token (`פתיתי` ⊂ `פתיתים`) and
enter the corpus. They were only partially caught **downstream** at BSIP1 curation (EV-045/045b),
*after* one (`פתיתים אורגנים כוסמין`) had already been whitelisted to **A and ranked #1** on the
live site. The fix must move the food-class decision **to the door** (Stage 4 acquisition / Stage 5
gate), so the wrong food never enters the set being compared.

Two distinct failure modes, both rooted in origination:
1. **Wrong food, right token** — pasta/bread/flour/confection/drink that share a grain word.
2. **Right food, wrong number** — a real cereal whose energy parsed per-serving (110–139 kcal)
   instead of per-100g (~440 kcal), i.e. a unit-plausibility failure, not a contamination.

---

## 1. Grounding — what the scraped corpus actually shows

Source inspected: `C:\Bari\02_products\breakfast_cereals\bsip0_outputs\cereals_bsip0_raw_20260601T152207.json`
(113 raw products; `category_raw` is the Shufersal `data-all-categories` path, a list of shelf codes
per product). Codes correlated against product names below.

### 1a. Shufersal category codes that ANCHOR cereals (the clean spine)

| Code family | Count | Houses (sample) | Verdict |
|---|---|---|---|
| **A2502** (`A250201`, `A250204`, `A250216`) | 59 of 113 | גרנולה / קוואקר / דגני בוקר / קוקו פבלס | **PRIMARY cereal+granola+kids shelf** |
| **A2803 / A2808** (`A280301`, `A280813`) | 19 | גרנולה תמר קשיו / תע.דגנים פירות ואגוז / גרנולה ללת"ס | granola & health-mix sub-shelf (mostly cereal) |
| **A2814** (`A281404`) | ~8 | דגני בוקר קראנצ'י / קואלה קריספ / טבעות תירס | extruded/kids cereal sub-shelf (**also leaks pasta — see 1b**) |
| **F050 / F120 / F130** | 14 / 7 / 4 | organic/health duplicates of the above | secondary "טבעי/אורגני" mirror shelves |

**Anchor recommendation:** **A2502** is the cereal spine. A2803/A2808 (granola/health mixes) and the
cereal members of A2814 are legitimate adjacents. F05/F12/F13 are the organic/natural mirror and
should be *allowed but flagged*, because they also host the organic-ptitim contaminant.

### 1b. Codes that carried the CONTAMINANTS (the off-shelf signal)

| Contaminant class | Dominant code(s) | Count | Note |
|---|---|---|---|
| **Ptitim pasta** (`פתיתים אפויים`) | **A2211 / A221116** | 8 | clean off-shelf signal — pasta shelf, never cereal |
| **Organic ptitim** (the #1/A product) | **F030** (+A500/A501) | 1+ | the "F03" code flagged in the task; off the F05 cereal mirror |
| **Bread / pita / rolls / sourdough** | **A100x / A101x** (`A100501`,`A101401`), A240/A241 | ~9–13 | bakery shelves — never cereal |
| **Pasta** (`פסטה שיבולת שועל`) | A281x / F120 | ~2–4 | shares the A2814 extruded family — code alone is insufficient here; needs the name/energy gate |
| **Flour as product** (`קמח`) | A280 / F030 | 1 | baking-aisle |
| **Chocolate confection / drink** | A400 / F100 / A011 | ~3 | confection & beverage aisles |

**Key finding for anchoring:** A code allow-list (anchor on A2502 + A2803/A2808 + cereal-A2814,
reject A2211/A100x/A101x/A240x) removes **most** contaminants by origin alone. But A2814/F120 are
*mixed* (both real extruded cereal and `פסטה שיבולת שועל`), and the organic ptitim sits on F030 next
to the F05 cereal mirror. **Therefore category-code anchoring is necessary but not sufficient** — it
must be paired with the name-head + ingredient + energy pre-scan (§4) to catch the mixed-shelf cases.

### 1c. Energy-implausibility cases observed (7 of 113)

| energy_kcal (raw) | name | true class |
|---|---|---|
| 29.0 | פסטה שיבולת שועל נודלס / פטוציני | wet pasta (cooked-basis or per-serving) |
| 59.0 | שיבולת שועל וויט | oat **drink** |
| 62.0 | מעדן שיבולת שועל | oat **dessert** |
| 110.0 | דגני בוקר קואלה קריספ | **real cereal, per-serving parse** (~30 g) |
| 120.0 | דגני טבעות תירס ואורז | **real cereal, per-serving parse** |
| 139.0 | כריות נוגט | **real cereal, per-serving parse** |

The < ~150 kcal/100g floor catches **both** the wet contaminants (29–62) **and** the per-serving
parse errors (110–139). The two outcomes differ: a wet product is *excluded*; a per-serving parse is
a *unit-sanity flag for re-parse/review*, not necessarily an exclusion. §4 separates them.

---

## 2. Ranked upgrades (impact × effort)

Scored 1–5 (impact: corpus-purity gain; effort: build cost). Ranked by impact-to-effort, with the
hard-gate (purity) value weighted up because the failure was consumer-facing (pasta at #1/A live).

| # | Upgrade | Impact | Effort | Owner | Verdict |
|---|---|---|---|---|---|
| **1** | **Contaminant + energy pre-scan at the BSIP0 gate** (§4 — reuse EV-045b classifier) | 5 | 2 | **Data (TASK-184)** | **ADOPT NOW** — highest ROI; catches mixed-shelf cases code-anchoring misses; spec is ready |
| **2** | **Category-code anchoring** over name-substring (anchor A2502 + A2803/A2808 + cereal-A2814; reject A2211/A100x/A101x/A240x; flag F03/F05) | 5 | 3 | **Data (TASK-184 / next)** | **ADOPT** — removes most contaminants by origin; record `source_category_codes` per product (already in `category_raw`, just not gated on) |
| **3** | **Ingredient-aware acquisition / early food-class tag** — run EV-045b at Stage 4/5, not only Stage 6; persist `food_class` + `food_class_reason` on the BSIP0 record | 4 | 2 | **Data** | **ADOPT** — turns the gate from a name check into a name-head + first-ingredient-dominance + energy decision; tag travels downstream for QA Gate 1/2 |
| **4** | **Leaderboard-integrity assert in promotion (Gate 2)** — block any `display_approved:false`/suspect product from rank ≥ approved, hard-fail at #1 | 5 | 1 | **Data + QA** | **ADOPT** — cheapest insurance; this is the gate that would have stopped pasta-at-#1. Pattern exists in `split_cereals_005_frontend.py`. (Governance already mandates it; wire the assertion.) |
| **5** | **De-dup + brand-line awareness** — collapse same-barcode across queries/retailers (already done on barcode); add a known pasta/bakery brand-line denylist (Osem/Intaria/השדה ptitim, מאפיית X bread) as a *flag*, not a silent drop | 3 | 2 | **Data** | **ADOPT (flag-only)** — brand denylist as a soft signal feeding the pre-scan reason, never an auto-exclude (avoids the `חומוס גרגרים` false-positive class) |
| **6** | **Multi-retailer sourcing** (add Rami Levy/Victory via `il_prices`, panels via OFF/USDA) | 4 | 4 | **Data (TASK-184 feasibility)** | **DEFER / SCOPE in TASK-184** — widens corpus + enables cross-retailer dedup, but `il_prices` carries identity+price only (never nutrition), Cerberus chains are `NEEDS-ENV-VERIFY`, and EDPG requires every external value start as `candidate` until a BSIP0/QA pass promotes it. Real value, but a program, not a quick fix |

**Recommended adoption set for TASK-184 (cheap, high-impact, reversible):** #1 (pre-scan), #3 (early
food-class tag — the pre-scan *is* the tagger), #4 (leaderboard assert), and #5 flag-only. #2
(code-anchoring) is the structural fix and should land in the same or the immediately following pass
since the codes are already present in `category_raw`. #6 is a feasibility spike, separately scoped.

**Why pre-scan ranks above code-anchoring** even though both score impact 5: the pre-scan is
category-agnostic, ships in hours, and catches the cases code-anchoring *can't* (mixed A2814/F120
shelves, the per-serving parse errors). Code-anchoring is the durable structural win but is
per-retailer and needs the verified code map; do it, but the pre-scan is the immediate safety net.

---

## 3. Where each upgrade wires into `category_factory_v1.md`

(For TASK-184/CC to apply — this memo does **not** edit the factory doc.)

- **Stage 3 (Corpus Filter):** record the anchor **category-code allow-list** and contaminant
  **code denylist** in `corpus_filter.md` alongside the existing name signals. Document F03/F05 as
  "allow + flag" (organic mirror that hosts the organic-ptitim contaminant).
- **Stage 4 (BSIP0 Acquisition):** acquire from the anchor codes as the **primary spine**; name
  queries become *supplements*. Persist `source_category_codes` (parse from `category_raw`) and the
  energy/unit raw basis on every record.
- **Stage 5 (BSIP0 Gate):** run the **contaminant + energy pre-scan (§4)** here (this is the
  "OOS quick-scan in BSIP0 gate" already listed as automation candidate #7 / Stage-5 Future
  Automation in the factory doc). Emit `bsip0_prescan_report.json`: per-product `food_class`,
  `flags`, `reason`. The gate **surfaces** suspects with reasons; it does not silently drop.
- **Stage 6 (Corpus Cleanup):** EV-045/045b stays as the confirming curation pass (defence in
  depth) — the pre-scan moves detection earlier, it does not replace curation.
- **Stage 10 (Website Readiness):** wire the **Gate-2 leaderboard assertion** (upgrade #4).

---

## 4. PRE-SCAN SPEC handed to TASK-184 (apply-ready)

> Reuses the EV-045b classifier logic already in
> `03_operations/bsip0/scrape/shufersal_cereals/02_build_bsip1_cereals.py` (functions
> `_is_ptitim_pasta`, `_is_bread_leakage`, `_is_confection`, `_contaminant_reason`,
> `_first_ingredient`, and the `*_RE` patterns). Lift those into a **category-agnostic** module
> `03_operations/bsip0/_shared/bsip0_prescan.py` and call it from the Stage-5 gate. Generalize the
> *principle* (name-head disambiguation + first-ingredient dominance + Hebrew word-boundaries +
> energy floor), not the cereal-specific tokens — per `corpus_purity_gates_v1.md`.

### 4a. Inputs (per BSIP0 raw record)
- `name_he`
- `ingredients_raw`
- `energy_kcal_raw` (parse with the existing `_parse_num`; cereals `DRY_CEREAL_ENERGY_FLOOR = 150.0`)
- `category_raw` → parse to `source_category_codes` with `re.findall(r"[AF]\d{3,}", category_raw)`
- (optional) `brand`

### 4b. Signal list and thresholds (cereals instance; floor + token sets are category params)

```
# --- 1. CATEGORY-CODE ANCHOR (upgrade #2; cereals values) ---
ANCHOR_CODE_PREFIXES   = ("A2502", "A2803", "A2808", "A2814")   # cereal + granola + extruded/kids
CONTAMINANT_CODE_PREFIXES = ("A2211",  # ptitim pasta shelf
                             "A1005", "A1014", "A1015", "A100", "A101",  # bread/bakery
                             "A240", "A241")                    # bakery/loaves
ALLOW_BUT_FLAG_PREFIXES = ("F03", "F05", "F12", "F13")          # organic/natural mirror (hosts organic-ptitim)

def code_signal(codes):
    if any(c.startswith(CONTAMINANT_CODE_PREFIXES) for c in codes):
        return "off_shelf_contaminant_code"          # strong exclude signal
    if any(c.startswith(ANCHOR_CODE_PREFIXES) for c in codes):
        return "on_anchor_shelf"                      # strong keep signal
    if any(c.startswith(ALLOW_BUT_FLAG_PREFIXES) for c in codes):
        return "organic_mirror_review"                # keep + flag for ingredient/energy confirm
    return "no_anchor_code"                           # unknown — fall through to name+ingredient gate

# --- 2. FOOD-CLASS CLASSIFIER (reuse EV-045b verbatim) ---
# _is_ptitim_pasta(name, ingr)  -> "ptitim_pasta_excluded"     (name HEADED by פתיתים, or פתיתים + shape,
#                                                               or flour(+water)-only ingredient signature)
# _is_bread_leakage(ingr)       -> "bread_ingredient_leakage"  (שמרים w/ Hebrew word-boundary | מחמצת |
#                                                               מהלחם | sourdough | yeast)  ← EV-029 boundary trap
# _is_confection(name, ingr)    -> "chocolate_confection_excluded"
# PASTA_RE / DRINK_RE / flour-head -> "pasta_excluded" / "drink_excluded" / "flour_product_excluded"

# --- 3. ENERGY / UNIT-PLAUSIBILITY (upgrade, split from EV-045b) ---
DRY_ENERGY_FLOOR = 150.0          # kcal/100g; category param (cereal). Lowest legit dry: oat bran 246.
def energy_signal(name, ingr, energy_kcal):
    if energy_kcal is None:
        return None                                   # no number — handled by coverage gate, not here
    if energy_kcal < DRY_ENERGY_FLOOR:
        # disambiguate wet contaminant vs per-serving parse error:
        is_wet = bool(DRINK_RE.search(name) or "וויט" in name
                      or re.search(r"מעדן|פסטה|נודלס|פטוצ", name))
        if is_wet:
            return "energy_implausible_wet_product"      # EXCLUDE (drink/dessert/cooked pasta)
        return "energy_implausible_per_serving_parse"    # FLAG for re-parse/review — likely a real cereal
                                                         # whose panel parsed per-serving (~30g) not per-100g
    if energy_kcal > 600:
        return "energy_implausible_high"                 # FLAG (fat/oil-dense outlier or parse error)
    return None
```

### 4c. Decision policy (what the gate does with the signals)

```
food_class_reason = (_is_ptitim_pasta(...) and "ptitim_pasta_excluded")
                 or (_is_bread_leakage(...) and "bread_ingredient_leakage")
                 or _contaminant_reason(name, ingr, energy_kcal)   # pasta/flour/confection/drink/<floor>
energy_reason     = energy_signal(name, ingr, energy_kcal)
code              = code_signal(source_category_codes)

# OUTCOME (gate surfaces, does NOT silently drop):
if food_class_reason in EXCLUDE_REASONS or energy_reason == "energy_implausible_wet_product":
    flag = "EXCLUDE_CANDIDATE"        # contamination ≠ calibration — route to Stage-6 exclusion, never re-grade
elif code == "off_shelf_contaminant_code" and code is the ONLY signal:
    flag = "REVIEW_off_shelf"         # off-shelf code but name/ingredient look in-class -> human confirm
elif energy_reason in ("energy_implausible_per_serving_parse","energy_implausible_high"):
    flag = "REVIEW_unit_sanity"       # likely real product, bad number -> re-parse, do not exclude on this alone
elif code == "organic_mirror_review":
    flag = "REVIEW_organic_mirror"
else:
    flag = "PASS"
```

### 4d. Output — `bsip0_prescan_report.json` (Stage 5)

```json
{
  "run_id": "...", "generated": "ISO-8601", "source_file": "...",
  "raw_count": 113,
  "summary": {"PASS": N, "EXCLUDE_CANDIDATE": N, "REVIEW_off_shelf": N,
              "REVIEW_unit_sanity": N, "REVIEW_organic_mirror": N},
  "products": [
    {"barcode": "...", "name_he": "...", "source_category_codes": ["A2502","A250204"],
     "energy_kcal": 110.0, "food_class": "cereal|ptitim_pasta|bread|confection|drink|flour|unknown",
     "flag": "REVIEW_unit_sanity", "reasons": ["energy_implausible_per_serving_parse"]}
  ]
}
```

### 4e. Hard rules carried into the spec (must not be violated by TASK-184)
1. **Contamination ≠ calibration (Gate 1):** an `EXCLUDE_CANDIDATE` for being the wrong *food* is
   removed at curation, **never** re-graded/NOVA-capped. The pre-scan emits a *reason*, never a score.
2. **No silent drops:** the gate **surfaces** suspects with reasons; exclusion is enacted at Stage 6
   with the existing exclusion log. A `REVIEW_*` flag requires confirmation, not auto-removal — this
   preserves the `חומוס גרגרים בתטבילה` false-positive lesson (name keyword alone never excludes when
   ingredient/code data confirm in-class).
3. **Hebrew word-boundary on `שמרים`** is mandatory (EV-029 family): `שמרים` ⊂ `משמרים` ("no
   preservatives"). Reuse the existing `(?<![א-ת])שמרים` lookbehind verbatim — a naive match falsely
   excludes Nesquik / Cini Minis / Lion.
4. **Energy floor is a category parameter**, not a constant — 150 kcal/100g is the *cereal* value
   (justified: lowest legit dry items observed are oat bran 246, Weetabix 342). Other categories pass
   their own floor. Per-serving-parse flags re-parse; they do not exclude on energy alone.
5. **No invented data:** the pre-scan classifies and flags only; it never fabricates a nutrition value
   or ingredient. External-source values (OFF/USDA/il_prices, if #6 lands) stay `candidate` per EDPG
   until a BSIP0/QA pass promotes them.

---

## 5. Definition-of-Done check (TASK-183)

- [x] Ranked improvement memo (impact × effort), recommended adoption set, wiring map to factory
      Stages 3–6/10 (§2, §3) — under `03_operations/factory/`.
- [x] Contaminant + energy pre-scan specified concretely enough for TASK-184 to apply (§4 — signals,
      thresholds, decision policy, output schema, reuse pointer to EV-045b).
- [x] Shufersal cereal-anchor codes identified and grounded against the scraped `category_raw` (§1).
- [x] No published scores or engine touched; no product/nutrition data invented.

**Proposed status: RETURNED** (memo attached). Central Controller / CC records CLOSED.
