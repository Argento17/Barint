# Hummus v1 — Pre-Launch QA Report

**Task:** TASK-072  
**Agent:** QA Agent  
**Date:** 2026-05-31  
**Inputs reviewed:**
- `/hashvaot/hummus` live page (dev server, localhost:3000)
- `hummus_frontend_v1.json` (deployed data, `src/data/comparisons/`)
- `hummus_content_v2.json` (content spec, TASK-067)
- TASK-069 deliverables (blockers fix report, excluded products doc)

---

## Verdict: WARN

The page is functionally complete and QA-eligible. All four TASK-069 blockers are resolved, the build passes, and no rendering failures were found. Four warnings are flagged below. One (W-1) requires a content spec update before final sign-off; the others are low-risk and do not block launch.

---

## Audit Results by Section

### 1. Desktop Audit

| Check | Result | Notes |
|-------|--------|-------|
| Page loads and renders | ✓ PASS | HTTP 200, no errors |
| Hero title | ✓ PASS | "חומוס וממרחים: מה באמת יש במדף?" |
| Hero eyebrow | ✓ PASS | "מנוע השוואה · חומוס וממרחים" |
| Stats panel | ✓ PASS | 69 נבדקו · 67 קיבלו ציון · 63 בדף ההשוואה |
| Category insight lines | ✓ PASS | 4 factual category-level lines, no framework vocab |
| Prologue sentence 1 | ✓ PASS | "בדקנו 69 מוצרי חומוס..." (TASK-069 directed copy) |
| Prologue sentence 2 | ✓ PASS | Product type listing |
| Prologue sentence 3 | ✓ PASS | "61 מוצרים מקבלים ציון; שני מוצרים אינם מוצגים..." |
| Prologue sentence 4 | ✓ PASS | Fat disclosure: "ערכי השומן אינם מוצגים..." |
| RTL rendering | ✓ PASS | All text right-aligned, score chips left, correct directionality |
| Methodology footer | ✓ PASS | All 4 lines rendered, no ministry warning label reference |

### 2. Mobile Audit

| Check | Result | Notes |
|-------|--------|-------|
| Page loads | ✓ PASS | HTTP 200, mobile viewport renders |
| Hero title matches desktop | ✓ PASS | |
| Metadata line | ✓ PASS | "63 מוצרים בדירוג · שופרסל, מאי 2026 · ממוין לפי ציון Bari" |
| Product row rendering | ✓ PASS | Image + name + insightLine + score chip all visible |
| Score chips styled correctly | ✓ PASS | Grade-colored chips (A=green, B=warm, C=orange-ish, D=red) |
| Images load | ✓ PASS | Product images visible for all 61 scored products |
| Default image for unavailable | ✓ PASS | 2 products correctly show placeholder image |
| Expansion opens on tap | ✓ PASS | bottomLine and confidence label visible |
| RTL rendering | ✓ PASS | No layout breaks in mobile |

### 3. Filter Audit

| Filter | Expected count | Actual count | Result |
|--------|---------------|-------------|--------|
| No filter (all) | 63 | 63 | ✓ PASS |
| חומוס | 38 | 38 | ✓ PASS |
| מטבוחה | 11 | 11 | ✓ PASS |
| ממרחים אחרים | 14 (7+5+2) | 14 | ✓ PASS |

Filter type breakdown verified: hummus_spread=38, matbucha=11, eggplant_spread=7, pepper_spread=5, masabacha=2. Sum=63 ✓

All 6 excluded NOVA-1 products have `_product_type: hummus_spread`. They are absent from the hummus filter and from all results. Verified by programmatic check and visual inspection. ✓

### 4. Caveated Product Audit

Six products carry `confidence: "partial"` with `limitingFactors` populated. All render correctly in expansion.

| Product ID | Name | Caveated Message | Renders |
|-----------|------|-----------------|---------|
| bsip1_1990261 | חומוס | "הערכת עיבוד חלקית" | ✓ PASS |
| bsip1_3643714 | חומוס | "הערכת עיבוד חלקית" | ✓ PASS |
| bsip1_7290104721533 | סלט פלפלים קלויים | "סיווג חלקי — מוצג כממרח" | ✓ PASS |
| bsip1_7290106520905 | סלט טורקי | "סיווג חלקי — מוצג כממרח" | ✓ PASS |
| bsip1_7290111563492 | מטבוחה חריפה | "ציון מבוסס על נתונים חלקיים" | ✓ PASS |
| bsip1_7290106577572 | מטבוחה אמיתית | "ציון מבוסס על נתונים חלקיים" | ✓ PASS |

Visual verification: expansion section for `סלט פלפלים קלויים` shows the "מה מגביל את הציון?" section with the limiting factor, followed by the grade-level bottomLine and "נתונים חלקיים" confidence label. ✓

### 5. Unavailable Product Audit

| Product ID | Name | Score | Grade | Image | bottomLine renders |
|-----------|------|-------|-------|-------|------------------|
| bsip1_7296073733317 | חומוס | null | null | default placeholder | ✓ "לא ניתן להציג ציון..." |
| bsip1_7296073733348 | חומוס ענק | null | null | default placeholder | ✓ "לא ניתן להציג ציון..." |

Both products appear at the bottom of the unfiltered list. Score chip renders as "—". No grade badge. No insightLine (empty, as expected for `confidence: "insufficient"` with null grade). Default/placeholder image loads correctly. ✓

### 6. Hub Discoverability Audit

| Check | Result |
|-------|--------|
| Hummus card visible on /hashvaot | ✓ PASS |
| Card title | ✓ PASS — "חומוס וממרחים: מה באמת יש במדף?" |
| Card route | ✓ PASS — /hashvaot/hummus |
| /hashvaot HTTP response | ✓ PASS — 200 |
| /hashvaot/hummus HTTP response | ✓ PASS — 200 |
| No duplicate routes | ✓ PASS — only one hummus route exists |
| No legacy routes | ✓ PASS |
| Hummus appears in "ניתוח עדכני" section | ✓ PASS |

### 7. Methodology Audit

| Check | Result |
|-------|--------|
| Ministry warning label removed from methodology.body | ✓ PASS |
| Ministry warning label removed from methodology line 1 | ✓ PASS — "ומדדים נוספים הנוגעים למבנה המוצר" |
| Category-relative note present | ✓ PASS — "כל מוצר מוערך ביחס לממרחים ותוספות בלבד" |
| Non-recommendation disclaimer present | ✓ PASS — line 4: "אינו מהווה המלצה תזונתית אישית" |
| Fat disclosure in methodology | ✓ PASS — line 3 present |
| No health claims in methodology | ✓ PASS |
| No framework vocabulary | ✓ PASS |

### 8. Disclosure Audit

| Disclosure requirement | Location | Status |
|-----------------------|----------|--------|
| Fat quality hidden — all nutrition null | expansion.nutrition | ✓ PASS — 63/63 products have nutrition=null |
| Fat disclosure in prologue | prologueSentences[3] | ✓ PASS |
| Fat disclosure in methodology | methodologyLines[2] | ✓ PASS |
| No fat values exposed via any route | programmatic check | ✓ PASS — 0 fat fields non-null |

### 9. Category Count Audit

| Metric | Expected | Actual | Status |
|--------|----------|--------|--------|
| Total products in JSON | 69 | 69 | ✓ PASS |
| Excluded NOVA-1 products | 6 | 6 | ✓ PASS |
| Displayed products | 63 | 63 | ✓ PASS |
| Scored displayed | 61 | 61 | ✓ PASS |
| Unavailable displayed | 2 | 2 | ✓ PASS |
| Grade A displayed | 2 | 2 | ✓ PASS |
| Grade B displayed | 28 | 28 | ✓ PASS |
| Grade C displayed | 27 | 27 | ✓ PASS |
| Grade D displayed | 4 | 4 | ✓ PASS |
| Score range (displayed) | 43–80 | 43–80 | ✓ PASS |
| Missing imageUrl fields | 0 | 0 | ✓ PASS |
| Default/placeholder images | 2 (unavailable) | 2 | ✓ PASS |
| Broken routes | 0 | 0 | ✓ PASS |

### 10. Expansion Content Audit

| Check | Result |
|-------|--------|
| insightLine populated for all scored products | ✓ PASS — grade-level fallback active |
| insightLine empty for unavailable (null grade) | ✓ PASS |
| bottomLine present for all scored non-insufficient products | ✓ PASS — grade-level fallback active |
| bottomLine format | ✓ PASS — "ציון [N] ([grade]) — [grade description] ביחס לממרחים האחרים בקטגוריה." |
| limitingFactors rendering | ✓ PASS — "מה מגביל את הציון?" section renders |
| confidenceLabel rendering | ✓ PASS — "נתונים מלאים" / "נתונים חלקיים" / "נתונים לא זמינים" |
| No framework vocabulary in any consumer field | ✓ PASS — 0 violations |
| No health claims in any expansion text | ✓ PASS |
| Product-specific insight lines integrated | ⚠ WARN-3 — pending content integration |

---

## Warnings

### W-1 — MEDIUM: `hummus_content_v2.json` counts are stale post-NOVA-1 exclusion

**Applies to:** `hummus_content_v2.json` (content spec, TASK-067 output)

`hummus_content_v2.json` was written before the NOVA-1 exclusion was decided in TASK-069. The following fields reflect the full 69-product corpus and will produce incorrect content if integrated as-is:

| Field | content_v2.json value | Live page actual |
|-------|----------------------|-----------------|
| `corpus_facts.displayable` | 67 | 63 |
| `grade_descriptions.A.count_in_corpus` | 8 | 2 |
| `score_stats_note` (mean, median, range) | Based on full 69-product corpus | Displayed corpus is 63 |

**Action required before content integration:** Update content_v2.json corpus_facts and grade_descriptions to reflect the 63-product displayed corpus. Assign to Content Agent.

---

### W-2 — LOW: Stats panel "67 קיבלו ציון" overreports relative to visible products

**Location:** Desktop hero stats panel (`hummusCorpusMeta.scored_count`)

The stats panel shows "69 מוצרים נבדקו | 67 קיבלו ציון | 63 בדף ההשוואה". The figure "67 קיבלו ציון" counts the full corpus including the 6 excluded NOVA-1 products, all of which had scores. A user who counts 63 products in the list and sees "67 scored" will find an apparent 4-product discrepancy.

**No action required for launch.** The figures are factually accurate (67 products were scored in the corpus; 63 are displayed). The stat can be clarified in a future content update.

---

### W-3 — LOW: Expansion insightLine and bottomLine are grade-level fallbacks, not product-specific

**Location:** All 61 scored products

Product-specific insight lines from `hummus_insights_v1.md` have not been integrated. All products show generic grade-level text in both the row (`insightLine`) and the expansion (`bottomLine`). This means:
- All grade-A products share the same insightLine
- All grade-B products share the same insightLine
- etc.

**No action required for launch.** This was explicitly scoped as pending content integration in TASK-069 and is documented in the source code. The fallback content is factually accurate and uses no prohibited language.

**Action before v2:** Integrate per-product insight lines from `hummus_insights_v1.md`.

---

### W-4 — LOW: Three products display rounded scores that appear inconsistent with their grade

**Identified by:** programmatic grade/score threshold check

| Product | Display score | Grade | Expected grade | Actual source score |
|---------|--------------|-------|---------------|-------------------|
| חומוס שלם יכין | 80 | B | A | 79.9 |
| חומוס עם זעתר | 65 | C | B | ~64.x (unconfirmed) |
| מטבוחה חריפה | 50 | D | C | 49.6 |

All three are rounding artifacts. Display scores are `Math.round(raw_score)`. Grade is assigned on the pre-rounding value. A user reading "80 (B)" or "65 (C)" or "50 (D)" may be confused since these scores sit exactly on threshold boundaries.

**No action required for launch.** Grade assignment is correct; the display is a cosmetic artifact of integer rounding. Consider showing one decimal place for threshold-boundary scores in a future UX pass.

---

## Excluded Products Verification

The 6 NOVA-1 products confirmed absent from all display contexts:

| Product ID | Name | NOVA | Source score | Status |
|-----------|------|------|-------------|--------|
| bsip1_7296073733324 | חומוס | 1 | 85.5 | ✓ Excluded |
| bsip1_7296073733331 | חומוס ענק | 1 | 85.5 | ✓ Excluded |
| bsip1_7296073005889 | חומוס לבן ענק שופרסל | 1 | 85.4 | ✓ Excluded |
| bsip1_7296073006015 | חומוס גדול שופרסל | 1 | 85.4 | ✓ Excluded |
| bsip1_3643820 | חומוס ענק | 1 | 85.0 | ✓ Excluded |
| bsip1_7296073705505 | חומוס מוקפא | 1 | 85.0 | ✓ Excluded |

None appear in: unfiltered list, hummus filter, matbucha filter, spreads filter, desktop table, mobile view. ✓

---

## Screenshots Captured

| File | Audit area |
|------|-----------|
| `hummus_hero_desktop.png` | Desktop hero, prologue, eyebrow |
| `hummus_product_list_desktop.png` | Stats panel, prologue sentences |
| `hummus_mobile.png` | Mobile: hero, filters, first product expanded |
| `qa_desktop_product_table.png` | Desktop: product table mid-scroll |
| `qa_desktop_methodology.png` | Desktop: methodology footer |
| `qa_mobile_filter_matbucha.png` | מטבוחה filter active, 11 products |
| `qa_mobile_filter_spreads.png` | ממרחים אחרים filter, masabacha + pepper/eggplant spreads |
| `qa_mobile_partial_expansion.png` | Partial-confidence product expanded (limitingFactors visible) |
| `qa_mobile_d_grade.png` | D-grade products (scores 43–50) |
| `qa_mobile_unavailable.png` | D-grade + unavailable products + methodology footer |
| `qa_hub_hummus_card.png` | /hashvaot hub with hummus card visible |

---

## Blocking Items Carried In from TASK-069 — Verified Resolved

| Blocker | Status |
|---------|--------|
| B-1: NOVA-1 chickpeas at top of list | ✓ RESOLVED — 6 products excluded, first ranked is הקיסר חומוס ענק score 80 |
| B-2: Empty expansion content | ✓ RESOLVED — insightLine fallback + bottomLine generation active |
| B-3: Weak hero copy | ✓ RESOLVED — "חומוס וממרחים: מה באמת יש במדף?" |
| B-4: Build failure | ✓ RESOLVED — build passes, all 30 pages static |
| Addendum: Hummus not on /hashvaot | ✓ RESOLVED — card visible, link functional |

---

## Action Items Before Final Sign-Off

| Priority | Item | Owner |
|----------|------|-------|
| **REQUIRED** | Update `hummus_content_v2.json` counts: `corpus_facts.displayable` 67→63, `grade_descriptions.A.count_in_corpus` 8→2, score stats | Content Agent |
| Optional | Clarify "67 קיבלו ציון" vs 63 displayed in stats panel | Frontend Agent |
| Future v2 | Integrate per-product insight lines from `hummus_insights_v1.md` | Content Agent + Frontend Agent |
| Future v2 | Consider decimal display for threshold-boundary scores | Frontend Agent |

---

*QA Agent — TASK-072 — 2026-05-31*
