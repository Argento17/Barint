# Explanation Framework Review — Nutrition Agent

**Task:** TASK-076
**Reviewer:** Nutrition Agent
**Date:** 2026-05-31
**Input reviewed:** `bari_explanation_framework_v1.md` (TASK-073 — Product Agent)
**Cross-checked against:** `hummus_frontend_v1.json` (run_hummus_002), `hummus_insights_v1.md`, `hummus_frontend_build_report.md`, `hummus_content_review.md` (TASK-064)

---

## Overall Verdict

**REVISIONS REQUIRED**

The framework is structurally sound and correctly anchored in the canonical `explainability_v1.md` and `score_presentation_v1.md`. Its diagnosis of the root cause (generic per-grade descriptions standing in for a per-product explanation layer) is accurate, and the savory-spread translation system is a legitimate, well-scoped fill of the `explainability_v1.md §5` gap. No health claims and no recommendation framing were found anywhere in the document.

However, **two of the five worked examples contain product-level factual errors**, and the **Section-3 fat-data guidance is written in a way that caused one of them**. These must be corrected before the framework is used to author production copy. The framework's *rules* are correct; the *application* in two examples is not.

---

## Verdict Summary

| Item | Severity | Verdict |
|---|---|---|
| Framework philosophy, anchoring, §1–§2 | — | APPROVE |
| Mandatory template §3 (3-section structure) | — | APPROVE |
| Savory-spread signal-language tables §3 | — | APPROVE |
| Section-3 fat-data guidance (§3, §2 item 7) | BLOCKING | REVISE |
| Example 4.1 — A-grade hummus | BLOCKING | REVISE |
| Example 4.2 — B-grade hummus | — | APPROVE |
| Example 4.3 — C-grade hummus | RECOMMENDED | APPROVE (with note) |
| Example 4.4 — Matbucha | — | APPROVE |
| Example 4.5 — Canned chickpeas | BLOCKING | REVISE |
| Governance checklist §6 | — | APPROVE (one addition) |

---

## Section 1 — Factual & Nutrition-Interpretation Accuracy

### Verified correct

| Claim in framework | Verification |
|---|---|
| Cited generic lines are the per-grade `grade_descriptions` | Confirmed — `hummus_content_v2.json:42-65`. ✓ |
| `explainability_v1.md §5` has no savory-spread translation system | Confirmed — only bread / snack bars / milk. ✓ |
| Matbucha must be described **מבושל**, not **קלוי** | Correct — matbucha is stewed, not roasted (consistent with TASK-064 B-6). ✓ |
| Single-ingredient floor products are "data-conditional, not earned organically" | Correct — matches build report §3.5. ✓ |
| Masabacha is a prepared dip and stays in the ranked set | Nutritionally correct — whole chickpeas in tahini/sauce is a finished dish, not raw material. ✓ |
| Anti-attribution, no-weights, no-NOVA rules | Correctly carried from canonical frameworks. ✓ |

### B-1 — BLOCKING: Section-3 fat-data note is written as a near-universal default and will be mis-applied

**Location:** §3 "Section 3 — uncertainty language" table (row: "fat-data gap (default, 84% of corpus)") and §2 item 7.

**Issue:** The framework labels the fat note as the **default** Section-3 content "84% of corpus." This is true as a corpus statistic but wrong as an authoring instruction. Only **5 of 69 products have `fat_quality_reliable = true`** (`bsip1_7296073705505`, `bsip1_7290018359686`, `bsip1_6666307`, `bsip1_208428`, `bsip1_6666444`). For those five, the statement "ערכי השומן לא היו זמינים במקור הנתונים" is **factually false** — their fat data *was* available and reliable. Writing it as the default is what produced the error in Example 4.1.

**Required correction:** The per-product fat note must be **conditioned strictly on `fat_quality_reliable == false`**. The five fat-reliable products must NOT carry it.

**Important distinction (must be preserved):** The *category-wide mandatory disclosure* (`hummus_content_v2.json.mandatory_disclosure` — "ערכי השומן אינם מוצגים בקטגוריה זו…") is a separate, accurate statement: the fat *dimension* is suppressed from display across the whole category per KL-1, even for the 5 reliable products. That category-level note stays. What is forbidden is the *product-level* claim that fat data "was not available" on a product where it was. The framework conflates the two; the revision must separate them:
- Category level: "fat dimension not displayed for this category" — applies to all.
- Product Section 3: "fat values were not available from the data source" — applies **only** where `fat_quality_reliable == false`.

### No unsupported nutrition inferences elsewhere
Aside from Examples 4.1 and 4.5 (below), no health claims, no "healthy/unhealthy," no dietary advice, and no manufacturer-intent attribution were found. The framework's exclusion list (§2) is complete and correct.

---

## Section 3 — Worked Example Verdicts

Each example cross-checked against its actual `hummus_frontend_v1.json` record.

### 4.1 — A-grade hummus — סלט חומוס (`bsip1_6666307`) → **REVISE**

Record: score 80.2, A, nova 3, `ingredient_count` 5, `additive_count` 1, **`fat_quality_reliable = true`**, state normal.

- Section 1 ("רשימת רכיבים קצרה, בלי מייצבים או עמילן מוסף"): supported — `additive_count` 1 (a single preservative) backs the absence claim. ✓
- Section 2 ("חומר משמר אחד"): correct — `additive_count` 1. ✓
- **Section 3 (fat note): FACTUALLY WRONG.** This product has reliable fat data. The "fat values were not available" sentence must be **removed**; Section 3 should be empty for this product (no caveat applies).

**Required fix:** drop Section 3 entirely from this example, and use it to illustrate the `fat_quality_reliable == true` path (Section 3 omitted) — turning the error into a teaching case.

### 4.2 — B-grade hummus — חומוס (`bsip1_2987963`) → **APPROVE**

Record: 68.2, B, nova 3, `ingredient_count` 10, `additive_count` 3, `fat_quality_reliable = false`.
- 61% chickpea / 15.5% tahini / garlic: declared figures verified in TASK-064. ✓
- Section 2 names preservative + acidity regulator without claiming "one preservative only" — correctly avoids the TASK-064 R-3 trap given `additive_count` 3. ✓
- Fat note correctly present (`fat_quality_reliable = false`). ✓

### 4.3 — C-grade hummus — חומוס עם טחינה אחלה (`bsip1_7290104061417`) → **APPROVE (with note)**

Record: 63.5, C, nova 3, `ingredient_count` 1, `additive_count` **7**, `fat_quality_reliable = false`.
- Direction is correct: lower chickpea share + complex additive list → C. ✓
- 56% / 17% sourced from the approved `hummus_insights_v1.md` line. ✓
- Fat note correct. ✓
- **Note (non-blocking):** the actual `additive_count` is **7** — materially higher than "מייצבים וחומר משמר" implies to a reader. The Section-1 phrase "מבנה רכיבים מורכב יותר" covers it, so this is not a false statement, but Content Agent may strengthen Section 2 to reflect the genuine additive load. Not required.

### 4.4 — Matbucha — סלט מטבוחה (`bsip1_7290010931330`) → **APPROVE**

Record: 61.8, C, nova 3, `ingredient_count` 11, `additive_count` 1, `fat_quality_reliable = false`.
- "63% עגבניות / 13% פלפל": declared figures verified in TASK-064. ✓
- **מבושל** (not קלוי): correct — the exact TASK-064 B-6 fix. ✓
- White sugar "מצוין ברשימה": verified in TASK-064, anti-attribution phrasing correct. ✓
- Correctly notes the two `structural_emptiness`-caveated matbucha products take the caveat string in Section 3 instead. ✓

### 4.5 — Canned chickpeas — הקיסר חומוס ענק (`bsip1_7290018359686`) → **REVISE**

Record: 80.4, A, **nova 3**, **`ingredient_count` 8**, `additive_count` 0, `fat_quality_reliable = true`.

- **Section 1 ("מוצר חד-רכיבי" — single-ingredient): UNSUPPORTED, contradicts the record.** The product carries `ingredient_count` 8 and NOVA 3. TASK-064 R-2 flagged this exact inconsistency ("הקיסר: nova 3, ingredient_count 8 — inconsistent with a single-ingredient product"). Asserting "חד-רכיבי" as fact repeats a claim the data does not support.
- Section 3 (unverified-list caveat) is correct and the fat note was correctly omitted (`fat_quality_reliable = true`). ✓
- The boundary-treatment line is appropriate.

**Required fix:** reframe Section 1 to describe the product by its label identity *without asserting single-ingredient status* — e.g. "גרגירי חומוס שלמים בשימור — מוצר על בסיס גרגירי חומוס שלמים, ולא ממרח מוכן." Keep the Section-3 caveat that the ingredient detail was not verifiable (which is precisely *why* "חד-רכיבי" cannot be claimed). The two must be consistent: if the list is unverified, the explanation cannot simultaneously assert the list has one item.

**Scoring-path note for the companion review:** הקיסר reaches A via `additive_count` 0 on an unverified/marketing-copy list — **not** via the NOVA-1 single-ingredient floor (it is NOVA 3). This strengthens, not weakens, the boundary recommendation: its A grade rests on absent ingredient data, exactly the data-integrity concern the boundary review raises.

---

## Section 4 — Required Revisions (checklist)

- [ ] **B-1:** Rewrite Section-3 fat guidance — condition the product-level fat note on `fat_quality_reliable == false`; separate it explicitly from the category-wide mandatory disclosure. Name the 5 fat-reliable PIDs as exceptions.
- [ ] **4.1:** Remove the fat note from Example 4.1; re-cast it as the fat-reliable (Section 3 omitted) path.
- [ ] **4.5:** Remove the "חד-רכיבי" assertion; reframe by label identity; keep the unverified-list caveat.
- [ ] **§6 governance checklist addition:** add a line — *"Product-level fat note appears only where `fat_quality_reliable == false`; never on the 5 fat-reliable products."*
- [ ] (Optional, 4.3) strengthen Section 2 to reflect `additive_count` 7.

When B-1, 4.1, and 4.5 are corrected, this review upgrades to **APPROVE**. Examples 4.2, 4.3, 4.4 are accurate as written.

---

*Nutrition Agent — TASK-076 — 2026-05-31*
*Verdict: REVISIONS REQUIRED. Framework rules approved; two examples and the fat-note guidance require correction.*
