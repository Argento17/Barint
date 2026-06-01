# Four Category MVP Rollout Plan v1
**Date:** 2026-05-30
**Goal:** 70% MVP — all four categories live on /hashvaot/ with recalibrated scoring and shared Milk/Snacks format
**Status:** Planning → Implementation

---

## Summary Table

| Category | Route | Data | Component | Format | Scoring | Launch |
|---|---|---|---|---|---|---|
| Milk | `/hashvaot/milk-comparison` | ✓ 18 products | ✓ MilkComparisonPage | ✓ Reference | Hand-curated | **LIVE NOW** |
| Snacks | `/hashvaot/snacks` | ✓ 18 products | ✓ SnacksComparisonDesktopPage | ✓ Updated | BSIP2 (recal needed) | **LIVE — rescore** |
| Bread | `/hashvaot/bread` | ✓ 24 products | ✗ Old ComparisonShelfPage | ✗ Old format | BSIP2 (recal needed) | **Needs component swap + rescore** |
| Yogurts | `/hashvaot/yogurts` | ✗ No data | ✗ No component | ✗ None | None | **Blocked — create data first** |

---

## Category 1: Milk

**Route:** `/hashvaot/milk-comparison`  
**Status:** LIVE ✓ — Reference implementation

### What exists
- `MilkComparisonPage` — custom component, reference for all categories
- `src/data/milk-comparison.json` — 18 products, custom schema (NOT BariProductVM)
- Filters: milk type (dairy/oat/soy/almond/rice) + trait (protein, low sugar, etc.)
- Scores: 70–90, A/B grades. Hand-curated, not from BSIP2.

### Required for MVP
- Nothing. Already live and correct.

### Post-MVP
- Consider BSIP2 re-run for milk to generate engine-backed scores
- When/if milk re-runs, apply R-04 (dairy sugar relief)
- Consider migrating to BariProductVM format for consistency

### Launch readiness: ✅ LIVE

---

## Category 2: Snacks

**Route:** `/hashvaot/snacks`  
**Status:** LIVE ✓ — Component updated to milk format, needs rescore

### What exists
- `SnacksComparisonDesktopPage` — milk-aligned desktop component ✓
- `src/data/comparisons/snacks_frontend_v2.json` — 18 products, BariProductVM
- Filters: date-based, oat-cereal, wellness, grade-e
- Scores: 17–70, E/D/C/B. BSIP2-derived.

### Required for MVP
1. Apply scoring recalibration R-01, R-02, R-03 in `score_engine.py` and `constants.py`
2. Re-run BSIP2 on snacks corpus
3. Update `snacks_frontend_v2.json` with new scores and grades
4. Update grade fields if any products cross grade boundaries

### Known data gaps
- Nutrition values (kcal, protein, sugar, fat, fiber) are mostly null — scraped label data was incomplete
- This is acceptable for MVP
- Ingredient text available for most products

### Launch readiness: ✅ LIVE — rescore before promotion

---

## Category 3: Bread

**Route:** `/hashvaot/bread`  
**Status:** Live but wrong format — needs component swap

### What exists
- `BreadComparisonPage` (wraps old `ComparisonShelfPage`) — WRONG format
- `src/data/comparisons/bread_frontend_v2.json` — 24 products, BariProductVM
- Filters: everyday, fermentation (מחמצת), strong (מלא ודגנים), wellness_ambig (לחמי בריאות), crackers
- Scores: 59–82, C/B/A grades
- Route: `/hashvaot/bread` (active)

### Data issue: Grade inconsistency
- Product "לחם ירוק מקמח מלא" shows `score: 80, grade: "B"` — incorrect (80 ≥ 80 = A)
- Audit bread JSON for all grade/score mismatches before rescore

### Required for MVP
1. Create `BreadComparisonDesktopPage` following `SnacksComparisonDesktopPage` pattern (see Cursor handoff)
2. Update `/hashvaot/bread/page.tsx` to use new component
3. Apply scoring recalibration R-01, R-02, R-03 in BSIP2 engine
4. Re-run BSIP2 on bread corpus
5. Update `bread_frontend_v2.json` with new scores
6. Fix grade/score mismatches

### Post-recalibration expected grade changes
- Sourdough whole grain breads: B → A (≈ 3–5 products)
- Standard whole grain: stays B but higher numeric score
- Low-quality standard bread: stays C (scores 59–64), no change
- Crackers (spelt): stays A, scores rise 2–5 pts

### Launch readiness: 🟡 Needs component swap + rescore (~1 day work)

---

## Category 4: Yogurts

**Route:** `/hashvaot/yogurts` (does not exist)  
**Status:** NOT READY — requires data creation

### What exists
- Nothing. No data file, no component, no route.

### Path to MVP

**Option A (recommended): Manual corpus creation (1–2 days)**
1. Define a corpus of 12–15 well-known Israeli yogurt products
2. Manually assign scores using BSIP2 scoring logic + R-01–R-05 calibration
3. Create `src/data/comparisons/yogurts_frontend_v1.json`
4. Write expansion content (positiveSignals, limitingFactors, bottomLine)
5. Build `YogurtsComparisonDesktopPage` following snacks pattern
6. Register route `/hashvaot/yogurts`

**Option B: Full BSIP2 run**
- Requires scraping Israeli yogurt labels
- More accurate but takes 3–5 days
- Better for post-MVP

### Proposed yogurt corpus (12 minimum products)
Products to include:
- תנובה יוגורט 3% — plain whole milk, NOVA1 — target score: 88/A
- יוגורט 0% — skim plain, NOVA1 — target: 83/A
- ביו 1.5% — bio-cultured, fermented markers — target: 87/A (+R-02)
- דנונה אקטיביה — NOVA3 bio yogurt, fruit — target: 72/B
- יופלה פטל/תות — NOVA3 flavored, sugar — target: 65/B
- יופלה GO — higher protein variant — target: 72/B (as scored in מעדנים run)
- מילקי יוגורט — NOVA4 style dessert — target: 42/D
- סויה יוגורט נטורל — non-dairy plain, NOVA2 — target: 75/B
- יוגורט קוקוס — non-dairy flavored, additives — target: 55/C
- יוגורט יווני 5% — strained, high protein, NOVA2 — target: 84/A
- יוגורט לבן גבישים — drinking yogurt, added sugar — target: 60/C
- סנו לייף יוגורט — flavored, sweetener — target: 52/C

### Filters for yogurt
- `plain` — plain/unflavored only
- `greek` — strained/Greek style
- `dairy-free` — non-dairy alternatives
- `high-protein` — protein ≥ 8g/100g
- `no-added-sugar` — no sucrose, no sweeteners

### Launch readiness: 🔴 Blocked — create data first (estimated: 2 days)

---

## Rollout Sequence

**Week 1:**
1. Implement R-01, R-02, R-03 in BSIP2 engine (scoring recalibration)
2. Re-run BSIP2 snacks + bread
3. Update snacks_frontend_v2.json and bread_frontend_v2.json
4. Build `BreadComparisonDesktopPage` component
5. Swap `/hashvaot/bread` route to new component

**Week 2:**
1. Create yogurt corpus JSON (manual scoring)
2. Write yogurt expansion content
3. Build `YogurtsComparisonDesktopPage` component
4. Register `/hashvaot/yogurts` route
5. QA all four categories

**Week 3:**
1. Implement R-04 (dairy sugar relief) if needed for milk/yogurt accuracy
2. Implement R-06 (whole grain primary bonus, SHOULD-HAVE)
3. Final QA pass
4. Promote all four categories

---

## 70% MVP Acceptance Criteria

All four categories must meet these bars before promotion:

- [ ] Page loads on desktop and mobile
- [ ] ≥10 products displayed (yogurt: ≥12)
- [ ] Scores visible on all products
- [ ] Rankings preserved after recalibration
- [ ] Images present on ≥90% of products
- [ ] Expansion panel opens with product-specific content
- [ ] No internal scoring language in consumer-facing text
- [ ] No NOVA labels in shelf-facing fields
- [ ] Methodology section present
- [ ] Filters functional
- [ ] RTL correct
- [ ] Mobile layout preserved

NOT blocking MVP:
- Full nutrition data (nulls are acceptable)
- Ingredient text on all products
- Blog content
- yogurt BSIP2-derived scores (manual OK)
