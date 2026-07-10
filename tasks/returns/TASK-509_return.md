# TASK-509 Return — Expansion Nutrition Bar Config: DEFAULT vs Category Scales

**Proposed status:** RETURNED
**Closing authority:** Orchestrator (verify artifacts before accepting)
**Date:** 2026-07-05

---

## Verdict Summary

Four categories — bread, cheese, crackers, milk — currently render expansion nutrition bars using `DEFAULT_NUTRITION` scales because no `category` prop is passed from their comparison page components. Analysis of real product data from live comparison JSONs confirms this is a latent display bug for three of the four categories (bread, cheese, milk) and a partial bug for crackers.

### Per-Category Findings

**Bread — Latent display bug (low-medium severity)**
- Config `bread` exists in expansion-section.tsx (lines 104–110).
- Protein thresholds happen to match DEFAULT (goodAbove=8), but energy scale (bread max=350 vs DEFAULT max=400) and sugar scale (bread max=10 vs DEFAULT max=20) are miscalibrated under DEFAULT.
- Bar proportions misrepresent bread shelf context.
- Fix: pass `category="bread"` in `bread-comparison-page.tsx`.

**Cheese — Latent display bug (high severity)**
- Config `cheese` exists in expansion-section.tsx (lines 135–141).
- Critical flip: protein `goodAbove` is 8 under DEFAULT vs 20 under `cheese` config.
- Effect: ALL fresh cheese products (11–17g protein per 100g) display a green protein bar under DEFAULT. Under `cheese` config, they correctly show neutral grey (baseline for fresh cheese) — only genuinely high-protein cheeses (>20g) would show green.
- This is nutritionally dishonest: DEFAULT makes cottage cheese look exceptional when 11g is the category baseline.
- Fix: pass `category="cheese"` in `cheese-comparison-page.tsx`.

**Crackers — Partial bug (medium severity, missing config)**
- No `crackers` config exists in CATEGORY_NUTRITION. `crackers` is absent from the map entirely.
- Primary problem: energy scale DEFAULT max=400 causes bar overflow for typical crackers (380–418 kcal), since crackers are legitimately 380–480 kcal as dehydrated products.
- Protein goodAbove=8 under DEFAULT flags essentially the whole crackers shelf green (little differentiation).
- Proposed new config: energyKcal max=500, protein goodAbove=12/warnBelow=5, sugar max=10/goodBelow=1/warnAbove=5, sodium max=600.
- This proposed config requires D7 co-sign (Nutrition + Product Agent) before going live.

**Milk — Severe latent display bug**
- Config `milk` exists in expansion-section.tsx (lines 89–94) but is unreachable.
- Two-layer bug: (1) `category` prop not passed by `milk-comparison-page.tsx`; (2) even if passed, the route id `milk-comparison` has no alias to the config key `milk` in `CATEGORY_NUTRITION_ALIASES`.
- Under DEFAULT: serving label is "ל-100 גרם" (factually wrong unit — milk is per 100 ml); energy bars are 7–17% fill (near-invisible, max=400 vs milk actual 43–69 kcal/100ml); sodium bars are ~7% fill (max=600 vs milk actual 41–60 mg/100ml); the protein differentiator for enriched milk (6.5g) is invisible (neutral grey under DEFAULT, would be green under `milk` config goodAbove=5).
- Fix: pass `category="milk-comparison"` in `milk-comparison-page.tsx` AND add alias `"milk-comparison": "milk"` to `CATEGORY_NUTRITION_ALIASES` in expansion-section.tsx (or pass `category="milk"` directly).

---

## What a Follow-Up Implementation Task Would Change

A frontend PR (separate from nav/SEO) would:
1. `bari-web/src/components/comparisons/bread-comparison-page.tsx` — add `category="bread"` to `<ComparisonPage>`.
2. `bari-web/src/components/comparisons/cheese-comparison-page.tsx` — add `category="cheese"` to `<ComparisonPage>`.
3. `bari-web/src/components/comparisons/milk-comparison-page.tsx` — add `category="milk-comparison"` to `<ComparisonPage>`.
4. `bari-web/src/components/comparisons/crackers-comparison-page.tsx` — add `category="crackers"` to `<ComparisonPage>`.
5. `bari-web/src/components/shared/expansion-section.tsx` — add `"milk-comparison": "milk"` to `CATEGORY_NUTRITION_ALIASES`; add new `crackers` config to `CATEGORY_NUTRITION`.

Gate requirements: Nutrition Agent sign-off (this memo), Product Agent D7 co-sign on the crackers config (new rule), Design Agent render re-verify (milk bars will look substantially different).

---

## Artifacts

| Path | Action | SHA256 |
|---|---|---|
| `03_operations/reports/nutrition/task509_expansion_config_recommendation_v1.md` | created | E72B74544C5B4BD4857F5F562EB0B6F466D658EE6A5C1AF1CA8994823D930E45 |
| `tasks/returns/TASK-509_return.md` | created | (self) |

---

```json
{
  "task": "TASK-509",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/nutrition/task509_expansion_config_recommendation_v1.md",
      "action": "created",
      "sha256": "E72B74544C5B4BD4857F5F562EB0B6F466D658EE6A5C1AF1CA8994823D930E45"
    }
  ],
  "counts": {
    "categories_analysed": "4/4 (bread, cheese, crackers, milk — all specified in task scope)",
    "products_sampled_bread": "5/23 (bread_frontend_v4.json, ranks 1-5 by score)",
    "products_sampled_cheese": "6/47 (cheese_frontend_v4.json, ranks 1-6 by score)",
    "products_sampled_crackers": "3/19 (crackers_frontend_v1.json, ranks 1-3 by score)",
    "products_sampled_milk": "5/18 (milk_frontend_v1.json, ranks 1-4 + rank 7 by score)",
    "configs_existing_and_correct": "3/4 (bread, cheese, milk configs exist; crackers absent)",
    "configs_currently_active": "0/4 (none wired — category prop not passed in any of the 4 comparison page components)",
    "categories_passing_category_prop": "13/17 live comparison pages pass category= (bread, cheese, crackers, milk are the 4 that do not — verified by grep of comparisons/ directory)",
    "protein_color_flips_cheese": "5/5 sampled products flip from green (DEFAULT) to neutral-grey (cheese config) — the defining display bug"
  },
  "commands_run": [
    {
      "cmd": "Read C:\\bari\\bari-web\\src\\components\\shared\\expansion-section.tsx",
      "exit_code": 0
    },
    {
      "cmd": "Read C:\\bari\\bari-web\\src\\data\\comparisons\\bread_frontend_v4.json (ranks 1-5)",
      "exit_code": 0
    },
    {
      "cmd": "Read C:\\bari\\bari-web\\src\\data\\comparisons\\cheese_frontend_v4.json (ranks 1-6)",
      "exit_code": 0
    },
    {
      "cmd": "Read C:\\bari\\bari-web\\src\\data\\comparisons\\crackers_frontend_v1.json (ranks 1-3)",
      "exit_code": 0
    },
    {
      "cmd": "Read C:\\bari\\bari-web\\src\\data\\comparisons\\milk_frontend_v1.json (ranks 1-7)",
      "exit_code": 0
    },
    {
      "cmd": "Grep pattern=category= path=C:\\bari\\bari-web\\src\\components\\comparisons output_mode=content",
      "exit_code": 0
    },
    {
      "cmd": "Read C:\\bari\\bari-web\\src\\components\\comparisons\\bread-comparison-page.tsx",
      "exit_code": 0
    },
    {
      "cmd": "Read C:\\bari\\bari-web\\src\\components\\comparisons\\cheese-comparison-page.tsx",
      "exit_code": 0
    },
    {
      "cmd": "Read C:\\bari\\bari-web\\src\\components\\comparisons\\crackers-comparison-page.tsx",
      "exit_code": 0
    },
    {
      "cmd": "Read C:\\bari\\bari-web\\src\\components\\comparisons\\milk-comparison-page.tsx",
      "exit_code": 0
    },
    {
      "cmd": "PowerShell Get-FileHash task509_expansion_config_recommendation_v1.md -Algorithm SHA256",
      "exit_code": 0
    }
  ],
  "not_done": [],
  "self_check": "Spec requires: per-category verdict table (DEFAULT-correct vs latent-bug), product-level flip analysis with real numbers and source file:line, recommendation, and what a follow-up implementation task would change. All four items delivered in the memo. Flip analysis for cheese: 5/5 sampled products flip from green to grey on protein (DEFAULT goodAbove=8 vs cheese goodAbove=20) — source expansion-section.tsx line 137, cheese_frontend_v4.json products barcode 7290014758681/6040619/4127077/4127329/41445 protein 11.5/17.0/11.0/11.0/11.0g respectively. Milk unit error confirmed: DEFAULT servingLabel is 'ל-100 גרם' (expansion-section.tsx line 196) vs milk config 'ל-100 מ״ל' (line 93)."
}
```
