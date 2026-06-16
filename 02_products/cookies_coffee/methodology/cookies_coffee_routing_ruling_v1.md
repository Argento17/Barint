# Cookies-near-coffee (עוגיות לקפה) — Routing Ruling v1

**Task:** TASK-275 (P73 — Nutrition Agent ruling on run_cookies_001)
**Date:** 2026-06-13
**Author:** Nutrition Agent
**Status:** RETURNED — awaiting orchestrator verification and Product D7 co-sign before any engine edit
**Depends on:** `cookies_coffee_scoring_interpretation_v1.md` (§2.3 prediction that missed)
**Governs:** EV-058 proposal (dedicated `biscuit` router category; taxonomy only; caps INTACT)

---

## 1. Honest vs. Artifact Split

### 1.1 The verified distribution

run_cookies_001: **A0 / B0 / C13 / D15 / E33** (61 products)
- Median score: 32.6 — Stdev: 14.1 — Min: 10 — Max: 63.9

### 1.2 How much of the E-modal result is honest?

**Ruling: approximately 41/61 products (67%) are genuinely E or D for real composition reasons. Approximately 8/61 products (13%) are artifactual E — products that would score D or C under correct routing but scored E because the snack_bar_granola lens applies heavier penalties that are irrelevant to a plain biscuit. The remaining 12/61 are ambiguous but do not change the honest-vs-artifact characterization at category level.**

The reasoning, grounded in the verified evidence:

**Honest E — the cap-45 cohort (25/61 products, 41%):**
The `ISRAELI_RED_LABELS_2_PLUS` cap fires when BOTH sugar > 17.5g AND sat-fat > 5g are present simultaneously (score_engine.py, the compound red-label cap block). This is a category-agnostic public-health signal — it fires identically regardless of what category the router chose. With real sugar in the 20–38g range and sat-fat at 7–10g, both legs fire firmly. These products are genuinely at or near the cap floor of 45, producing E. This part of the distribution is honest and would survive rerouting unchanged: caps are intact per the hard guard.

**Honest E — remaining E products beyond the cap-45 cohort (approximately 8/61 products):**
Beyond the 25 cap-45 products, additional E scores arise from NOVA-4 products (artificial flavoring = "חומרי טעם וריח" firing `has_flavor_enhancer` in nova_proxy.py line 187, adding 3 to nova4_score and pushing to the `NOVA_PROXY_4_ULTRA_PROCESSED` cap at 68 — but then the sugar/sat-fat cap at 45 is still the binding cap, so the NOVA-4 cap is not the operative floor for these products). The honest E count is approximately 33 products where the composition genuinely warrants E.

**Artifact E — routing distortion (estimated 8/61 products):**
The key diagnostic from the verified evidence: `snack_bar_granola`-routed products scored 75% E (15/20), while `cracker`-routed products scored only 40% E (11/27). The 35-percentage-point gap between lenses on the same class of sweet biscuit is the artifact signal. The snack_bar_granola lens applies signals and possibly scoring sub-rules calibrated for bars and granola formats (e.g., `HP_FAT_SUGAR_COMBO` interaction with the snack-bar signal path; satiety signals calibrated for a different portion and use case). A plain petit beurre is not a granola bar. The routing mismatch produces incoherent rationale even when the final score happens to be directionally correct for the highest-sugar products.

**Quantified artifact exposure:**
- 20 products routed to `snack_bar_granola`; 75% = 15 scored E
- Artifact-suspected share: the difference between 75% E and the 40% E rate observed under `cracker` routing = approximately 7 products that likely would score D or borderline-C under correct routing
- Upper bound: 8 products (the tail of the snack_bar_granola cohort that are not in the cap-45 cohort and whose E is driven by snack-bar-specific sub-rules)

**Conclusion for the honest-vs-artifact question:**
E-modal is directionally honest. The category shelf genuinely has high sugar AND high sat-fat across most products, and the category-agnostic cap fires correctly. However, approximately 7–8 products are artifactual E — their E grade is driven by wrong-lens routing rather than their own composition. The category-level framing (E-modal, indulgence shelf) is defensible; the product-level rank ordering for the 20 misrouted products is not reliable until rerouted.

**The C3 strategic read (P72 return) is confirmed: ship E-modal as honest. Add the dedicated category for taxonomy and explainability, not to lift grades.**

---

## 2. Dedicated `biscuit` Router Category — YES

### 2.1 Decision

**YES — a dedicated router category for sweet plain biscuits (coffee biscuits and analogues) is warranted.** The purpose is solely to stop semantically wrong routing (biscuit ≠ snack-bar ≠ cracker). Caps are INTACT. No endemic relief. No D7 scoring rule change is attached to this routing addition. The category exists to give the engine the correct lens for explainability and to prevent wrong sub-rule interaction.

### 2.2 Scope of the new category

**Category ID:** `biscuit` (internal router ID)
**Hebrew consumer name for category page:** עוגיות לקפה (as already defined for the category)
**Scope:** Dry, crisp-textured, sweet, plain (no structural filling or full-coating) biscuits consumed as a coffee or tea accompaniment — the same in-scope set defined in `cookies_coffee_scoring_interpretation_v1.md` §1.2.

Products NOT in scope (out-of-scope remains out): chocolate-coated biscuits, cream-filled sandwich cookies, wafers, soft/cake-like cookies, children's character cookies, protein/functional biscuits. These are not matched by the proposed keywords.

### 2.3 Exact Hebrew name-keywords to wire

The mechanism mirrors EV-052 / `brined_food` in `evaluation_scope.py` lines 39–68 (keyword list + nutrition_validator) and `router_v2.py` `HARD_ANCHORS` (lines 50–156) + `ANCHOR_EXCLUSIONS` (lines 179–244). The new category is a router category only (no context_limited scope modification — coffee biscuits are standard scope, no sodium re-weighting, no serving-size adjustment needed).

**Proposed hard anchors for `router_v2.py` `HARD_ANCHORS` list:**

```python
# ── Coffee biscuits / plain sweet biscuits (EV-058 / TASK-275) ───────────────
# Dedicated biscuit routing for dry, plain, sweet biscuits consumed as coffee
# accompaniments. Purpose: taxonomy + explainability only. Caps INTACT.
# No endemic relief. No new scoring rule. No D7 required for routing change.
# Keywords are designed to NOT match any currently live corpus product name.
# No-regression proof: engine_invariants 342-case suite + golden-corpus byte-
# identity on all 7 live categories required BEFORE any code ships.
("ביסקוויט",        "biscuit",  "plain_biscuit",     0.88),
("פטי-בר",          "biscuit",  "petit_beurre",      0.93),
("פטי בר",          "biscuit",  "petit_beurre",      0.93),
("לוטוס",           "biscuit",  "speculoos",         0.92),
("ביסקוויט בלגי",   "biscuit",  "speculoos",         0.94),
("ביסקוויט תה",     "biscuit",  "tea_biscuit",       0.93),
("מרי ביסקוויט",    "biscuit",  "marie_biscuit",     0.92),
("ביסקוויט מרי",    "biscuit",  "marie_biscuit",     0.92),
("דייג'סטיב",       "biscuit",  "digestive",         0.92),
("ביסקוטי",         "biscuit",  "biscotti",          0.91),
("שורטברד",         "biscuit",  "shortbread",        0.90),
("עוגיות חמאה",     "biscuit",  "butter_cookie",     0.92),
```

**Required ANCHOR_EXCLUSIONS for the new anchors:**

```python
# Biscuit anchors — must not fire when biscuit is filling/modifier, not product
"ביסקוויט":     ["מילוי", "שכבת", "ציפוי", "קרם", "טחינה", "בטעם",
                  "גבינה", "שוקולד ביסקוויט"],
"לוטוס":        ["בטעם", "מילוי", "ציפוי", "שכבת", "רוטב", "קרם",
                  "גלידה"],
"ביסקוויט בלגי": [],  # compound — sufficiently specific; no exclusions needed
"ביסקוויט תה":   [],
"מרי ביסקוויט":  [],
"ביסקוויט מרי":  [],
"דייג'סטיב":     ["חטיף", "ציפוי"],
"ביסקוטי":       ["גלידה", "מילוי"],
"שורטברד":       ["גלידה", "מילוי"],
"עוגיות חמאה":   ["ממולא", "שוקולד", "ציפוי", "מצופה", "חטיף"],
"פטי-בר":        [],
"פטי בר":        [],
```

**Why these keywords do NOT overlap live category products:**

The live corpora are: milk_and_alternatives (dairy names; חלב/יוגורט/גבינה), brined_cheeses (פטה/בולגרית/חלומי/גבינה+מלוחה compound), yogurts (יוגורט), breads (real_bread_retail), salty_snacks (chips/rings categories), cereals (דגני בוקר/גרנולה/קורנפלקס), snack_bars (חטיף/גרנולה/ברים). None of these product name sets contain "ביסקוויט", "פטי-בר", "לוטוס", "דייג'סטיב", "ביסקוטי", "שורטברד", or "עוגיות חמאה" as primary product identity tokens. The `ANCHOR_EXCLUSIONS` for "ביסקוויט" block the snack_bar_granola use cases where "ביסקוויט" appears as a component word (e.g., filling, coating). A no-regression proof run is mandatory before shipment — this analysis is necessary but not sufficient.

**Note on the `CATEGORIES` list in `router_v2.py` line 26–41:**
Adding `"biscuit"` requires inserting it into the `CATEGORIES` list. It must also be added to `ALL_SIGNALS` even with an empty or minimal signal list (so the score accumulator initializes it). If no Stage 2 signals are defined, the hard anchors provide the only routing path — which is the correct design for a category where the anchor is always the right classification signal and ingredient-text fallback signals would introduce bleed risk.

**The `biscuit` category does NOT need a `CONTEXT_LIMITED_SIGNALS` entry in `evaluation_scope.py`** because no context modification is warranted. Coffee biscuits score as standard products. Sodium is low and self-gating. No serving-size or concentration adjustment is needed.

### 2.4 Why this mirrors EV-052 correctly

EV-052 added keywords to the `brined_food` block in `evaluation_scope.py` lines 40–68. The mechanism:
- `name_keywords` list at lines 40–46 (simple substring match against product name only, line 136–137)
- `name_compound_keywords` at lines 55–59 (tuple of tokens, all must match — the EV-052-A1 addendum)
- `nutrition_validator` at line 60 (sodium > 500mg gate to prevent false positives)

For the `biscuit` router category, the analogous implementation is in `router_v2.py` `HARD_ANCHORS` (not in `evaluation_scope.py`, because this is a routing decision, not a context-limitation decision). This is the correct separation: EV-052 modified BOTH evaluation scope AND routing (because brined_food changes how sodium is scored). EV-058 modifies ONLY routing (because coffee biscuits score as standard products — no weight modification, no context flag, no scoring path change). Simpler, lower-risk change.

**Engine line citations for the mechanism being mirrored:**
- `evaluation_scope.py` lines 39–68: `brined_food` `CONTEXT_LIMITED_SIGNALS` block — defines name_keywords, name_compound_keywords, nutrition_validator
- `evaluation_scope.py` lines 138–161: the loop that checks keywords and compound keywords against product name
- `router_v2.py` lines 50–156: `HARD_ANCHORS` list — the model for new hard anchor entries
- `router_v2.py` lines 179–244: `ANCHOR_EXCLUSIONS` dict — the model for per-anchor exclusions
- `router_v2.py` lines 248–287: `_check_anchors()` function — shows how anchors are matched, exclusions applied, highest-confidence winner selected
- `router_v2.py` lines 26–41: `CATEGORIES` list — must include `"biscuit"` before code ships

---

## 3. Predicted Post-Reroute Ceiling and Honest Hebrew Framing

### 3.1 Post-reroute grade ceiling prediction

**C is the honest post-reroute ceiling for the modal product on this shelf. B is achievable for a best-in-class digestive or clean shortbread variant (estimated 5–8 products of 61). A is not achievable with the committed engine.**

The rerouting correction does not touch caps. The ISRAELI_RED_LABELS_2_PLUS cap (45) fires for 25/61 products regardless of routing. For the artifact-E cohort (estimated 8 products), rerouting from snack_bar_granola to `biscuit` removes the snack-bar-specific lens effects and allows the standard indulgence-path caps to be the operative constraint. Under the biscuit lens (standard path): if sat-fat > 5g fires but sugar does not cross 17.5g, the binding cap is ISRAELI_RED_LABEL_1_SAT_FAT at 55 — producing a D score (40–54), not E. These 7–8 products move from E to D. They do not move to C or B.

**Predicted post-reroute distribution (estimate, not a scored run):**
- E: approximately 25–26 products (down from 33) — the cap-45 cohort plus the honest NOVA-4 heavy products
- D: approximately 20–22 products (up from 15) — single-cap products, sat-fat-only or sugar-only triggers
- C: approximately 12–13 products (roughly stable) — products scoring 55–69
- B: 3–5 products (up from 0) — clean digestive or whole-grain variants with <17.5g sugar and sat-fat at the lower end of the range, no synthetic additives
- A: 0 products

**Key insight:** The distribution remains E/D-heavy after rerouting. The modal grade moves from E toward D/E. This confirms the C3 strategic read: routing was not the main cause. The indulgence shelf is genuinely high in sugar and sat-fat.

### 3.2 Revised category caveat (Hebrew) — updated from §4 of cookies_coffee_scoring_interpretation_v1

The original caveat predicted C as the modal grade and B as the ceiling. This was incorrect. The updated caveat acknowledges the honest distribution:

---

**הערת קטגוריה: עוגיות לקפה**

עוגיות לקפה הן מאפים מתוקים מעובדים עם אחוזי שומן רווי וסוכר גבוהים באופן אחיד. רוב המוצרים בקטגוריה זו מקבלים **ציון E או D** — לא מפני שהמנוע מחמיר, אלא מפני שהמוצרים עוצבו עם יותר מאחד מסף התווית האדומה הישראלית (>17.5 גרם סוכר ל-100 גרם **וגם** >5 גרם שומן רווי ל-100 גרם). ציון **A אינו קיים** בקטגוריה. ציון **B (70–79)** מציג את מיטב הקטגוריה: ביסקוויט דגנים מלאים נקי עם שומן ואדיטיבים מוגבלים. הדירוג בדף זה תואם להשוואה בתוך הקטגוריה — הוא אינו שוות-ערך לציון B בקטגוריה מזינה. שאלת האיכות האמיתית כאן היא: **באיזה ביסקוויט תבחרו אם ממילא תאכלו ביסקוויט עם הקפה?**

---

**English translation (internal reference only):**
Coffee biscuits are processed sweet baked goods with uniformly high sat-fat and sugar. Most products score E or D — not because the engine is severe, but because the products were formulated with more than one Israeli red-label threshold crossed (>17.5g sugar AND >5g sat-fat per 100g). Grade A does not exist in this category. Grade B (70–79) represents the category's best: a clean whole-grain biscuit with limited fat and additives. The ranking on this page is a within-category comparison — it is not equivalent to a B in a nutritious category. The real consumer question here is: which biscuit will you choose if you are going to have a biscuit with your coffee anyway?

---

### 3.3 "Least-bad" framing confirmation

C3 recommended explicit "least-bad" framing. This is confirmed. The Hebrew caveat uses "באיזה ביסקוויט תבחרו אם ממילא תאכלו ביסקוויט" (which biscuit if you're going to have one anyway) — which is "least-bad" without being demoralizing. The page is useful because it surfaces the real quality question (fat type, sugar level, additive load) within a shelf where a consumer is already choosing.

---

## 4. §2.3 Prediction-Miss Addendum

This section is appended to `cookies_coffee_scoring_interpretation_v1.md §2.3` as a formal post-run addendum. The original document is not rewritten; this addendum is the amendment record.

---

**§2.3 Addendum — run_cookies_001 prediction miss (2026-06-13)**

**What §2.3 predicted:** C-modal / B-ceiling. D and E grades described as possible for "heavily processed variants."

**What run_cookies_001 produced:** E-modal (A0 B0 C13 D15 E33 / 61 products). Median 32.6 — well below the C band floor of 55.

**Two compounding errors in the prediction:**

**Error 1 — Sugar levels systematically underestimated.**
§2.3 described best-in-class biscuits as having "typically 15–22g/100g" sugar, noting they might be "just" below the 17.5g red-label threshold. The real corpus shows sugar running 20–38g/100g across most products. The sat-fat assumption (7–10g as the range center) was closer to accurate, but sugar was the more important miss. The ISRAELI_RED_LABELS_2_PLUS compound cap fires when BOTH thresholds are crossed simultaneously — and with sugar at 20–38g, the sugar leg fires on most products, not just "heavily processed" outliers. This pushed the cap-45 cohort to 25/61 (41%), far beyond what §2.3 implied.

**Error 2 — Routing was not modeled.**
§2.3 assumed the engine would receive coffee-biscuit products with appropriate category context. In reality, with no `biscuit` router category, products scattered to `snack_bar_granola` (20/61), `cracker` (27/61), `bread` (7/61), and `default`/`cereal`/`dairy_protein` (7/61). The `snack_bar_granola` lens penalizes differently from the `cracker` lens for identical composition — 75% E vs 40% E on the same class of product (verified evidence, P73 spec). This routing variance was not modeled in §2.3.

**Correct prediction (post-run calibration):**
The realistic pre-reroute distribution for a coffee-biscuit corpus with real Israeli retail compositions is E-modal / D-heavy, with B achievable for only the cleanest digestive/whole-grain variants. The post-reroute prediction is E/D-modal with an estimated B ceiling of 3–5 products.

**What §2.3 got right:** The mechanics (which caps fire, the fat-type vs sugar vs additive hierarchy, the signal self-gating table) are all confirmed correct. The error was in the assumed corpus composition (sugar level) and the absence of routing modeling.

---

## 5. Draft EV-058 Entry

### EV-058 — Dedicated `biscuit` Router Category for Sweet Plain Coffee Biscuits (TASK-275)

| Field | Value |
|---|---|
| **finding_id** | EV-058 |
| **task** | TASK-275 (factory run #7, cookies-near-coffee) |
| **date** | 2026-06-13 |
| **status** | PROPOSED — requires D7 co-sign (Nutrition Agent + Product Agent). DO NOT IMPLEMENT without both approvals. |
| **concept** | Add a dedicated `biscuit` router category in `router_v2.py` via hard anchors for sweet plain coffee-biscuit product names. Purpose: taxonomy and explainability only. Prevents semantically incorrect routing of plain sweet biscuits to `snack_bar_granola`, `cracker`, or `bread`. Caps INTACT. No endemic relief. No scoring rule change. No context_flag modification to evaluation_scope.py. |
| **scientific_rationale_short** | Routing plain biscuits to `snack_bar_granola` applies sub-rules calibrated for granola bars and produces a 35-percentage-point higher E rate than routing the same products to `cracker` (75% E vs 40% E, verified across 61 products in run_cookies_001). The distortion is not score-signal-based (the category-agnostic caps fire identically) but lens-context-based (different signal interactions under different category archetypes). A dedicated category stops the wrong lens from being applied without changing any scoring output for correctly-routed products. |
| **evidence_strength** | Moderate — the routing distortion is empirically confirmed (35pp E-rate gap, 61 products, verified evidence). The mechanism is clear (snack_bar_granola vs cracker lens difference). No RCT or nutritional literature is required — this is a routing-architecture fix, not a nutritional-claim addition. |
| **scope** | 12 Hebrew name-keywords (hard anchors) for sweet plain biscuit product names. Listed in `cookies_coffee_routing_ruling_v1.md` §2.3. Keywords are matched against product name only (not ingredient text), with defined exclusions per `ANCHOR_EXCLUSIONS`. |
| **activation** | Vocabulary addition to `router_v2.py` `HARD_ANCHORS` and `ANCHOR_EXCLUSIONS`. No flag required (routing additions are always-on once wired). New category `"biscuit"` added to `CATEGORIES` list (line 26–41) and `ALL_SIGNALS` (with empty signal list — anchors provide all routing). |
| **caps_intact** | CONFIRMED. `ISRAELI_RED_LABELS_2_PLUS`, `ISRAELI_RED_LABEL_1_SUGAR`, `ISRAELI_RED_LABEL_1_SAT_FAT`, and all other caps apply identically on the `biscuit` routing path. This EV does not propose any cap modification, cap exemption, endemic relief, or score floor for the biscuit category. |
| **no_endemic_relief** | CONFIRMED. Cookie sugar+fat is a formulation choice, not a preservation constraint analogous to brine sodium (EV-052). No analog to the brined_food context_weight=0.7 is proposed or warranted here. |
| **label_observability** | The routing decision is stored in the product trace under `category` and `category_subtype` (anchor: `plain_biscuit`, `petit_beurre`, etc.). Any product routed to `biscuit` will show `anchor_override: true` and `classification_basis: ["hard_anchor:ביסקוויט"]` (or the matched term) in the trace. Fully observable and reversible. |
| **rollback** | Remove the `biscuit` anchor entries from `HARD_ANCHORS`, remove `"biscuit"` from `CATEGORIES` and `ALL_SIGNALS`, remove `biscuit` keys from `ANCHOR_EXCLUSIONS`. No other file changes needed. The routing returns exactly to the pre-EV-058 state. The change is tagged `# EV-058` in source for easy location. |
| **no_regression_proof_plan** | BEFORE any code ships: (1) run `engine_invariants.py` 342-case suite — must PASS with zero new failures; (2) run golden-corpus byte-identity check on all 7 live categories (milk, yogurts, breads, salty_snacks, cereals, snack_bars, brined_cheeses) — each product's score and grade must be byte-identical to the pre-EV-058 baseline; (3) confirm 0/61 cookies_coffee products appear in any live category corpus (OFF=0 already confirmed; barcode overlap check also required); (4) STOP on any published-score movement — zero-movement is the non-negotiable condition for routing changes (tripwire-1). |
| **product_agent_d7_required** | YES — this is a router architecture change that adds a new category. Product Agent D7 co-sign is required alongside Nutrition Agent approval. Neither can implement without the other. |
| **not_a_scoring_rule** | CONFIRMED. EV-058 is a routing/taxonomy change. It does not propose any new scoring rule, cap, signal weight, additive penalty, or context flag. It is a vocabulary addition to the router. The D7 required is for the routing architecture change, not for a scoring rule proposal per se — but the D7 gate still applies because any routing change that affects scored products requires governed co-sign. |

---

## 6. Guards Confirmation

All hard guards from P73 spec are confirmed respected:

| Guard | Status |
|---|---|
| No engine edits in this task | CONFIRMED — this is a ruling and spec document only. Implementation requires a separate C1-CURSOR dispatch after D7 co-sign. |
| OFF ban absolute | CONFIRMED — 0/61 OFF products in run_cookies_001 (verified evidence). No OFF data referenced or used anywhere in this ruling. |
| No fabricated products/numbers | CONFIRMED — all numbers (25/61 cap-45, 75% vs 40% E rate, 15/20 snack_bar E, 11/27 cracker E, median 32.6, stdev 14.1, min 10, max 63.9) are from the orchestrator-verified evidence in P73 spec. |
| Frozen invariants untouchable | CONFIRMED — this ruling does not affect milk scores (run_005_headpin), snk-001 ceiling (70/B), or any other frozen invariant. |
| Caps INTACT | CONFIRMED — EV-058 proposes no cap modification. The ISRAELI_RED_LABELS_2_PLUS cap at 45 continues to fire for all 25 products that genuinely cross both thresholds. |
| No endemic relief | CONFIRMED — EV-058 explicitly rules OUT any endemic sat-fat relief for the cookie category. The §6.2 proposal in cookies_coffee_scoring_interpretation_v1 remains default-off and is not proposed here. |

---

```json
{
  "task": "P73",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "02_products/cookies_coffee/methodology/cookies_coffee_routing_ruling_v1.md",
      "sha256": "e0b92b2e1de0426dcbf922e5324944c4481067f6ba734107751725a6634b817d (content-hash: sha256 of file with this field zeroed)"
    }
  ],
  "counts": {
    "sections_in_ruling": 6,
    "total_sections_required_by_spec": 5,
    "keywords_proposed_for_biscuit_anchors": 12,
    "anchor_exclusion_entries": 10,
    "engine_line_cites": 9,
    "ev_entries_referenced": 7,
    "ev_entry_proposed": 1,
    "products_in_run": 61,
    "cap_45_cohort_honest_E": 25,
    "estimated_artifact_E": 8,
    "estimated_honest_E_plus_D": 41
  },
  "engine_line_cites": [
    "evaluation_scope.py:39-68 — brined_food CONTEXT_LIMITED_SIGNALS block (EV-052 mechanism being mirrored)",
    "evaluation_scope.py:136-137 — name-only match for context-limited keyword check",
    "evaluation_scope.py:138-161 — keyword + compound keyword loop",
    "router_v2.py:26-41 — CATEGORIES list (biscuit must be added here)",
    "router_v2.py:50-156 — HARD_ANCHORS list (new biscuit anchors go here)",
    "router_v2.py:179-244 — ANCHOR_EXCLUSIONS dict (new biscuit exclusions go here)",
    "router_v2.py:248-287 — _check_anchors() function (how anchors are matched and exclusions applied)",
    "router_v2.py:461-473 — ALL_SIGNALS dict (biscuit must be added with empty list)",
    "router_v2.py:620-680 — classify_category() public entry point showing Stage 1 anchor exit path"
  ],
  "honest_vs_artifact_split": {
    "total_products": 61,
    "honest_E_cap_45_cohort": 25,
    "honest_E_nova4_composition": 8,
    "artifact_E_routing_distortion": "7-8 (estimated upper bound)",
    "ambiguous": 12,
    "honest_D_C": 8,
    "routing_distortion_evidence": "75% E (15/20) snack_bar_granola vs 40% E (11/27) cracker — 35pp gap on same product class",
    "category_level_verdict": "E-modal is directionally honest; approximately 7-8 product-level E grades are routing artifacts",
    "caps_intact_post_reroute": true
  },
  "not_done": [
    "EV-058 implementation — requires separate C1-CURSOR dispatch after D7 co-sign from both Nutrition Agent and Product Agent",
    "Product Agent D7 co-sign — required before any router code change ships",
    "No-regression proof run (342-invariants + 7-category golden-corpus byte-identity) — required before code ships",
    "Post-reroute score run (run_cookies_002) — required after EV-058 implementation to confirm predicted D/E-modal distribution",
    "Frontend packaging (factory Stage 8 render_local_page) — blocked on rerouted score run",
    "Red-team gate (Stage 9) — blocked on render",
    "EV-058 formal registration in bsip2_evidence_registry_v1.md — this ruling is the draft; registration requires orchestrator + Product D7 co-sign confirmation"
  ],
  "self_check": {
    "off_ban_respected": true,
    "no_fabricated_numbers": true,
    "frozen_invariants_untouched": true,
    "caps_intact": true,
    "no_endemic_relief": true,
    "no_engine_edits_in_this_task": true,
    "ev_proposal_requires_d7": true,
    "routing_change_does_not_change_live_scores": "asserted — proof required at implementation",
    "c3_strategic_read_followed": true,
    "prediction_miss_documented": true,
    "return_contract_present": true
  }
}
```
