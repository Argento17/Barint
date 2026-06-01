# BSIP2 Hummus Baseline — run_hummus_001 Run Report

**Run date:** 2026-05-31 04:23 UTC
**Category:** hummus_and_savory_dips
**Source:** Shufersal corpus — 69 canonical BSIP1 products
**Framework:** BSIP2 proto_v0 (unmodified baseline run)
**Products processed:** 69
**Scored (sufficient data):** 67
**Insufficient data:** 2
**Pipeline errors:** 0

> **Known limitation: fat_quality dimension may be unreliable for 58/69 products due to confirmed Shufersal fat-row scraping defect identified in TASK-039.**

---

## Score Distribution

| Statistic | Value |
|-----------|-------|
| Count     | 67 |
| Mean      | 65.1 |
| Median    | 64.5 |
| Std Dev   | 9.5 |
| Min       | 42.8 |
| Max       | 85 |
| P25       | 60.4 |
| P75       | 67.7 |

### Score Buckets (10-point intervals)

|   0–10  |   0 |  |
|  10–20  |   0 |  |
|  20–30  |   0 |  |
|  30–40  |   0 |  |
|  40–50  |   5 | █████ |
|  50–60  |   9 | █████████ |
|  60–70  |  41 | █████████████████████████████████████████ |
|  70–80  |   6 | ██████ |
|  80–90  |   6 | ██████ |
|  90–100 |   0 |  |

---

## Grade Distribution

| Grade | Score Range | Count | Expected (framework) |
|-------|-------------|-------|----------------------|
| A     | 85–100      | 6     | 5–10 |
| B     | 70–84       | 25     | 20–28 |
| C     | 55–69       | 31     | 20–25 |
| D     | 40–54       | 5     | 10–15 |
| E     | 0–39        | 0     | 2–5 |
| insufficient_data | — | 0 | — |

---

## Top 10 Products

| Product               | Score | Grade | Category       | NOVA | Fat Anomaly | Cap |
|-----------------------|-------|-------|----------------|------|-------------|-----|
| חומוס ענק             | 85    | A     | dessert        | 1    | MEDIUM      | -   |
| חומוס לבן ענק שופרסל  | 85    | A     | dessert        | 1    | MEDIUM      | -   |
| חומוס גדול שופרסל     | 85    | A     | dessert        | 1    | MEDIUM      | -   |
| חומוס מוקפא           | 85    | A     | dessert        | 1    | NONE        | -   |
| חומוס                 | 85    | A     | dessert        | 1    | MEDIUM      | -   |
| חומוס ענק             | 85    | A     | dessert        | 1    | MEDIUM      | -   |
| חומוס שלם יכין        | 79.9  | B     | sauce_spread   | 3    | NONE        | 87  |
| הקיסר חומוס ענק       | 79.7  | B     | dessert        | 3    | NONE        | 87  |
| סלט חומוס             | 79.4  | B     | dessert        | 3    | HIGH        | 87  |
| חומוס עשיר ב40% טחינה | 72.8  | B     | whole_food_fat | 3    | CRITICAL    | 87  |

---

## Bottom 10 Products

| Product            | Score | Grade | Category       | NOVA | Fat Anomaly | Cap | Key Flags                                                    |
|--------------------|-------|-------|----------------|------|-------------|-----|--------------------------------------------------------------|
| ממרח פלפלים קלויים | 42.8  | D     | sauce_spread   | 3    | MEDIUM      | 87  | CATEGORY_INSTABILITY: primary=sauce_spread secondary=whole_f |
| ממרח פלפלים קלויים | 48.0  | D     | whole_food_fat | 3    | MEDIUM      | 60  |                                                              |
| מטבוחה אמיתית      | 48.7  | D     | default        | 3    | LOW         | 87  | CATEGORY_INSTABILITY: primary=default secondary=default, con |
| מטבוחה חריפה       | 49.6  | D     | default        | 3    | LOW         | 87  | CATEGORY_INSTABILITY: primary=default secondary=default, con |
| פלפל צ'ומה         | 49.6  | D     | default        | 3    | MEDIUM      | 60  | CATEGORY_INSTABILITY: primary=default secondary=default, con |
| מטבוחה פיקנטית     | 52.0  | C     | default        | 3    | MEDIUM      | 60  | CATEGORY_INSTABILITY: primary=default secondary=default, con |
| סלט מטבוחה פיקנטי  | 52.0  | C     | default        | 3    | MEDIUM      | 60  | CATEGORY_INSTABILITY: primary=default secondary=default, con |
| חציל על האש בטחינה | 52.2  | C     | whole_food_fat | 3    | CRITICAL    | 60  |                                                              |
| סלט חציל בטעם כבד  | 55.3  | C     | dessert        | 3    | MEDIUM      | 72  | CATEGORY_INSTABILITY: primary=dessert secondary=sauce_spread |
| סלט חציל פיקנטי    | 56.4  | C     | default        | 3    | MEDIUM      | 87  | CATEGORY_INSTABILITY: primary=default secondary=default, con |

---

## Full Score Table

| Product                  | Score | Grade | Category       | NOVA | Wtd Dim | Cap | Conf | Fat      |
|--------------------------|-------|-------|----------------|------|---------|-----|------|----------|
| חומוס ענק                | 85    | A     | dessert        | 1    | 72.19   | -   | 87   | MEDIUM   |
| חומוס לבן ענק שופרסל     | 85    | A     | dessert        | 1    | 84.61   | -   | 92   | MEDIUM   |
| חומוס גדול שופרסל        | 85    | A     | dessert        | 1    | 84.61   | -   | 92   | MEDIUM   |
| חומוס מוקפא              | 85    | A     | dessert        | 1    | 78.58   | -   | 92   | NONE     |
| חומוס                    | 85    | A     | dessert        | 1    | 84.72   | -   | 82   | MEDIUM   |
| חומוס ענק                | 85    | A     | dessert        | 1    | 84.72   | -   | 82   | MEDIUM   |
| חומוס שלם יכין           | 79.9  | B     | sauce_spread   | 3    | 79.92   | 87  | 87   | NONE     |
| הקיסר חומוס ענק          | 79.7  | B     | dessert        | 3    | 79.65   | 87  | 87   | NONE     |
| סלט חומוס                | 79.4  | B     | dessert        | 3    | 79.42   | 87  | 82   | HIGH     |
| חומוס עשיר ב40% טחינה    | 72.8  | B     | whole_food_fat | 3    | 72.85   | 87  | 90   | CRITICAL |
| חומוס מסעדות             | 72.7  | B     | dessert        | 3    | 72.72   | 87  | 87   | CRITICAL |
| סלט חומוס עם טחינה       | 70.7  | B     | whole_food_fat | 3    | 73.7    | 87  | 95   | CRITICAL |
| חומוס                    | 69.6  | B     | dessert        | 2    | 69.61   | -   | 42   | MEDIUM   |
| חומוס                    | 69.6  | B     | dessert        | 2    | 69.61   | -   | 42   | MEDIUM   |
| חומוס גלילי              | 68.3  | B     | dessert        | 3    | 68.32   | 87  | 82   | HIGH     |
| חומוס גלילי              | 68.2  | B     | dessert        | 3    | 68.16   | 87  | 82   | HIGH     |
| חומוס מסעדה              | 67.7  | B     | dessert        | 3    | 67.68   | 87  | 82   | HIGH     |
| חומוס יום יום            | 67.7  | B     | dessert        | 3    | 67.66   | 87  | 82   | HIGH     |
| חומוס                    | 67.7  | B     | dessert        | 3    | 67.66   | 87  | 82   | HIGH     |
| חומוס מסעדה              | 67.7  | B     | dessert        | 3    | 67.68   | 87  | 82   | HIGH     |
| חומוס אסלי               | 67.6  | B     | dessert        | 3    | 70.62   | 87  | 87   | CRITICAL |
| חומוס                    | 67.6  | B     | dessert        | 3    | 70.62   | 87  | 87   | CRITICAL |
| חומוס                    | 67.5  | B     | dessert        | 3    | 67.5    | 87  | 82   | HIGH     |
| חומוס ישראלי             | 67.5  | B     | dessert        | 3    | 67.51   | 87  | 82   | HIGH     |
| חומוס                    | 67.5  | B     | dessert        | 3    | 67.5    | 87  | 82   | HIGH     |
| חומוס אבו מרוואן26%טחינה | 67.4  | B     | whole_food_fat | 3    | 70.42   | 87  | 90   | CRITICAL |
| חומוס אבו גוש            | 66.9  | B     | dessert        | 3    | 69.89   | 87  | 87   | CRITICAL |
| חומוס צנובר צבר          | 66.3  | B     | dessert        | 3    | 69.33   | 87  | 82   | HIGH     |
| חומוס עם טחינה אחלה      | 65.8  | B     | whole_food_fat | 3    | 68.78   | 72  | 90   | HIGH     |
| חומוס עם טחינה צבר       | 65.7  | B     | whole_food_fat | 3    | 68.68   | 72  | 90   | HIGH     |
| סלט חומוס+מסבחה          | 65.2  | B     | dessert        | 3    | 68.24   | 87  | 87   | CRITICAL |
| חומוס עם צנובר אחלה      | 64.7  | C     | dessert        | 3    | 67.66   | 87  | 82   | HIGH     |
| חומוס מסעדה צבר          | 64.7  | C     | dessert        | 3    | 67.68   | 87  | 82   | HIGH     |
| חומוס עם מלא מטבוחה חריף | 64.5  | C     | dessert        | 3    | 67.45   | 87  | 82   | MEDIUM   |
| חומוס עם זעתר            | 64.4  | C     | dessert        | 3    | 67.42   | 87  | 82   | HIGH     |
| חומוס עם זעתר            | 64.1  | C     | dessert        | 3    | 67.07   | 87  | 82   | HIGH     |
| סלט פלפלים קלויים        | 63.5  | C     | default        | 3    | 63.54   | 87  | 65   | NONE     |
| חומוס אבו גוש+צנובר+חריף | 63.4  | C     | dessert        | 3    | 66.41   | 87  | 82   | HIGH     |
| חומוס מסבחה              | 63.4  | C     | dessert        | 3    | 70.44   | 87  | 87   | CRITICAL |
| חומוס מועשר 40% עם חריף  | 62.4  | C     | dessert        | 3    | 65.38   | 72  | 82   | CRITICAL |
| חומוס עם חריף אחלה       | 62.3  | C     | dessert        | 3    | 65.32   | 72  | 82   | HIGH     |
| מלך החומוס אבו מרוואן    | 62.2  | C     | dessert        | 3    | 65.25   | 87  | 82   | CRITICAL |
| חומוס לבנוני צבר         | 62.1  | C     | dessert        | 3    | 65.09   | 87  | 82   | CRITICAL |
| מטבוחה חריפה אש          | 62.0  | C     | default        | 3    | 64.95   | 87  | 75   | MEDIUM   |
| חומוס עם חריף            | 61.9  | C     | dessert        | 3    | 64.94   | 72  | 82   | HIGH     |
| סלט מטבוחה               | 61.8  | C     | default        | 3    | 64.76   | 87  | 75   | MEDIUM   |
| סלט מטבוחה יום יום       | 61.8  | C     | default        | 3    | 64.76   | 87  | 75   | MEDIUM   |
| סלט חצילים על האש        | 61.6  | C     | default        | 3    | 64.64   | 87  | 80   | MEDIUM   |
| סלט מטבוחה מרוקאית       | 61.5  | C     | default        | 3    | 64.54   | 87  | 75   | LOW      |
| מלך החומוס סמיר הגדול    | 61.4  | C     | dessert        | 3    | 64.39   | 87  | 82   | CRITICAL |
| סלט מטבוחה               | 60.4  | C     | default        | 3    | 63.43   | 87  | 75   | NONE     |
| סלט טורקי                | 60.4  | C     | default        | 3    | 67.42   | 87  | 80   | MEDIUM   |
| חומוס גרגרים בתטבילה     | 60.1  | C     | dessert        | 3    | 63.1    | 87  | 82   | CRITICAL |
| ממרח פלפלים קלויים       | 59.6  | C     | sauce_spread   | 3    | 62.65   | 87  | 87   | MEDIUM   |
| חציל על האש              | 58.0  | C     | default        | 3    | 61.02   | 87  | 75   | MEDIUM   |
| מעדן חצילים              | 57.3  | C     | dessert        | 3    | 60.33   | 87  | 95   | MEDIUM   |
| חומוס עם חציל פיקנטי     | 57.1  | C     | dessert        | 3    | 64.14   | 87  | 82   | HIGH     |
| סלט חציל פיקנטי          | 56.4  | C     | default        | 3    | 63.44   | 87  | 75   | MEDIUM   |
| סלט חציל בטעם כבד        | 55.3  | C     | dessert        | 3    | 58.34   | 72  | 82   | MEDIUM   |
| חציל על האש בטחינה       | 52.2  | C     | whole_food_fat | 3    | 59.25   | 60  | 90   | CRITICAL |
| סלט מטבוחה פיקנטי        | 52.0  | C     | default        | 3    | 66.29   | 60  | 80   | MEDIUM   |
| מטבוחה פיקנטית           | 52.0  | C     | default        | 3    | 66.29   | 60  | 80   | MEDIUM   |
| פלפל צ'ומה               | 49.6  | D     | default        | 3    | 58.58   | 60  | 75   | MEDIUM   |
| מטבוחה חריפה             | 49.6  | D     | default        | 3    | 56.62   | 87  | 75   | LOW      |
| מטבוחה אמיתית            | 48.7  | D     | default        | 3    | 56.7    | 87  | 75   | LOW      |
| ממרח פלפלים קלויים       | 48.0  | D     | whole_food_fat | 3    | 65.3    | 60  | 87   | MEDIUM   |
| ממרח פלפלים קלויים       | 42.8  | D     | sauce_spread   | 3    | 49.83   | 87  | 82   | MEDIUM   |

---

## Dimension Contribution Summary

Average dimension scores across all scored products.

| Dimension           | Weight | Avg Score | Contribution |
|---------------------|--------|-----------|--------------|
| processing_quality   | 0.15   | 68.3      | 10.2 |
| nutrient_density     | 0.15   | 27.5      | 4.1 |
| calorie_density      | 0.15   | 71.0      | 10.7 |
| glycemic_quality     | 0.12   | 92.2      | 11.1 |
| protein_quality      | 0.10   | 35.3      | 3.5 |
| additive_quality     | 0.10   | 72.1      | 7.2 |
| satiety_support      | 0.06   | 48.4      | 2.9 |
| fat_quality          | 0.08   | 50.0      | 4.0 ⚠ (fat anomaly) |
| regulatory_quality   | 0.05   | 92.4      | 4.6 |
| whole_food_integrity | 0.04   | 65.2      | 2.6 |

> ⚠ fat_quality scores are derived from incorrect fat_g values for 58/69 products (TASK-039).
  Scores for this dimension are systematically inflated and should not be used for comparison.

---

## NOVA Distribution

| NOVA | Count | Description |
|------|-------|-------------|
| NOVA 1 | 6 | Unprocessed or minimally processed |
| NOVA 2 | 4 | Processed culinary ingredients |
| NOVA 3 | 59 | Processed foods |
| NOVA 4 | 0 | Ultra-processed |
| Unknown | 0 | Not inferred |

---

## Category Routing Distribution

| Category | Count |
|----------|-------|
| dessert | 44 |
| default | 15 |
| whole_food_fat | 7 |
| sauce_spread | 3 |

---

## Guardrail Activity

Products with binding cap: **59** of 69

| Cap Rule | Count |
|----------|-------|
| NOVA_PROXY_3_PROCESSED | 59 |
| ADDITIVE_MARKERS_3_PLUS | 6 |
| HIGH_SODIUM_700MG_PLUS | 4 |
| ADDITIVE_MARKERS_5_PLUS | 1 |

| Penalty Rule | Count |
|-------------|-------|
| SEED_OIL_PRESENT | 43 |
| LONG_INGREDIENT_LIST | 8 |
| MULTIPLE_ADDED_SUGAR_MARKERS | 4 |
| HP_FAT_SODIUM_COMBO | 1 |
| HIGH_CAL_LOW_SATIETY_SOFT | 1 |

---

## Category Observations

### Routing

| Product Type | Count | Avg Score | Min | Max |
|--------------|-------|-----------|-----|-----|
| hummus_spread        | 40    | 70.0      | 60.1  | 85  |
| light_hummus         | 2     | 67.6      | 62.4  | 72.8  |
| masabacha            | 2     | 64.3      | 63.4  | 65.2  |
| matbucha             | 10    | 57.4      | 48.7  | 64.5  |
| eggplant_spread      | 7     | 56.8      | 52.2  | 61.6  |
| other_spread         | 2     | 55.0      | 49.6  | 60.4  |
| pepper_spread        | 4     | 53.5      | 42.8  | 63.5  |

---

## Fat Anomaly Impact (TASK-039)

| Severity | Count | Notes |
|----------|-------|-------|
| CRITICAL | 15 | Gap > 15g, tahini declared |
| HIGH     | 21 | Gap 10–15g |
| MEDIUM   | 23 | Gap 5–10g |
| LOW      | 5 | Gap 2–5g |
| NONE     | 5 | Consistent with caloric balance |

> Products with `fat_quality` unreliable: **58/69** (84%)
> Maximum score impact per product from fat anomaly: ~8 points (fat_quality weight = 8%)


---

*Run: run_hummus_001 | Generated: 2026-05-31 04:23 UTC*
*BSIP2 proto_v0 — Hummus Baseline. Do not modify BSIP1 records. Do not patch fat values.*