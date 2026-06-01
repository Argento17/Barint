# Hummus Routing Fix — Comparison Report

**Generated:** 2026-05-31 04:43 UTC
**Fix:** router_v2.py — added savory-spread hard anchors and exclusions
**Corpus:** Shufersal hummus, 69 products
**Baseline run:** run_hummus_001 (old routing)
**Fixed run:** run_hummus_002 (router_v2 with savory anchors)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total products | 69 |
| Products rerouted | **64** |
| Products unchanged | 5 |
| Grade changes | 12 |
| Score increases (rerouted) | 41 |
| Score decreases (rerouted) | 7 |
| Old corpus mean score | 64.6 |
| New corpus mean score | 65.2 |
| Mean score delta (all) | 0.6 |
| Mean score delta (rerouted only) | 0.6 |

---

## Root Causes Fixed

**RC-1: `"מוס"` (mousse) substring fires on `"חומוס"` (hummus)**

The Stage 2 signal `("מוס", 0.85, "name_weighted")` in `_DESSERT` matches as a
substring of "חומוס", giving dessert score = 1.70. The `"חומוס"` signal in `_SAUCE`
also gives sauce_spread = 1.70. They tie; Python's stable dict sort puts `dessert`
before `sauce_spread` in CATEGORIES ordering → dessert wins every tie.

**Fix:** Added `"חומוס"` as a hard anchor for `sauce_spread` at confidence 0.94.
Hard anchors bypass Stage 2 entirely, eliminating the substring collision.

**RC-2: `"טחינה"` anchor (conf=0.93) reroutes hummus+tahini products to `whole_food_fat`**

Products named e.g. "חומוס עם טחינה 16.9%" triggered the `"טחינה"` anchor first.
Since `"טחינה"` conf=0.93 > `"חומוס"` was not in anchors, tahini won.

**Fix:** `"חומוס"` anchor at conf=0.94 beats `"טחינה"` at 0.93. Added ANCHOR_EXCLUSIONS
for `"טחינה"`: excludes when `"חציל"` or `"חצילים"` appears in name (eggplant+tahini
dishes are spreads, not tahini products).

**RC-3: `"מטבוחה"`, `"מסבחה"`, `"חציל"`, `"חצילים"` had zero sauce_spread signals**

These product types had no matching signals and fell through to `default` with
low-confidence routing.

**Fix:** Added hard anchors: `"מטבוחה"` and `"מסבחה"` at 0.92; `"חצילים"` and
`"חציל"` at 0.91; `"ממרח פלפלים"` at 0.92; `"פלפל צ'ומה"` at 0.91.
Also added backup `_SAUCE` signals for all terms.

**RC-4: `"מעדן"` anchor fires on `"מעדן חצילים"` (eggplant delicacy) → dessert**

**Fix:** Added `"חציל"` and `"חצילים"` to ANCHOR_EXCLUSIONS for `"מעדן"`.

---

## Routing Change Summary

| Old Category → New Category | Count |
|---|---|
| dessert → sauce_spread | 44 |
| default → sauce_spread | 13 |
| whole_food_fat → sauce_spread | 7 |

---

## Per-Product Delta Table

Products that changed category (sorted by score delta descending):

| Product                  | Old Category   | New Category | Old Score | New Score | Δ Score | Grade             |
|--------------------------|----------------|--------------|-----------|-----------|---------|-------------------|
| חומוס                    | dessert        | sauce_spread | 69.6      | 72.6      | +3.0    | B                 |
| חומוס                    | dessert        | sauce_spread | 69.6      | 72.6      | +3.0    | B                 |
| מלך החומוס סמיר הגדול    | dessert        | sauce_spread | 61.4      | 64.4      | +3.0    | C                 |
| מלך החומוס אבו מרוואן    | dessert        | sauce_spread | 62.2      | 65.2      | +3.0    | C→B               |
| חומוס לבנוני צבר         | dessert        | sauce_spread | 62.1      | 65.1      | +3.0    | C→B               |
| חומוס גרגרים בתטבילה     | dessert        | sauce_spread | 60.1      | 63.1      | +3.0    | C                 |
| חומוס מועשר 40% עם חריף  | dessert        | sauce_spread | 62.4      | 65.4      | +3.0    | C→B               |
| סלט חומוס+מסבחה          | dessert        | sauce_spread | 65.2      | 68.2      | +3.0    | B                 |
| חומוס אבו גוש            | dessert        | sauce_spread | 66.9      | 69.9      | +3.0    | B                 |
| חומוס מסעדות             | dessert        | sauce_spread | 72.7      | 75.7      | +3.0    | B                 |
| חומוס אסלי               | dessert        | sauce_spread | 67.6      | 70.6      | +3.0    | B                 |
| חומוס                    | dessert        | sauce_spread | 67.6      | 70.6      | +3.0    | B                 |
| פלפל צ'ומה               | default        | sauce_spread | 49.6      | 51.0      | +1.4    | D→C               |
| סלט חומוס                | dessert        | sauce_spread | 79.4      | 80.2      | +0.8    | B→A               |
| חומוס עם זעתר            | dessert        | sauce_spread | 64.4      | 65.2      | +0.8    | C→B               |
| חומוס עם חריף אחלה       | dessert        | sauce_spread | 62.3      | 63.1      | +0.8    | C                 |
| סלט חציל בטעם כבד        | dessert        | sauce_spread | 55.3      | 56.1      | +0.8    | C                 |
| חומוס צנובר צבר          | dessert        | sauce_spread | 66.3      | 67.1      | +0.8    | B                 |
| חומוס אבו גוש+צנובר+חריף | dessert        | sauce_spread | 63.4      | 64.2      | +0.8    | C                 |
| חומוס גלילי              | dessert        | sauce_spread | 68.3      | 69.1      | +0.8    | B                 |
| חומוס עם חריף            | dessert        | sauce_spread | 61.9      | 62.7      | +0.8    | C                 |
| חומוס עם חציל פיקנטי     | dessert        | sauce_spread | 57.1      | 57.9      | +0.8    | C                 |
| חומוס ישראלי             | dessert        | sauce_spread | 67.5      | 68.3      | +0.8    | B                 |
| חומוס מסבחה              | dessert        | sauce_spread | 63.4      | 64.2      | +0.8    | C                 |
| מעדן חצילים              | dessert        | sauce_spread | 57.3      | 58.1      | +0.8    | C                 |
| חומוס                    | dessert        | sauce_spread | 67.5      | 68.2      | +0.7    | B                 |
| חומוס מסעדה              | dessert        | sauce_spread | 67.7      | 68.4      | +0.7    | B                 |
| חומוס יום יום            | dessert        | sauce_spread | 67.7      | 68.4      | +0.7    | B                 |
| הקיסר חומוס ענק          | dessert        | sauce_spread | 79.7      | 80.4      | +0.7    | B→A               |
| חומוס עם צנובר אחלה      | dessert        | sauce_spread | 64.7      | 65.4      | +0.7    | C→B               |
| חומוס                    | dessert        | sauce_spread | 67.7      | 68.4      | +0.7    | B                 |
| חומוס מסעדה              | dessert        | sauce_spread | 67.7      | 68.4      | +0.7    | B                 |
| חומוס מסעדה צבר          | dessert        | sauce_spread | 64.7      | 65.4      | +0.7    | C→B               |
| חומוס גלילי              | dessert        | sauce_spread | 68.2      | 68.9      | +0.7    | B                 |
| חומוס עם זעתר            | dessert        | sauce_spread | 64.1      | 64.8      | +0.7    | C                 |
| חומוס עם מלא מטבוחה חריף | dessert        | sauce_spread | 64.5      | 65.2      | +0.7    | C→B               |
| חומוס                    | dessert        | sauce_spread | 67.5      | 68.2      | +0.7    | B                 |
| חומוס                    | dessert        | sauce_spread | 85        | 85.5      | +0.5    | A                 |
| חומוס ענק                | dessert        | sauce_spread | 85        | 85.5      | +0.5    | A                 |
| חומוס לבן ענק שופרסל     | dessert        | sauce_spread | 85        | 85.4      | +0.4    | A                 |
| חומוס גדול שופרסל        | dessert        | sauce_spread | 85        | 85.4      | +0.4    | A                 |
| חומוס ענק                | dessert        | sauce_spread | 85        | 85        | +0.0    | A                 |
| סלט מטבוחה               | default        | sauce_spread | 60.4      | 60.4      | +0.0    | C                 |
| סלט מטבוחה               | default        | sauce_spread | 61.8      | 61.8      | +0.0    | C                 |
| סלט מטבוחה מרוקאית       | default        | sauce_spread | 61.5      | 61.5      | +0.0    | C                 |
| מטבוחה אמיתית            | default        | sauce_spread | 48.7      | 48.7      | +0.0    | D                 |
| מטבוחה חריפה אש          | default        | sauce_spread | 62.0      | 62.0      | +0.0    | C                 |
| מטבוחה חריפה             | default        | sauce_spread | 49.6      | 49.6      | +0.0    | D                 |
| חציל על האש              | default        | sauce_spread | 58.0      | 58.0      | +0.0    | C                 |
| ממרח פלפלים קלויים       | whole_food_fat | sauce_spread | 48.0      | 48.0      | +0.0    | D                 |
| חומוס מוקפא              | dessert        | sauce_spread | 85        | 85        | +0.0    | A                 |
| סלט חצילים על האש        | default        | sauce_spread | 61.6      | 61.6      | +0.0    | C                 |
| סלט מטבוחה פיקנטי        | default        | sauce_spread | 52.0      | 52.0      | +0.0    | C                 |
| מטבוחה פיקנטית           | default        | sauce_spread | 52.0      | 52.0      | +0.0    | C                 |
| חומוס                    | dessert        | sauce_spread | 50        | 50        | +0.0    | insufficient_data |
| חומוס ענק                | dessert        | sauce_spread | 50        | 50        | +0.0    | insufficient_data |
| סלט מטבוחה יום יום       | default        | sauce_spread | 61.8      | 61.8      | +0.0    | C                 |
| סלט חציל פיקנטי          | default        | sauce_spread | 56.4      | 54.2      | -2.2    | C                 |
| חציל על האש בטחינה       | whole_food_fat | sauce_spread | 52.2      | 50.0      | -2.2    | C                 |
| חומוס אבו מרוואן26%טחינה | whole_food_fat | sauce_spread | 67.4      | 65.2      | -2.2    | B                 |
| סלט חומוס עם טחינה       | whole_food_fat | sauce_spread | 70.7      | 68.5      | -2.2    | B                 |
| חומוס עם טחינה אחלה      | whole_food_fat | sauce_spread | 65.8      | 63.5      | -2.3    | B→C               |
| חומוס עם טחינה צבר       | whole_food_fat | sauce_spread | 65.7      | 63.4      | -2.3    | B→C               |
| חומוס עשיר ב40% טחינה    | whole_food_fat | sauce_spread | 72.8      | 68.3      | -4.5    | B                 |

---

## Unchanged Routing (for completeness)

| Product | Category | Score |
|---------|----------|-------|
| חומוס שלם יכין | sauce_spread | 79.9 |
| סלט פלפלים קלויים | default | 63.5 |
| סלט טורקי | default | 60.4 |
| ממרח פלפלים קלויים | sauce_spread | 59.6 |
| ממרח פלפלים קלויים | sauce_spread | 42.8 |

---

## Grade Distribution Comparison

| Grade | Old Count | New Count | Change |
|-------|-----------|-----------|--------|
| A | 6 | 8 | +2 |
| B | 25 | 28 | +3 |
| C | 31 | 27 | -4 |
| D | 5 | 4 | -1 |
| E | 0 | 0 | — |
| insufficient_data | 2 | 2 | — |

---

## New Category Routing Distribution

| Category | Old Count | New Count |
|----------|-----------|-----------|
| default | 15 | 2 |
| dessert | 44 | 0 |
| sauce_spread | 3 | 67 |
| whole_food_fat | 7 | 0 |

---

## Top 10 — Old vs New

### Old Top 10 (run_hummus_001)

| Product               | Old Score | Old Grade | Old Category   | New Score | Δ Score |
|-----------------------|-----------|-----------|----------------|-----------|---------|
| חומוס ענק             | 85        | A         | dessert        | 85        | +0.0    |
| חומוס לבן ענק שופרסל  | 85        | A         | dessert        | 85.4      | +0.4    |
| חומוס גדול שופרסל     | 85        | A         | dessert        | 85.4      | +0.4    |
| חומוס מוקפא           | 85        | A         | dessert        | 85        | +0.0    |
| חומוס                 | 85        | A         | dessert        | 85.5      | +0.5    |
| חומוס ענק             | 85        | A         | dessert        | 85.5      | +0.5    |
| חומוס שלם יכין        | 79.9      | B         | sauce_spread   | 79.9      | +0.0    |
| הקיסר חומוס ענק       | 79.7      | B         | dessert        | 80.4      | +0.7    |
| סלט חומוס             | 79.4      | B         | dessert        | 80.2      | +0.8    |
| חומוס עשיר ב40% טחינה | 72.8      | B         | whole_food_fat | 68.3      | -4.5    |

### New Top 10 (run_hummus_002 — fixed routing)

| Product              | New Score | New Grade | New Category | Old Score | Δ Score |
|----------------------|-----------|-----------|--------------|-----------|---------|
| חומוס                | 85.5      | A         | sauce_spread | 85        | +0.5    |
| חומוס ענק            | 85.5      | A         | sauce_spread | 85        | +0.5    |
| חומוס לבן ענק שופרסל | 85.4      | A         | sauce_spread | 85        | +0.4    |
| חומוס גדול שופרסל    | 85.4      | A         | sauce_spread | 85        | +0.4    |
| חומוס ענק            | 85        | A         | sauce_spread | 85        | +0.0    |
| חומוס מוקפא          | 85        | A         | sauce_spread | 85        | +0.0    |
| הקיסר חומוס ענק      | 80.4      | A         | sauce_spread | 79.7      | +0.7    |
| סלט חומוס            | 80.2      | A         | sauce_spread | 79.4      | +0.8    |
| חומוס שלם יכין       | 79.9      | B         | sauce_spread | 79.9      | +0.0    |
| חומוס מסעדות         | 75.7      | B         | sauce_spread | 72.7      | +3.0    |

---

## Bottom 10 — Old vs New

### Old Bottom 10 (run_hummus_001)

| Product            | Old Score | Old Grade         | Old Category   | New Score | Δ Score |
|--------------------|-----------|-------------------|----------------|-----------|---------|
| ממרח פלפלים קלויים | 42.8      | D                 | sauce_spread   | 42.8      | +0.0    |
| ממרח פלפלים קלויים | 48.0      | D                 | whole_food_fat | 48.0      | +0.0    |
| מטבוחה אמיתית      | 48.7      | D                 | default        | 48.7      | +0.0    |
| פלפל צ'ומה         | 49.6      | D                 | default        | 51.0      | +1.4    |
| מטבוחה חריפה       | 49.6      | D                 | default        | 49.6      | +0.0    |
| חומוס              | 50        | insufficient_data | dessert        | 50        | +0.0    |
| חומוס ענק          | 50        | insufficient_data | dessert        | 50        | +0.0    |
| סלט מטבוחה פיקנטי  | 52.0      | C                 | default        | 52.0      | +0.0    |
| מטבוחה פיקנטית     | 52.0      | C                 | default        | 52.0      | +0.0    |
| חציל על האש בטחינה | 52.2      | C                 | whole_food_fat | 50.0      | -2.2    |

### New Bottom 10 (run_hummus_002 — fixed routing)

| Product            | New Score | New Grade         | New Category | Old Score | Δ Score |
|--------------------|-----------|-------------------|--------------|-----------|---------|
| ממרח פלפלים קלויים | 42.8      | D                 | sauce_spread | 42.8      | +0.0    |
| ממרח פלפלים קלויים | 48.0      | D                 | sauce_spread | 48.0      | +0.0    |
| מטבוחה אמיתית      | 48.7      | D                 | sauce_spread | 48.7      | +0.0    |
| מטבוחה חריפה       | 49.6      | D                 | sauce_spread | 49.6      | +0.0    |
| חציל על האש בטחינה | 50.0      | C                 | sauce_spread | 52.2      | -2.2    |
| חומוס              | 50        | insufficient_data | sauce_spread | 50        | +0.0    |
| חומוס ענק          | 50        | insufficient_data | sauce_spread | 50        | +0.0    |
| פלפל צ'ומה         | 51.0      | C                 | sauce_spread | 49.6      | +1.4    |
| סלט מטבוחה פיקנטי  | 52.0      | C                 | sauce_spread | 52.0      | +0.0    |
| מטבוחה פיקנטית     | 52.0      | C                 | sauce_spread | 52.0      | +0.0    |

---

## Recommendation: Should Hummus BSIP2 Be Refreshed?

_[Populated after comparison data is reviewed]_

---

*Generated: 2026-05-31 04:43 UTC | Router fix: router_v2.py savory-spread anchors v1*