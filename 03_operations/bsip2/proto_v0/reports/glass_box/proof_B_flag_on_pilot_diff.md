**Task:** TASK-179G

# Glass Box D5/D6 — Proof B: FLAG-ON Pilot Diff (hummus + maadanim)

**Date:** 2026-06-04 · **Author:** Data Agent · **Flag:** `BARI_GLASSBOX_D5D6=on` vs `off`
**Result: PASS — every ON-vs-OFF delta is a DEMOTE or a NULL. Zero promotions.**

---

## 1. What this proves

D6 can only **demote** (ceiling/`insufficient_data`) or **withhold→null** (`לא נוקד`); it can
never raise a score or improve a grade (spec §2.4, EV-038/039). The pilot scores both pilot
corpora through the standard pipeline twice, toggling only `BARI_GLASSBOX_D5D6`, and checks
every product. Harness: `src/run_glassbox_pilot_diff.py`. Scratch tables:
`reports/glass_box/_pilot_{hummus,maadanim}_{off,on}.json`, `_pilot_summary.json`.

## 2. Counts

| Corpus | n | demoted | withheld→null | unchanged | endemic_flavoring detected | **promotions** |
|---|---|---|---|---|---|---|
| hummus | 69 | 0 | 4 | 65 | 3 | **0** |
| maadanim | 200 | 5 | 32 | 163 | 130 | **0** |

**Promotions across both pilots: 0** (hard invariant holds — no score up, no grade up).

### Endemic-flavoring exclusion (EV-036) confirmed working
`חומרי טעם וריח` bare was detected in **130/200 maadanim panels (~65%)** — matching the spec's
129/184. Because EV-036 **excludes** bare flavorings from band-raising and from the D6
reduction, the bulk of maadanim does **not** demote: only 5 demoted + 32 withheld, **163
unchanged**. Without the exclusion, ~65% of the shelf would have demoted (a category-blind
distortion). The exclusion is load-bearing and behaving as designed.

### Withhold breakdown (the conservative, reluctant-to-withhold posture, Q1)
The 32 maadanim + 4 hummus withholds are **floor-of-observability failures only**:
- maadanim: **31 `no_nutrition_data`** (already non-graded under OFF — the existing
  evaluation-scope flag; Glass Box relabels `insufficient_data → לא נוקד`, a more honest
  "we decline to rank" rather than a guessed middle), **1 ingredient-panel-absent**.
- hummus: **4 panel-absent** (no `ingredients_raw` at all — `panel_present=False`).

No product was withheld for being merely thin: the `d6_confidence < 30 AND severe-band` co-
requirement (NULL_FLOOR=30) reserves null for genuine floor failures. Short clean single-
ingredient hummus (e.g. `חומוס לבן ענק שופרסל`, `חומוס מוקפא`) correctly resolve to the
**full** band via single-ingredient protection and keep their 85/A (byte-identical to OFF) —
the perverse "clean whole food looks incomplete" inversion is prevented.

## 3. Concrete examples (OFF → ON, with the D5 gap that drove it)

| Product | OFF | ON | Driver |
|---|---|---|---|
| `ג'לי בטעם ענבים` (maadanim) | 34.5/E, conf 45 | 34.5/**insufficient_data**, conf 35 | D5 band **partial** (bare additive + missing fields) → −10 conf → crosses legacy <40 insufficient gate. **demote.** |
| `סוכריות תפוז לל"ס` (maadanim) | 41.8/D, conf 40 | 41.8/**insufficient_data**, conf 30 | D5 band **partial** → −10 conf (40→30) → legacy insufficient gate fires. **demote** (grade removed, score unchanged). |
| `בולגרית מעודנת 24%` (maadanim) | 45.0/D | **None / לא נוקד** | D5 band **severe** + thin nutrition (conf<30 after reduction) → floor failure. **withhold.** |
| `פרוביוטיק פמינה` (maadanim) | 50/insufficient_data | **None / לא נוקד** | `no_nutrition_data` (no nutrition panel; ingredient panel = cultures only) → panel-absent floor failure. **withhold** (was already non-graded; relabelled). |
| `חומוס` (hummus, `bsip1_1990261`) | 72.1/B | **None / לא נוקד** | `ingredients_raw` absent (`panel_present=False`) → severe band + conf<30 floor failure. **withhold** — engine declines to publish a grade built on an invisible formulation. |

Contrast (protection working): `חומוס מוקפא`, `חומוס גדול שופרסל` — clean single-ingredient
panels → **full** band → **unchanged 85/A** (no demote). Only the genuinely panel-less
`חומוס` SKUs are withheld.

## 4. Verdict

**PASS.** Every ON-vs-OFF delta is a demote or a null; zero promotions. The endemic-flavoring
exclusion (EV-036) keeps the maadanim shelf from over-demoting (163/200 unchanged). Withholds
are reserved for genuine floor failures (panel/nutrition absent, or severe+thin). All ON
behavior is consistent with the spec and the frozen-invariant safety guarantee (D6 only
removes/caps, never promotes). **Nothing ships:** these numbers are produced behind the
default-OFF flag and the −10/−20/30/60 thresholds remain PROPOSALS pending Product D7 co-sign.
