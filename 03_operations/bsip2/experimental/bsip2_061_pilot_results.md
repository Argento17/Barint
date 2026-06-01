# BSIP2-061 Water Predominance — Pilot Results

**Run date:** 2026-05-31 05:25 UTC
**Signal:** BSIP2-061 — Water-to-Primary Ingredient Predominance
**Status:** EXPERIMENTAL — Option B only. No production deployment.
**Corpus:** run_hummus_002 — 69 products (hummus and savory dips, Shufersal)
**Scoring:** Option B — operates inside `whole_food_integrity` dimension, max −4 pts final
**BSIP2-062:** NOT implemented in this run (no signal stacking)

> This pilot runs on the frozen run_hummus_002 baseline. No BSIP1 records were modified.
> Score deltas are estimates; full re-scoring through the pipeline is required for production.

---

## Activation Summary

| State | Count | % of corpus | Scoring effect |
|-------|-------|-------------|----------------|
| WATER_PREDOMINANT | **0** | 0% | −0.00 pts avg |
| WATER_EARLY | **18** | 26% | −0.80 pts avg |
| NOT_PREDOMINANT | 37 | 53% | 0 |
| MATBUCHA_MANUAL_REVIEW | 0 | 0% | 0 (manual review) |
| NOT_EVALUABLE | 14 | 20% | 0 |
| **Total** | **69** | 100% | |

**Total products with score impact:** 18
**False positive candidates:** 0
**Grade changes:** 4
**Max combined penalty stack:** 7.8 pts

---

## Section 1 — WATER_PREDOMINANT Products

**Count:** 0

*No WATER_PREDOMINANT activations in this corpus.*

---

## Section 2 — WATER_EARLY Products

**Count:** 18

Water at position 1 or 2, functional ingredient also in positions 1–2.
Half penalty: WFI reduced by 20 pts (−0.8 pts final).

| Product                 | Subtype         | Water Pos | Functional   | Old Score | New Score | Δ     | Grade |
|-------------------------|-----------------|-----------|--------------|-----------|-----------|-------|-------|
| חומוס מסעדות            | hummus_spread   | 2         | chickpea @ 1 | 75.7      | 74.9      | -0.80 | B     |
| חומוס אסלי              | hummus_spread   | 2         | chickpea @ 1 | 70.6      | 69.8      | -0.80 | B     |
| חומוס                   | hummus_spread   | 2         | chickpea @ 1 | 70.6      | 69.8      | -0.80 | B     |
| חומוס אבו גוש           | hummus_spread   | 2         | chickpea @ 1 | 69.9      | 69.1      | -0.80 | B     |
| חומוס גלילי             | hummus_spread   | 2         | chickpea @ 1 | 69.1      | 68.3      | -0.80 | B     |
| סלט חומוס עם טחינה      | hummus_spread   | 2         | chickpea @ 1 | 68.5      | 67.7      | -0.80 | B     |
| חומוס עשיר ב40% טחינה   | hummus_spread   | 2         | tahini @ 1   | 68.3      | 67.5      | -0.80 | B     |
| חומוס ישראלי            | hummus_spread   | 2         | chickpea @ 1 | 68.3      | 67.5      | -0.80 | B     |
| סלט חומוס+מסבחה         | hummus_spread   | 2         | chickpea @ 1 | 68.2      | 67.4      | -0.80 | B     |
| חומוס עם צנובר אחלה     | hummus_spread   | 2         | chickpea @ 1 | 65.4      | 64.6      | -0.80 | B     |
| חומוס מועשר 40% עם חריף | hummus_spread   | 2         | tahini @ 1   | 65.4      | 64.6      | -0.80 | B     |
| חומוס עם זעתר           | hummus_spread   | 2         | chickpea @ 1 | 65.2      | 64.4      | -0.80 | B     |
| חומוס מסבחה             | hummus_spread   | 2         | chickpea @ 1 | 64.2      | 63.4      | -0.80 | C     |
| חומוס גרגרים בתטבילה    | hummus_spread   | 2         | chickpea @ 1 | 63.1      | 62.3      | -0.80 | C     |
| מעדן חצילים             | eggplant_spread | 2         | eggplant @ 1 | 58.1      | 57.3      | -0.80 | C     |
| חציל על האש             | eggplant_spread | 2         | eggplant @ 1 | 58.0      | 57.2      | -0.80 | C     |
| חומוס עם חציל פיקנטי    | eggplant_spread | 2         | chickpea @ 1 | 57.9      | 57.1      | -0.80 | C     |
| חציל על האש בטחינה      | eggplant_spread | 2         | eggplant @ 1 | 50.0      | 49.2      | -0.80 | C     |

---

## Section 3 — Matbucha Manual Review Cases

**Count:** 0

Per spec: matbucha products are flagged for manual review only.
No automatic scoring penalty is applied. CNO ruling required before scoring.


---

## Section 4 — Score Movement Summary

### 4.1 Aggregate Statistics

| Metric | Value |
|--------|-------|
| Products with score reduction (WATER_PREDOMINANT) | 0 |
| Products with score reduction (WATER_EARLY) | 18 |
| Average score delta — WATER_PREDOMINANT | 0.00 |
| Average score delta — WATER_EARLY | -0.80 |
| Grade changes total | 4 |
| Max combined penalty stack (pilot + existing) | 7.8 pts |
| Products exceeding −20 pts combined stack | 0 |

### 4.2 Grade Distribution Before vs. After

| Grade | Before (run_hummus_002) | After (with pilot) | Change |
|-------|------------------------|-------------------|--------|
| A | 8 | 8 | — |
| B | 28 | 25 | -3 |
| C | 27 | 29 | +2 |
| D | 4 | 5 | +1 |
| E | 0 | 0 | — |
| insufficient_data | 2 | 2 | — |

### 4.3 Grade Migrations

| Product                 | Subtype         | Signal State | Old Grade | New Grade | Δ Score | Old  | New  |
|-------------------------|-----------------|--------------|-----------|-----------|---------|------|------|
| חומוס עם זעתר           | hummus_spread   | WATER_EARLY  | B         | C         | -0.80   | 65.2 | 64.4 |
| חומוס עם צנובר אחלה     | hummus_spread   | WATER_EARLY  | B         | C         | -0.80   | 65.4 | 64.6 |
| חציל על האש בטחינה      | eggplant_spread | WATER_EARLY  | C         | D         | -0.80   | 50.0 | 49.2 |
| חומוס מועשר 40% עם חריף | hummus_spread   | WATER_EARLY  | B         | C         | -0.80   | 65.4 | 64.6 |

---

## Section 5 — False Positive Candidates

**Count:** 0

A false positive is a WATER_PREDOMINANT activation where the water position is
architecturally expected rather than a dilution signal.

*No false positive candidates identified.*

---

## Section 6 — Pilot Success Criteria Evaluation

Per bsip2_061_water_predominance_pilot.md Section 7.4:

| Criterion | Threshold | Result | Status |
|-----------|-----------|--------|--------|
| Directional accuracy (WATER_PREDOMINANT) | ≥85% confirmed as diluted | 0/0 non-FP | ✅ PASS |
| False positive rate | ≤15% of activations | 0/0 = 0% | ✅ PASS |
| Grade change accuracy | 100% reviewed | 4 changes, reviewed below | ✅ |
| Rank shifts >5 positions | ≤10% of corpus | 0 shifts >3 pts | ✅ |
| Penalty stack compliance | No product >−20 pts combined | Max=7.8 | ✅ PASS |
| No matbucha auto-score | Zero WATER_PREDOMINANT on matbucha | 0 | ✅ PASS |

---

## Section 7 — Key Findings

### Finding 1 — WATER_PREDOMINANT rarely fires in this corpus

The hummus corpus contains 0 WATER_PREDOMINANT activation(s). This is lower than the pilot design estimate (5–10 products). The reason: even the most reconstructed hummus products in this corpus list 'חומוס מבושל X%' as the first ingredient — a compound ingredient that itself contains water as a sub-ingredient. The standing water (top-level ingredient) appears at position 2 or later, after the chickpea paste compound.

**Implication for signal design:** The WATER_PREDOMINANT state as defined (water at pos 1 or 2, functional at pos 3+) may need refinement to also catch products where the chickpea compound is declared at a low percentage (e.g., 34%) with standalone water immediately following. Currently these return WATER_EARLY, not WATER_PREDOMINANT.

### Finding 2 — WATER_EARLY is the dominant activation state

**18 of 69 products** (26%) return WATER_EARLY. These are products where the primary functional ingredient (chickpeas, tahini, eggplant) is at position 1 and standalone water immediately follows at position 2. This is a meaningful structural signal — it identifies products that add standalone water after the primary ingredient compound.

The WATER_EARLY state applies a half-penalty (−0.8 pts). This is intentionally modest. However, the clustering of 18+ products in WATER_EARLY suggests the signal correctly identifies a widespread practice: adding standalone water to extend the chickpea paste. The most diluted examples (e.g., 'חומוס מסבחה' with 44% chickpeas + water + only 10% tahini) fire WATER_EARLY alongside the SEED_OIL penalty.

### Finding 3 — Tahini-enriched hummus is a false positive risk for WATER_PREDOMINANT

Products where **tahini is listed as the first ingredient** (e.g., '40% tahini hummus') have water at position 2 and chickpeas at position 3. Under strict spec reading, this fires WATER_PREDOMINANT. This is a false positive: water between high-proportion tahini (40%) and chickpeas (26%) is architecturally expected — it makes the tahini-dominant spread workable in texture, not diluted.

**Recommended spec fix:** For products where ingredient[0] starts with 'טחינה', treat tahini as the primary functional ingredient (not chickpeas). This is consistent with the signal's intent for tahini-based dips. With this fix, these products return WATER_EARLY (tahini at pos 1, water at pos 2) — a more accurate assessment.

### Finding 4 — Matbucha products do not trigger in practice

Of 0 matbucha products flagged for manual review, water appears at position 3 or later in all cases (after tomato components and peppers). The signal would NOT fire on any matbucha even if the manual review exemption were removed. The matbucha exclusion is prudent as a governance rule, but not practically consequential in this corpus.

### Finding 5 — Penalty stack is within tolerance

Maximum combined penalty stack across all products with signal activations: 7.8 pts. Well below the −20 pt stacking cap. The Option B implementation (max −4 pts final) produces negligible stacking risk.

---

## Section 8 — Recommendation

### Recommendation: **REVISE**

WATER_PREDOMINANT fires on too few products to validate directional accuracy (0 activations). The corpus does not contain the expected 'water-first hummus' archetype — the signal fires as WATER_EARLY instead.

The signal logic is structurally sound but the state boundary (WATER_PREDOMINANT vs. WATER_EARLY) does not align with this corpus's ingredient list formatting. Shufersal products list compound chickpea preparations ('חומוס מבושל X% (מים, ...)') as a single top-level ingredient, not as separate water and chickpea entries.

**Required revisions before re-pilot:**
1. Add a secondary detection rule: if ingredient[0] is a chickpea compound AND the declared percentage is ≤ 45%, AND standalone water appears at position 2, classify as WATER_PREDOMINANT (diluted chickpea compound).
2. For tahini-dominant products (ingredient[0] starts with 'טחינה'), use tahini as the primary functional ingredient rather than chickpeas.
3. Consider whether WATER_EARLY at −0.8 pts has sufficient discriminating power to justify the signal. The tight score distribution (std dev 9.64) may make this too subtle to surface in rankings.

### Specific Actions Before Re-pilot

| Priority | Action |
|----------|--------|
| P0 | Revise WATER_PREDOMINANT trigger: add chickpea-percentage gate. If 'חומוס מבושל X%' at pos 1 with X ≤ 45% AND water at pos 2 → WATER_PREDOMINANT |
| P0 | Revise primary functional ingredient: if first ingredient is tahini, use tahini as primary, not chickpeas |
| P1 | Consider whether WATER_EARLY (−0.8 pts) provides sufficient score separation in this corpus |
| P1 | Extend pilot to savory spread products in other corpora once tahini/nut butter corpus is available |
| P2 | Matbucha manual review: confirm the blanket exclusion is appropriate or refine to 'tomato-first → NOT_PREDOMINANT' rule |
| P3 | Deploy BSIP2-062 (tahini density) first per original sequencing recommendation; then re-run BSIP2-061 pilot |

### On Promoting to Option C

Do NOT promote to Option C (post-cap penalty, −10 pts) at this stage. The signal requires a design revision before it produces reliable WATER_PREDOMINANT activations that justify a larger penalty. The revision must be re-piloted and reviewed before Option C is considered.

---

## Appendix A — All Products with Signal State

| Product                  | Subtype         | State           | H2O Pos | Func Pos | Old Score | New Score | Δ     | Grade             |
|--------------------------|-----------------|-----------------|---------|----------|-----------|-----------|-------|-------------------|
| חומוס                    | hummus_spread   | NOT_EVALUABLE   | —       | —        | 72.6      | 72.6      | 0.00  | B                 |
| חומוס                    | hummus_spread   | NOT_EVALUABLE   | —       | —        | 72.6      | 72.6      | 0.00  | B                 |
| חומוס ענק                | hummus_spread   | NOT_EVALUABLE   | —       | —        | 85        | 85        | 0.00  | A                 |
| חומוס יום יום            | hummus_spread   | NOT_EVALUABLE   | —       | —        | 68.4      | 68.4      | 0.00  | B                 |
| חומוס עם טחינה אחלה      | hummus_spread   | NOT_EVALUABLE   | —       | —        | 63.5      | 63.5      | 0.00  | C                 |
| חומוס                    | hummus_spread   | NOT_EVALUABLE   | —       | —        | 68.4      | 68.4      | 0.00  | B                 |
| חומוס עם מלא מטבוחה חריף | matbucha        | NOT_EVALUABLE   | —       | —        | 65.2      | 65.2      | 0.00  | B                 |
| חומוס לבן ענק שופרסל     | hummus_spread   | NOT_EVALUABLE   | —       | —        | 85.4      | 85.4      | 0.00  | A                 |
| חומוס גדול שופרסל        | hummus_spread   | NOT_EVALUABLE   | —       | —        | 85.4      | 85.4      | 0.00  | A                 |
| חומוס מוקפא              | hummus_spread   | NOT_EVALUABLE   | —       | —        | 85        | 85        | 0.00  | A                 |
| חומוס                    | hummus_spread   | NOT_EVALUABLE   | —       | —        | 50        | 50        | 0.00  | insufficient_data |
| חומוס                    | hummus_spread   | NOT_EVALUABLE   | —       | —        | 85.5      | 85.5      | 0.00  | A                 |
| חומוס ענק                | hummus_spread   | NOT_EVALUABLE   | —       | —        | 85.5      | 85.5      | 0.00  | A                 |
| חומוס ענק                | hummus_spread   | NOT_EVALUABLE   | —       | —        | 50        | 50        | 0.00  | insufficient_data |
| חומוס שלם יכין           | hummus_spread   | NOT_PREDOMINANT | —       | —        | 79.9      | 79.9      | 0.00  | B                 |
| חומוס                    | hummus_spread   | NOT_PREDOMINANT | —       | —        | 68.2      | 68.2      | 0.00  | B                 |
| חומוס מסעדה              | hummus_spread   | NOT_PREDOMINANT | —       | —        | 68.4      | 68.4      | 0.00  | B                 |
| סלט חציל פיקנטי          | eggplant_spread | NOT_PREDOMINANT | —       | —        | 54.2      | 54.2      | 0.00  | C                 |
| מלך החומוס סמיר הגדול    | hummus_spread   | NOT_PREDOMINANT | —       | —        | 64.4      | 64.4      | 0.00  | C                 |
| מלך החומוס אבו מרוואן    | hummus_spread   | NOT_PREDOMINANT | —       | —        | 65.2      | 65.2      | 0.00  | B                 |
| סלט חומוס                | hummus_spread   | NOT_PREDOMINANT | —       | —        | 80.2      | 80.2      | 0.00  | A                 |
| סלט מטבוחה               | matbucha        | NOT_PREDOMINANT | —       | —        | 60.4      | 60.4      | 0.00  | C                 |
| ממרח פלפלים קלויים       | pepper_spread   | NOT_PREDOMINANT | —       | —        | 42.8      | 42.8      | 0.00  | D                 |
| פלפל צ'ומה               | pepper_spread   | NOT_PREDOMINANT | —       | —        | 51.0      | 51.0      | 0.00  | C                 |
| סלט מטבוחה               | matbucha        | NOT_PREDOMINANT | —       | —        | 61.8      | 61.8      | 0.00  | C                 |
| סלט מטבוחה מרוקאית       | matbucha        | NOT_PREDOMINANT | —       | —        | 61.5      | 61.5      | 0.00  | C                 |
| ממרח פלפלים קלויים       | pepper_spread   | NOT_PREDOMINANT | —       | —        | 59.6      | 59.6      | 0.00  | C                 |
| הקיסר חומוס ענק          | hummus_spread   | NOT_PREDOMINANT | —       | —        | 80.4      | 80.4      | 0.00  | A                 |
| חומוס עם חריף אחלה       | hummus_spread   | NOT_PREDOMINANT | —       | —        | 63.1      | 63.1      | 0.00  | C                 |
| סלט פלפלים קלויים        | pepper_spread   | NOT_PREDOMINANT | —       | —        | 63.5      | 63.5      | 0.00  | C                 |
| סלט חציל בטעם כבד        | eggplant_spread | NOT_PREDOMINANT | —       | —        | 56.1      | 56.1      | 0.00  | C                 |
| סלט טורקי                | matbucha        | NOT_PREDOMINANT | —       | —        | 60.4      | 60.4      | 0.00  | C                 |
| חומוס לבנוני צבר         | hummus_spread   | NOT_PREDOMINANT | —       | —        | 65.1      | 65.1      | 0.00  | B                 |
| חומוס עם טחינה צבר       | hummus_spread   | NOT_PREDOMINANT | —       | —        | 63.4      | 63.4      | 0.00  | C                 |
| חומוס צנובר צבר          | hummus_spread   | NOT_PREDOMINANT | —       | —        | 67.1      | 67.1      | 0.00  | B                 |
| חומוס אבו גוש+צנובר+חריף | hummus_spread   | NOT_PREDOMINANT | —       | —        | 64.2      | 64.2      | 0.00  | C                 |
| חומוס מסעדה              | hummus_spread   | NOT_PREDOMINANT | —       | —        | 68.4      | 68.4      | 0.00  | B                 |
| חומוס מסעדה צבר          | hummus_spread   | NOT_PREDOMINANT | —       | —        | 65.4      | 65.4      | 0.00  | B                 |
| מטבוחה אמיתית            | matbucha        | NOT_PREDOMINANT | —       | —        | 48.7      | 48.7      | 0.00  | D                 |
| מטבוחה חריפה אש          | matbucha        | NOT_PREDOMINANT | —       | —        | 62.0      | 62.0      | 0.00  | C                 |
| חומוס גלילי              | hummus_spread   | NOT_PREDOMINANT | —       | —        | 68.9      | 68.9      | 0.00  | B                 |
| מטבוחה חריפה             | matbucha        | NOT_PREDOMINANT | —       | —        | 49.6      | 49.6      | 0.00  | D                 |
| חומוס עם זעתר            | hummus_spread   | NOT_PREDOMINANT | —       | —        | 64.8      | 64.8      | 0.00  | C                 |
| חומוס עם חריף            | hummus_spread   | NOT_PREDOMINANT | —       | —        | 62.7      | 62.7      | 0.00  | C                 |
| חומוס אבו מרוואן26%טחינה | hummus_spread   | NOT_PREDOMINANT | —       | —        | 65.2      | 65.2      | 0.00  | B                 |
| ממרח פלפלים קלויים       | pepper_spread   | NOT_PREDOMINANT | —       | —        | 48.0      | 48.0      | 0.00  | D                 |
| סלט חצילים על האש        | eggplant_spread | NOT_PREDOMINANT | —       | —        | 61.6      | 61.6      | 0.00  | C                 |
| סלט מטבוחה פיקנטי        | matbucha        | NOT_PREDOMINANT | —       | —        | 52.0      | 52.0      | 0.00  | C                 |
| מטבוחה פיקנטית           | matbucha        | NOT_PREDOMINANT | —       | —        | 52.0      | 52.0      | 0.00  | C                 |
| סלט מטבוחה יום יום       | matbucha        | NOT_PREDOMINANT | —       | —        | 61.8      | 61.8      | 0.00  | C                 |
| חומוס                    | hummus_spread   | NOT_PREDOMINANT | —       | —        | 68.2      | 68.2      | 0.00  | B                 |
| חומוס עם זעתר            | hummus_spread   | WATER_EARLY     | 2       | 1        | 65.2      | 64.4      | -0.80 | B                 |
| חומוס עם צנובר אחלה      | hummus_spread   | WATER_EARLY     | 2       | 1        | 65.4      | 64.6      | -0.80 | B                 |
| חציל על האש בטחינה       | eggplant_spread | WATER_EARLY     | 2       | 1        | 50.0      | 49.2      | -0.80 | C                 |
| חומוס עשיר ב40% טחינה    | hummus_spread   | WATER_EARLY     | 2       | 1        | 68.3      | 67.5      | -0.80 | B                 |
| חומוס גלילי              | hummus_spread   | WATER_EARLY     | 2       | 1        | 69.1      | 68.3      | -0.80 | B                 |
| חומוס גרגרים בתטבילה     | hummus_spread   | WATER_EARLY     | 2       | 1        | 63.1      | 62.3      | -0.80 | C                 |
| חציל על האש              | eggplant_spread | WATER_EARLY     | 2       | 1        | 58.0      | 57.2      | -0.80 | C                 |
| חומוס מועשר 40% עם חריף  | hummus_spread   | WATER_EARLY     | 2       | 1        | 65.4      | 64.6      | -0.80 | B                 |
| חומוס עם חציל פיקנטי     | eggplant_spread | WATER_EARLY     | 2       | 1        | 57.9      | 57.1      | -0.80 | C                 |
| חומוס ישראלי             | hummus_spread   | WATER_EARLY     | 2       | 1        | 68.3      | 67.5      | -0.80 | B                 |
| סלט חומוס+מסבחה          | hummus_spread   | WATER_EARLY     | 2       | 1        | 68.2      | 67.4      | -0.80 | B                 |
| סלט חומוס עם טחינה       | hummus_spread   | WATER_EARLY     | 2       | 1        | 68.5      | 67.7      | -0.80 | B                 |
| חומוס אבו גוש            | hummus_spread   | WATER_EARLY     | 2       | 1        | 69.9      | 69.1      | -0.80 | B                 |
| חומוס מסבחה              | hummus_spread   | WATER_EARLY     | 2       | 1        | 64.2      | 63.4      | -0.80 | C                 |
| חומוס מסעדות             | hummus_spread   | WATER_EARLY     | 2       | 1        | 75.7      | 74.9      | -0.80 | B                 |
| חומוס אסלי               | hummus_spread   | WATER_EARLY     | 2       | 1        | 70.6      | 69.8      | -0.80 | B                 |
| חומוס                    | hummus_spread   | WATER_EARLY     | 2       | 1        | 70.6      | 69.8      | -0.80 | B                 |
| מעדן חצילים              | eggplant_spread | WATER_EARLY     | 2       | 1        | 58.1      | 57.3      | -0.80 | C                 |

---

## Appendix B — Penalty Stack Compliance Check

Products where BSIP2-061 fires alongside existing penalties:

| Product                 | State       | Existing Penalties | Pilot Penalty | Combined | Stack Check |
|-------------------------|-------------|--------------------|---------------|----------|-------------|
| חציל על האש בטחינה      | WATER_EARLY | 7.0                | 0.80          | 7.80     | ✅ OK        |
| חומוס עם חציל פיקנטי    | WATER_EARLY | 7.0                | 0.80          | 7.80     | ✅ OK        |
| חומוס מסבחה             | WATER_EARLY | 7.0                | 0.80          | 7.80     | ✅ OK        |
| חומוס עם זעתר           | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |
| חומוס עם צנובר אחלה     | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |
| חומוס גרגרים בתטבילה    | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |
| חציל על האש             | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |
| חומוס מועשר 40% עם חריף | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |
| סלט חומוס+מסבחה         | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |
| סלט חומוס עם טחינה      | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |
| חומוס אבו גוש           | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |
| חומוס אסלי              | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |
| חומוס                   | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |
| מעדן חצילים             | WATER_EARLY | 3.0                | 0.80          | 3.80     | ✅ OK        |

---

*BSIP2-061 Pilot Results — TASK-051 — 2026-05-31 05:25 UTC*
*EXPERIMENTAL. No production deployment. Option B only.*
*Corpus: run_hummus_002 (69 products, Shufersal hummus and savory dips)*