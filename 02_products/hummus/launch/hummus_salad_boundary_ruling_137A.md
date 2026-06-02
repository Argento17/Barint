# Hummus Boundary Ruling: Raw Chickpeas vs Prepared Hummus — Nutrition Agent

**Task:** TASK-137A
**Reviewer:** Nutrition Agent
**Date:** 2026-06-01
**Trigger:** Product Owner: raw chickpeas are still apparent on a shelf meant for prepared hummus.

---

## The discriminator (this is the rule going forward)

"Has chickpeas" is **not** a boundary test — every hummus contains chickpeas. "Named סלט" is
**not** a boundary test either — a tahini-based chickpea salad is still hummus. The only test is:
**is this a prepared, ready-to-eat hummus/masabacha product, or is it raw/dry/canned chickpeas?**

| Marker | Prepared hummus (KEEP) | Raw/dry chickpeas (EXCLUDE) |
|--------|------------------------|------------------------------|
| Tahini (טחינה) | present | absent |
| Sodium /100g | 300–480 mg (salted) | ~0–15 mg (unsalted) |
| Energy /100g | 250–290 kcal (water/oil diluted) | 360–390 kcal (dry legume) |
| Ingredient list | full prepared list | absent or just chickpea/water/salt |
| Protein /100g | ~7–8 g (diluted); up to ~18 g for a thick salad | high, but **alone proves nothing** |

**Protein is NOT a boundary signal by itself.** A thick tahini-based salad legitimately reaches
~18 g (that is why `סלט חומוס` is kept). Sodium + energy + tahini are the reliable separators.

---

## Ruling

### EXCLUDE — raw/dry chickpeas mis-tagged as `hummus_spread`
| ID | Name | Score | Sodium | Energy | Tahini | Why |
|----|------|-------|--------|--------|--------|-----|
| `bsip1_1990261` | חומוס | 73/B | **12 mg** | **380 kcal** | none (no ingredient list) | Dry/raw chickpeas, not a spread. |
| `bsip1_3643714` | חומוס | 73/B | **12 mg** | **380 kcal** | none (no ingredient list) | Duplicate of the above; same signature. |

Same class as the existing `EXCLUDED_NOVA1_IDS` (raw/frozen/canned whole chickpeas, TASK-069).
They slipped the filter only because they were tagged `hummus_spread` and carried partial data
(scored 73/B with no ingredient list). Implemented in `hummus-comparison-page-data.ts` as
`EXCLUDED_RAW_CHICKPEA_IDS`.

### KEEP — all prepared, tahini-based salads/spreads (Product Owner ruling: "DO NOT EXCLUDE HUMUS SPREADS/SALAD")
| ID | Name | Score | Sodium | Energy | Tahini |
|----|------|-------|--------|--------|--------|
| `bsip1_6666307` | סלט חומוס | 80/A | 480 mg | 257 kcal | yes (שומשומין) |
| `bsip1_7296073725374` | סלט חומוס עם טחינה | 68/B | 365 mg | 285 kcal | yes (גולמית 17%) |
| `bsip1_7296073725367` | סלט חומוס+מסבחה | 68/B | 373 mg | 288 kcal | yes (גולמית 15%) |

> **Correction of record:** an earlier draft of this ruling proposed excluding `bsip1_6666307`
> on a protein-only read (18.2 g). That was wrong — protein alone is not a boundary signal, and
> the product is a salted, tahini-based prepared salad. Product Owner declined the exclusion;
> the corrected discriminator above (sodium + energy + tahini) keeps it and correctly catches the
> two genuinely raw items instead.

---

## Impact (for 137D)
- Displayed: 37 → **35**. Grade-A: **1** (unchanged — `סלט חומוס` stays #1 at 80/A). Top 80, range 63–80.
- Counts are computed dynamically from the displayed set, so hero stats / prologue counts update
  automatically; no hardcoded count edits required.
- **Pre-existing content drift to fix in 137B:** the component insight line "פער ציון של 37
  נקודות … לתחתית הרשימה" no longer matches the data (current range is 80→63 = 17 pts). Stale,
  not caused by this change.

---

## Part — Why protein is the right HEADLINE metric (feeds the 137B prologue)
Unchanged and still valid. Protein is the headline because it is hummus's defining nutritional
contribution, a legible proxy for the real-food (chickpea+tahini) fraction vs. water/oil dilution,
the most trustworthy number we can show (fat is suppressed in this corpus), and consumer-legible.
**Guardrail:** protein is the headline, not the whole score, and — per this ruling — not a
category-boundary test.

---

*Nutrition Agent — TASK-137A — 2026-06-01*
*Ruling: EXCLUDE 2 raw-chickpea items (sodium 12 / energy 380 / no tahini). KEEP all prepared
tahini-based salads & spreads incl. סלט חומוס 80/A. Discriminator = sodium + energy + tahini, never protein alone.*
