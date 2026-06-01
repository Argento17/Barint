# Wave 2 Category Recommendation

**Task:** TASK-054  
**Owner:** Data Agent  
**Date:** 2026-05-31  
**Verdict: GO — Tahini (Candidate A)**

---

## Decision

**Recommended category: Tahini**  
**Verdict: GO — acquisition-ready**

Tahini is the strongest Wave 2 category on every axis that matters for delivery reliability: the boundary is pre-defined, the scraper works, the BSIP2 routing is provisioned, the corpus is sufficient, and Israeli consumer value is high. This is the lowest-risk path to a frozen second category.

Nut Butters and Protein Yogurts both carry blockers that Tahini does not. The evaluation is below.

---

## Candidate Evaluation Matrix

Scores are 1–5. Higher is better.

| Criterion | Tahini | Nut Butters | Protein Yogurts |
|-----------|:------:|:-----------:|:---------------:|
| Acquisition complexity | **5** | 3 | 2 |
| Shelf mapping complexity | **5** | 3 | 2 |
| Corpus size (vs. 30-product gate) | **4** | 2 | 4 |
| BSIP0 compatibility | **5** | 4 | 3 |
| BSIP1 compatibility | **4** | 4 | 3 |
| BSIP2 transferability | **5** | 5 | 3 |
| Consumer value | **5** | 3 | 4 |
| Factory stress-testing value | **5** | 3 | 4 |
| **Total** | **38 / 40** | **27 / 40** | **25 / 40** |

---

## Candidate A — Tahini

### Verdict: GO

**What it is:** Raw sesame paste products (ground sesame, hulled or whole), ready-to-eat tahini dips (tahini + lemon + garlic + water), and tahini with natural sweeteners (date/honey). All sold as ambient retail products under the "Tahini" category at Israeli supermarkets.

**Why it wins:**

**1. Pre-defined boundary.** The hummus corpus_filter (TASK-026) explicitly deferred ready-to-eat tahini dips to this category. The deferred boundary is already documented and resolved. No new scope decision is required from the Head of Product — the scope has been decided.

**2. BSIP2 routing is provisioned.** The router has a hard anchor `"טחינה"` → `whole_food_fat` at confidence 0.93. The `whole_food_fat` calorie density table is correctly calibrated for this category (350–900 kcal range). The NOVA 1 single-ingredient floor (85) applies to pure sesame paste — this is architecturally correct and prevents data gaps from suppressing scores on simple, high-quality products.

**3. Fat_quality is the primary differentiator.** The existing `fat_quality` dimension scores pure sesame fat (high PUFA/MUFA, ~13–16% saturated fraction) significantly higher than palm-oil-stabilized preparations. This differentiation is already in the engine and has not been validated on a real corpus. Tahini provides that validation test.

**4. Acquisition is straightforward.** Tahini has a dedicated shelf section at Shufersal and Yohananof. The product boundary is obvious — a jar of tahini is a jar of tahini. Contamination (halva, chocolate spreads) is clearly identifiable and easily filtered.

**5. Corpus is sufficient.** Estimate: 35–55 products at Shufersal; 15–20 additional products from Yohananof including local/organic brands. Combined: 45–70 products. Comfortably above the 30-product gate minimum.

**6. Israeli consumer value is highest of the three.** Tahini is a daily ingredient in Israeli cooking. It is purchased weekly by most households. The gap between premium artisanal tahini and industrial tahini is large and not well understood by consumers. Bari's score can directly address a question consumers face at the shelf.

**7. Data quality is controllable.** The Shufersal fat-row scraping defect (TASK-039) must be audited at the BSIP0 gate — tahini's high fat content (~55g/100g) means the caloric gap analysis will reliably detect any corruption. Unlike hummus (where 8g sat fat could pass undetected), tahini's gap would be 45+ grams.

**Known risks:**

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Shufersal fat-row defect applies here too | Critical | Mandatory caloric gap audit at BSIP0 gate (established protocol from TASK-039) |
| Tahini corpus may be smaller than expected (shelf concentration varies) | Medium | Include Yohananof as second retailer; use search queries for organic brands |
| Ready-to-eat tahini dips require explicit scope decision vs. raw tahini | Low | Boundary pre-defined in TASK-046 wave2_planning.md; no new decision needed |
| "Tahini with honey/date" is a sweet variant that BSIP2 will penalize via glycemic_quality | Low | Include and flag; the penalty is correct — sweetened tahini is structurally different |

---

## Candidate B — Nut Butters

### Verdict: NO-GO as standalone Wave 2

**What it is:** Peanut butter, almond butter, cashew butter, walnut butter, pistachio butter, and mixed nut butters sold in retail packaging.

**Why it loses:**

**1. Corpus size fails the gate as a standalone category.** The Israeli market for nut butters other than peanut butter is thin. Almond butter: 6–12 products. Cashew butter: 3–7 products. Mixed nut butter: 3–5 products. Peanut butter: 10–18 products. Total: 22–42 products. At the low end, this fails the 30-product gate. At the expected mid-point of ~30, it passes by a narrow margin with no safety buffer.

**2. Contamination risk is the highest of the three candidates.** Nut butters are shelved alongside Nutella, chocolate hazelnut spreads, halva spreads, and nut-based energy bars. The contamination rate on the "sweet spreads" shelf code is 70–80%. Nut butter products are scattered across multiple codes. Shelf mapping requires more manual probe work than any other candidate.

**3. Consumer value is limited for Israel specifically.** Nut butter is a growing but niche category in Israel. The tahini + hummus spread culture is much more central to the daily shopping basket. A "peanut butter comparison" page has lower expected traffic and engagement than a "tahini comparison" page for the Israeli audience.

**4. Factory stress-testing value is duplicative.** Nut butters use the same `whole_food_fat` archetype as tahini. The stress-test value of running both in the same Wave is low — the same failure modes (fat_quality, NOVA routing, calorie density table) would be tested twice.

**When nut butters should be done:** As Wave 3 or as an extension of the Tahini page. The two categories share the same archetype and the same shelf neighborhood. Once Tahini is frozen, adding a "Nut Butters" tab to the same comparison page is a natural expansion. Running them as a combined acquisition (Tahini + Nut Butters, as originally planned in TASK-046) is the correct long-term path.

---

## Candidate C — Protein Yogurts

### Verdict: NO-GO as Wave 2

**What it is:** Yogurt and skyr products with elevated protein content, marketed with protein claims (>10g protein per 100g or similar), including Greek-style yogurt, skyr, protein-fortified yogurt, and kefir-adjacent fermented products.

**Why it loses:**

**1. The "protein yogurt" boundary does not correspond to a retail shelf code.** Israeli supermarkets do not have a dedicated "protein yogurt" section. These products are distributed across: regular yogurt shelves, health food sections, sports nutrition areas, and dairy alternatives refrigerators. Discovery is necessarily keyword-driven (searching for protein claims) with no traversal anchor. Expected contamination from regular yogurt is high and hard to filter automatically.

**2. The scope boundary requires a protein content threshold that has not been decided.** Is a Greek yogurt with 8g protein a "protein yogurt"? What about full-fat plain yogurt with 5g? Flavored Activia with 4.5g? The definition of "Protein Yogurt" is a marketing category, not a food architecture category. Every product decision during candidate review will require a judgment call that a clear shelf code or ingredient rule would normally make automatic.

**3. The yogurt BSIP2 system has only been validated on synthetic data.** The `batch_run_yogurt_001.py` runner processed 45 synthetic products with sequential barcodes (7290200000001–7290200000045). These are generated test data, not real retailer scrapes. Running a real yogurt corpus against the BSIP2 yogurt archetype for the first time in Wave 2 introduces unknown calibration risks — the exact risks Wave 2 is supposed to eliminate before Wave 3+.

**4. Acquisition complexity is highest.** The dairy refrigerated section at Shufersal mixes: plain yogurt, flavored yogurt, protein yogurt, kefir, drinking yogurt, soy yogurt, and children's dairy products. These all share shelf codes. A keyword-based filter is the only viable acquisition strategy, and it requires post-scrape classification of each product against the protein threshold. This is Stage 4 + Stage 6 complexity rolled into one.

**5. Consumer value is high — but the timing is wrong.** The protein yogurt market is large and high-interest. Bari should eventually cover it. But covering it correctly requires: a locked protein threshold definition, a real corpus validation of the yogurt BSIP2 archetype, and a router update to handle skyr and Greek yogurt correctly alongside "יוגורט". These are three prerequisites that are not yet done. Rushing to Wave 2 creates a category that may need significant rework post-launch.

**When protein yogurts should be done:** Wave 3 or Wave 4, after: (a) the protein threshold is defined by CNO, (b) a small probe run validates the yogurt BSIP2 archetype against a real corpus, (c) the scope boundary resolves the Greek yogurt / skyr / kefir overlap.

---

## Comparative Risk Summary

| Risk | Tahini | Nut Butters | Protein Yogurts |
|------|:------:|:-----------:|:---------------:|
| Corpus below 30-product gate | Low | Medium-High | Low |
| Scope boundary unclear | **None** (pre-defined) | Low | **High** |
| BSIP2 archetype unvalidated | No | No | **Yes** |
| Dedicated shelf code exists | Yes | Partial | **No** |
| Fat data quality risk | Known, manageable | Known, manageable | N/A |
| Scraper already proven | Yes | Yes | Partial |
| Real corpus validation done | Hummus (adjacent) | None | **None** |

---

## Recommendation: GO — Tahini

**Scope:** Tahini (raw, ready-to-eat dip variants, sweetened tahini). Excludes halva, chocolate tahini, cooking tahini sauces. Boundary per `category_boundary_definition.md` and `inclusion_exclusion_rules.md` in this directory.

**Action to proceed:**

1. Lock `corpus_filter.md` (this document set serves as the input)
2. Run BSIP0 discovery on Shufersal + Yohananof per `shelf_mapping_v1.md`
3. Apply mandatory fat anomaly audit at BSIP0 gate before proceeding to BSIP1
4. Target run ID: `run_tahini_001`

**Nut Butters:** Deferred to Wave 3, to be run as an extension of the Tahini page (combined acquisition, single BSIP2 run).

**Protein Yogurts:** Deferred pending protein threshold definition, real corpus validation of yogurt BSIP2, and scope boundary decisions.

---

*Category Recommendation — TASK-054 — Data Agent — 2026-05-31*  
*Verdict: GO on Tahini. Acquisition-ready pending corpus_filter.md lock.*
