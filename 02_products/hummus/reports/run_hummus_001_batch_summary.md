# BSIP2 Hummus Baseline — run_hummus_001 Run Report

**Run date:** 2026-06-02 06:10 UTC
**Category:** hummus_and_savory_dips
**Source:** Shufersal corpus — 69 canonical BSIP1 products
**Framework:** BSIP2 proto_v0 (unmodified baseline run)
**Products processed:** 69
**Scored (sufficient data):** 69
**Insufficient data:** 0
**Pipeline errors:** 0

> **Known limitation: fat_quality dimension may be unreliable for 58/69 products due to confirmed Shufersal fat-row scraping defect identified in TASK-039.**

---

## Score Distribution

| Statistic | Value |
|-----------|-------|
| Count     | 69 |
| Mean      | 63.2 |
| Median    | 61.9 |
| Std Dev   | 10.5 |
| Min       | 38.9 |
| Max       | 85.5 |
| P25       | 57.3 |
| P75       | 65.7 |

### Score Buckets (10-point intervals)

|   0–10  |   0 |  |
|  10–20  |   0 |  |
|  20–30  |   0 |  |
|  30–40  |   1 | █ |
|  40–50  |   6 | ██████ |
|  50–60  |  15 | ███████████████ |
|  60–70  |  33 | █████████████████████████████████ |
|  70–80  |   7 | ███████ |
|  80–90  |   7 | ███████ |
|  90–100 |   0 |  |

---

## Grade Distribution

| Grade | Score Range | Count | Expected (framework) |
|-------|-------------|-------|----------------------|
| A     | 85–100      | 7     | 5–10 |
| B     | 70–84       | 17     | 20–28 |
| C     | 55–69       | 38     | 20–25 |
| D     | 40–54       | 7     | 10–15 |
| E     | 0–39        | 0     | 2–5 |
| insufficient_data | — | 0 | — |

---

## Top 10 Products

| Product              | Score | Grade | Category     | NOVA | Fat Anomaly | Cap |
|----------------------|-------|-------|--------------|------|-------------|-----|
| חומוס                | 85.5  | A     | sauce_spread | 1    | MEDIUM      | -   |
| חומוס ענק            | 85.5  | A     | sauce_spread | 1    | MEDIUM      | -   |
| חומוס ענק            | 85    | A     | sauce_spread | 1    | MEDIUM      | -   |
| חומוס לבן ענק שופרסל | 85    | A     | sauce_spread | 1    | MEDIUM      | -   |
| חומוס גדול שופרסל    | 85    | A     | sauce_spread | 1    | MEDIUM      | -   |
| חומוס מוקפא          | 85    | A     | sauce_spread | 1    | NONE        | -   |
| הקיסר חומוס ענק      | 80.3  | A     | sauce_spread | 3    | NONE        | 87  |
| חומוס שלם יכין       | 79.9  | B     | sauce_spread | 3    | NONE        | 87  |
| סלט חומוס            | 77.2  | B     | sauce_spread | 3    | HIGH        | 87  |
| חומוס מסעדות         | 75.1  | B     | sauce_spread | 3    | CRITICAL    | 87  |

---

## Bottom 10 Products

| Product            | Score | Grade | Category     | NOVA | Fat Anomaly | Cap | Key Flags |
|--------------------|-------|-------|--------------|------|-------------|-----|-----------|
| ממרח פלפלים קלויים | 38.9  | D     | sauce_spread | 3    | MEDIUM      | 87  |           |
| ממרח פלפלים קלויים | 44.7  | D     | sauce_spread | 3    | MEDIUM      | 60  |           |
| חציל על האש בטחינה | 46.4  | D     | sauce_spread | 3    | CRITICAL    | 60  |           |
| פלפל צ'ומה         | 47.1  | D     | sauce_spread | 3    | MEDIUM      | 60  |           |
| מטבוחה פיקנטית     | 49.0  | D     | sauce_spread | 3    | MEDIUM      | 60  |           |
| סלט מטבוחה פיקנטי  | 49.0  | D     | sauce_spread | 3    | MEDIUM      | 60  |           |
| סלט חציל פיקנטי    | 49.1  | D     | sauce_spread | 3    | MEDIUM      | 87  |           |
| מטבוחה אמיתית      | 50.0  | C     | sauce_spread | 3    | LOW         | 87  |           |
| מטבוחה חריפה       | 50.5  | C     | sauce_spread | 3    | LOW         | 87  |           |
| סלט חציל בטעם כבד  | 51.5  | C     | sauce_spread | 3    | MEDIUM      | 72  |           |

---

## Full Score Table

| Product                  | Score | Grade | Category     | NOVA | Wtd Dim | Cap | Conf | Fat      |
|--------------------------|-------|-------|--------------|------|---------|-----|------|----------|
| חומוס                    | 85.5  | A     | sauce_spread | 1    | 85.47   | -   | 90   | MEDIUM   |
| חומוס ענק                | 85.5  | A     | sauce_spread | 1    | 85.47   | -   | 90   | MEDIUM   |
| חומוס ענק                | 85    | A     | sauce_spread | 1    | 74.41   | -   | 95   | MEDIUM   |
| חומוס לבן ענק שופרסל     | 85    | A     | sauce_spread | 1    | 83.34   | -   | 100  | MEDIUM   |
| חומוס גדול שופרסל        | 85    | A     | sauce_spread | 1    | 83.34   | -   | 100  | MEDIUM   |
| חומוס מוקפא              | 85    | A     | sauce_spread | 1    | 79.33   | -   | 100  | NONE     |
| הקיסר חומוס ענק          | 80.3  | A     | sauce_spread | 3    | 80.3    | 87  | 95   | NONE     |
| חומוס שלם יכין           | 79.9  | B     | sauce_spread | 3    | 79.92   | 87  | 95   | NONE     |
| סלט חומוס                | 77.2  | B     | sauce_spread | 3    | 80.17   | 87  | 90   | HIGH     |
| חומוס מסעדות             | 75.1  | B     | sauce_spread | 3    | 75.12   | 87  | 95   | CRITICAL |
| חומוס                    | 75    | B     | sauce_spread | 2    | 83.37   | -   | 55   | LOW      |
| חומוס ענק                | 75    | B     | sauce_spread | 2    | 84.02   | -   | 55   | LOW      |
| חומוס                    | 72.1  | B     | sauce_spread | 2    | 72.13   | -   | 50   | MEDIUM   |
| חומוס                    | 72.1  | B     | sauce_spread | 2    | 72.13   | -   | 50   | MEDIUM   |
| חומוס אסלי               | 66.8  | B     | sauce_spread | 3    | 72.84   | 87  | 95   | CRITICAL |
| חומוס                    | 66.8  | B     | sauce_spread | 3    | 72.84   | 87  | 95   | CRITICAL |
| חומוס אבו גוש            | 66.1  | B     | sauce_spread | 3    | 72.09   | 87  | 95   | CRITICAL |
| חומוס גלילי              | 65.7  | B     | sauce_spread | 3    | 68.73   | 87  | 90   | HIGH     |
| חומוס גלילי              | 65.6  | B     | sauce_spread | 3    | 68.58   | 87  | 90   | HIGH     |
| חומוס מסעדה              | 65.2  | B     | sauce_spread | 3    | 68.25   | 87  | 90   | HIGH     |
| חומוס מסעדה              | 65.2  | B     | sauce_spread | 3    | 68.25   | 87  | 90   | HIGH     |
| חומוס יום יום            | 65.1  | B     | sauce_spread | 3    | 68.08   | 87  | 90   | HIGH     |
| חומוס                    | 65.1  | B     | sauce_spread | 3    | 68.08   | 87  | 90   | HIGH     |
| חומוס עשיר ב40% טחינה    | 65.0  | B     | sauce_spread | 3    | 68.05   | 87  | 90   | CRITICAL |
| חומוס                    | 64.9  | C     | sauce_spread | 3    | 67.92   | 87  | 90   | HIGH     |
| חומוס ישראלי             | 64.9  | C     | sauce_spread | 3    | 67.93   | 87  | 90   | HIGH     |
| חומוס                    | 64.9  | C     | sauce_spread | 3    | 67.92   | 87  | 90   | HIGH     |
| סלט חומוס עם טחינה       | 64.7  | C     | sauce_spread | 3    | 70.73   | 87  | 95   | CRITICAL |
| סלט חומוס+מסבחה          | 64.5  | C     | sauce_spread | 3    | 70.46   | 87  | 95   | CRITICAL |
| חומוס צנובר צבר          | 63.9  | C     | sauce_spread | 3    | 69.86   | 87  | 90   | HIGH     |
| מלך החומוס אבו מרוואן    | 62.2  | C     | sauce_spread | 3    | 68.25   | 87  | 90   | CRITICAL |
| חומוס מסעדה צבר          | 62.2  | C     | sauce_spread | 3    | 68.25   | 87  | 90   | HIGH     |
| חומוס עם צנובר אחלה      | 62.1  | C     | sauce_spread | 3    | 68.11   | 87  | 90   | HIGH     |
| חומוס אבו מרוואן26%טחינה | 62.0  | C     | sauce_spread | 3    | 67.99   | 87  | 90   | CRITICAL |
| חומוס לבנוני צבר         | 61.9  | C     | sauce_spread | 3    | 67.91   | 87  | 90   | CRITICAL |
| חומוס מועשר 40% עם חריף  | 61.9  | C     | sauce_spread | 3    | 67.9    | 72  | 90   | CRITICAL |
| חומוס עם זעתר            | 61.8  | C     | sauce_spread | 3    | 67.84   | 87  | 90   | HIGH     |
| סלט פלפלים קלויים        | 61.7  | C     | default      | 3    | 61.68   | 87  | 65   | NONE     |
| חומוס עם זעתר            | 61.6  | C     | sauce_spread | 3    | 67.64   | 87  | 90   | HIGH     |
| מלך החומוס סמיר הגדול    | 61.4  | C     | sauce_spread | 3    | 67.39   | 87  | 90   | CRITICAL |
| חומוס עם מלא מטבוחה חריף | 61.3  | C     | sauce_spread | 3    | 67.26   | 87  | 90   | MEDIUM   |
| חומוס אבו גוש+צנובר+חריף | 61.0  | C     | sauce_spread | 3    | 66.98   | 87  | 90   | HIGH     |
| סלט מטבוחה               | 60.4  | C     | sauce_spread | 3    | 63.43   | 87  | 90   | NONE     |
| חומוס מסבחה              | 60.4  | C     | sauce_spread | 3    | 70.38   | 87  | 95   | CRITICAL |
| חומוס עם טחינה אחלה      | 60.2  | C     | sauce_spread | 3    | 66.2    | 72  | 90   | HIGH     |
| חומוס עם טחינה צבר       | 60.2  | C     | sauce_spread | 3    | 66.25   | 72  | 90   | HIGH     |
| חומוס גרגרים בתטבילה     | 60.0  | C     | sauce_spread | 3    | 65.96   | 87  | 90   | CRITICAL |
| חומוס עם חריף אחלה       | 59.6  | C     | sauce_spread | 3    | 65.59   | 72  | 90   | HIGH     |
| חומוס עם חריף            | 59.5  | C     | sauce_spread | 3    | 65.51   | 72  | 90   | HIGH     |
| ממרח פלפלים קלויים       | 58.8  | C     | sauce_spread | 3    | 61.75   | 87  | 95   | MEDIUM   |
| סלט חצילים על האש        | 58.0  | C     | sauce_spread | 3    | 63.98   | 87  | 95   | MEDIUM   |
| סלט מטבוחה מרוקאית       | 57.3  | C     | sauce_spread | 3    | 63.34   | 87  | 90   | LOW      |
| סלט מטבוחה               | 56.9  | C     | sauce_spread | 3    | 62.9    | 87  | 90   | MEDIUM   |
| מטבוחה חריפה אש          | 56.9  | C     | sauce_spread | 3    | 62.91   | 87  | 90   | MEDIUM   |
| סלט מטבוחה יום יום       | 56.9  | C     | sauce_spread | 3    | 62.9    | 87  | 90   | MEDIUM   |
| סלט טורקי                | 55.3  | C     | default      | 3    | 65.27   | 87  | 80   | MEDIUM   |
| חציל על האש              | 54.1  | C     | sauce_spread | 3    | 60.06   | 87  | 90   | MEDIUM   |
| חומוס עם חציל פיקנטי     | 53.9  | C     | sauce_spread | 3    | 63.93   | 87  | 90   | HIGH     |
| מעדן חצילים              | 53.5  | C     | sauce_spread | 3    | 59.55   | 87  | 95   | MEDIUM   |
| סלט חציל בטעם כבד        | 51.5  | C     | sauce_spread | 3    | 57.55   | 72  | 90   | MEDIUM   |
| מטבוחה חריפה             | 50.5  | C     | sauce_spread | 3    | 60.52   | 87  | 90   | LOW      |
| מטבוחה אמיתית            | 50.0  | C     | sauce_spread | 3    | 60.96   | 87  | 90   | LOW      |
| סלט חציל פיקנטי          | 49.1  | D     | sauce_spread | 3    | 59.09   | 87  | 90   | MEDIUM   |
| סלט מטבוחה פיקנטי        | 49.0  | D     | sauce_spread | 3    | 64.49   | 60  | 95   | MEDIUM   |
| מטבוחה פיקנטית           | 49.0  | D     | sauce_spread | 3    | 64.49   | 60  | 95   | MEDIUM   |
| פלפל צ'ומה               | 47.1  | D     | sauce_spread | 3    | 59.09   | 60  | 90   | MEDIUM   |
| חציל על האש בטחינה       | 46.4  | D     | sauce_spread | 3    | 56.4    | 60  | 90   | CRITICAL |
| ממרח פלפלים קלויים       | 44.7  | D     | sauce_spread | 3    | 59.72   | 60  | 95   | MEDIUM   |
| ממרח פלפלים קלויים       | 38.9  | D     | sauce_spread | 3    | 48.87   | 87  | 90   | MEDIUM   |

---

## Dimension Contribution Summary

Average dimension scores across all scored products.

| Dimension           | Weight | Avg Score | Contribution |
|---------------------|--------|-----------|--------------|
| processing_quality   | 0.15   | 68.8      | 10.3 |
| nutrient_density     | 0.15   | 29.2      | 4.4 |
| calorie_density      | 0.15   | 75.9      | 11.4 |
| glycemic_quality     | 0.12   | 86.1      | 10.3 |
| protein_quality      | 0.10   | 36.8      | 3.7 |
| additive_quality     | 0.10   | 72.9      | 7.3 |
| satiety_support      | 0.06   | 49.9      | 3.0 |
| fat_quality          | 0.08   | 50.0      | 4.0 ⚠ (fat anomaly) |
| regulatory_quality   | 0.05   | 92.5      | 4.6 |
| whole_food_integrity | 0.04   | 65.8      | 2.6 |

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
| sauce_spread | 67 |
| default | 2 |

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
| HP_FAT_SODIUM_COMBO | 54 |
| SEED_OIL_PRESENT | 43 |
| LONG_INGREDIENT_LIST | 8 |
| MULTIPLE_ADDED_SUGAR_MARKERS | 4 |
| HIGH_CAL_LOW_SATIETY_SOFT | 1 |

---

## Category Observations

### Routing

| Product Type | Count | Avg Score | Min | Max |
|--------------|-------|-----------|-----|-----|
| hummus_spread        | 42    | 68.8      | 59.5  | 85.5  |
| light_hummus         | 2     | 63.5      | 61.9  | 65.0  |
| masabacha            | 2     | 62.5      | 60.4  | 64.5  |
| matbucha             | 10    | 54.8      | 49.0  | 61.3  |
| eggplant_spread      | 7     | 52.4      | 46.4  | 58.0  |
| other_spread         | 2     | 51.2      | 47.1  | 55.3  |
| pepper_spread        | 4     | 51.0      | 38.9  | 61.7  |

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

*Run: run_hummus_001 | Generated: 2026-06-02 06:10 UTC*
*BSIP2 proto_v0 — Hummus Baseline. Do not modify BSIP1 records. Do not patch fat values.*