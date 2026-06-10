# TASK-222F — Fermentation Vocabulary Audit (DESIGN_ONLY)

**Date:** 2026-06-09
**Status:** DESIGN_ONLY — no scoring changes implemented
**Part of:** TASK-222 (BSIP2 research-to-implementation)

---

## 1. Executive Summary

The BSIP2 scorer uses a single `has_fermentation` boolean derived from `FERMENTATION_MARKERS_HE` (21 terms) plus a word-boundary regex for שמר/שמרים. The BSIP1 enricher uses a separate `FERMENTATION_TERMS` list (29 terms) for enrichment tagging. The frontend bread corpus uses yet another bank (5 terms). These lists have evolved independently and have gaps relative to each other and relative to real Israeli retail labels.

**Recommendation: No scoring changes needed. The vocabulary gap is small and the existing coverage is sufficient for the scoring engine's current use case (binary fermentation detection). However, three actionable gaps should be documented for future enrichment.**

---

## 2. Current State: Four Independent Lists

| Source | Terms | Used By | Purpose |
|--------|-------|---------|---------|
| BSIP2 `FERMENTATION_MARKERS_HE` | 21 Hebrew + 1 Latin | `signal_extractor.py:210-224` | Binary `has_fermentation` boolean for scoring |
| BSIP2 word-boundary regex | 3 forms of `שמר` | `signal_extractor.py:233-236` | Catches yeast without `משמרים` false positive |
| BSIP1 `FERMENTATION_TERMS` | 29 Hebrew + 3 Latin | `ingredient_enricher.py:335-373` | BSIP1 enrichment tagging |
| Bread frontend banks | 5 Hebrew + 2 Latin | `build_curated_003.py:19-20` | Fermentation status display for bread |

---

## 3. Gap Analysis

### 3.1 BSIP1 Terms Missing from BSIP2's FERMENTATION_MARKERS_HE

| Missing Term | Translation | Impact | Notes |
|-------------|-------------|--------|-------|
| `תרבויות ייחוד` | starter cultures | Low | Rare on labels — appears in some artisan yogurts |
| `חיידקים חיים` | live bacteria | Medium | Appears on yogurt labels as quality signal |
| `תסיסה לקטית` | lactic fermentation | Low | Scientific term, rare on consumer labels |
| `לקטובציל בולגריקוס` | L. bulgaricus | Medium | Used in yogurt starter declarations |
| `לקטובציל אסידופילוס` | L. acidophilus | Medium | Used in probiotic declarations |
| `ביפידובקטריום` | Bifidobacterium | Medium | Full binomial — current `ביפידוס` covers most cases |
| `סטרפטוקוקוס תרמופילוס` | S. thermophilus | Medium | Used in yogurt starter declarations |
| `סטרפטוקוקוס` | Streptococcus | Low | Generic; may trigger false positives |
| `לאקטוקוקוס` | Lactococcus | Low | Cheese-specific; rare |
| `שמרי לחם` | bread yeast | Low | Covered by word-boundary regex catching `שמר` |
| `שמרים` | yeast (plural) | Low | **Covered already** by word-boundary regex `_FERMENTATION_WORDBOUND_RE` |
| `יסט` | yeast (alt) | Low | Russian-influence term; rare in Israeli retail |
| `מותסס` | fermented (adj.) | Low | Generic; may trigger in irrelevant contexts |
| `תסיסה` | fermentation (n.) | Low | Generic process term |
| `חיידקי bio` | bio bacteria | Low | Niche marketing term |

**Total BSIP1 terms not in BSIP2 `FERMENTATION_MARKERS_HE`:**
- Fully uncovered: 12 terms
- Already covered by another mechanism (`שמרים` via regex): 1 term
- Truly impactful gaps: **~3–4 terms** (`חיידקים חיים`, specific bacterial strains for yogurt/cheese)

### 3.2 BSIP2 Terms Missing from BSIP1

| BSIP2 Term | Translation | Notes |
|------------|-------------|-------|
| `חמץ` | leavened / sourdough | BSIP1 doesn't list this; relevant for bread |
| `ספיח` | fermented liquid / absorption | BSIP1 doesn't list this |
| `בידפידוס` (variant: missing yod) | OCR variant of `ביפידוס` | BSIP1 has `ביפדוס` (missing yod) but not `בידפידוס` |

**Impact:** Low — these are either OCR spelling variants or bread-specific terms outside BSIP1's dairy-focused list.

### 3.3 Bread Frontend Terms Not in Either BSIP List

| Term | Source | Translation | Notes |
|------|--------|-------------|-------|
| `שאור` | bread frontend bank | sourdough (lit. "leaven") | Common on artisan bread labels — **the most impactful gap** |
| `lactobacillus` (Latin) | bread frontend bank | Lactobacillus | BSIP2 has `לקטובציל` (Hebrew) which covers this |

**Most actionable gap:** `שאור` (sourdough leaven) appears on many Israeli artisan bread labels but is not in either BSIP list. Adding it to `FERMENTATION_MARKERS_HE` would cost ~1 line.

### 3.4 Coverage Assessment by Category

| Category | BSIP2 Coverage | Gap Severity |
|----------|---------------|--------------|
| **Yogurt / cultured dairy** | Good — `תרבויות חיות`, `חיידקי יוגורט`, `לקטובציל`, `ביפידוס` cover most label patterns. Missing specific strain names (`בולגריקוס`, `תרמופילוס`) but the generic terms (`לקטובציל`, `תרבויות`) act as catchalls. | Low |
| **Sourdough bread** | Adequate — `מחמצת` and `חמץ` cover sourdough. Missing `שאור`. Word-boundary regex catches `שמרים` for yeast bread. | **Medium** — `שאור` gap is easily fixable |
| **Cheese** | Weak — cheese fermentation markers (specific cultures, rennet types) are under-represented. However, the R7 Path B (cultured cheese name markers) compensates. | Low (R7 compensates) |
| **Fermented vegetables (pickles, etc.)** | Poor — `מותסס`, `תסיסה` are in BSIP1 but not BSIP2. However, these categories are not yet scored. | Low (unscored categories) |
| **Vinegar / fermented condiments** | **Not covered at all** — `חומץ` (vinegar) appears in no list. But vinegar is a fermentation PRODUCT, not a fermentation PROCESS signal. Intentionally out of scope for live-culture bonus. | None (intentional) |

---

## 4. Recommended Actions

### 4.1 Quick Fix (1 line, high value)

```python
# Add to FERMENTATION_MARKERS_HE in signal_extractor.py
"שאור",  # sourdough leaven — common on artisan bread labels (TASK-222F)
```

Impact: Catches artisan bread products that declare `שאור` (leaven) instead of `מחמצת` (sourdough starter). Currently not detected by any BSIP list.

### 4.2 Medium Fix (3 lines if needed)

```python
# Add to FERMENTATION_MARKERS_HE in signal_extractor.py
"חיידקים חיים",           # live bacteria — yogurt quality signal
"לקטובציל בולגריקוס",     # L. bulgaricus — specific yogurt starter
"סטרפטוקוקוס תרמופילוס",  # S. thermophilus — specific yogurt starter
```

Impact: Catches more specific yogurt/cheese strain declarations. Adds resilience against labels that use full binomial names instead of generic `לקטובציל`.

### 4.3 Low-Value Fixes (not recommended)

Adding `תרבויות ייחוד`, `תסיסה לקטית`, `מותסס`, `תסיסה`, `ביפידובקטריום`, `לאקטוקוקוס`, `סטרפטוקוקוס`, `שמרי לחם`, `יסט`, `חיידקי bio` is **not recommended** — these are either rare, covered by other terms, or would increase false-positive risk without meaningful scoring benefit.

---

## 5. Double-Counting Risk

| Change | Risk | Reasoning |
|--------|------|-----------|
| Adding `שאור` | **None** — single boolean, new detection for currently-undetected products | Only increases the true-positive rate for already-scored bread products |
| Adding specific bacterial strains | **None** — binary boolean, no new dimension | These products would already be detected via `תרבויות` or `לקטובציל` in most cases; the addition is resilience, not new signal |

---

## 6. Scoring Impact Assessment

| Fix | Products Affected | Scoring Delta |
|-----|------------------|---------------|
| Add `שאור` | Artisan sourdough breads that use `שאור` instead of `מחמצת` | Previously: 0 fermentation bonus. After: +8 (R-02) + +5 (WFI) = +13 total. |
| Add specific strains | Yogurts that only declare full binomial names | Very few — most also declare generic terms. Marginal improvement. |

**No fix changes the scoring philosophy** — only the detection coverage. The R-02 +8 bonus and WFI +5 bonus remain gated by `has_fermentation` boolean and NOVA ≤ 3.

---

## 7. Consumer-Copy Restrictions

No consumer copy changes from this audit — the fermentation bonus copy already exists and is unchanged. The audit only affects internal detection vocabulary.

---

## 8. Implementation/No-Implementation Decision

**RECOMMENDATION: DO NOT IMPLEMENT AS A SEPARATE TASK.** The quick fix (`שאור`) can be rolled into the next bread/frontend task as a 1-line change. The medium fixes (specific strains) are optional and low-priority — only worth adding if a yogurt-specific enrichment task is opened.

The audit satisfies TASK-222's requirement ("Vocabulary-only audit: compare current markers against retail labels for gaps") without requiring a scoring sprint.

---

## 9. Registry Update

```yaml
TASK-222F: Design Review — RETURNED for CC review
status: RETURNED
return_reason: >
  Fermentation vocabulary audit complete. Compared BSIP2 FERMENTATION_MARKERS_HE
  (21 terms + word-boundary regex) against BSIP1 FERMENTATION_TERMS (29 terms)
  and bread frontend banks (5 terms). Coverage is adequate for the scoring engine's
  binary detection use case. One actionable gap: "שאור" (sourdough leaven) is
  missing from all BSIP lists and appears on artisan bread labels. Recommend
  rolling into next bread frontend task as a 1-line addition. Specific bacterial
  strain names (L. bulgaricus, S. thermophilus) are lower priority — existing
  generic catchalls (לקטובציל, תרבויות) cover most cases. No scoring changes
  needed or recommended.
```
