# Hummus Sodium Distribution Stats — n=60 In-Scope Corpus
## P136 Re-run | TASK-278 Phase-12 | Generated 2026-06-14

### Context

Original D6 stats were computed on n=69, including 9 out-of-scope products:
- 4 eggplant_spread
- 5 matbucha_pepper_spread

This re-run filters to n=60 in-scope: `hummus_spread` (30) + `hummus_and_savory_dips` (30).

Source: `C:\Bari\02_products\hummus\canonical_bsip1\` — direct BSIP0/BSIP1 scrape panels only.
OFF: not used (banned).

---

### Corpus Filter

| product_category | n | in_scope |
|---|---|---|
| hummus_spread | 30 | YES |
| hummus_and_savory_dips | 30 | YES |
| eggplant_spread | 4 | NO — excluded |
| matbucha_pepper_spread | 5 | NO — excluded |
| **Total** | **69** | **60 in-scope** |

Products with missing sodium_mg: 0

n with valid sodium: **60**

---

### Distribution Statistics (n=60)

| Statistic | Value (mg/100g) |
|---|---|
| n | 60 |
| mean | 342.85 |
| stdev | 187.93 |
| min | 6.00 |
| Q1 (25th pct) | 352.00 |
| median (50th pct) | 390.00 |
| Q3 (75th pct) | 395.00 |
| P80 | 395.00 |
| P85 | 395.00 |
| max | 864.00 |
| IQR (Q3 - Q1) | 43.00 |
| MAD | 10.00 |
| robust_scale = max(IQR/1.349, 1.4826*MAD, 3.0) | 31.88 |

robust_scale computation:
- IQR / 1.349 = 43.00 / 1.349 = 31.88
- 1.4826 * MAD = 1.4826 * 10.00 = 14.83
- floor = 3.0
- robust_scale = max(31.88, 14.83, 3.0) = **31.88**

---

### Floor Threshold Decision

|Q3 - median| = |395 - 390| = **5.00mg**

The D7 escalation rule is: "if Q3 still within 5mg of median, escalate to Nutrition Agent to select P80 or P85 instead."

5.00mg is exactly at the boundary (within 5mg, not strictly greater than 5mg). Applying the rule: **flag triggered**.

Note: P80 = 395.0mg and P85 = 395.0mg are both the same value as Q3. The 375-400 bucket contains 34 of 60 products (57%). The distribution has a very sharp mode at ~395mg with a long left tail of very low-sodium products (plain/frozen hummus, ~9 products below 25mg).

**Floor threshold recommendation:** Escalate to Nutrition Agent.

Q3, P80, and P85 all resolve to 395mg due to the dense spike at that value. The Nutrition Agent should assess whether:
1. 395mg is the correct floor threshold, OR
2. A lower percentile (e.g., 65th, ~393mg) or a different approach should be used
3. The very low-sodium outliers (n=9 products below 25mg sodium) should be treated as a separate cluster (plain chickpeas without salt) that pulls the mean down artificially

---

### Histogram — Frequency by 25mg Bucket

| Bucket (mg) | Count | Notes |
|---|---|---|
| 0 – 25 | 9 | Very low sodium cluster: likely plain/frozen chickpeas |
| 25 – 50 | 0 | |
| 50 – 75 | 1 | |
| 75 – 100 | 0 | |
| 100 – 125 | 0 | |
| 125 – 150 | 0 | |
| 150 – 175 | 2 | |
| 175 – 200 | 0 | |
| 200 – 225 | 0 | |
| 225 – 250 | 1 | |
| 250 – 275 | 0 | |
| 275 – 300 | 0 | |
| 300 – 325 | 0 | |
| 325 – 350 | 2 | |
| 350 – 375 | 6 | |
| 375 – 400 | **34** | **Dense spike — 57% of corpus** |
| 400 – 425 | 0 | |
| 425 – 450 | 0 | |
| 450 – 475 | 0 | |
| 475 – 500 | 1 | |
| 500 – 875 | 0 | (empty mid-range) |
| 600 – 625 | 1 | |
| 850 – 875 | 3 | High-sodium outliers |

Distribution is strongly bimodal: a cluster at 0-25mg (plain chickpeas, n=9) and a cluster at 360-400mg (seasoned hummus, n=44). The mean (342.85) is not representative — median (390mg) is more informative.

---

### 5 Highest Sodium Products

| Barcode | Name (Hebrew) | Sodium mg/100g | Category |
|---|---|---|---|
| 7290010154265 | פלפל צ'ומה | 864.0 | hummus_and_savory_dips |
| 7296073725510 | סלט מטבוחה פיקנטי | 852.0 | hummus_and_savory_dips |
| 7296073725633 | מטבוחה פיקנטית | 852.0 | hummus_and_savory_dips |
| 6666444 | סלט מטבוחה | 623.0 | hummus_and_savory_dips |
| 6666307 | סלט חומוס | 480.0 | hummus_spread |

### 5 Lowest Sodium Products

| Barcode | Name (Hebrew) | Sodium mg/100g | Category |
|---|---|---|---|
| 7296073705505 | חומוס מוקפא | 6.0 | hummus_and_savory_dips |
| 1990261 | חומוס | 12.0 | hummus_and_savory_dips |
| 3643714 | חומוס | 12.0 | hummus_spread |
| 3643820 | חומוס ענק | 17.0 | hummus_spread |
| 7296073733317 | חומוס | 23.0 | hummus_and_savory_dips |

---

### Distribution Note for Product Agent

The n=60 distribution has a structural issue that the n=69 stats concealed: when eggplant/matbucha are removed, Q3, P80, and P85 all collapse to the same value (395mg) because of the extremely dense spike at that sodium level. The "floor threshold" question is therefore not about which percentile to pick — it is about whether 395mg is the right floor or whether a different signal is needed.

The 9 low-sodium outliers (below 25mg) are almost certainly unseasoned/frozen chickpea products (e.g., "חומוס מוקפא" = frozen hummus, barcodes with 3-7 digit codes suggesting PLU/non-standard retail). These pull the mean down to 342mg and inflate the IQR/stdev, but do not affect Q3/P80/P85.

Escalation to Nutrition Agent is required before finalizing the floor constant.

---

### Computation Provenance

- Script: `C:\Bari\02_products\hummus\methodology\compute_sodium_stats.py`
- Source: BSIP1 canonical files, `normalized_nutrition_per_100g.sodium_mg`
- Filter: `bsip0_source.product_category in {hummus_spread, hummus_and_savory_dips}`
- Percentile method: linear interpolation (numpy-compatible)
- OFF used: NO
- Date: 2026-06-14
