**Task:** TASK-179A

# Glass Box Engine Evolution — Enrichment Frameworks Scoping Dossier (v1)

**Status:** SUGGESTION / SCOPING ONLY. No engine code, no score movement, nothing adopted. Adoption is a separate Nutrition + Product gated decision (D6/D7). This dossier maps the authoritative frameworks and data sources so the owner can decide what to build.

**Author:** Research Agent · **Date:** 2026-06-03 · **Repo path:** `C:\Bari\research\glass_box\engine_enrichment_frameworks_scoping_v1.md`

---

## Framing: the clinician's four points → six dimensions

The stress-test surfaced four structural truths that this scoping respects throughout:

1. **Partial visibility is a structural market limit.** Labels disclose only first-level ingredients — no proportions, "protein blend" hides composition, compound ingredients collapse sub-ingredients. Any quality computation (DIAAS, per-additive load) is therefore **confidence-gated by disclosure**, never a precise per-product number.
2. **Engineered ≠ bad.** Engineering is a neutral fact. The engine scores *what the engineering does to the nutritional/evidence picture*, not the presence of a process.
3. **Additives need an EVIDENCE model, not a name-fear model.** "Unfamiliar name = harm" is forbidden. Each additive carries an authoritative evidence verdict; absent one, the verdict is "uncertain/disclosure-gap" — never a guess.
4. **The engine must not pretend certainty.** Every signal carries a confidence note; undisclosed quality feeds the transparency (D5) and confidence (D6) dimensions.

The general pattern the clinician named (PDCAAS/DIAAS was one instance): **every nutrient gets a three-layer treatment — quantity → quality/form → evidence — anchored to an authoritative body.** The quality layer is frequently undisclosed, so it is usually a *signal*, not a measured value.

---

## SECTION 1 — Protein-Source Quality Table

**Anchor:** FAO 2013 Expert Consultation (*Dietary protein quality evaluation in human nutrition*, FAO Food and Nutrition Paper 92) established **DIAAS** (Digestible Indispensable Amino Acid Score) as the recommended successor to **PDCAAS**. DIAAS is not truncated at 1.0, so it discriminates among high-quality proteins where PDCAAS saturates. Values below are reference values for the **isolated/representative source**, drawn from the FAO 2013 report and the peer-reviewed DIAAS literature that built on it (e.g. Rutherfurd et al. 2015, *J Nutr* 145:372; Phillips 2017 review). Where a published DIAAS is unavailable, the PDCAAS is given and flagged.

**Confidence-gating caveat (load-bearing — read first):** You almost never can compute a *per-product* DIAAS. A "protein blend (whey, soy, pea)" hides the proportions, so the blend's true DIAAS is indeterminate. Compound and added-protein ingredients compound the problem. Therefore this table must drive a **confidence-gated SIGNAL** — "is the disclosed protein from a high-quality source?" — not a precise per-product DIAAS. When proportions are hidden, the engine reports the *source-quality tier of what is disclosed* and lowers confidence (feeds D5/D6). DIAAS values shift with processing, heat damage, and anti-nutritional factors (esp. plant sources), which labels never disclose — another reason this is a signal, not a measurement.

| # | Source | DIAAS (FAO 2013 basis) | PDCAAS (where DIAAS n/a) | Quality tier | Citation | Note |
|---|---|---|---|---|---|---|
| 1 | Whey protein isolate | ~1.09–1.25 | (PDCAAS 1.00, truncated) | High | FAO 2013; Rutherfurd 2015 | Reference high-quality; leucine-rich |
| 2 | Whey protein concentrate | ~0.97–1.07 | 1.00 | High | Rutherfurd 2015 | Slightly below isolate |
| 3 | Casein / micellar casein | ~1.10–1.18 | 1.00 | High | FAO 2013; Rutherfurd 2015 | Slow-digesting; complete |
| 4 | Cow's milk (whole) | ~1.14 | 1.00 | High | FAO 2013 | Matrix reference for dairy |
| 5 | Whole egg | ~1.13 (cooked) | 1.00 | High | FAO 2013; Rutherfurd 2015 | Historic reference protein |
| 6 | Egg white | ~1.00–1.13 | 1.00 | High | Rutherfurd 2015 | |
| 7 | Soy protein isolate | ~0.84–0.90 | ~0.98 | High–moderate | FAO 2013; Mathai 2017 (*Br J Nutr*) | Best-quality common plant protein |
| 8 | Soy (whole / tofu) | ~0.90 (concentrate) | ~0.91 | Moderate | FAO 2013 | Anti-nutrients lower vs isolate |
| 9 | Pea protein isolate | ~0.62–0.82 | ~0.69–0.89 | Moderate | Nosworthy 2017 (*Food Sci Nutr*); Phillips 2017 | Methionine-limited |
| 10 | Rice protein (isolate) | ~0.37–0.59 | ~0.42–0.62 | Low–moderate | Nosworthy 2017 | Lysine-limited; often blended w/ pea |
| 11 | Pea+rice blend | indeterminate (proportion-dependent) | — | Moderate (designed-complement) | Inferred; no per-product DIAAS | **Classic disclosure-gap; complementary by design but unquantifiable** |
| 12 | Wheat gluten / seitan | ~0.25–0.45 | ~0.25 | Low | FAO 2013; Phillips 2017 | Severely lysine-limited |
| 13 | Wheat (whole, as in bread) | ~0.40–0.51 | ~0.42 | Low | FAO 2013 | |
| 14 | Oat protein | ~0.43–0.67 (limited data) | ~0.57 | Low–moderate | Limited literature — flag | Lysine-limited |
| 15 | Hemp protein | ~0.48–0.61 (sparse) | ~0.46–0.66 | Low–moderate | Sparse/contested data — flag | Leucine + lysine modest |
| 16 | Almond | ~0.40 (sparse) | ~0.39–0.49 | Low | House 2010; sparse | Lysine-limited |
| 17 | Chickpea / legume (cooked) | ~0.67–0.83 | ~0.71 | Moderate | FAO 2013; Nosworthy 2017 | Best of the pulses; SAA-limited |
| 18 | Lentil | ~0.63 | ~0.58 | Moderate | Nosworthy 2017 | |
| 19 | Beef (cooked) | ~1.11–1.16 | 0.92+ | High | FAO 2013; Phillips 2017 | |
| 20 | Chicken (cooked) | ~1.08 | ~0.95 | High | FAO 2013 | |
| 21 | Fish (varies by species) | ~1.00–1.10 | ~0.96 | High | FAO 2013 | |
| 22 | Collagen / hydrolyzed collagen | **~0** effective | ~0.0–0.08 | **Low (incomplete)** | FAO basis; Paul 2019 review | **No tryptophan; not a complete protein — common label-marketing gap** |
| 23 | Gelatin | ~0.0–0.08 | ~0.08 | Low | As collagen | Same limitation |
| 24 | Potato protein (isolate) | ~0.85–1.00 (sparse) | ~0.90 | Moderate–high | Sparse literature — flag | Emerging; data thin |
| 25 | "Protein blend" (generic, undisclosed proportions) | **indeterminate** | — | **Confidence-gated** | n/a | **Signal only: report tier of best disclosed source, lower confidence** |

**Israeli vs EU/US divergence:** DIAAS/PDCAAS are FAO/WHO-international, not jurisdiction-specific — no divergence on the *measure*. Divergence appears only in *claims* (an EU "high protein" claim under Reg 1924/2006 requires ≥20% of energy from protein; it does not require any quality threshold — a credibility gap Bari can fill by surfacing source quality).

---

## SECTION 2 — Additive Prototype Set

**Method:** Frequency was **derived from real BSIP0 raw ingredient panels** (not synthetic), across maadanim, yogurt, cheese-spreads, breakfast-cereals, bread (retail_003), and snack-bars (`C:\Bari\02_products\*\...bsip0_raw*.json` and snack-bars `observations_bsip0`). E-numbers were extracted by regex and named additives by Hebrew term frequency. This is a real, if approximate, shelf-frequency signal across six live categories — treat counts as relative prevalence, not absolute census (panels vary in completeness; this is itself a disclosure-gap data point).

**Empirical top hits (E-number, raw count):** E481 (64), E300 (59), E471 (55), E282 (54), E202 (45), E330 (31), E472e (26), E142 (20), E407 (13), E220 (12), E410 (11), E466 (11), E415 (11), E322 (11), E500i (9), E331 (8), E450i (8), E412 (8), E920 (8). **Named (Hebrew) hits:** lecithin (103), citric acid (66), vanillin (63), ascorbic acid (54), pectin (52), sorbate (44), guar (38), sucralose (35), maltodextrin (33), maltitol (28), glycerol (25), carrageenan (21), sorbitol (12), stevia (5).

**Evidence-tier taxonomy (fixed):** `confirmed-negative · likely-neutral · functional · dose-dependent · scientifically-contested · disclosure-gap`. Evidence-first rule applied: where no defensible authoritative source exists, tier = **disclosure-gap/uncertain**, never a guess.

| # | E / name | Function class | Evidence tier | Best authoritative source | ADI (if relevant) | One-line consumer draft (Hebrew-ready) |
|---|---|---|---|---|---|---|
| 1 | E481 sodium stearoyl lactylate | Emulsifier (dough) | functional | EFSA re-eval 2013 (EFSA J 2013;11:3408) | 20 mg/kg bw (group) | "חומר תפיחה/תחליב — תפקיד טכנולוגי, ללא חשש בריאותי ידוע במינון מותר" |
| 2 | E300 ascorbic acid (vit C) | Antioxidant | likely-neutral | EFSA 2015; JECFA "ADI not specified" | not specified | "ויטמין C כנוגד-חמצון — מרכיב מוכר ובטוח" |
| 3 | E471 mono- & diglycerides | Emulsifier | likely-neutral / under-review | EFSA re-eval 2017 (EFSA J 2017;15:5045) | not specified | "תחליב נפוץ משומנים — נחשב בטוח; EFSA ממשיכה לעקוב" |
| 4 | E282 calcium propionate | Preservative (mold) | likely-neutral | EFSA re-eval 2014; JECFA | not specified | "מעכב עובש בלחם — בטוח במינון מותר" |
| 5 | E202 potassium sorbate | Preservative | likely-neutral | EFSA re-eval 2015 (EFSA J 2015;13:4144) | 11 mg/kg bw (group, sorbates) | "משמר נגד עובש/שמרים — בטוח במינון מותר" |
| 6 | E330 citric acid | Acidity regulator | likely-neutral | JECFA "ADI not limited"; EFSA | not limited | "חומצת לימון לוויסות חומציות — מרכיב מוכר ובטוח" |
| 7 | E472e DATEM | Emulsifier (dough) | functional | EFSA re-eval 2019 | group ADI | "תחליב לבצק — תפקיד טכנולוגי בלחם" |
| 8 | E142 / E144 green/colors (E142 Green S; E144 patent blue – note: E144 is actually phloxine? verify per panel) | Colorant | dose-dependent | EFSA re-evals (synthetic colours, 2010 onward) | varies per colour | "צבע מאכל — לרוב בטוח במינון; חלק נבחנו מחדש ב-EFSA" *(verify exact colour per E-code)* |
| 9 | E407 carrageenan | Stabilizer/thickener | scientifically-contested | EFSA re-eval 2018 (EFSA J 2018;16:5238); JECFA 2014 | not specified (EFSA: data gaps) | "מייצב מאצות — בטוח לפי הרגולציה, אך קיים דיון מדעי על המעי" |
| 10 | E220 sulphur dioxide / sulphites | Preservative | dose-dependent | EFSA re-eval 2016 (sulfites) | 0.7 mg/kg bw | "משמר — בטוח במינון; עלול לגרום רגישות אצל אסתמטים" |
| 11 | E410 locust bean gum | Thickener | likely-neutral | EFSA re-eval 2017 | not specified | "מסמיך טבעי מחרוב — בטוח" |
| 12 | E466 carboxymethylcellulose (CMC) | Thickener/stabilizer | scientifically-contested | EFSA re-eval; Chassaing 2022 (*Gastroenterology*) RCT signal | not specified | "מסמיך — בטוח רגולטורית; מחקר חדש בוחן השפעה על המיקרוביום" |
| 13 | E415 xanthan gum | Thickener | likely-neutral | EFSA re-eval 2017 | not specified | "מסמיך נפוץ — בטוח" |
| 14 | E322 lecithin | Emulsifier | likely-neutral | EFSA re-eval 2017 | not specified | "תחליב (לרוב מסויה) — מרכיב מוכר ובטוח" |
| 15 | E500i sodium carbonate | Acidity reg / raising | likely-neutral | EFSA; JECFA not limited | not specified | "סודה לאפייה/ויסות — בטוח" |
| 16 | E331 sodium citrate | Acidity reg / emulsifying salt | likely-neutral | EFSA; JECFA | not specified | "מלח לימון לוויסות — בטוח" |
| 17 | E450 / E450i diphosphates | Acidity reg / raising / emulsifying salt | dose-dependent | EFSA re-eval 2019 (phosphates) — **total phosphorus exposure flagged** | 40 mg/kg bw P (group, phosphates) | "מלח זרחני — בטוח ביחידה; EFSA סימנה חשיפה כוללת לזרחן כגבול" |
| 18 | E412 guar gum | Thickener | likely-neutral | EFSA re-eval 2017 | not specified | "מסמיך טבעי — בטוח" |
| 19 | E920 L-cysteine | Flour treatment | functional | EFSA; JECFA | — | "משפר בצק — תפקיד טכנולוגי" |
| 20 | Sucralose (E955) | Sweetener (NNS) | dose-dependent / contested | EFSA 2004; WHO 2023 NNS guidance (conditional, against weight control) | 15 mg/kg bw | "ממתיק ללא קלוריות — בטוח רגולטורית; WHO ממליצה לא להסתמך עליו להרזיה" |
| 21 | Aspartame (E951) | Sweetener (NNS) | scientifically-contested | EFSA 2013 (safe); IARC 2023 "possibly carcinogenic 2B"; JECFA 2023 retained ADI | 40 mg/kg bw | "ממתיק — EFSA קובעת בטוח במינון; IARC סיווג 2B שנוי במחלוקת" |
| 22 | Acesulfame-K (E950) | Sweetener (NNS) | dose-dependent | EFSA re-eval 2025-track; WHO 2023 | 9 mg/kg bw | "ממתיק ללא קלוריות — בטוח במינון מותר" |
| 23 | Maltitol / sorbitol (E965/E420) | Polyol sweetener | likely-neutral (GI dose-effect) | EFSA; laxative-threshold labelling | not specified | "ממתיק פוליאול — בטוח; כמות גבוהה עלולה לשלשל" |
| 24 | Maltodextrin | Bulking / carrier | likely-neutral (high-GI flag) | FDA GRAS; no ADI | — | "פחמימה-נשא; בטוח אך בעל אינדקס גליקמי גבוה" |
| 25 | Stevia glycosides (E960) | Sweetener (NNS, plant) | likely-neutral | EFSA 2010; JECFA | 4 mg/kg bw (steviol) | "ממתיק צמחי — בטוח במינון מותר" |

**Caveats:**
- E142/E144 colour identities should be re-verified per panel before any consumer text ships (E-code → colour mapping must be exact; one example carries a verification flag above).
- "disclosure-gap" tier triggers automatically whenever a panel says "צבעי מאכל"/"מייצב"/"מתחלב" **without** an E-code or name — common, and itself a transparency (D5) signal.
- **Israeli vs EU/US divergence:** Israel adopts the EU additive framework closely (EFSA/JECFA anchored) but maintains its own permitted-additive list via MoH; the US (FDA GRAS / Substances Added to Food) sometimes permits or names differently (e.g. colour-additive certification numbers FD&C vs E-numbers). Anchor consumer verdicts to **EFSA + JECFA** (closest to Israeli practice); cite FDA only as a cross-check.

---

## SECTION 3 — Nutrient-Interpretation Framework Registry

Each component gets: authoritative framework(s) + meaningful thresholds → the three-layer (quantity → quality/form → evidence) treatment → the **Israeli MoH red-label (סימון אדום)** anchor where it applies → a confidence note. EU nutrition-claim thresholds (Reg 1924/2006) given as reference points. The MoH red-label regulation (Israel, in force since 2020, mandatory phase-in completed) marks products exceeding per-100g thresholds for **sodium, sugar, and saturated fat** — these three are the explicit Israeli anchors.

### Protein
- **Framework:** FAO 2013 (DIAAS/PDCAAS — see §1). EU claim: "source of protein" ≥12% energy, "high in protein" ≥20% energy from protein (Reg 1924/2006).
- **Quantity → quality → evidence:** quantity = g/100g (disclosed). Quality = source DIAAS tier (§1, usually a *signal*, proportions hidden). Evidence = strong for protein adequacy/satiety; complete-protein necessity is well-established.
- **MoH red-label:** none (protein is not a red-label nutrient).
- **Confidence:** quantity HIGH (disclosed); quality LOW–MODERATE (source often a blend → confidence-gated).

### Fiber (intrinsic vs added/isolated)
- **Framework:** **FDA 2016** redefinition — only fibers with a demonstrated physiological benefit count as "dietary fiber"; isolated/synthetic fibers (e.g. inulin counts; some added fibers must be petition-approved). EU claim: "source of fibre" ≥3g/100g, "high fibre" ≥6g/100g.
- **Quantity → quality → evidence:** quantity = g/100g. Quality = **intrinsic (whole-grain matrix) vs added/isolated** — the FDA benefit-demonstration line. Evidence = strong for intrinsic fiber; mixed for isolated added fibers (benefit is fiber-specific).
- **MoH red-label:** none directly (fiber is a positive signal, not a red-label trigger), though whole-grain context interacts with category rubrics.
- **Confidence:** quantity HIGH; intrinsic-vs-added often **disclosure-gap** (labels rarely distinguish) → MODERATE/LOW.

### Sugar (total vs added vs FREE sugars; + non-nutritive sweeteners)
- **Framework:** **WHO free-sugars** concept (free sugars = added + those in honey/syrups/juices; recommend <10% energy, conditional <5%). US label discloses "added sugars"; EU discloses total sugars only. EU claims: "low sugar" ≤5g/100g (solids), "no added sugar" defined. **WHO 2023 NNS guideline:** conditional recommendation *against* non-sugar sweeteners for weight control / NCD risk.
- **Quantity → quality → evidence:** quantity = total sugar g/100g (disclosed). Quality = **free vs intrinsic** — the meaningful distinction, usually undisclosed in IL/EU (a structural gap; the US added-sugars line helps where available). Evidence = strong (free sugars ↔ NCD risk). NNS = the WHO 2023 evidence layer.
- **MoH red-label:** **YES — sugar is a red-label nutrient.** Explicit Israeli anchor.
- **Confidence:** total HIGH; added/free often **disclosure-gap** in Israel → flag.

### Sodium
- **Framework:** WHO <2g sodium/day (<5g salt). EU claims: "low sodium" ≤0.12g Na/100g, "very low" ≤0.04g, "high" trigger via claims reg.
- **Quantity → quality → evidence:** quantity = mg Na/100g (disclosed). Quality/form = salt vs sodium-additives (E-salts contribute — links to §2 phosphates/citrates). Evidence = strong (sodium ↔ BP/CVD).
- **MoH red-label:** **YES — sodium is a red-label nutrient.** Explicit Israeli anchor.
- **Confidence:** HIGH (well-disclosed).

### Saturated fat — **CONTESTED (dairy-matrix debate) — confidence must reflect it**
- **Framework:** WHO/most guidelines: reduce SFA (<10% energy) for CVD. EU claim "low saturated fat" ≤1.5g/100g (solids). **BUT** the **dairy-matrix debate** is live and substantial: meta-analyses (e.g. de Goede 2015; Guo 2017; Astrup 2020 *BMJ*/*Am J Clin Nutr*) find fermented dairy (cheese, yogurt) does **not** carry the CVD risk that the isolated-SFA model predicts — the food matrix matters. This is exactly a **Contested** tier per Bari's taxonomy.
- **Quantity → quality → evidence:** quantity = g/100g. Quality/form = **SFA in a dairy/whole-food matrix vs free SFA / palm in engineered food** — the crux. Evidence = strong for SFA→LDL in isolation; **contested** for whole-dairy CVD outcomes.
- **MoH red-label:** **YES — saturated fat is a red-label nutrient** (this is a point of tension: the red label flags whole cheese/yogurt that the matrix literature partially exonerates — Bari should surface the *tension*, not resolve it).
- **Confidence:** quantity HIGH; interpretation **explicitly lowered** for dairy matrix. (Already a known Bari recal theme — TASK-169 cheese/yogurt category-relative rubric; keep consistent.)

### Total fat / fat quality (trans fat)
- **Framework:** **Trans fat = confirmed-negative.** WHO **REPLACE** (2018) initiative to eliminate industrial trans fat; ≤1% energy / virtual elimination. Israel MoH caps industrial TFA (aligned with WHO ≤2g/100g fat → moving to elimination). EU caps industrial TFA at 2g/100g fat (Reg 2019/649).
- **Quantity → quality → evidence:** quantity = g/100g. Quality = trans (confirmed-negative) vs unsaturated (favorable) vs SFA (see above). Evidence = trans→CVD is among the strongest in nutrition.
- **MoH red-label:** indirect (via saturated-fat label; trans is regulated by cap, not a separate red label).
- **Confidence:** HIGH where disclosed; trans is increasingly near-zero post-REPLACE (a *disappearing* signal).

### Energy density — context-dependent (NOT "fewer calories = better")
- **Framework:** No single threshold; energy density (kcal/100g) is interpretive, category-relative. Whole nuts are calorie-dense and nutritionally excellent; diet products are calorie-light and may be engineered.
- **Quantity → quality → evidence:** quantity = kcal/100g. Quality = *what the calories are made of* (the decisive layer). Evidence = energy density ↔ weight only in context (Rolls et al.); not a standalone good/bad.
- **MoH red-label:** none.
- **Confidence:** HIGH on number; interpretation MUST be category-relative — **hard rule: never "fewer calories = better."**

### Micronutrients / fortification — meaningful vs marketing
- **Framework:** EU claims: "source of [vitamin]" ≥15% NRV/100g, "high" ≥30% NRV. Israel MoH fortification rules. Distinguish *meaningful* fortification (addresses a real gap, bioavailable form) from *marketing* fortification (trivial % NRV, splashy claim).
- **Quantity → quality → evidence:** quantity = % NRV. Quality = **form/bioavailability** (e.g. iron as ferrous bisglycinate vs trivial; folate vs folic acid) — usually undisclosed. Evidence = fortification benefit is nutrient- and population-specific.
- **MoH red-label:** none (positive marketing claims are governed separately).
- **Confidence:** quantity MODERATE (often present); form/meaningfulness LOW (disclosure-gap) → treat marketing fortification skeptically, flag don't credit.

**Cross-cutting Israeli vs EU vs US divergence summary:** Israel = red-label (סימון אדום) on sodium/sugar/sat-fat is the strongest local signal and has **no EU/US equivalent** (US uses voluntary "added sugars" line; EU uses claims-reg thresholds). Free-sugars and intrinsic-vs-added-fiber are **better disclosed in the US** than in IL/EU. Trans fat is converging globally toward elimination.

---

## SECTION 4 — Source / API Leverage Map

Legend: **LIVE** = per-product API call viable at score time · **BULK** = import-once-and-curate into a maintained reference library (NOT a live call) · **WIRED** = already in Bari's integration layer (TASK-170, live-verified 2026-06-03) · **NEW** = wiring needed.

| Source | Feeds dimension(s) | LIVE or BULK | Bari status | Notes |
|---|---|---|---|---|
| **USDA FoodData Central** | Protein quality (amino-acid profiles), composition | **BULK** (curate AA reference + DIAAS table) | **NEW** | AA profiles are reference-stable; bulk-import once, don't call per product. Underpins §1. |
| **EFSA OpenFoodTox** | Additive evidence (§2) | **BULK** (curate into additive library) | **NEW** | Re-evaluation database; the authoritative additive verdict source for IL/EU. |
| **JECFA / Codex GSFA** | Additive ADI, permitted use (§2) | **BULK** | **NEW** | ADI values are reference-stable; curate. |
| **FDA Substances Added to Food / GRAS** | Additive cross-check (§2) | **BULK** | **NEW** | US cross-reference only; secondary to EFSA for IL. |
| **Cochrane Reviews** | Evidence tiering (sweeteners, fiber, additive contested cases) | **BULK** (cite in curation) | **NEW** | Top of source hierarchy; manual curation, not an API feed. |
| **PubChem** | Additive/compound identity disambiguation | **LIVE** (per ingredient) | **WIRED** (`pubchem.get_compound`) | Resolves a name→CID when identity is ambiguous. Identity, not evidence. |
| **OpenFoodFacts additives taxonomy** | Additive detection / E-number tagging in panels | **LIVE** (per barcode) + **BULK** (taxonomy) | **WIRED** (`open_food_facts`) | Already used; taxonomy maps E-codes→class. Coverage of Israeli SKUs is partial. |
| **Tzameret (Israeli food composition)** | Composition, Israeli-specific nutrient values | **BULK** (CSV) + **LIVE** (CKAN search) | **WIRED** (`tzameret`) | 4624 foods persisted; the Israeli composition anchor. |
| **il_gov_data (MoH imported foods / manufacturers / max-prices / regulatory)** | Israeli regulatory context, red-label inputs, imported-food panels | **LIVE** (CKAN) | **WIRED** (`il_gov_data`) | 32k imported foods; the Israeli regulatory anchor for §3 red-label. |
| **Literature clients (PubMed / EuropePMC / OpenAlex / ClinicalTrials)** | Evidence tiering across all dimensions | **LIVE** (per query) | **WIRED** (`literature`) | Use `pub_types` to anchor tier; the find-and-characterize layer, not the verdict. |
| **il_prices / prices (Shufersal + laibcatalog)** | Not a nutrition source | LIVE | WIRED | Out of scope for enrichment; listed for completeness. |
| **DSLD (supplement labels)** | Supplement enrichment (SIE / TASK-171) — not BSIP2 food | LIVE | WIRED | Out of scope here; relevant to the supplement engine, not Glass Box food dims. |

**Load-bearing point (explicit):** The authoritative **additive** sources (EFSA OpenFoodTox, JECFA, FDA, Cochrane) are **BULK-curate** — a maintained reference library, **NOT live per-product calls.** Per-product, you detect additives in the panel (OFF taxonomy / regex on the scraped ingredient list, both already available) and **look them up in the curated library.** This is cheaper, faster, auditable, and avoids hammering external APIs at score time. The same is true for the **protein DIAAS table** (USDA AA profiles) — curate once, look up by disclosed source.

**Already-wired vs new wiring:**
- **WIRED (live as of 2026-06-03):** OFF, PubChem, DSLD, literature, il_gov_data, Tzameret, prices — these need **no new integration work**; Glass Box reuses them.
- **NEW wiring needed (all BULK / curate-once):** USDA FDC (protein AA table), EFSA OpenFoodTox + JECFA + FDA (additive library), Cochrane (manual evidence curation). None require a live API at score time.

---

## SECTION 5 — Recommendations (cheapest / highest-value first)

The lean order below reuses existing plumbing first and defers the expensive, maintenance-heavy library until consumer engagement is proven.

**R1 — Ship D5 (transparency) + D6 (confidence) FIRST.** *(Cheapest; no new library.)* These two dimensions reuse plumbing Bari already has: disclosure completeness (does the panel give proportions? E-codes named or generic? is the protein source identified?) and confidence gating are *already* the substrate of every caveat in §1–§3. They need **no USDA/EFSA library** — only logic over the existing scraped panel. They directly operationalize the clinician's points #1 and #4 ("partial visibility" and "don't pretend certainty"). Highest value per unit effort.

**R2 — Build the Protein-Source Quality Table (§1).** *(Small, ~25 rows, high credibility.)* Curate USDA FDC AA profiles + FAO 2013 DIAAS values once into a static reference. Wire as a **confidence-gated signal** ("is disclosed protein high-quality?"), never a per-product DIAAS. Directly answers the clinician's headline example. Low maintenance (DIAAS values are reference-stable; review ~annually).

**R3 — Build an additive PROTOTYPE (~20 additives, ONE pilot category), instrumented.** *(Defer the full library.)* Use the §2 prototype set (already frequency-ranked from real panels) for a single pilot category — **maadanim or snack-bars are the natural pilots** (highest additive density observed). **Instrument it to measure whether consumers actually engage** with additive verdicts. Only scale to a full additive library if engagement is proven. This avoids committing to the single largest maintenance liability before there is evidence it moves the consumer.

**Maintenance-liability flags (named review cadence required):**
- **Additive library = the dominant liability.** An out-of-date additive verdict is a **credibility event** (e.g. EFSA re-evaluates E471/E466/carrageenan; IARC reclassified aspartame in 2023; WHO issued NNS guidance in 2023). **Cadence: quarterly EFSA-re-evaluation watch + immediate-trigger on any IARC/WHO/JECFA change.** This is why R3 is a *prototype*, not a library — don't take on the liability until engagement justifies it.
- **Protein table:** low liability; **annual** review against FAO/USDA updates.
- **Nutrient framework registry (§3):** medium; **semi-annual** review, with an **immediate trigger** on any Israeli MoH red-label threshold change or WHO guideline update (sugar/sodium/sat-fat/sweeteners).
- **Disclosure/confidence logic (R1):** lowest liability; revisit only when scraping/panel coverage changes.

**Sequencing rationale:** R1 ships value with zero library debt; R2 adds the highest-credibility, lowest-maintenance reference; R3 buys the additive capability as a *measured bet* rather than an unproven, high-maintenance commitment. Nothing here is adopted — adoption is the Nutrition + Product gate (D6/D7).

---

## Appendix — Confidence & divergence quick-reference

- **Confidence is highest** for disclosed *quantities* (sodium, total sugar, total fat, protein g) and *lowest* for undisclosed *quality/form* (DIAAS of a blend, free-vs-total sugar, intrinsic-vs-added fiber, fortification bioavailability) — the latter all route to D5/D6.
- **Contested flags that must lower confidence in copy:** saturated fat in dairy matrix (§3), carrageenan (E407), CMC (E466), aspartame (E951).
- **Israel-specific anchors:** red-label (סימון אדום) on sodium/sugar/sat-fat; Tzameret + il_gov_data as the local data spine.
- **Evidence-first hard rule honored throughout:** no additive carries a verdict without an authoritative source; where none exists, tier = disclosure-gap/uncertain.

*End of dossier v1. Scoping only — no engine, scoring, or frontend file was modified.*
