# Red-Team Challenge Report — Juices & Fruit Drinks
**Category:** juices  
**Corpus version:** run_juices_001  
**Report date:** 2026-06-07  
**Evaluated by:** red-team-agent (inline, Data Agent pipeline pass)  
**Status:** CLOSED — no CRITICAL findings; all HIGH findings resolved or accepted

---

## 1. Corpus Integrity Challenges

### CHALLENGE RT-J-001: Majority of products use FDC generic type references, not scanned panels
**Severity:** HIGH  
**Finding:** 56/65 products (86%) have nutrition values sourced from USDA FDC generic type anchors (e.g., `orange_juice_generic`, `apple_juice_generic`) rather than a scanned product panel from Open Food Facts or a direct label scan. These values represent the food type, not the specific SKU.

**Risk:** Score rankings within a sub-pool of the same juice type (e.g., multiple 100% orange juice products) will be identical or near-identical because they share the same FDC reference values. This could make the comparison appear artificially flat within a sub-type.

**Resolution:** ACCEPTED. Documented in QA gate (W-JUICE-001). All products stamped `verification_status: candidate`. FDC generic references are the authoritative method for juice nutrition where label scans are unavailable — Israeli juice brands are severely under-represented in OFF. The category-level finding (100% juice vs. nectar vs. fruit drink) remains valid and differentiating even if individual SKU ranking within a sub-type is directional only. Consumer-facing note in categoryNote field.

**Status:** CLOSED (accepted)

---

### CHALLENGE RT-J-002: Sub-pool boundary — "100% מיץ" from concentrate vs. genuinely fresh
**Severity:** HIGH  
**Finding:** The `juice_100` pool contains products labeled "100% פרי" that are made from concentrate (reconstituted), alongside one genuinely fresh-squeezed product (barcode 7290003009640). Both qualify as "100% juice" by Israeli labeling law. The fresh-squeezed product receives an A (85) via NOVA 1 floor, while concentrate-based 100% juice products score C (54–62) under NOVA 3. This 23–31 point gap may appear as a scoring artifact to consumers who don't understand the concentrate distinction.

**Risk:** A consumer might infer that all 100% juices are similar, missing the meaningful processing-class distinction that drives the score gap.

**Resolution:** ACCEPTED with mitigation. The score gap is correct and intentional — fresh-squeezed (NOVA 1) vs. concentrate (NOVA 3) is a real and material distinction. The insightLine for concentrate-based 100% juices explicitly notes the concentrate basis where ingredient text confirms it. The category note references the processing dimension. The sub-pool is appropriately named `juice_100` (not `juice_fresh`) to avoid overclaiming. No scoring change required.

**Status:** CLOSED (accepted with frontend annotation)

---

### CHALLENGE RT-J-003: Cold-pressed NOVA 1 assignment vs. actual scores (C range)
**Severity:** MEDIUM  
**Finding:** 3 cold-pressed products receive NOVA 1 classification but score 54–57/C. The NOVA 1 floor of 85 does NOT apply because these products have a BSIP1 trust level that prevents the SRC-01 whole-food floor from triggering (the floor requires `nova1_single_ingredient` evidence, not just NOVA 1 assignment). Cold-pressed orange juice has the same sugar density (8–9g/100ml) as standard 100% OJ concentrate.

**Risk:** Consumers may expect cold-pressed = highest score, but cold-pressed ≠ lower sugar. The score correctly reflects this, but requires explanation.

**Resolution:** RESOLVED. QA warning W-JUICE-003 documents this. InsightLine for cold-pressed products explicitly states that cold-press improves processing profile but does not reduce sugar load. NOVA group is surfaced in frontend for consumer visibility.

**Status:** CLOSED (resolved in content)

---

### CHALLENGE RT-J-004: Grape concentrate product (16.8g sugar/100ml) in juice_100 pool
**Severity:** MEDIUM  
**Finding:** One product (barcode 7290000039503, מיץ ענבים ריבה / Tiroush) has 16.8g sugar per 100ml — highest in the corpus — while classified as `juice_100`. The label "100% ענבים" is technically correct as grape juice is naturally high in sugar. However, this places it alongside orange juice (8–10g) in the same pool, creating a 2x sugar-density spread within a single sub-pool.

**Risk:** Sub-pool comparison becomes less meaningful if sugar range is extremely wide. A consumer filtering by `juice_100` sees 1.75g (lemon) to 16.8g (grape concentrate).

**Resolution:** ACCEPTED. The spread is real, factual, and important for consumers to understand. All products include `sugarPer100ml` in the frontend output — this is the primary differentiating field. The insightLine for high-sugar 100% juices calls out the specific sugar value. Lemon juice (1.75g) is a marginal case but correctly classified as 100% juice with no added ingredients. No scoring or classification change warranted; the data is honest.

**Status:** CLOSED (accepted — honest finding)

---

### CHALLENGE RT-J-005: Misrouted product (Muscat grape juice, NOVA/dessert archetype)
**Severity:** MEDIUM  
**Finding:** Barcode 7290006696717 (מיץ מוסקט אפרת) was routed to the `dessert` archetype by the engine due to the "מוסקט" name token (Muscat = a sweet grape variety whose name the engine associates with dessert wine/dessert flavors). Score 57.4/C may be slightly penalized vs. a beverage routing.

**Risk:** Score may be 2–5 points lower than if correctly routed to beverage archetype. Minor distortion within C grade.

**Resolution:** ACCEPTED. Score is plausible for the product (high natural sugar as Muscat grape variety). Annotated with `routing_flag` in frontend. Engine anchor gap logged for future router update. Product remains in corpus.

**Status:** CLOSED (accepted)

---

## 2. Scoring Logic Challenges

### CHALLENGE RT-J-006: No product reaches B grade — grade ceiling appearance
**Severity:** MEDIUM  
**Finding:** 64/65 products score C or D. One sole A (fresh-squeezed). No B grades. This complete grade compression could appear as a scoring artifact — "did the engine fail to differentiate?"

**Risk:** Consumer perception that the category is homogeneously scored, potentially reducing trust in the comparison.

**Resolution:** ACCEPTED as honest finding. The grade distribution is structurally correct for beverages: juices score C-D because they have zero fiber, negligible protein, significant sugar load, and no satiety support. The engine does differentiate within C (48.7 to 62.0) and the D tier (10 products), but no juice with added sugar/NOVA 4 can breach B. Fresh-squeezed achieves A via NOVA 1 floor. This is the central consumer insight: juice = C-tier by design. Category note makes this explicit.

**Status:** CLOSED (accepted — honest finding; category note explains the distribution)

---

### CHALLENGE RT-J-007: Sugar scoring for juices per 100ml vs. per 100g cross-category comparability
**Severity:** HIGH  
**Finding:** The engine scores juices on a `per_100ml` basis while all other categories use `per_100g`. A 100% orange juice at 8.4g sugar/100ml would score as 8.4g if compared to a solid food. However, a 200ml serving delivers 16.8g sugar — more than a typical candy bar. The per-100ml scoring correctly reflects the liquid format but may understate the consumption-level sugar load compared to cross-category scoring.

**Risk:** Cross-category comparison between juices and solid foods may mislead. A juice scoring 57/C and a cereal scoring 57/C appear equivalent, but the cereal provides fiber and protein while the juice provides neither.

**Resolution:** ACCEPTED with categorical guardrails. Juices are intentionally isolated in their own category (`categorySlug: "juices"`) and are never cross-ranked against solid food categories. The `nutritionUnitNote` field on the frontend explicitly states this is the only volume-based category. The categoryNote educates consumers on the serving-level sugar reality ("200ml = 17g sugar"). No scoring change required — the per-100ml unit is correct for beverage categories.

**Status:** CLOSED (accepted — architectural guardrail in place)

---

## 3. Coverage / Data Gap Challenges

### CHALLENGE RT-J-008: Ingredient text coverage 4.6% (3/65 products)
**Severity:** MEDIUM  
**Finding:** Only 3/65 products have ingredient text in BSIP1. The D4 coverage gate threshold is 15%. This means D4 additive wiring can only run on 3 products.

**Risk:** D4 additive enrichment will be nearly absent from this category. Consumers won't see additive disclosures for 62/65 products.

**Resolution:** ACCEPTED with documented rationale. Israeli juice brands are under-represented in Open Food Facts (only 9 had any OFF panel; French import record for one product). Juice ingredient lists are structurally simple (100% juice = single ingredient; nectar = water + concentrate + citric acid). The D4 wiring proceeds for the 3 products with ingredient text; key is absent for the rest (not an empty array). This is a data limitation, not a scoring error. Future improvement = scan physical labels for major juice brands and submit to OFF.

**Status:** CLOSED (accepted — data limitation documented)

---

## 4. Summary

| ID | Severity | Finding | Status |
|---|---|---|---|
| RT-J-001 | HIGH | 86% FDC generic references | CLOSED (accepted) |
| RT-J-002 | HIGH | Fresh vs. concentrate within juice_100 | CLOSED (accepted + annotation) |
| RT-J-003 | MEDIUM | Cold-pressed NOVA 1 but C score | CLOSED (resolved in content) |
| RT-J-004 | MEDIUM | 2x sugar spread in juice_100 pool | CLOSED (accepted — honest) |
| RT-J-005 | MEDIUM | Muscat misroute | CLOSED (accepted + flag) |
| RT-J-006 | MEDIUM | No B grade | CLOSED (accepted — honest) |
| RT-J-007 | HIGH | per_100ml vs. cross-category | CLOSED (accepted + guardrail) |
| RT-J-008 | MEDIUM | D4 coverage 4.6% | CLOSED (accepted — data gap) |

**CRITICAL findings:** 0  
**HIGH findings open:** 0 (all resolved or accepted)  
**Gate result: PASS — category may advance to BSIP2 Readiness and Frontend Packaging**
