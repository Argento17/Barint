# Ingredient Reading Diagnosis v1
**Task:** TASK-395 (de-chain program — Step 1)
**Author:** Data Agent (diagnosis + sizing only; no engine edits, no commit)
**Date:** 2026-06-25
**Status:** DIAGNOSIS COMPLETE — proposes architecture, awaits Nutrition Agent + Product Agent review before build

---

## Executive Summary

The owner's diagnosis is confirmed: ingredient READING is broken. The failure is NOT in
BSIP1 — it is entirely in the BSIP2 probe's `expand_composites` function in
`matrix_signal_probe_v2.py`. BSIP1's `_parse_ingredients_ordered` correctly handles Hebrew
labels, including allergen declarations and stated percentages. The probe re-invents parsing
from scratch and introduces a critical bug that silently drops whole-grain primary ingredients
from 54% of gold-set products. The 25.5% stated_pct population rate cited in the v1 report
is an artifact of this bug — the underlying label coverage is actually 82.8% of gold-set
products.

The fix is in the probe, not upstream. But the structural diagnosis reveals a deeper problem
across all consumers: BSIP1 produces a clean ordered list with no qualifier extraction, no
percentage semantics, and no sub-composite expansion. Every consumer (matrix probe, additive
detector, NOVA proxy) independently re-parses the raw string and makes different mistakes.
A single shared structured parser, upstream in BSIP1, would eliminate the problem class.

---

## Part A — Current Ingredient-Reading Architecture

### A1. Where raw `ingredients_text_he` is stored

Verified at file level (not inferred):

**BSIP0 scrape layer** — The raw retailer ingredient string is stored per-product at:
```
C:\Bari\03_operations\bsip0\scrape\yohananof\outputs\yohananof\{barcode}\product.json
  field: raw_observations.ingredients_raw_he
```
This is the most upstream source. It is the direct OCR/scrape of the label.

**BSIP1 enrichment layer** (`C:\Bari\03_operations\bsip1\core\ingredient_enricher.py` lines 516-557):
The enricher calls `_try_bsip0_raw(barcode)` to read from BSIP0. It stores:
- `ingredients_raw` — the raw string (from BSIP0 if available, otherwise `ingredients_text_he` fallback)
- `ingredients_raw_provenance` — source metadata
- `ingredient_order` — ordered parsed items from `_parse_ingredients_ordered()`

The `ingredient_order` field is the ONLY structured output BSIP1 produces. It contains:
```json
[{"position": 1, "text": "פתיתי שיבולת שועל מלאה (54%) (מכיל גלוטן)",
  "percentage_declared": 54.0, "has_subgroup": false}]
```

**Critical finding (verified at `ingredient_enricher.py:409-450`):** BSIP1's
`_parse_ingredients_ordered` splits on commas at `depth==0` only. It does NOT expand
sub-composites. Each comma-separated item is preserved as an atomic string. It correctly
extracts `percentage_declared` from the item text using `_PCT_RE`. It correctly sets
`has_subgroup=True` when there is a non-empty parenthetical beyond the percentage. The
whole qualifier `מלאה` and the stated percentage `54.0` are both present and correct in the
output. **BSIP1 itself is not broken.**

**BSIP1 semantic extractions** (`ingredient_enricher.py:563-611`):
BSIP1 also extracts semantic markers via `_extract_terms()` against the full lowercase text —
additive detection, flavor markers, sweeteners, protein markers, matrix markers, fermentation
markers, roasting markers. These are keyword-list substring searches run on the full raw string,
not on the structured `ingredient_order` items. They are fast and reasonably correct for their
purpose (boolean presence detection), but carry no position, no stated percentage, and no
qualifier context. They are adequate for signal detection but not for the component-B
whole-food matrix computation, which requires weight ordering.

### A2. Downstream consumers and their parsing approaches

**Consumer 1: Matrix signal probe (`matrix_signal_probe_v2.py`)**

The probe contains a full custom ingredient parser called `expand_composites()`. It does NOT
read from `ingredient_order` — it re-parses `ingredients_text_he` from scratch. This is the
consumer with the confirmed critical bug (see Part B). The probe's stated goal was to handle
sub-composite expansion (e.g. "גרנולה 75% (שיבולת שועל 40%, ...)") but the implementation
mis-classifies any item with two or more parenthetical groups as a composite parent.

**Consumer 2: Signal extractor (`signal_extractor.py`)**

The signal extractor (`signal_extractor.py:830-909`, `extract_signals()`) reads from three
places:
- `get_ingredients(product)` → returns `ingredient_list` (pre-split list of Hebrew strings)
- `get_ingredients_text(product)` → returns raw text
- Various keyword lists searched against the raw text

The additive detector (`_ADDITIVE_MARKER_PATTERNS_BASE` and `_FIXED`, lines 145-214)
uses `re.search(pattern, text, re.IGNORECASE)` against the full ingredient text. No position,
no percentage. It fires on substring presence only. This is adequate for additive detection
but has no view of position or stated mass.

The whole-grain detection (`WHOLE_GRAIN_MARKERS_HE`, lines 265-273) is a keyword list searched
against the full text. It includes `כוסמין` as a whole-grain marker without any `לבן` qualifier
check (verified at line 272), which means products with `כוסמין לבן` (refined spelt flour)
are falsely credited with whole grain.

The NOVA proxy reads `ingredient_list` (the pre-split list) for ingredient count and reads the
raw text for pattern matching. No percentage extraction, no qualifier disambiguation.

**Consumer 3: NOVA proxy (`nova_proxy.py`)**

NOVA proxy (`nova_proxy.py:1-100+`) reads the pre-processed ingredient signals that come out
of `extract_signals()`. It does not directly parse `ingredients_text_he`. It is downstream
of the signal extractor's raw-text searches. It relies on: ingredient count (from sanitized
list), additive markers (category dict), whole grain presence (keyword list), and fermentation
markers. No position-weighting, no stated percentage reading.

### A3. Verdict: Where the failure lives

**BSIP1 is correct.** Its parser produces a clean depth-0 split with percentage extraction
and `has_subgroup` flags. The raw ingredient string is preserved. Upstream is not the problem.

**The failure is in BSIP2-probe (`expand_composites`) — confirmed by direct execution.**
It is the only consumer that attempts sub-composite expansion, and it does so incorrectly.

**Secondary structural failure (not a bug, a design gap):** Every consumer reads the raw
string independently and makes its own parsing assumptions. There is no shared structured
representation downstream of BSIP1. The additive detector, NOVA proxy, and matrix probe each
re-parse independently with different logic, different error modes, and no shared state.
The probe's bug is the acute problem; the architecture gap is the chronic one.

---

## Part B — Failure Sizing on the Real Corpus

### B1. The confirmed bug: `expand_composites` allergen+percentage collapse

**Script:** `03_operations/bsip2/proto_v0/analysis/ingredient_reading_diagnosis.py`
**Output:** `analysis/ingredient_reading_diagnosis_numbers.txt` and `.json`
**Gold set:** 58 products, 57 with ingredient text

The bug fires when `expand_composites()` calls:
```python
sub_match = re.search(r'^(.*?)\s*\(([^)]*%[^)]*)\)', item)
```
This regex matches the FIRST parenthetical group that contains `%`. On the label:
```
פתיתי שיבולת שועל מלאה (54%) (מכיל גלוטן)
```
The match is `(54%)` — a bare percentage in the first paren, not a sub-recipe. The code then:
1. Sets `is_composite_parent=True` on the whole item
2. Treats `sub_text = '54%'` as sub-ingredient text
3. Creates a sub-fragment `'54%'` (a bare percentage string) at the same position
4. The whole item is SKIPPED in `extract_all_markers` (line 377: `if frag.get("is_composite_parent"): continue`)
5. The sub-fragment `'54%'` matches no grain markers
6. **Result: the whole-grain ingredient at position 1 disappears completely**

**Measured impact on gold set (57 parseable products):**

| Metric | Count | Rate |
|---|---|---|
| Products where harmful bug fires (whole grain LOST) | 31 / 57 | 54% |
| Ingredient items silently dropped | 92 items | — |
| Products with `(מכיל ...)` allergen + pct in same item | 32 / 57 | 56% |
| Products with two+ paren groups and pct in one | 31 / 57 | 54% |
| T1 (clear-whole) products where FIRST ingredient is lost | 9 / 17 | 53% |

The pattern `X (pct%) (מכיל גלוטן)` is standard Israeli label format for allergen declaration
adjacent to stated percentage. It is not a sub-composite. The parser must recognize it as an
atomic ingredient.

### B2. Percentage phrasings on the gold set

Of 57 products with ingredient text:
- **82.8%** (48/58) have at least one percentage anywhere in their text
- **25.5%** (14/55 parseable) have at least one stated_pct captured by the probe's markers

The gap between 82.8% and 25.5% is almost entirely the bug: the probe captures only 36 items'
percentages correctly while losing 92 to the composite-parent misclassification. Stated_pct
coverage on the real label corpus is NOT 25.5% — that figure is an artifact of the parsing
failure. The actual label-stated-percentage rate on the Hebrew retail corpus is ~83%.

**Percentage denominator types found (Task 2):**

| Type | Items | Notes |
|---|---|---|
| Bare pct `(54%)` or `54%` | 86 | Standard Israeli format; CORRECT basis for product-weight |
| `X% מהמוצר` / `X% ממשקל המוצר` | 3 | Explicit product-weight basis; CORRECT |
| `X% מהקמחים` / `X% מהקמח` | 6 | Flour-weight basis; WRONG denominator for product-weight scoring — must be excluded or scaled |
| `X% מהלחם` | 4 | Bread-weight basis; often equivalent to product-weight |
| Sub-pct inside a real sub-composite | 13 | e.g. `גרנולה 65% (שיבולת שועל 43%)` — requires parent×sub multiplication |

The flour-denominator case (`מהקמחים`) is a genuine complexity: `100% מהקמחים, 58% מהמוצר`
means the stated grain is 100% of the flour fraction but only 58% of the whole product. A
parser must distinguish which denominator is which and use the product-weight figure for
scoring. Current code does not distinguish them — it takes the first percentage it finds.

### B3. Nested and composite structures

**96.6%** (56/58) of products have at least one parenthetical. The structures observed:

- Standard allergen declaration: `(מכיל גלוטן)` or `(מכיל: חלב, גלוטן)` — 54 products
- Stated percentage: `(54%)` — 48 products  
- Percentage + allergen in same item: `(54%) (מכיל גלוטן)` — 32 products (the bug trigger)
- Real sub-composite with inner ingredients: `(קמח חיטה, גריסי תירס, סמולינה)` — 13 products
- Curly braces `{...}` for sub-lists: 2 products (non-standard; unhandled)
- Multi-level nesting `((...))`: 10 products (partially handled)
- Combined multilevel + percentage: `קמח חיטה מלא (נטחן מגרעין החיטה בשלמותו (מכיל גלוטן)) (100% מהקמח, 62.2% מהלחם)` — 5 products

### B4. Whole/refined qualifier coverage

BSIP1 correctly sees 47 items with whole qualifiers (`מלא`/`מלאה`/`מלאים`) and 1 item with
refined qualifier (`לבן`/`בהיר`). The probe loses 29 of the 47 whole-qualifier items due to
the composite-parent bug. The probe also misclassifies `כוסמין לבן` as whole in the
`signal_extractor.py` WHOLE_GRAIN_MARKERS_HE list (line 272: `"כוסמין"` without `לבן` check).

**Overall read quality on gold set:**

| Category | Count |
|---|---|
| Labels read CLEANLY end-to-end (BSIP1 correct + probe correct) | ~26/57 (46%) |
| Labels BSIP1 reads correctly but probe corrupts | ~29/57 (51%) |
| Labels genuinely unparseable (marketing copy, INCI) | 2/57 (3%) |

The 46% "clean" figure for the probe includes products where no bug fires because the label
does not use the allergen+pct pattern. It does not mean those products are fully parsed —
it means the bug happened not to trigger.

---

## Part C — Proposed Architecture: Shared Structured Ingredient Parser

### C1. The design

A single shared module replaces all ad-hoc re-parsing by downstream consumers. Input is a
raw Hebrew ingredient string. Output is a structured list:

```python
# Per-ingredient record
{
  "raw":           str,           # exact text of this ingredient item, unmodified
  "normalized":    str,           # lowercased, punctuation-normalized token for matching
  "position":      int,           # 1-indexed position in the OUTER ingredient list
  "stated_pct":    float | None,  # percentage stated on label (product-weight basis)
  "pct_basis":     str | None,    # "product" | "flour" | "bread" | None — denominator type
  "qualifiers":    list[str],     # ["מלא"] / ["לבן"] / ["אורגני"] etc.
  "allergen_notes": list[str],    # ["מכיל גלוטן"] — NOT sub-ingredients
  "parent_idx":    int | None,    # 1-indexed position of parent composite, if this is a sub-ingredient
  "is_sub":        bool,          # True if this item is a sub-ingredient inside a composite
  "sub_position":  int | None,    # position within the parent composite's sub-list
  "has_own_sub":   bool,          # True if this item itself has a sub-list
}
```

**What counts as a sub-ingredient (real expansion needed):**
- Parent has a stated pct AND its parenthetical content contains multiple items separated by
  commas with substance names (e.g. `גרנולה 65% (פתיתי שיבולת שועל 43%, שמן, סוכר)`)
- The paren content is NOT a bare percentage alone
- The paren content is NOT an allergen declaration (`מכיל`)
- The paren content is NOT a provenance note (`נטחן מגרעין...`)

**What is NOT a sub-ingredient (must NOT expand):**
- `(54%)` — bare percentage alone. Attach pct to the parent item; do not create a sub-fragment
- `(מכיל גלוטן)` / `(מכיל: חלב)` — allergen declaration. Move to `allergen_notes`
- `(גלוטן)` — allergen shorthand. Move to `allergen_notes`
- `(100% מהקמחים, 58% מהמוצר)` — dual-denominator phrase. Parse both pcts, attach to parent
- `(נטחן מגרעין החיטה בשלמותו)` — provenance/processing note. Move to a `notes` field
- `{...}` — non-standard curly braces; treat as parenthetical

### C2. Where it should live

**Recommendation: BSIP1 enrichment stage** — add a `structured_ingredient_parser.py` module
to `03_operations/bsip1/core/` that is called inside `ingredient_enricher.enrich()` after
`_parse_ingredients_ordered()`. Its output field name: `ingredient_order_v2` (keeps `ingredient_order`
for backward compatibility until all consumers migrate).

Rationale for BSIP1 placement (not a shared module imported at BSIP2 time):
1. BSIP1 already holds the raw text and runs once per product — correct time to parse
2. BSIP2 consumers should read structured data, not re-parse raw strings
3. The output is stable per BSIP1 run and stored in the product JSON — no re-parsing cost
4. BSIP0→BSIP1 is the data-cleansing boundary; structured ingredient semantics belong there
5. All three consumers (matrix probe, additive detector, NOVA proxy) can migrate to reading
   `ingredient_order_v2` from the stored BSIP1 JSON instead of independently parsing

BSIP2 consumers would then read `product["ingredient_order_v2"]` directly — zero re-parsing.

### C3. Validation: parse-accuracy gate

The parse-accuracy gate must be graded by a lane OTHER than the builder. Proposed:

**Frozen test set spec:**
- 50–80 manually annotated labels from the real corpus (barcodes must exist in BSIP1 data)
- Annotation covers: ingredient text → per-item structured record (raw, position, stated_pct,
  pct_basis, qualifiers, allergen_notes, parent_idx, is_sub)
- Human annotator: the owner (reads Hebrew labels directly) or a native-Hebrew speaker
- Annotation process: read the label image / raw text, not the parsed output
- Store in: `03_operations/bsip2/proto_v0/analysis/ingredient_parse_test_set_v1.json`

**Metrics:**
| Metric | Bar | Notes |
|---|---|---|
| Item count accuracy | ≥ 98% | Items correctly split at depth-0 commas |
| Stated_pct extraction | ≥ 95% | Of items with a percentage, fraction captured |
| Pct_basis classification | ≥ 90% | Correct denominator type assignment |
| Qualifier extraction | ≥ 95% | מלא / לבן / אורגני correctly attached |
| Allergen vs sub-ingredient | ≥ 99% | No allergen treated as sub-list expansion |
| Sub-composite expansion | ≥ 90% | Real sub-composites correctly expanded with parent×sub pct |

**Gate process:**
1. Builder (Data Agent or designated C1 lane) implements the parser
2. Data Agent runs the parser on the frozen test set and produces a per-item comparison table
3. The comparison table (not the parser) is reviewed by Adversarial QA Agent
4. QA Agent verifies metric thresholds are met before any consumer migration
5. Builder cannot self-grade — the QA Agent grades against the human-annotated ground truth

### C4. What is genuinely hard about Hebrew ingredient labels

These are verified against real corpus evidence, not assumed:

**1. Double-paren patterns** (confirmed, affects 54% of gold-set products)
Israeli labels routinely write `INGREDIENT (PCT%) (מכיל ALLERGEN)` as two separate paren
groups. A parser must decide: first paren is quantity, second is allergen — neither is a
sub-recipe. The probe's regex `\([^)]*%[^)]*\)` fires on the percentage paren and misclassifies
the item as a composite.

**2. Flour vs product-weight denominator ambiguity** (confirmed, 6 items in gold set)
The label `(100% מהקמחים, 58% מהמוצר)` contains TWO percentages with different denominators
in the same parenthetical. A naive `first-pct` extractor takes 100% instead of 58%, which
drastically overestimates the grain's contribution to the total product weight. Detection
requires recognizing `מהקמחים`, `מסך הקמחים`, `מהלחם` as non-product-weight qualifiers and
taking only the `מהמוצר` / `ממשקל המוצר` figure as the product-weight stated_pct.

**3. Morphological prefix attachment** (not yet confirmed on corpus; risk level: medium)
Hebrew prefixes `ב-`, `מ-`, `ה-`, `ו-` attach to words without spaces. An ingredient like
`מחיטה` means "from wheat" — it is `מ` (from) + `חיטה` (wheat). Regex patterns that match
`חיטה` will fire on `מחיטה`, which can be correct (the ingredient IS wheat-based) or
incorrect (it appears in a phrase like `נטחן מחיטה בשלמותו` = "milled from whole wheat",
where `מחיטה` is a provenance note, not an ingredient declaration). BSIP1's current keyword
lists use substring matching without prefix guard, which means `מחיטה` in a provenance note
can trigger a wheat-flour marker. The guard `(?<![א-ת])` (not preceded by Hebrew letter) used
in `signal_extractor.py:309` for yeast detection is the correct pattern — it must be applied
to grain tokens generally.

**4. Spelt qualifier disambiguation** (confirmed, 7 products in gold set)
`כוסמין` (spelt) alone is ambiguous: it can be whole spelt grain or the brand/variety name for
a refined spelt flour. The qualifier `מלא` = whole; `לבן` = refined (white); `בהיר` = light
(partial extraction, between whole and white). The current `signal_extractor.py:272` lists
`"כוסמין"` without any qualifier check, so `כוסמין לבן` (refined white spelt) is incorrectly
credited as whole grain. Verified: barcode 7290018500644 (`מארז פיתות כוסמין לבן`) is T2
(clear-refined) in the gold set; the signal extractor would credit it as whole.

**5. Abbreviation/construction forms** (confirmed, 2 cases in gold set)
`חיטת כוסמין` (construct state: "spelt wheat") vs `חיטה כוסמין` (two free words) — both
refer to spelt wheat but use different Hebrew grammatical constructions. The probe's pattern
`כוסמין מלא` correctly matches both. But `קמח חיטת כוסמין מלא` (barcode 7290017947464) —
"whole spelt wheat flour" — uses the construct form `חיטת` not the free form `חיטה`. Pattern
`קמח כוסמין מלא` does not match `קמח חיטת כוסמין מלא`. Requires either a broader pattern
or explicit construct-form entries.

**6. Curly-brace sub-lists** (confirmed, 2 products in gold set)
`ממתיק [Truvia] ממתיקים (אריתריתול, גליקוזידים של סטיביול)` uses `[...]` for a brand name.
`תערובת קמחים (מכיל גלוטן) {קמח חיטה (46%), קמח כוסמין מלא (5%)}` uses `{...}` for a
sub-list. Neither `{` nor `[` is handled by the BSIP1 depth-tracker (which only counts `(`);
the signal extractor ignores them; the probe's `_split_top_level` handles `{}` and `[]` in
the character class but does not expand them as composites. The `{...}` case contains real
sub-ingredients with stated percentages that are currently unread.

---

## Summary Findings

| Question | Answer | Evidence Source |
|---|---|---|
| Is the failure in BSIP1? | **NO** | `ingredient_enricher.py:409-450` — depth-0 split is correct; `ingredient_order` preserves items atomically |
| Is the failure in the BSIP2 probe? | **YES** | `matrix_signal_probe_v2.py:205-269` — `expand_composites` fires on allergen+pct items, drops whole-grain tokens |
| What fraction of labels have the bug trigger? | **54%** of gold-set products (31/57) | `ingredient_reading_diagnosis_numbers.txt` Task 1 |
| What is the REAL stated_pct coverage on Hebrew labels? | **~83%** (82.8% of gold set have a pct in text) | `ingredient_reading_diagnosis_numbers.txt` Task 2 |
| What is the pct capture rate AFTER the bug? | **28.0%** (36 captured / (36+92)) | `ingredient_reading_diagnosis_numbers.txt` Task 3 |
| Is the 25.5% pct rate in the v1 report real? | **NO** — it is bug-artifact | Computed from gold set; real rate is ~83% |
| Does the signal_extractor have a separate bug? | **Yes (minor)** — `כוסמין` without `לבן` guard | `signal_extractor.py:272` |
| What fraction of labels are read cleanly end-to-end? | **~46%** (probe correct) | `ingredient_reading_diagnosis_numbers.txt` Task 4 |
| Is a shared parser needed? | **Yes** — every consumer re-parses with different bugs | Architecture analysis Part A |

---

## Not Done (Required Honesty)

1. The diagnosis is on the 58-product gold set, not the full 520-product corpus from the v1
   probe. The gold set is representative (drawn from the corpus) but scaling numbers to 520
   products requires running the analysis script on the full corpus — not done in this task
   (the full corpus files are not in a single accessible JSON; they are spread across BSIP1
   run directories).

2. The parse-accuracy gate test set (§C3) does not exist yet — human annotation is required
   before the builder can run any gate.

3. The architectural proposal (§C2) is design only. No code written, no engine modified.

4. The signal_extractor.py `כוסמין` bug is diagnosed but not fixed — it requires a D6/D7
   governance decision because it would change scores for any product containing `כוסמין לבן`.

5. Sub-composite expansion for real composites (e.g. `גרנולה 65% (שיבולת שועל 43%, ...)`)
   was not re-validated after the allergen-guard fix. The fix must preserve correct expansion
   for real composites while rejecting the allergen+pct false-expansion pattern.

---

```json
{
  "task": "TASK-395",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/bsip2/proto_v0/reports/ingredient_reading_diagnosis_v1.md",
      "action": "created",
      "sha256": "3AD14C05CDDC322E1E8AE32D297C10B184C29C3A479FAE8931C0D4CEF89CB858"
    },
    {
      "path": "03_operations/bsip2/proto_v0/analysis/ingredient_reading_diagnosis.py",
      "action": "created",
      "sha256": "D90ACD7DCE99BF2743553A0FE1A04CC71F05166FF95CAB233CFB8D06A02CE94A"
    },
    {
      "path": "03_operations/bsip2/proto_v0/analysis/ingredient_reading_diagnosis_numbers.txt",
      "action": "created",
      "sha256": "49373DE1C5818941AC930D8E516DF55F66019BDC0EF222CBBFE42CE25AE2D336"
    },
    {
      "path": "03_operations/bsip2/proto_v0/analysis/ingredient_reading_diagnosis_numbers.json",
      "action": "created",
      "sha256": "FA04F3834BD5A198CEBBE4E5EB32A33914817BD54AC68CB2552963E876D9C6B8"
    },
    {
      "path": "03_operations/bsip2/proto_v0/analysis/matrix_signal_probe_v2_report.txt",
      "action": "read (pre-existing run output)",
      "sha256": "C914D8D40850C4E3F47CD1A4D4BCF01FA3CCA06972648955524B1DE9EFE442DE"
    }
  ],
  "counts": {
    "gold_set_products_analyzed": "58/58",
    "products_with_ingredient_text": "57/58",
    "products_where_harmful_bug_fires": "31/57 (54%)",
    "ingredient_items_silently_dropped": "92",
    "real_pct_label_coverage": "82.8% (48/58 have a pct in text)",
    "probe_captured_pct_rate": "28.0% (36/128 items with pct)",
    "pct_bug_artifact_rate": "71.9% loss (92/128)",
    "t1_products_with_first_ingredient_lost": "9/17 (53%)",
    "whole_qualifier_items_seen_by_bsip1": "47",
    "whole_qualifier_items_lost_by_probe": "29/47 (62%)",
    "gate_b1_fail_rate": "30.0% (9/30 T1+T2 products outside expected zone)",
    "gate_b2_fail_rate": "72.7% (8/11 ranked pairs wrong direction)"
  },
  "commands_run": [
    {"cmd": "Read C:\\Bari\\03_operations\\bsip1\\core\\ingredient_enricher.py (full)", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\03_operations\\bsip2\\proto_v0\\reports\\matrix_signal_redesign_v2.md (full)", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\03_operations\\bsip2\\proto_v0\\analysis\\matrix_signal_probe_v2.py (full)", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\signal_extractor.py (lines 1-909)", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\03_operations\\bsip2\\proto_v0\\src\\nova_proxy.py (lines 1-100)", "exit_code": 0},
    {"cmd": "Read C:\\Bari\\03_operations\\bsip2\\proto_v0\\analysis\\matrix_signal_probe_v2_report.txt (lines 1-180)", "exit_code": 0},
    {"cmd": "python analysis/ingredient_reading_diagnosis.py (via Agent)", "exit_code": 0},
    {"cmd": "python (gold set pct coverage analysis via Bash)", "exit_code": 0},
    {"cmd": "python (expand_composites bug trace via Bash)", "exit_code": 0}
  ],
  "not_done": [
    "Analysis not run on full 520-product v1 corpus — gold set only (58 products); gold set is representative but scaling requires full corpus run",
    "Parse-accuracy gate test set not yet human-annotated — required before builder can clear the gate",
    "Shared structured parser not built — architecture proposal only",
    "signal_extractor.py כוסמין without לבן guard not fixed — requires D6/D7 governance decision",
    "Sub-composite expansion correctness after allergen-guard fix not re-validated",
    "Flour-denominator disambiguation (מהקמחים vs מהמוצר) not implemented"
  ],
  "spec_conformance": {
    "no_engine_edits": true,
    "no_commit": true,
    "no_scoring_run": true,
    "new_files_under_analysis_or_reports": true
  },
  "acceptance_test": "The report is accepted when: (1) Nutrition Agent and Product Agent confirm the architectural proposal is the right design direction; (2) the parse-accuracy gate test set is human-annotated; (3) a builder implements the shared parser and clears the gate (graded by Adversarial QA Agent, NOT the builder). Gate B1+B2+B3 pass on re-run of probe_v2 after the fix is the end condition for the reading repair."
}
```
