# Bari Row Description — Nutrition Grounding Guide v1

Companion to `row_description_standard_v1.md`. The standard says every line must be
**trace-anchored**; this guide says, per category, **what is true to cite and what is
off-limits**, so sharper "decision-driver-first" copy never overstates. Produced by the
Nutrition Agent (TASK-168 Phase 1). No scores/copy/code changed by this doc.

## Cross-category hard rules (all 252 lines)

- **Cite only fields that are non-null in that product's record.** Null is null — never infer,
  round up, or "estimate." If `sugar: null`, the line may not mention sugar at all.
- **Banned vocabulary in consumer text:** NOVA, BSIP, cap, floor, structural_class.
- **No health/diet claims.** Bari scores nutritional architecture, not health outcomes. No
  "healthy / good for you / guilt-free." `נקי` only as a *structural* statement (short list /
  no additives detected) and only when data supports it — never as a health verdict.
- **Units:** protein/sugar/fat in grams, sodium in mg, energy in kcal, **per 100g**. Echo the
  record's own precision (`11.5` stays `11.5`, `10.4` stays `10.4`). Don't invent precision.
- **Ingredient counts / declared %** citable only from the actual list arrays, not eyeballed.
- **A short ingredient list is a structural fact, not a virtue.** "3 רכיבים" citable; "ולכן בריא" not.
- **The score is not a recommendation.** High score within a category ≠ "good" in absolute terms.

## Quick reference — citable nutrition fields per category

| Category | Citable (non-null) | Never cite (null/suppressed) |
|---|---|---|
| מעדנים | protein, energy, fat, sodium; sugar *only where present* | sugar where null |
| חומוס | protein, energy, sodium, declared % | **fat & sat-fat (suppressed)**, **sugar (0% coverage)** |
| גבינות | protein, fat, energy, sodium | sugar (mostly null), fiber; ingredient string withheld; sodium/sat-fat not "favorable" |
| יוגורט | protein, energy, fat, sodium; sugar *only where present* | sugar where null; ingredient string withheld |
| לחם | protein, fiber, sodium | **energy, sugar, fat (all null)**; ingredient string null |
| חטיפים | ingredient %, ingredient count, trace-surfaced figures only | **all nutrition-panel grams (all null)** |

---

## 1. מעדנים (dairy desserts)
- **Decision-drivers:** (1) protein source — milk/milk-protein vs thin sweet base; (2) added-sugar / sweetener + stabilizer load.
- **May cite:** protein, energy, fat, sodium; sugar only where present; ingredient identity (main ingredient, named sweetener/flavor/stabilizer/probiotic when actually in the list); ingredient count.
- **Forbidden:** calling a diet/light 4g cup "high protein"; implying "no sugar" when `sugar:null`; reading "מעודנת/light/ביו" as a virtue; "probiotic = healthy."
- **Signature tension:** the מילקי icon-paradox — the most trusted-looking dessert scores bottom (E) while a plain high-protein cup leads. *Icon ≠ architecture.* For minimal-looking plant cups: *looks minimal, list is long.*

## 2. חומוס וממרחים
- **Decision-drivers:** (1) protein as proxy for real chickpea+tahini vs water/oil dilution; (2) additive/stabilizer/preservative presence. Declared chickpea % / tahini % are cleanest.
- **May cite:** protein, energy, sodium; declared %; ingredient count; named additives that appear.
- **Forbidden:** **any fat claim** (fat & sat-fat suppressed, HUM-001); **any sugar claim** (0% coverage, HUM-002); equating higher protein with "more tahini" as a guarantee; "clean" when named preservatives present; treating matbucha/eggplant/pepper spreads as protein-driven.
- **Signature tension:** protein (and declared %) exposes dilution — two identical-looking tubs differ because one is chickpea+tahini, the other padded with water+oil.

## 3. גבינות לבנות וממרחים
- **Decision-drivers:** (1) protein-to-fat balance; (2) processing structure of spread/light variants (stabilizers/gums/starch replacing fat).
- **May cite:** protein, fat, energy, sodium; ingredient count / "no additives detected" **from signals only** (ingredient string withheld); sub-pool identity from `_cluster`. **Saturated fat IS citable** as a value with the red-label "סימון אדום" when it comes from the product's real `limitingFactors`/trace — even though it is not in the displayed `nutrition` grid — PROVIDED it is framed as **"מחוץ לציון"** (outside the score), never as a virtue. (Owner-approved TASK-168, 2026-06-02; this is the honest-transparency exception to the cross-category "non-null displayed field" rule.)
- **Forbidden:** citing sodium/sat-fat as favorable or "low," or implying the score covers them (**it does not**); treating "לייט" as cleaner (light often adds stabilizers+salt, may rank below full-fat); quoting an ingredient when `ingredients:null`; "high fiber" (dairy is fiber-free).
- **Signature tension:** macro-good, structure-processed — best protein-to-fat ratio on the shelf can still be a processed spread carrying salt/sat-fat the score leaves out.

## 4. יוגורט
- **Decision-drivers:** (1) protein level + source; (2) added sugar vs plain base.
- **May cite:** protein, energy, fat, sodium; sugar **only where present**; live-culture/base-simplicity **from signals only** (ingredient string withheld); "ללא סוכר מוסף שזוהה" only where the trace asserts it.
- **Forbidden:** "no added sugar / low sugar" when `sugar:null`; naming a specific culture not in the product's signals; probiotic health claims; presenting the top product as excellent in absolute terms — **validated ceiling is B, not A.**
- **Signature tension:** protein vs added sugar — the shelf rewards protein but is full of cups where sweetened flavoring offsets it. Preserve the "שזוהה/detected" hedge; never flatten to "no sugar."

## 5. לחם
- **Decision-drivers:** (1) whole-grain base vs refined flour; (2) genuine fermentation (sourdough); secondarily fiber *source* (grain-intrinsic vs added inulin/chicory).
- **May cite:** protein, fiber, sodium; whole-grain/sourdough/refined/added-fiber **from signals only**. **Never cite energy, sugar, fat (all null)** or quote ingredients (null).
- **Forbidden:** asserting "מחמצת/sourdough" unless that product's signal carries it (engine can't distinguish genuine from industrial sourdough-powder); calling fiber "from whole grain" when flagged as added; calling a "מלא"-claim bread whole-grain when `limitingFactors` says "בסיס קמח מזוקק." Re `shufersal_3268429`: follow the live grade, don't re-litigate the A/B divergence in copy.
- **Signature tension:** "healthy-looking" white flour — the bread that *looks* wholesome (dark, seeds, "מלא/אקטיב") is often refined-flour base + added fiber + seed halo.

## 6. חטיפים (snack bars)
- **Decision-drivers:** (1) sugar source — whole-fruit (dates) vs added syrup/glucose; (2) protein quality/source (real nuts/legumes vs coating+syrup).
- **May cite:** **nutrition panel is entirely null** — cite ONLY trace-derived ingredient figures already in the record (declared % like "תמרים 76%", ingredient counts, and the specific sugar/protein figures already embedded in that product's surfaced signals). If a number isn't already in that product's arrays, it can't be introduced.
- **Forbidden:** inventing/citing any nutrition-panel number (highest fabrication risk of all six); implying "low sugar/healthy" from a short list; presenting whole-fruit sugar as "free" (a date bar can still cross the red-label threshold); any A-grade implication — **ceiling is B (snk-001 = 70/B).**
- **Signature tension:** clean list ≠ low sugar — the best-scoring snack wins on minimal structure yet is still sugar-dense from fruit. State both, or neither.

## Top fabrication-risk flags for writers
1. **Snacks** — panel fully null; only trace ingredient figures already in the record may be cited.
2. **Hummus** — fat/sat-fat suppressed, sugar uncovered; any fat/sugar claim is ungrounded.
3. **Cheese** — sodium & sat-fat are *outside the score*; a high score is never "healthy/low-salt."
4. **Bread** — sourdough unverifiable; cite מחמצת only where the product's own signal asserts it.
5. **Sugar "שזוהה/detected" hedge** (yogurt, snacks) is deliberate — preserve it; never flatten.
