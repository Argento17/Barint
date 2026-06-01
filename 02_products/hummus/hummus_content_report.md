# Hummus Content — Build Report

**Task:** TASK-062  
**Owner:** Data Agent  
**Date:** 2026-05-31  
**Output:** `C:\Bari\02_products\hummus\hummus_content_v1.json`

---

## Section 1 — Sources Used

| Source | What was drawn from it |
|--------|----------------------|
| `hummus_frontend_v1.json` | Product counts, grade distribution, score statistics, product type breakdown, known limitations (KL-1 through KL-5), grade thresholds, corpus date and retailer |
| `hummus_frontend_build_report.md` | KL-1 through KL-5 severity and consumer-facing rephrasing guidance |
| `01_framework/bsip2_framework/ui_language.md` | Grade language ("מבנה תזונתי חזק" / "פרופיל כללי טוב" etc.), list of prohibited language, tradeoff language principles |
| `01_framework/bsip2_framework/architecture_v2/framework_philosophy.md` | Scope constraint language: Bari is not a health recommender; not threshold scoring; not NOVA-only |

No other sources were used. No facts were invented.

---

## Section 2 — Content Produced

### A. Category Introduction

**Length:** 5 sentences (requirement: 5–7)  
**Language:** Hebrew  
**Facts used:**
- 69 products total (from `category.total_products`)
- Product types: 44 hummus, 11 matbucha, 7 eggplant, 5 pepper, 2 masabacha (from `category.product_type_distribution`)
- Retailer: Shufersal (from `category.retailer`)
- Scrape date: May 2026 (from `bsip_metadata.bsip0_scrape_date`)
- 67 displayable, 2 unavailable (from `category.displayable_products` and `category.unavailable_products`)
- BSIP methodology name used exactly as it appears in the framework

**What was NOT said:**
- No claim that BSIP is the "best" or "most accurate" methodology
- No characterisation of any product as "healthy" or "unhealthy"
- No dietary recommendation ("you should eat X")
- No assertion that high score = nutritious for the individual

---

### B. Methodology Section

**User-friendly approach:** Dimensions are described as "מדדים מרובים" (multiple metrics) without naming all ten individually by their technical names. The description groups them into categories a consumer can understand: processing level, additive burden, nutritional values, regulatory warnings.

**Grade descriptions:** Language lifted directly from `ui_language.md`:
- A: "מבנה תזונתי חזק" (Strong nutritional structure)
- B: "פרופיל כללי טוב" (Good overall profile)
- C: "היבטים לעיון" (Areas requiring consideration — adapted from "Some areas of concern")
- D: "חששות מבניים" (Structural concerns — adapted from "Notable structural concerns")

**Score ranges:** Taken directly from `grade_thresholds` in the JSON (A≥80, B≥65, C≥50, D≥35).

**Grade counts:** Taken directly from `category.grade_distribution` (A=8, B=28, C=27, D=4).

**Category-relative note:** Added explicitly because the framework philosophy and ui_language.md both require this disclosure. The JSON's `category_relative_note` in `methodology.md` is a direct reference to this principle.

**Score stats:** "Median 65.2, mean 65.7, range 61–69 for most products" — all from `category.score_statistics`.

---

### C. Known Limitations

Each KL was translated from technical to consumer language. The mapping:

| Internal KL | Consumer title | Consumer text approach |
|-------------|---------------|----------------------|
| KL-1 (fat_quality unreliable) | "נתוני השומן אינם זמינים" | States the data gap, clarifies the score is not penalised as a result |
| KL-2 (2 products missing nutrition) | "שני מוצרים ללא ציון" | States outcome simply; no technical reason |
| KL-3 (2 products imprecise routing) | "שני מוצרים בסיווג כללי" | Explains routing gap in plain terms; confirms score is valid |
| KL-4 (structural emptiness) | "ציון עשוי שלא לשקף את מלוא ההרכב" | Explains low score is data-driven, not a product quality verdict |
| KL-5 (low NOVA confidence) | "הערכת עיבוד חלקית" | States the limitation scope (processing dimension only) |

**Jargon removed:**
- "SRC-04 structural emptiness gate" → not mentioned
- "NOVA proxy" → not mentioned
- "bsip1_7296073733317" → not mentioned
- "fat_g < 0.5" → not mentioned
- "BSIP2 dimension score" → not mentioned

---

### D. Mandatory Disclosure

Reproduced verbatim as required:

> ערכי השומן אינם מוצגים בקטגוריה זו בשל מגבלות באיכות מקור הנתונים.

This is the exact string from the task requirement. It appears as a top-level field (`mandatory_disclosure`) in the JSON and also references `known_limitations[0].mandatory_disclosure_applies: true` for KL-1.

---

### E. Caveated Product Messages

Four message variants produced, mapped to the four `display_caveats` values in the data:

| Trigger | `display_caveats` value | Short label | Long message |
|---------|------------------------|-------------|-------------|
| `structural_emptiness` | `structural_emptiness: calorie_density capped...` | ציון מבוסס על נתונים חלקיים | Explains data incompleteness without promising a specific different score |
| `low_nova_confidence` | `low_nova_confidence: processing_quality...` | הערכת עיבוד חלקית | States limitation to processing dimension only |
| `category_routing_imprecise` | `category_routing_imprecise: display as...` | סיווג חלקי — מוצג כממרח | Notes routing uncertainty; confirms score is on the same method |
| `unavailable` | `score_unavailable: no nutrition panel` | ציון לא זמין | Simple statement; no explanation of internal reason |

Both a `short` label (suitable for a badge or tooltip) and a `long` message (suitable for an info panel) are provided for each.

---

### F. FAQ Section

**8 Q&A items produced** (requirement: 5–8).

| Item | Grounded in |
|------|------------|
| faq-01: What was evaluated? | Product types and count from frontend JSON; retailer and date from metadata |
| faq-02: How is the score calculated? | Dimension description and weighting from `dimension_weights`; scale from `grade_thresholds` |
| faq-03: Is it compared globally? | Category-relative principle from `ui_language.md` and methodology section |
| faq-04: What do grades A–D mean? | `grade_thresholds` and `methodology.grade_descriptions` |
| faq-05: Why is fat quality not shown? | KL-1 from build report; mandatory disclosure |
| faq-06: Is score related to taste or price? | Scope constraint from `framework_philosophy.md` |
| faq-07: Is it a dietary recommendation? | Scope constraint from `framework_philosophy.md` |
| faq-08: When are data updated? | `bsip_metadata.bsip0_scrape_date` from the JSON |

---

## Section 3 — Assumptions Made

The following decisions required judgment where the source material did not prescribe an exact answer:

| Decision | Assumption made | Rationale |
|----------|----------------|-----------|
| **Hebrew register** | Formal but accessible; no slang; complete sentences | Consistent with the neutral, analytical tone of `ui_language.md` |
| **Grade description mapping** | "היבטים לעיון" for C (instead of a literal translation of "Some areas of concern") | "Areas of concern" can sound alarming in Hebrew; "היבטים לעיון" (aspects for consideration) is more neutral and precise |
| **Dimension naming in methodology** | Grouped into "processing level, additive burden, nutritional values, regulatory warnings" rather than listing all 10 by name | Listing 10 technical dimension names (e.g., "processing_quality", "glycemic_quality") in a consumer-facing section violates the "no internal implementation details" requirement |
| **Score stat in methodology** | Included corpus mean (65.7) and median (65.2) | These are facts from the JSON. They help users contextualise where a product sits relative to the corpus without making claims about what is "good" |
| **FAQ count** | 8 items | Requirement was 5–8; 8 items adequately covers the most likely consumer questions without repetition |
| **Caveated messages: short + long** | Provided both a `short` and `long` variant | The `display_caveats` in the JSON are used at multiple UI locations (badge, tooltip, info panel) with different space constraints |
| **Category intro: 5 sentences** | Chose the minimum of the 5–7 range | Fewer sentences reduce the risk of overpromising or drifting into health-claim territory while still satisfying the informational requirement |

---

## Section 4 — What Was NOT Done

Per task requirements and Bari framework constraints:

| Prohibited | Status |
|-----------|--------|
| Health claims ("improves digestion", "good for heart health") | Not included |
| Dietary recommendations ("you should prefer X") | Not included |
| Marketing language ("best", "premium", "exceptional") | Not included |
| Invented facts (claims not found in source files) | Not included |
| Internal technical details (BSIP2 trace fields, gate names, internal IDs) | Not included in consumer content |
| Moral language ("clean eating", "guilt-free") | Not included |
| Absolute statements about product quality outside category context | Not included |

---

## Section 5 — Integration Notes

**Mandatory disclosure placement:** The `mandatory_disclosure` string must appear on any view that shows dimension scores or the corpus-level score distribution. It should not appear only on individual product cards — it applies to the entire category.

**Caveated product message activation:** Match `display_caveats[0]` keyword against the message keys in `caveated_product_messages`. One caveat → show the corresponding message. Multiple caveats (possible) → show all applicable messages.

**FAQ placement:** Suitable for an expandable section below the product list or on a "How it works" information page. Items faq-01 through faq-04 are category-specific; items faq-05 through faq-08 are also valid for future categories with minimal modification.

**Grade description text:** The `grade_descriptions` object in `methodology` provides both `label` (short, for badges) and `description` (one sentence, for tooltips or info panels). Use the `label` in the product card grade badge and the `description` in the expanded info section.

---

*Content Report — TASK-062 — Data Agent — 2026-05-31*  
*Output: `hummus_content_v1.json`*  
*All content grounded in source data. No health claims. No marketing language.*
