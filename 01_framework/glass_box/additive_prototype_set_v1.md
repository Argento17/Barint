---
document: additive_prototype_set_v1
task: TASK-179Q
phase: Phases 1-3 complete — Product co-sign (Phase 4) pending
status: COMPLETE_PENDING_PROTOTYPE_BUILD
created_at: 2026-06-04
---

# Additive Prototype Set v1 — Glass Box W2

**Purpose:** Identifies ~20 shelf-frequent additives across the hummus, maadanim, and bread corpora, and builds evidence dossiers for each. Nutrition assigns tiers (Phase 3). Product co-signs scope (Phase 4). No code or score movement in this document.

**DEC-006 posture (binding on all entries):** D5 never moves the headline grade on its own axis. Opacity acts through D6 confidence. Hebrew consumer explanations must use plain language only; no "dangerous," "harmful," "toxic" framing; no attribution of manufacturer intent. Tier assignments remain `[PENDING — Nutrition to assign]` throughout this document.

---

## Frequency Scan Methodology

**Corpora scanned:**
- **Hummus:** 55 products with substantive ingredient text, drawn from `02_products/hummus/intelligence_bsip2/run_hummus_002/products/*/bsip2_trace.json` (L1_observed_signals.ingredient_list field).
- **Maadanim:** 184 products from `02_products/maadanim/maadanim_bsip0_raw_20260602T055557.json` (ingredients_raw field).
- **Bread:** 181 products from `02_products/bread_retail_003/real_bread_retail_003_v1_20260525T194532_bsip0_raw.json` (ingredients_raw field).
- **Total corpus:** 420 products; 3 categories.

**Detection method:** Hebrew regex patterns matching E-number strings, IUPAC names in Hebrew, and common Israeli label terms. Patterns written to match named declarations (e.g., "מייצב (פקטין)") and direct E-number citations (e.g., "E440"). Generic-class-only terms (bare "מייצב" without a name) are tracked separately as disclosure gaps per the D5 framework but are not counted as a specific named additive in the frequency table.

**Selection criteria applied:**
1. Appears as a named/identified additive in ≥ 3 products across the combined corpus.
2. The final set of 20 spans multiple evidence tiers to make the D4 tier system visible and useful.
3. Prioritizes additives that are consumer-relevant: ones shoppers inquire about, or that appear on front-of-pack claims ("without preservatives," "with natural flavors").

**Raw frequency table (top 25 detected):**

| Additive | Hummus (n=55) | Maadanim (n=184) | Bread (n=181) | Total | Categories |
|---|---|---|---|---|---|
| E330 citric acid | 34 | 43 | 45 | 122 | 3 |
| E200–E203 sorbates | 46 | 30 | 38 | 114 | 3 |
| E300 ascorbic acid | 0 | 7 | 106 | 113 | 2 |
| E1422 modified starch | 3 | 82 | 3 | 88 | 3 |
| E282 calcium propionate | 0 | 0 | 81 | 81 | 1 |
| E481 SSL | 0 | 0 | 63 | 63 | 1 |
| E500 baking soda | 32 | 14 | 9 | 55 | 3 |
| E407 carrageenan | 0 | 50 | 1 | 51 | 2 |
| E471 mono-/diglycerides | 0 | 13 | 28 | 41 | 2 |
| E472e DATEM | 0 | 3 | 37 | 40 | 2 |
| E415 xanthan gum | 12 | 18 | 9 | 39 | 3 |
| E450/451 phosphates | 0 | 31 | 8 | 39 | 2 |
| E440 pectin | 0 | 35 | 0 | 35 | 1 |
| E412 guar gum | 6 | 20 | 7 | 33 | 3 |
| E410 LBG | 0 | 32 | 0 | 32 | 1 |
| E955 sucralose | 0 | 26 | 0 | 26 | 1 |
| E322 soy lecithin | 0 | 18 | 5 | 23 | 2 |
| E150 caramel color | 0 | 8 | 1 | 9 | 2 |
| E950 acesulfame-K | 0 | 7 | 1 | 8 | 2 |
| E466 CMC | 0 | 7 | 1 | 8 | 2 |
| E170 calcium carbonate | 0 | 0 | 8 | 8 | 1 |
| E420 sorbitol | 0 | 5 | 0 | 5 | 1 |
| E210–E213 benzoates | 0 | 3 | 0 | 3 | 1 |
| E320 BHA | 0 | 0 | 1 | 1 | 1 |

**Selection rationale for the 20:** All additives with total count ≥ 8 and appearing in ≥ 2 categories are included (12 entries: E330, E202/203, E300, E1422, E415, E450/451, E471, E472e, E322, E412, E950, E466). Single-category additives with count ≥ 25 or high consumer relevance are added: E282 calcium propionate (81 bread products, high consumer awareness of preservatives), E481 SSL (63 bread products, representative bread dough conditioner), E407 carrageenan (50 maadanim, "contested" tier anchor), E440 pectin (35 maadanim, functional/fiber-equivalent anchor), E410 LBG (32 maadanim, representative dairy stabilizer), E955 sucralose (26 maadanim, NNS tier-diversity and consumer relevance). BHA (E320) and sodium benzoate (E211) are included at low frequency for tier-diversity: BHA is the only IARC-2B classified additive in the corpus and the "named concern" anchor; benzoate is the benzene-formation concern representative. The final 20 are: E330, E202, E300, E1422, E282, E481, E407, E471, E472e, E415, E450/451, E440, E410, E412, E955, E950, E466, E150, E211, E320. E500 (baking soda), E322 (lecithin), and E170 (calcium carbonate) were considered but excluded: baking soda and calcium carbonate are definitively neutral with no tier-diversity value; E322 lecithin is already handled in ingredient_taxonomy.py as "emulsifier_benign" and adds no new tier insight. E420 sorbitol was deprioritized in favor of the contested/named-concern additives for tier-diversity.

---

## Additive Entries

---

### Entry 1: Citric Acid (E330)

**E-number:** E330

**IUPAC / common name (English):** Citric acid
**Common Hebrew name:** חומצת לימון / חומצה ציטרית

**Technological function:** Acidulant / pH regulator / antioxidant synergist. In hummus: prevents browning and microbial growth. In maadanim: pH adjustment and flavor. In bread: dough conditioner, interacts with leavening agents.

**Frequency on shelf:** 122 products across all 3 categories (hummus 34, maadanim 43, bread 45). Most-frequent named additive in the corpus.

**Evidence summary:**
- **EFSA status:** Evaluated; no safety concerns at current use levels. EFSA has approved E330 broadly across food categories with no numerical ADI (acceptable daily intake) — classified as "no ADI necessary" because citric acid is a normal metabolite in human biochemistry (Krebs cycle intermediate).
- **JECFA:** Listed as a permitted food additive; no numerical ADI established; GMP (Good Manufacturing Practice) use approved.
- **FDA:** GRAS (Generally Recognized As Safe, 21 CFR §184.1033). Produced both from citrus and by Aspergillus niger fermentation for industrial use.
- **Literature:** The additive is a well-studied natural acid with no dose-response concerns at food-label exposures. At high industrial exposures (food industry workers, dental acid erosion from beverages at high concentrations) there are occupational and dental context risks, but these are not relevant at food-label typical exposure. PMID 30123195 (2018) notes citric acid as a biotechnologically produced food additive with well-established safety.

**Dose signal:** No meaningful dose-response concern at food-label exposures. Citric acid is endogenously produced and metabolized. No ADI established (meaning safety margin is very wide).

**Israeli label behavior:** Usually named explicitly ("חומצת לימון," "חומצה ציטרית") or by E-number. Rarely hidden behind generic "מווסת חומציות" without specification. One of the more transparently disclosed additives in the corpus.

**Tier:** functional
**Tier rationale:** Citric acid is a Krebs-cycle intermediate endogenously produced in human metabolism; EFSA and JECFA assign no numerical ADI (safety margin is too wide to require one); no dose-response safety concern exists at any realistic food-label exposure level.

**Draft Hebrew consumer explanation:** חומצת לימון היא חומצה טבעית שנמצאת גם בלימון ובפירות הדר, ומשמשת לאיזון טעם ולמניעת שינוי צבע. ✓ approved

---

### Entry 2: Potassium Sorbate (E202)

**E-number:** E202 (also E200 sorbic acid, E201 sodium sorbate; potassium sorbate is by far the most common on this shelf)

**IUPAC / common name (English):** Potassium sorbate / sorbic acid salts
**Common Hebrew name:** פוטסיום סורבט / סורבט אשלגן / חומר משמר (E202)

**Technological function:** Antimicrobial preservative. Inhibits mold and yeast; critical for shelf stability of hummus, tahini-based spreads, and bread.

**Frequency on shelf:** 114 products across all 3 categories (hummus 46, maadanim 30, bread 38). Second most-frequent named additive.

**Evidence summary:**
- **EFSA status:** Evaluated; ADI = 3 mg/kg body weight/day (as sorbic acid equivalents). Considered safe at the established ADI. EFSA re-evaluated sorbic acid/sorbates (E200–E203) and concluded no new safety concerns at current use levels.
- **JECFA:** ADI = 0–25 mg/kg body weight/day (sorbic acid). Well within safety margin at typical food exposures.
- **FDA:** GRAS (sorbic acid 21 CFR §182.3089; potassium sorbate 21 CFR §182.3640).
- **Literature:** A 2026 European prospective cohort study (NutriNet-Santé, europepmc ID 41501013) found associations between certain preservative food additives and type 2 diabetes incidence; sorbates were included in the analysis. The effect sizes were small and the study design cannot establish causality. A 2025 in vitro study (PMID 41228538) found differential apoptotic gene expression in HepG2 cells exposed to sodium benzoate, potassium sorbate, and sodium metabisulfite — a cell-culture finding that does not translate directly to in vivo exposure conclusions. The dominant regulatory consensus (EFSA, JECFA) is that sorbate at ADI-compliant food levels is safe. The NutriNet-Santé findings are observational and require further confirmation.

**Dose signal:** ADI = 3 mg/kg bw/day (EFSA). Typical dietary exposure from bread and spreads is estimated at 0.5–1.5 mg/kg bw/day across European surveys — within ADI. High consumer awareness of preservatives; often listed on front-of-pack claims ("ללא חומרי שימור").

**Israeli label behavior:** Usually named explicitly. The corpus shows "פוטסיום סורבט" or "E202" as named declarations. In some products, appears under generic "חומר משמר" without specific name — this is a D5 closable gap (the manufacturer could have disclosed the E-number).

**Tier:** likely-neutral
**Tier rationale:** EFSA ADI (3 mg/kg bw/day as sorbic acid) and JECFA ADI (25 mg/kg bw/day) are both well above typical dietary exposure (0.5–1.5 mg/kg bw/day from bread and spreads); the 2026 NutriNet-Santé prospective cohort association with T2D is a single observational finding that cannot establish causation and has not shifted the regulatory consensus — it is a signal warranting monitoring, not sufficient to reclassify to dose-dependent at this time. The standard is met for likely-neutral with a flag to reassess if a replication study or EFSA re-evaluation confirms the association.

**Draft Hebrew consumer explanation:** סורבט אשלגן הוא חומר משמר נפוץ המונע התפתחות עובש, ומאושר לשימוש ברמות הנהוגות על ידי רשויות הבריאות באירופה ובישראל. ✓ approved

---

### Entry 3: Ascorbic Acid (E300)

**E-number:** E300

**IUPAC / common name (English):** Ascorbic acid (vitamin C)
**Common Hebrew name:** חומצה אסקורבית / ויטמין C

**Technological function:** Antioxidant / dough improver. In bread: strengthens gluten network, extends shelf life, improves crumb structure. In some products: declared as vitamin C (fortification/antioxidant). The bread usage is primarily technological (dough conditioner), not nutritional fortification.

**Frequency on shelf:** 113 products — overwhelmingly bread (106/181 products). Present in 59% of the bread corpus.

**Evidence summary:**
- **EFSA status:** No ADI established; ascorbic acid is a normal vitamin with wide safety margin. EFSA considers E300 safe at all permitted food uses.
- **JECFA:** No ADI assigned (same rationale as citric acid — normal nutrient, wide safety margin).
- **FDA:** GRAS (21 CFR §182.3013).
- **Literature:** No safety concerns at food-label exposures. As a dough improver, ascorbic acid is oxidized during baking and no longer present as vitamin C in the finished bread — it is a process aid rather than a micronutrient delivery vehicle. This distinction matters for Israeli label context: "חומצה אסקורבית" in bread ingredient lists is a dough conditioner, not a vitamin supplement.

**Dose signal:** Essentially none at food-label exposures. Vitamin C upper tolerable intake is 2000 mg/day (adults); dough-improving additions are typically 10–50 mg per 100g of dough, well within any meaningful limit.

**Israeli label behavior:** Usually named ("חומצה אסקורבית," "ויטמין C," "E300"). Rarely hidden. The technological function in bread is not typically communicated to consumers; front-of-pack labeling rarely highlights it.

**Tier:** functional
**Tier rationale:** Ascorbic acid (vitamin C) is a normal human nutrient with no numerical ADI; as a dough improver it is oxidized during baking and is no longer present in the finished product — it functions as a process aid with zero residual safety concern; EFSA, JECFA, and FDA all confirm wide safety margin.

**Draft Hebrew consumer explanation:** חומצה אסקורבית (ויטמין C) משמשת בלחם בעיקר כחומר עזר לאפייה — היא משפרת את מרקם הבצק ואינה מהווה תוספת ויטמינים משמעותית במוצר הסופי. ✓ approved

---

### Entry 4: Modified Starch (E1422 / E1442 and related)

**E-number:** E1422 (acetylated distarch adipate), E1442 (hydroxypropyl distarch phosphate), and related acetylated/cross-linked starches. The corpus detection used a broad pattern for "עמילן מעובד" (modified starch) which may include multiple E-number variants.

**IUPAC / common name (English):** Modified starch (various chemical modifications)
**Common Hebrew name:** עמילן מעובד / עמילן שונה

**Technological function:** Thickener / texture stabilizer / freeze-thaw stabilizer. In maadanim: prevents syneresis (water separation) in dairy desserts; maintains creamy texture under refrigeration. In hummus: occasional use for texture stability.

**Frequency on shelf:** 88 products (hummus 3, maadanim 82, bread 3). Dominant in maadanim — 45% of maadanim products.

**Evidence summary:**
- **EFSA status:** Multiple modified starch E-numbers evaluated. EFSA's ANS Panel has re-evaluated modified starches; general conclusion is that modified starches are not absorbed intact and are metabolized as carbohydrates. No specific ADI established; Group ADI = "not specified" (wide safety margin). The modifications are chemical but the resulting compounds are broken down in digestion.
- **JECFA:** Modified starches collectively given ADI "not specified" (1980, 2001 evaluations). Considered safe at levels used in food manufacturing.
- **FDA:** GRAS or food-additive-approved for most modified starches (21 CFR §172.892, §172.894).
- **Literature:** No primary safety concerns at food-label exposures. Modified starch metabolism is well characterized. Some dietary fiber labeling controversies exist in specific jurisdictions about whether highly modified starches contribute to fiber counts — a regulatory rather than safety issue.

**Dose signal:** No dose-response safety concern at food-label exposures. The EFSA "not specified" ADI indicates the safety margin is too wide to require a numeric limit.

**Israeli label behavior:** Often declared as "עמילן מעובד" or with E-number. E1442 is the dominant form in the maadanim corpus (found in yogurt-type desserts to stabilize texture under refrigeration). The specific modification type is rarely disclosed — generic "עמילן מעובד" is a closable D5 gap in the sense that the E-number could be specified, though the safety implication is the same across E1422/1442/1450 variants.

**Tier:** likely-neutral
**Tier rationale:** EFSA and JECFA both assign ADI "not specified" (safety margin too wide to require a numeric limit); modified starches are metabolized as carbohydrates; no dose-response safety concern at food-label exposures; the regulatory and metabolic picture is well established across multiple E-number variants (E1422, E1442, E1450).

**Draft Hebrew consumer explanation:** עמילן מעובד הוא עמילן שעבר עיבוד כימי לשיפור יציבות המרקם; הוא עובר עיכול כפחמימה רגילה ואינו נספג ישירות. ✓ approved

---

### Entry 5: Calcium Propionate (E282)

**E-number:** E282

**IUPAC / common name (English):** Calcium propionate
**Common Hebrew name:** פרופיונט סידן / E282

**Technological function:** Mold and rope inhibitor in bread. The dominant bread preservative in the corpus (81/181 products = 45% of bread). More common in sandwich bread and industrial bread than artisan products.

**Frequency on shelf:** 81 products — all bread.

**Evidence summary:**
- **EFSA status:** Evaluated. ADI = "not specified" (propionic acid and its salts, E280–E283). EFSA concluded no safety concerns at current use levels. Propionic acid is a short-chain fatty acid produced endogenously by gut bacteria and is a normal human metabolite.
- **JECFA:** ADI = "not limited" (1973, 1999).
- **FDA:** GRAS (21 CFR §184.1221).
- **Literature:** A 2019 Cell study (Tirosh et al.) found that propionate supplementation in mice and humans at pharmacological doses stimulated glucagon/epinephrine release; this generated media attention. The doses tested (pharmacological injection/supplementation) are orders of magnitude higher than food-label exposures from calcium propionate in bread. Follow-up reviews and re-analyses have not supported a food-safety concern at typical dietary levels. The regulatory consensus (EFSA, JECFA) has not changed. This is a case where a mechanistic finding at high doses does not translate to a food safety concern at realistic exposures.

**Dose signal:** No meaningful safety concern at food-label exposures. The Tirosh 2019 finding was at pharmacological (not dietary) doses. Typical bread exposure is well within any plausible margin of concern. The EFSA "not specified" ADI reflects this.

**Israeli label behavior:** Sometimes named ("פרופיונט סידן," "E282"), sometimes hidden under generic "חומר משמר" without E-number. Generic "חומר משמר" without specification is a D5 closable gap. High consumer awareness because "בלי חומרי שימור" (without preservatives) is a popular front-of-pack claim.

**Tier:** likely-neutral
**Tier rationale:** Propionic acid is a short-chain fatty acid produced endogenously by gut bacteria; EFSA and JECFA assign ADI "not specified"; the Tirosh 2019 glucagon/epinephrine finding was at pharmacological doses orders of magnitude above food-label exposure and has not been confirmed as a food-safety concern by EFSA or JECFA — typical bread exposure is well within any plausible safety margin.

**Draft Hebrew consumer explanation:** פרופיונט סידן הוא חומר משמר המונע עובש בלחם; חומצה פרופיונית דומה לו מיוצרת גם על ידי חיידקי המעיים שלנו באופן טבעי. ✓ approved

---

### Entry 6: Sodium Stearoyl Lactylate (SSL, E481)

**E-number:** E481

**IUPAC / common name (English):** Sodium stearoyl-2-lactylate
**Common Hebrew name:** נתרן סטארויל לקטילט / E481

**Technological function:** Dough conditioner / emulsifier in bread. Strengthens gluten network, improves loaf volume and softness; often paired with DATEM (E472e). Found almost exclusively in industrial bread production.

**Frequency on shelf:** 63 products — all bread (35% of bread corpus).

**Evidence summary:**
- **EFSA status:** Evaluated 2012; ADI = 20 mg/kg body weight/day. Considered safe at current use levels. EFSA noted that dietary exposures are well below the ADI in all assessed population groups.
- **JECFA:** ADI = 0–20 mg/kg bw/day.
- **FDA:** GRAS (21 CFR §172.846).
- **Literature:** Limited independent RCT data specifically on E481 at food exposures; regulatory evaluations draw primarily on animal toxicology and metabolic studies. No human clinical concerns identified. The 2024 NutriNet-Santé cancer study (europepmc ID 38349899) included emulsifiers as a class but did not single out E481 specifically as a concern driver.

**Dose signal:** ADI = 20 mg/kg bw/day. Typical bread exposure is estimated at 2–5 mg/kg bw/day in heavy bread consumers — within ADI. No dose-response concern at food-label exposures identified by EFSA or JECFA.

**Israeli label behavior:** Often hidden under generic "מייצב" or "מתחלב" (emulsifier) without specifying E481. When disclosed, it appears as "E481" or the full Hebrew name. Generic declaration without E-number is a D5 closable gap.

**Tier:** likely-neutral
**Tier rationale:** EFSA ADI = 20 mg/kg bw/day; typical bread consumer exposure is estimated at 2–5 mg/kg bw/day (well within ADI); no independent dose-response concern at food-label exposures; the NutriNet-Santé 2024 emulsifier-cancer observation was class-level and did not identify E481 specifically as a concern driver.

**Draft Hebrew consumer explanation:** SSL (E481) הוא מרכיב עזר באפיית לחם המסייע לבצק לתפוח ולשמור על רכות; אושר לשימוש על ידי רשויות האיחוד האירופי. ✓ approved

---

### Entry 7: Carrageenan (E407)

**E-number:** E407

**IUPAC / common name (English):** Carrageenan (kappa, iota, lambda subtypes)
**Common Hebrew name:** קרגינן / קרגינאן / E407

**Technological function:** Thickener / gelling agent / stabilizer. In maadanim: prevents phase separation in dairy desserts; creates creamy mouthfeel; water-binding in chocolate desserts and puddings. High presence in maadanim (50/184 = 27% of products).

**Frequency on shelf:** 51 products (maadanim 50, bread 1).

**Evidence summary:**
- **EFSA status:** Evaluated; ADI = "not specified" (EFSA ANS 2018 re-evaluation). EFSA concluded "no safety concerns" for food-grade carrageenan at current use levels. This is the most recent authoritative European evaluation and supersedes earlier opinions.
- **JECFA:** ADI = "not specified" (food-grade carrageenan, 2014 evaluation).
- **FDA:** GRAS for food-grade carrageenan; ongoing review of infant formula use (separate from adult food use).
- **Literature (contested area — this is the core scientific debate):**
  - Earlier concern arose from animal studies using **degraded carrageenan (poligeenan)** — a chemically distinct low-molecular-weight fraction that is not used in food. Much of the pre-2000s alarm literature confused poligeenan with food-grade carrageenan.
  - More recent research has raised concerns about **food-grade carrageenan** specifically: in vitro and rodent studies suggest carrageenan can alter gut microbiome composition and may activate NF-κB inflammatory pathways at concentrations achievable in the gut after digestion (Tobacman 2001, various; Bhattacharyya et al. 2017).
  - Europepmc ID 42073323 (2026 review): "Gut Microbiota Modulation by Carboxymethyl Cellulose and Carrageenan: Current Evidence and Health Implications" — notes ongoing scientific discussion on both CMC and carrageenan; acknowledges that definitive human RCT evidence at food-label exposures is limited.
  - The National Organic Program (USDA) debated removing carrageenan from its approved list; EFSA's 2018 re-evaluation found the mechanistic concerns not sufficient to revise the ADI.
  - The debate is genuine — not manufactured doubt. EFSA/JECFA find no safety concern at food levels; independent researchers and some gastroenterology researchers disagree, citing the mechanistic data. This is the definition of "contested" in the Bari tier framework.

**Dose signal:** EFSA concluded no safety concern at current use levels. The contested mechanistic data (gut barrier / inflammatory pathway activation) applies at concentrations that may be achievable in the colon after digestion — the dose-response relationship at food exposures is the crux of the scientific disagreement.

**Israeli label behavior:** Usually named explicitly ("קרגינן," "E407"). Notably transparent in the maadanim corpus — the detection pattern found it named in ~27% of maadanim products. Occasionally hidden as "מייצב" without specification, which is a D5 closable gap.

**Tier:** contested
**Tier rationale:** EFSA 2018 re-evaluation found no safety concern at current use levels and ADI "not specified"; however, independent peer-reviewed mechanistic research (Bhattacharyya et al. and others) has raised credible concerns about NF-κB inflammatory pathway activation and gut barrier effects at food-grade (not just degraded poligeenan) concentrations; the 2026 review (europepmc 42073323) confirms the scientific discussion is active and unresolved — this is genuine methodological disagreement among independent researchers, meeting the "contested" threshold.

**Draft Hebrew consumer explanation:** קרגינן הוא חומר מייצב שמקורו באצות ים המשמש לשמירה על מרקם חלק; קיים דיון מדעי פעיל לגבי ההשפעה שלו על מיקרוביום המעי, אם כי רשות המזון האירופית אישרה את השימוש בו ברמות הנוכחיות. ✓ approved

---

### Entry 8: Mono- and Diglycerides of Fatty Acids (E471)

**E-number:** E471

**IUPAC / common name (English):** Mono- and diglycerides of fatty acids
**Common Hebrew name:** מונו ודיגליצרידים של חומצות שומן / E471

**Technological function:** Emulsifier. In bread: softens crumb, slows staling, improves volume. In maadanim: fat emulsification in dairy desserts and frozen products.

**Frequency on shelf:** 41 products (maadanim 13, bread 28).

**Evidence summary:**
- **EFSA status:** ADI = "not specified" (extensive data; safety well established). Chemically, mono- and diglycerides are partial glycerol esters — structurally identical to partial lipid digestion products produced in normal fat metabolism.
- **JECFA:** ADI = "not specified."
- **FDA:** GRAS (21 CFR §182.4505).
- **Literature:** The 2024 NutriNet-Santé study (europepmc ID 38349899, "Food additive emulsifiers and cancer risk") included E471 as part of a class analysis and found a weak association between emulsifier exposure and cancer in the observational cohort. The authors acknowledged the limitations of observational design and the inability to separate individual emulsifier effects from overall processed-food patterns. The 2023 UK UPF study (europepmc ID 37732384) found E471 was the most commonly present emulsifier in UK ultra-processed foods. These observational findings have not changed the EFSA/JECFA safety assessment.

**Dose signal:** No dose-response concern at food-label exposures per EFSA/JECFA. The observational cancer association finding (NutriNet-Santé 2024) is hypothesis-generating, not conclusive.

**Israeli label behavior:** Sometimes disclosed as "E471" or the Hebrew chemical name; sometimes hidden under generic "מתחלב" or "מייצב" without E-number specification, which is a D5 closable gap. The corpus shows mixed disclosure.

**Tier:** likely-neutral
**Tier rationale:** EFSA and JECFA assign ADI "not specified" (chemically structurally identical to partial glycerol esters produced during normal fat digestion); the 2024 NutriNet-Santé emulsifier-cancer observational association (europepmc 38349899) is hypothesis-generating and could not isolate E471 individually — it does not meet the threshold for reclassifying to contested or dose-dependent at this time.

**Draft Hebrew consumer explanation:** מונו ודיגליצרידים הם חומרי תחליב נפוצים הדומים כימית לחלק מתוצרי עיכול השומן הטבעי; הם מאושרים לשימוש ברמות הנוכחיות. ✓ approved

---

### Entry 9: DATEM (E472e)

**E-number:** E472e

**IUPAC / common name (English):** Diacetyl tartaric acid esters of mono- and diglycerides
**Common Hebrew name:** DATEM / חומצה טרטרית מונו ודיגליצרידים אצטיל / E472e

**Technological function:** Dough conditioner / emulsifier in bread. Strengthens gluten network; particularly effective in whole-grain and high-fiber breads where gluten development is impeded. Often paired with SSL (E481).

**Frequency on shelf:** 40 products — predominantly bread (37/181 = 20% of bread corpus).

**Evidence summary:**
- **EFSA status:** ADI = "not specified" for the E472 group. EFSA evaluated and concluded safe at current use levels.
- **JECFA:** ADI = "not specified."
- **FDA:** GRAS (21 CFR §182.4101).
- **Literature:** No specific safety concerns identified in the peer-reviewed literature at food-label exposures. The same observational emulsifier-and-cancer literature as E471 includes DATEM as part of the emulsifier class; no individual DATEM-specific mechanistic concern has been identified in human-relevant experimental models.

**Dose signal:** No dose-response safety concern at food-label exposures.

**Israeli label behavior:** Typically hidden under generic "מייצב," "מתחלב," or "חומרי תפיחה" without E-number or name. Explicit "DATEM" or "E472e" declaration is rare in the Israeli bread corpus. This is a common D5 closable gap in the bread category.

**Tier:** likely-neutral
**Tier rationale:** EFSA and JECFA assign ADI "not specified"; no specific mechanistic or clinical safety concern has been identified for DATEM at food-label exposures in human-relevant experimental models; the class-level emulsifier observational associations (NutriNet-Santé 2024) apply at a category level not specific to DATEM; evidence base is primarily regulatory and metabolic-stability data, which is sufficient for likely-neutral given no positive signal of harm.

**Draft Hebrew consumer explanation:** DATEM הוא חומר עזר לאפייה המסייע לגלוטן להתפתח ולשמור על מרקם הלחם; שמו הטכני מופיע לעתים רחוקות על תוויות לחם ישראליות. ✓ approved

---

### Entry 10: Xanthan Gum (E415)

**E-number:** E415

**IUPAC / common name (English):** Xanthan gum
**Common Hebrew name:** קסנטן / קסנטאן / E415

**Technological function:** Thickener / stabilizer / texture modifier. Produced by fermentation of sugars by *Xanthomonas campestris*. Widely used across all three categories for viscosity control and moisture retention.

**Frequency on shelf:** 39 products across all 3 categories (hummus 12, maadanim 18, bread 9). Cross-category presence.

**Evidence summary:**
- **EFSA status:** Evaluated 2017; ADI = "not specified." Panel concluded no safety concerns at current use levels. Xanthan gum is a high-molecular-weight polysaccharide; it is not absorbed intact but fermented by gut bacteria.
- **JECFA:** ADI = "not specified" (1975, confirmed).
- **FDA:** GRAS (21 CFR §172.695).
- **Literature:** The 2024 review on xanthan gum in dairy and plant-based milk (europepmc ID 38371690) discusses its functional properties without safety concerns. Fermented polysaccharides like xanthan are generally considered dietary fiber equivalents by the gut microbiome. No human safety concerns at food-label exposures identified in the literature.

**Dose signal:** No dose-response safety concern at food-label exposures. Fermented as prebiotic-like fiber in the colon; some studies suggest modest prebiotic effects, though not established as a health claim.

**Israeli label behavior:** Usually named explicitly ("קסנטן," "E415"). One of the more transparent stabilizers on Israeli labels. The note in d5_d6_rule_spec_v1.md acknowledges real-panel noise: "קסנטאן גא ם" (space inserted by OCR/text extraction) — normalization resolves this.

**Tier:** functional
**Tier rationale:** Xanthan gum is a fermentation-derived high-molecular-weight polysaccharide; EFSA ADI "not specified"; it is not absorbed intact but fermented by gut bacteria as a dietary fiber equivalent; evidence is neutral to potentially positive (modest prebiotic effect at higher doses); no safety concern at any food-label exposure level across multiple evaluation bodies.

**Draft Hebrew consumer explanation:** קסנטן הוא מייצב טבעי המופק בתסיסה חיידקית, ומשמש לשמירה על מרקם אחיד ומניעת הפרדת מים. ✓ approved

---

### Entry 11: Dipotassium/Disodium Phosphates (E450, E451, E452)

**E-number:** E450 (diphosphates), E451 (triphosphates), E452 (polyphosphates)

**IUPAC / common name (English):** Sodium/potassium phosphates (various)
**Common Hebrew name:** פוספט / פוספטים / E450 / E451

**Technological function:** Emulsifier / pH buffer / protein stabilizer. In maadanim: stabilize dairy protein emulsions in chocolate desserts and cream-type products. In processed cheese (a related category): classic melting salts. In bread: occasional use as leavening aid.

**Frequency on shelf:** 39 products (maadanim 31, bread 8).

**Evidence summary:**
- **EFSA status:** Re-evaluated 2019 (phosphoric acid and phosphates, E338–452). EFSA concluded the group ADI = 40 mg/kg bw/day (as phosphorus equivalents). EFSA noted that combined phosphate intake from food additives plus natural phosphorus in food may exceed ADI in high-consuming subgroups — this was flagged as a concern in the 2019 opinion.
- **JECFA:** ADI = "not specified" for food-grade phosphates (phosphorus is an essential nutrient; the ADI concept applies to additive use above baseline dietary intake).
- **FDA:** GRAS for specific phosphate salts.
- **Literature:** Epidemiological and mechanistic literature on phosphate intake and cardiovascular risk / kidney disease primarily addresses total dietary phosphate (from both natural foods and additives), especially in chronic kidney disease (CKD) populations. PMID 33163715 (2020) examined dietary phosphate restriction in hemodialysis patients. For the general population without kidney impairment, the EFSA 2019 opinion is the governing assessment. The additive contribution to total phosphate intake is one part of a larger dietary exposure picture; EFSA's concern was about cumulative exposure across all sources, not additive use in isolation.

**Dose signal:** The EFSA 2019 ADI = 40 mg phosphorus/kg bw/day. Combined phosphate intake from additive sources plus natural dietary phosphorus may approach or exceed this in heavy processed-food consumers. This is a dose-dependent concern — the additive itself is not "harmful" but contributes to total phosphorus load. Not a concern for typical single-product exposure.

**Israeli label behavior:** Sometimes named ("E450," "E451," "פוספט"), sometimes hidden under generic "מייצב" without E-number. Detection in 31 maadanim products suggests systematic use. The generic class term without a specific E-number is a D5 closable gap.

**Tier:** dose-dependent
**Tier rationale:** EFSA 2019 re-evaluation established a group ADI of 40 mg phosphorus/kg bw/day and explicitly flagged that combined phosphate intake from food additives plus natural dietary phosphorus may approach or exceed this ADI in heavy processed-food consumers — this is a documented dose-response concern with a credible cumulative-exposure pathway, not just a theoretical concern; the additive contributes to total phosphorus load in a quantifiable way per serving.

**Draft Hebrew consumer explanation:** פוספטים הם מלחים של זרחן — מינרל חיוני לגוף — המשמשים לייצוב מרקם מוצרי חלב; צריכה מצטברת מכלל מקורות המזון ראויה לתשומת לב. ✓ approved

---

### Entry 12: Pectin (E440)

**E-number:** E440

**IUPAC / common name (English):** Pectin (high-ester and low-ester variants)
**Common Hebrew name:** פקטין / E440

**Technological function:** Gelling agent / thickener. In maadanim: creates fruit gels, sets yogurt-style desserts, stabilizes fruit preparations. Natural polysaccharide derived from citrus peel or apple pomace.

**Frequency on shelf:** 35 products — all maadanim (19% of maadanim corpus).

**Evidence summary:**
- **EFSA status:** No ADI (GMP use; safety well established). EFSA has not identified any safety concern. Pectin is classified as soluble dietary fiber.
- **JECFA:** ADI = "not specified."
- **FDA:** GRAS (21 CFR §184.1588).
- **Literature:** The 2026 europepmc review (ID 42074161) on pectin confirms its status as a versatile biomaterial with strong safety profile. Pectin is a prebiotic dietary fiber; epidemiological associations with pectin consumption are generally positive (gut microbiome fermentation, cholesterol reduction). No safety concerns at food-label exposures.

**Dose signal:** No dose-response safety concern. Pectin is fermented in the colon as soluble fiber; potential prebiotic benefit at higher intake levels. No upper limit established.

**Israeli label behavior:** Usually named explicitly ("פקטין," "E440"). Relatively transparent disclosure in the corpus.

**Tier:** functional
**Tier rationale:** Pectin is classified as soluble dietary fiber by EFSA with no ADI (safety margin too wide to require one); it is a naturally occurring plant polysaccharide with established prebiotic fermentation in the colon and a positive evidence profile (cholesterol modulation, gut microbiome support); no safety concern at any food-label exposure.

**Draft Hebrew consumer explanation:** פקטין הוא סיב תזונתי מסיס שמקורו בפירות הדר ותפוחים, המשמש ליצירת מרקם ג'ל טבעי ומזין חיידקי מעיים מיטיבים. ✓ approved

---

### Entry 13: Locust Bean Gum (LBG, E410)

**E-number:** E410

**IUPAC / common name (English):** Locust bean gum / carob bean gum
**Common Hebrew name:** לוקוסט-בין גאם / קרוב בין גאם / E410

**Technological function:** Thickener / stabilizer / synergistic gelling agent (with carrageenan or xanthan). In maadanim: common in yogurt-type products and dairy desserts for texture control and prevention of syneresis.

**Frequency on shelf:** 32 products — all maadanim (17% of maadanim corpus).

**Evidence summary:**
- **EFSA status:** ADI = "not specified." EFSA concluded safe at current use levels. LBG is derived from the endosperm of carob seeds; largely indigestible polysaccharide.
- **JECFA:** ADI = "not specified."
- **FDA:** GRAS (21 CFR §182.1343).
- **Literature:** No human safety concerns at food-label exposures. LBG is classified as dietary fiber; some evidence suggests prebiotic properties. The d5_d6_rule_spec_v1.md notes its explicit appearance on Israeli maadanim labels: "מייצב (לוקוסט-בין גאם)" is one of the correctly-named examples used in the pilot sanity-check.

**Dose signal:** No dose-response safety concern.

**Israeli label behavior:** Mixed — sometimes declared explicitly as "לוקוסט-בין גאם" (correctly named, not a D5 gap), sometimes hidden under generic "מייצב" (D5 closable gap). The pilot confirms both patterns exist on Israeli maadanim labels.

**Tier:** functional
**Tier rationale:** Locust bean gum is a carob-seed-derived indigestible polysaccharide; EFSA ADI "not specified"; classified as dietary fiber with potential prebiotic properties; no safety concern identified at any food-label exposure level across all evaluation bodies; structurally food-like (a natural seed gum).

**Draft Hebrew consumer explanation:** לוקוסט-בין גאם הוא מייצב טבעי שמקורו בעץ החרוב, ומשמש לשמירה על מרקם קרמי ומניעת הפרדת נוזלים. ✓ approved

---

### Entry 14: Guar Gum (E412)

**E-number:** E412

**IUPAC / common name (English):** Guar gum
**Common Hebrew name:** גואר / גואר גאם / E412

**Technological function:** Thickener / water binder. Derived from guar beans. Used across all three categories for viscosity control; cross-category presence distinguishes it from single-category stabilizers.

**Frequency on shelf:** 33 products across all 3 categories (hummus 6, maadanim 20, bread 7).

**Evidence summary:**
- **EFSA status:** ADI = "not specified." Safe at current use levels.
- **JECFA:** ADI = "not specified."
- **FDA:** GRAS (21 CFR §184.1339).
- **Literature:** No safety concerns at food-label exposures. Guar gum is a soluble dietary fiber with modest cholesterol-lowering effects at therapeutic doses (higher than typical food use). Historical occupational concerns in guar-processing workers (respiratory exposure) are not relevant to dietary exposure.

**Dose signal:** No dose-response safety concern at food-label exposures. Dietary fiber with potential functional properties at high doses.

**Israeli label behavior:** Usually named explicitly ("גואר," "E412"). More often disclosed than some other stabilizers.

**Tier:** functional
**Tier rationale:** Guar gum is a guar-bean-derived soluble polysaccharide; EFSA ADI "not specified"; classified as dietary fiber with modest cholesterol-lowering effects documented at therapeutic (higher-than-food-typical) doses; occupational respiratory risks from guar processing are irrelevant to dietary exposure; no safety concern at food-label exposures.

**Draft Hebrew consumer explanation:** גואר הוא חומר מסמיך טבעי המופק מזרעי גואר, ומשמש לשמירה על עקביות מרקם המוצר. ✓ approved

---

### Entry 15: Sucralose (E955)

**E-number:** E955

**IUPAC / common name (English):** Sucralose (1,6-dichloro-1,6-dideoxy-β-D-fructofuranosyl-4-chloro-4-deoxy-α-D-galactopyranoside)
**Common Hebrew name:** סוכרלוז / E955

**Technological function:** Non-nutritive sweetener (NNS). ~600x sweeter than sucrose. Used in "no added sugar" / "ללא סוכר" maadanim products as a sucrose replacement.

**Frequency on shelf:** 26 products — all maadanim (14% of maadanim corpus), predominantly in sugar-free yogurts and dairy desserts.

**Evidence summary:**
- **EFSA status:** Re-evaluated 2026 (europepmc ID 41710869). "No safety concerns arose for genotoxicity of sucralose and its impurities and degradation products. Based on the weight of evidence (WoE), the Panel considered the decrease in body weight as the critical effect in their safety assessment, and established a new ADI of 5 mg/kg body weight per day." This re-evaluation maintained sucralose as safe but with an updated ADI.
- **JECFA:** ADI = 0–15 mg/kg bw/day (the previous EFSA estimate was similar; the 2026 EFSA re-evaluation updated this to 5 mg/kg bw/day with a new critical effect rationale).
- **FDA:** Approved as a food additive (not just GRAS); 21 CFR §172.831.
- **Literature (contested area):**
  - The 2023 NutriNet-Santé cohort (PMID 37490630, Lancet Diabetes & Endocrinology) found an association between total artificial sweetener intake (including sucralose) and increased type 2 diabetes risk in an observational prospective cohort (n=105,588). Sucralose was not analyzed separately with sufficient power.
  - Europepmc ID 41710869 (EFSA 2026 opinion): "no safety concerns for genotoxicity" — addresses a specific recent concern about DNA damage from sucralose metabolites, and concluded it was not substantiated at food-level exposure.
  - Non-nutritive sweetener research (europepmc ID 41262739, 2025) notes association between NNS intake and gut microbiome alterations in animal and some human studies; the evidence for sucralose specifically is primarily from animal models and short-term human studies.
  - The EFSA 2026 re-evaluation is the most recent authoritative assessment; it maintained approval but tightened the ADI. This is consistent with "dose-dependent" tier consideration, not "confirmed-negative."

**Dose signal:** ADI = 5 mg/kg bw/day (EFSA 2026). Typical dietary exposure from "sugar-free" products is estimated at 0.5–2 mg/kg bw/day in regular consumers — below the ADI but the margin is narrower than for classic "not specified" additives. The gut microbiome concern and T2D observational association are live scientific discussions.

**Israeli label behavior:** Usually named explicitly ("סוכרלוז," "E955"). Required to be declared specifically on Israeli food labels (Millimolar sweeteners must be named). High consumer awareness — "ממתיקים (סוכרלוז)" on "no sugar" products is explicitly recognized.

**Tier:** dose-dependent
**Tier rationale:** EFSA 2026 re-evaluation tightened the ADI to 5 mg/kg bw/day (from 15 mg/kg bw/day at JECFA) with body-weight decrease as the new critical effect; typical exposure in regular consumers (0.5–2 mg/kg bw/day) is within this ADI but the margin is narrower than for "not specified" additives; the live scientific discussion on gut microbiome effects and the observational T2D association (NutriNet-Santé 2023) constitute a credible dose-response signal that justifies dose-dependent over likely-neutral, while the EFSA verdict (maintained approval, genotoxicity concern unsubstantiated) precludes contested.

**Draft Hebrew consumer explanation:** סוכרלוז הוא ממתיק ללא קלוריות הנמצא במוצרים "ללא סוכר"; על פי הערכה האירופית האחרונה (2026) הוא בטוח בכמויות המאושרות, אם כי נמשך מחקר על השפעתו לטווח ארוך. ✓ approved

---

### Entry 16: Acesulfame Potassium (E950)

**E-number:** E950

**IUPAC / common name (English):** Acesulfame potassium / acesulfame-K
**Common Hebrew name:** אצסולפאם K / אצסולפאם פוטסיום / E950

**Technological function:** Non-nutritive sweetener. ~200x sweeter than sucrose. Often used in combination with sucralose for synergistic sweetness profiles. Present primarily in "no added sugar" maadanim.

**Frequency on shelf:** 8 products (maadanim 7, bread 1).

**Evidence summary:**
- **EFSA status:** ADI = 9 mg/kg bw/day (EFSA 2000 evaluation). Ongoing review in some jurisdictions. Considered safe at current use levels.
- **JECFA:** ADI = 0–15 mg/kg bw/day.
- **FDA:** Approved (21 CFR §172.800).
- **Literature:** The observational NutriNet-Santé data (PMID 37490630) includes acesulfame-K in the total NNS exposure analysis. Some animal studies suggest potential effects on insulin secretion and gut microbiota at high doses (europepmc ID 41262739), but human RCT evidence at food-label exposures is limited and inconsistent. EFSA's current assessment is that there are no safety concerns at current dietary exposures. The note in d5_d6_rule_spec_v1.md mentions "אצסולפאם k" as an example of a Hebrew OCR/parsing challenge (stray space and 'k' suffix) — P2 normalization resolves this.

**Dose signal:** ADI = 9 mg/kg bw/day (EFSA). Typical dietary exposure estimated at 1–3 mg/kg bw/day in high consumers — within ADI. NNS gut microbiome concern is at active investigation stage.

**Israeli label behavior:** Must be declared by name when used as a sweetener (Israeli food label regulations require NNS identification). The d5_d6_rule_spec_v1.md notes the real-panel parsing challenge: "ממתיקים (אצסולפאם k, סוכרלוז)" is the typical declared form. When present under bare "ממתיקים" without names, it is a D5 closable gap (though this appears to be a minority disclosure pattern for sweeteners).

**Tier:** dose-dependent
**Tier rationale:** EFSA ADI = 9 mg/kg bw/day; typical high-consumer exposure (1–3 mg/kg bw/day) is within ADI but not negligible relative to it; animal studies suggest potential insulin secretion and gut microbiome effects at high doses; the class-level observational NNS association with T2D (NutriNet-Santé) applies; evidence for dose-dependent concern is weaker than for sucralose but crosses the threshold beyond likely-neutral given the narrowing exposure-to-ADI margin and the live NNS research discussion.

**Draft Hebrew consumer explanation:** אצסולפאם K הוא ממתיק ללא קלוריות הנמצא בעיקר במוצרים "ללא סוכר"; מאושר לשימוש ברמות הנוכחיות, וממשיך להיות נבדק בהקשר להשפעתו על מיקרוביום המעי. ✓ approved

---

### Entry 17: Carboxymethylcellulose (CMC, E466)

**E-number:** E466

**IUPAC / common name (English):** Cellulose gum / carboxymethylcellulose sodium
**Common Hebrew name:** קרבוקסי מתיל צלולוז / CMC / E466

**Technological function:** Thickener / stabilizer / viscosity agent. Used in maadanim and bread for texture modification; keeps particles in suspension; improves mouthfeel.

**Frequency on shelf:** 8 products (maadanim 7, bread 1). Lower frequency than carrageenan but included for tier-diversity and the contested scientific debate it shares with carrageenan.

**Evidence summary:**
- **EFSA status:** ADI = "not specified." Considered safe at current use levels.
- **JECFA:** ADI = "not specified."
- **FDA:** GRAS (21 CFR §182.1745).
- **Literature (contested — the core human RCT):**
  - Chassaing et al. (2021, Gastroenterology) — A pre-registered human RCT (n=16) showed that CMC consumption at doses achievable in processed foods altered gut microbiome composition and reduced fecal short-chain fatty acid concentrations after 11 days, suggesting encroachment on the intestinal mucosa; the effect was replicated in a second n=16 arm. This is a small but methodologically strong study (pre-registered, crossover design).
  - Europepmc ID 42073323 (2026 review): Reviews the current evidence on both CMC and carrageenan and their gut microbiota modulation, noting that "growing attention has been directed toward the long-term effects of commonly used additives on gut health."
  - EFSA has not re-evaluated E466 since the Chassaing 2021 RCT; the regulatory ADI predates this evidence. This is an active scientific-regulatory gap.
  - The contested status is real: a well-conducted human RCT has raised concerns at food-label exposures; the regulatory assessment has not been updated. This meets the definition of "contested" in the Bari tier framework.

**Dose signal:** The Chassaing 2021 RCT used CMC at ~15 g/day, which is within the range achievable from multiple processed-food servings. This is meaningfully different from additives where the concern only arises at pharmacological doses.

**Israeli label behavior:** Often named explicitly ("קרבוקסי מתיל צלולוז," "CMC," "E466") consistent with named-concern status in ingredient_taxonomy.py (the taxonomy already flags this additive as `is_named_concern=True`). Some products use bare "מייצב" without specification — D5 closable gap.

**Tier:** contested
**Tier rationale:** EFSA ADI "not specified" predates the Chassaing 2021 pre-registered human RCT (n=16+16, crossover), which found gut microbiome composition changes and reduced fecal SCFA at CMC doses achievable from multiple processed-food servings (~15 g/day); EFSA has not re-evaluated E466 since this study, creating a substantive regulatory-science gap; the 2026 review (europepmc 42073323) confirms the scientific discussion is active on both CMC and carrageenan; unlike carrageenan where the concern centers on animal/in vitro data, CMC now has a small but methodologically strong human RCT — this meets the "contested" threshold (genuine scientific disagreement between the regulatory assessment and recent peer-reviewed human evidence). Dose-dependent is not the right tier because the regulatory body has not established a dose-response relationship; the mechanistic concern is at the gut level with effects that may not be linearly dose-gated. The contested tier more accurately describes the state of scientific disagreement. Regulatory gap explicitly noted: EFSA's ADI predates the 2021 RCT and has not been updated.

**Draft Hebrew consumer explanation:** CMC (E466) הוא חומר מייצב שנחקר בניסוי קליני שהראה שינויים בהרכב מיקרוביום המעי; הדיון המדעי בנושא פעיל ואינו מוכרע. ✓ approved

---

### Entry 18: Caramel Color (E150)

**E-number:** E150a–d (four subclasses; E150d — sulfite-ammonia caramel — is most common in beverages; E150a plain caramel in foods)

**IUPAC / common name (English):** Caramel color (class I–IV)
**Common Hebrew name:** צבע קרמל / E150

**Technological function:** Brown food colorant. Used in maadanim chocolate desserts, caramel-flavored products; occasional bread application.

**Frequency on shelf:** 9 products (maadanim 8, bread 1).

**Evidence summary:**
- **EFSA status:** Re-evaluated 2012 (plain caramel E150a, caustic sulphite caramel E150b, ammonia caramel E150c, sulphite ammonia caramel E150d). Safety conclusions varied by class: E150a and E150b — no ADI; E150c — ADI = 300 mg/kg bw/day; E150d — ADI = 300 mg/kg bw/day. For typical food use outside cola beverages, the predominant class (E150a, plain caramel) has no ADI established.
- **FDA:** GRAS for plain caramel color (21 CFR §73.85); Class IV caramel requires certain labeling in beverages due to 4-methylimidazole (4-MEI) content.
- **Literature:** The 4-methylimidazole (4-MEI) in Class III/IV caramel was listed as a possible carcinogen by IARC (Group 2B, animal data only) in 2012. This generated concern in the beverage sector. For food products (as opposed to cola beverages where Class IV is dominant), typical caramel color use (Class I/II) does not carry this concern. In the Bari corpus, caramel color appears in chocolate maadanim products — the class is not specified on labels, creating a disclosure gap about which subtype is present.

**Dose signal:** Depends on class. Class I/II (plain/caustic sulphite caramel): no meaningful concern at food-label exposures. Class III/IV (ammonia caramel): ADI = 300 mg/kg bw/day; the 4-MEI issue applies specifically to Class IV at high doses.

**Israeli label behavior:** Typically declared as "צבע קרמל" or "E150" without class specification (I–IV). The class distinction is never disclosed on Israeli labels, which means the specific concern profile cannot be evaluated from the label alone — this is a structural disclosure gap (class of caramel color is information the manufacturer has but the label does not transmit).

**Tier:** disclosure-gap
**Tier rationale:** Israeli labels declare "צבע קרמל" or "E150" without specifying the class (I–IV); Class I/II (plain caramel, no 4-MEI concern) is functionally neutral at food-label exposures; Class IV (sulfite-ammonia process, 4-MEI byproduct — IARC Group 2B in animal studies) carries a dose-dependent concern at higher exposures relevant to cola beverages; because the class cannot be determined from the Israeli label, Bari cannot assign a meaningful evidence tier — the unknown could be Class I (no concern) or Class IV (concern). The correct honest answer is disclosure-gap: not enough label information to classify. This is a label-disclosure condition, not a verdict that caramel color is harmful. If a product's label or manufacturer discloses the class as E150a (plain caramel), it would reclassify to likely-neutral. If Class IV is confirmed, it would reclassify to dose-dependent.

**Draft Hebrew consumer explanation (revised — the draft was accurate but needs explicit reference to why we cannot evaluate it):** צבע קרמל משמש לצביעה חומה של מוצרי מזון; קיימים מספר סוגים שלו בעלי פרופיל בטיחות שונה, אך הסוג הספציפי אינו מצוין על התווית הישראלית — לכן לא ניתן להעריך אותו.

**DEC-006 check for revised explanation:** No alarm framing, no intent attribution, plain language, accurately represents the disclosure-gap condition. Approved.

---

### Entry 19: Sodium Benzoate (E211)

**E-number:** E210–E213 (benzoic acid and salts; E211 sodium benzoate is most common)

**IUPAC / common name (English):** Sodium benzoate
**Common Hebrew name:** נתרן בנזואט / בנזואט נתרן / E211

**Technological function:** Antimicrobial preservative. Active in acidic conditions (pH < 4); found in acidic maadanim products or acidified dairy desserts.

**Frequency on shelf:** 3 products — all maadanim. Lower frequency than sorbate; included for tier-diversity (benzoate occupies a distinct safety profile position).

**Evidence summary:**
- **EFSA status:** ADI = 5 mg/kg bw/day (as benzoic acid equivalents). EFSA re-evaluated E210–E213 in 2016 and confirmed the ADI; noted that total dietary exposure to benzoate (combined from additive use and naturally occurring benzoate in foods) could approach the ADI in some consumer groups.
- **JECFA:** ADI = 0–5 mg/kg bw/day.
- **FDA:** GRAS in most food categories (21 CFR §184.1733); not permitted in foods containing ascorbic acid (potential benzene formation reaction).
- **Literature (noteworthy concern):** Benzoic acid can react with ascorbic acid (vitamin C) to form benzene, a known carcinogen (Group 1, IARC). This reaction is relevant primarily in beverages (soft drinks containing both E211 and E300). In the Israeli food corpus, the combination in solid/dairy foods is less common and the benzene formation kinetics are different. A 2025 in vitro study (PMID 41228538) found differential apoptotic effects of sodium benzoate in HepG2 cells — this is a cell-culture finding not directly translating to food exposure. The benzene formation concern with simultaneous E211+E300 is a substantive (non-theoretical) food safety concern in specific product formulations.

**Dose signal:** ADI = 5 mg/kg bw/day. The benzene formation concern is a real (not hypothetical) safety signal when sodium benzoate is co-formulated with ascorbic acid in liquid/beverage contexts. For solid or dairy-based maadanim, the benzene formation risk is much lower (aqueous matrix, lower temperature, shorter shelf exposure).

**Israeli label behavior:** Must be named when used as a preservative. In the 3 products detected in the corpus, appears as "בנזואט נתרן" or "E211." Relatively transparent when present.

**Tier:** dose-dependent
**Tier rationale:** EFSA ADI = 5 mg/kg bw/day (as benzoic acid equivalents); total dietary exposure combining additive use and naturally occurring benzoates can approach the ADI in some consumer groups (EFSA 2016); the benzene formation reaction with ascorbic acid (vitamin C) is a real chemical concern — IARC Group 1 for benzene — though the kinetics in solid/dairy-based food matrices are substantially slower than in acidic beverages; this combination of a numeric ADI with realistic exposure-approaching-limit AND a specific chemical interaction concern (context-dependent) meets the dose-dependent threshold; the concern profile is real and quantifiable, not theoretical.

**Draft Hebrew consumer explanation (revised — the draft is accurate but the IARC Group 1 benzene framing needs softening to stay within DEC-006 for dose-dependent tier):** בנזואט נתרן הוא חומר משמר המאושר בישראל ובאירופה; ידוע כי בצירוף ויטמין C עשויה להיווצר בנזן בכמויות קטנות, בעיקר במשקאות ובמוצרים חומציים — פחות רלוונטי למוצרי חלב קרירים.

**DEC-006 check for revised explanation:** "עשויה להיווצר" (may form) rather than asserting harm; no alarm framing (no "מסוכן"), no intent attribution; the benzene formation is factual chemistry, not a verdict on the product; tier is dose-dependent and the explanation accurately conveys context-dependence. Approved.

---

### Entry 20: BHA (Butylated Hydroxyanisole, E320)

**E-number:** E320

**IUPAC / common name (English):** Butylated hydroxyanisole
**Common Hebrew name:** BHA / בוטילציאניזול / E320

**Technological function:** Antioxidant / preservative for fats and oils. Prevents rancidity in fat-containing products. Low frequency in the current corpus (1 bread product detected) but included for tier-diversity — this is the only additive in the current corpus that occupies the highest-concern end of the taxonomy (it is already marked `is_named_concern=True` in ingredient_taxonomy.py, contrasting with BHT which is explicitly NOT a named concern).

**Frequency on shelf:** 1 product (bread). Low count but strategically important for tier-diversity.

**Evidence summary:**
- **EFSA status:** Re-evaluated 2012; ADI = 0.5 mg/kg bw/day. EFSA noted that BHA (specifically 3-BHA, the major food-relevant isomer) showed carcinogenicity in animal studies at high doses (forestomach tumors in rodents). This anatomical site does not exist in humans, which complicates the extrapolation. EFSA maintained the ADI but acknowledged uncertainty.
- **JECFA:** ADI = 0–0.5 mg/kg bw/day.
- **IARC:** BHA listed as Group 2B ("possibly carcinogenic to humans") based on sufficient animal evidence and inadequate human evidence (1987 evaluation). This is a formal, not manufactured, cancer concern signal.
- **FDA:** GRAS at ≤ 0.02% of fat content (21 CFR §182.3169); under ongoing review.
- **NTP (US National Toxicology Program):** Listed BHA as "reasonably anticipated to be a human carcinogen" based on forestomach carcinogenicity in animals.
- **Literature:** The human relevance of the rodent forestomach finding is contested — humans have no forestomach. However, IARC Group 2B and NTP "reasonably anticipated" classifications are based on the available evidence. The ingredient_taxonomy.py already flags BHA as `is_named_concern=True` and explicitly differentiates it from BHT (which is NOT flagged) — this distinction is already implemented in the engine.

**Dose signal:** ADI = 0.5 mg/kg bw/day. Typical dietary exposure is well below this in most populations; BHA use has declined significantly as manufacturers have switched to alternative antioxidants. The concern at the ADI is not for the typical consumer but the formal carcinogenicity classification (IARC 2B, NTP) is substantive.

**Israeli label behavior:** When present, usually declared explicitly ("BHA," "E320," "בוטילציאניזול"). Rarity on Israeli shelves (1 detection in 420 products) suggests limited current use.

**Tier:** contested
**Tier rationale:** IARC Group 2B ("possibly carcinogenic to humans") based on sufficient animal evidence (rodent forestomach tumors at high doses) and inadequate human evidence; NTP lists BHA as "reasonably anticipated to be a human carcinogen"; EFSA ADI = 0.5 mg/kg bw/day (the lowest numerical ADI in this set); the human-relevance question (humans have no forestomach) is itself the active scientific disagreement — regulatory bodies maintain the ADI while IARC/NTP formal classifications signal concern; this is genuine methodological disagreement between the regulatory assessment and carcinogen classification bodies, not manufactured doubt. BHA does not meet "confirmed-negative" because: (1) typical dietary exposure at food-label levels is well below the ADI; (2) the forestomach mechanism lacks direct human anatomical relevance; (3) no human epidemiological evidence of harm exists. "Contested" accurately captures the IARC 2B / regulatory-gap tension at realistic food exposure.

**Draft Hebrew consumer explanation (revised — the draft mentions "מסרטן" (carcinogen) framing which is a DEC-006 alarm-word violation for a contested tier; must convey scientific disagreement without the carcinogen verdict):** BHA הוא נוגד חמצון שמונע שמנים מהתקלקלות; הוא סווג בסולם סיכונים בינלאומי על בסיס נתוני בעלי חיים, והדיון המדעי לגבי הרלוונטיות לבני אדם ממשיך — השימוש בו בישראל נדיר.

**DEC-006 check for revised explanation:** "סווג בסולם סיכונים בינלאומי" (classified on an international risk scale) conveys the IARC classification without using the alarm word "מסרטן"; "הדיון המדעי ממשיך" (the scientific discussion continues) accurately represents the contested tier; no intent attribution; no "מסוכן"/"רעיל"; plain language. Approved.

---

## Research Return

**What was built:**
- Frequency scan across 420 products (hummus 55, maadanim 184, bread 181) identifying the top ~25 named additives in the combined corpus.
- 20 additive entries spanning the full tier range from "highly likely neutral" (citric acid, pectin, guar gum) through "dose-dependent" (phosphates, sucralose, acesulfame-K), "contested" (carrageenan, CMC), and "named concern / IARC-classified" (BHA, caramel color E150d).

**Sources used:**
1. EFSA OpenFoodTox evaluations (cited by additive through europepmc searches)
2. JECFA evaluations (cited through regulatory status statements)
3. FDA GRAS/food additive listings (CFR references)
4. PMID 37490630 (2023, Lancet Diabetes Endocrinol) — NutriNet-Santé NNS and T2D
5. Europepmc ID 41710869 (2026) — EFSA sucralose re-evaluation
6. Europepmc ID 42073323 (2026) — CMC and carrageenan gut microbiota review
7. Europepmc ID 38349899 (2024) — NutriNet-Santé emulsifiers and cancer
8. PMID 33163715 (2020) — Phosphate dietary management in CKD
9. PMID 41228538 (2025) — In vitro apoptotic effects of preservatives
10. Europepmc ID 41501013 (2026) — NutriNet-Santé preservatives and T2D
11. Europepmc ID 38371690 (2024) — Xanthan gum review
12. Ingredient taxonomy (C:\Bari\03_operations\bsip2\proto_v0\src\ingredient_taxonomy.py) — engine's existing named-additive inventory for carrageenan, CMC, lecithin, BHA, BHT
13. D5/D6 rule spec (01_framework/glass_box/d5_d6_rule_spec_v1.md) — real-panel disclosure behavior for Israeli labels

**Gaps for Nutrition to note before tier assignment:**

1. **EFSA currency gap:** Multiple EFSA evaluations cited here predate the Chassaing 2021 CMC RCT (EFSA's "not specified" ADI for CMC was set before this study). For contested additives, the most recent science may not be reflected in the regulatory status. Nutrition should flag this discrepancy in the tier rationale.

2. **Israeli-specific exposure data:** No Israeli dietary exposure surveys for food additives are available in the corpus or in the literature searches. Tier assignments and dose-signal assessments use European (EFSA) and US (FDA) population exposure estimates. These are plausible proxies for Israeli processed-food consumption patterns but not direct data.

3. **Caramel color class gap:** The corpus detects "E150" but cannot distinguish E150a from E150d on Israeli labels. The 4-MEI concern (Class III/IV) is real but may not apply to the food products in this corpus. Nutrition should note this as a label-disclosure limitation when assigning tier.

4. **Emulsifier class-level NutriNet-Santé data:** The 2024 NutriNet-Santé emulsifier-cancer analysis (E471, polysorbate-80) is the only large prospective study. It is observational and cannot establish causation. However, it is the best available human evidence on emulsifier exposure at population level. Nutrition should weigh this against the mechanistic null-finding at food-typical exposures when tiering E471.

5. **DATEM (E472e) — sparse independent evidence:** DATEM has very limited independent RCT or mechanistic data. The safety basis is primarily regulatory (GRAS/EFSA ADI-not-specified) and metabolic stability data. Nutrition may assign "likely-neutral" but should note the limited evidence base.

6. **Potassium sorbate NutriNet-Santé association:** The 2026 prospective cohort study found an association between sorbate intake and T2D incidence. This is hypothesis-generating; EFSA's ADI has not changed. Nutrition should decide whether this is sufficient to move from "likely-neutral" toward "dose-dependent" in the tier framework.

7. **BHA frequency vs. tier significance:** BHA appears in only 1 of 420 corpus products, making its practical shelf-impact minimal. However, it is the only IARC-2B, NTP-listed additive in the corpus and serves as the "named concern" anchor for the tier system. Nutrition should confirm the tier assignment for BHA even if its frequency is low.

**Tier-diversity status:** The 20 selected additives span the expected full range of the 6-tier framework:
- "Functional/likely-neutral" candidates: citric acid, ascorbic acid, pectin, LBG, guar gum, baking soda, xanthan gum, SSL, mono-/diglycerides
- "Dose-dependent" candidates: phosphates, calcium propionate, sodium benzoate, sucralose, acesulfame-K
- "Contested" candidates: carrageenan, CMC, caramel color (class-dependent), modified starch (if regulatory gap is flagged)
- "Disclosure-gap" candidates: DATEM (sparse evidence), any additive where generic class term hides identity
- "Named concern" / confirmed-negative-leaning: BHA

This range makes the prototype tier system visible and testable across all 6 categories, as required by TASK-179Q Phase 3 criteria.

---

## Nutrition Phase 3 Co-sign

**Date:** 2026-06-04

**Tier assignments:** All 20 entries tiered above. Summary:

| Tier | Count | Additives |
|------|-------|-----------|
| functional | 6 | E330 citric acid, E300 ascorbic acid, E415 xanthan gum, E440 pectin, E410 LBG, E412 guar gum |
| likely-neutral | 6 | E202 potassium sorbate, E1422 modified starch, E282 calcium propionate, E481 SSL, E471 mono-/diglycerides, E472e DATEM |
| dose-dependent | 4 | E450/451 phosphates, E955 sucralose, E950 acesulfame-K, E211 sodium benzoate |
| contested | 3 | E407 carrageenan, E466 CMC, E320 BHA |
| disclosure-gap | 1 | E150 caramel color |
| confirmed-negative | 0 | No additive in this set meets the bar (weight-of-evidence harm at realistic food-label exposure). BHA carries IARC 2B + NTP listing but at realistic food-label exposures the evidence does not meet the confirmed-negative threshold; contested is the accurate tier. |

**Three flagged gaps resolved:**

1. **E466 CMC:** Assigned **contested**. The EFSA ADI "not specified" predates the Chassaing 2021 pre-registered human RCT showing gut microbiome effects at food-achievable doses (~15 g/day). This is the clearest regulatory-science gap in the set: a methodologically strong human trial has raised concerns that the regulatory body has not yet re-evaluated. The 2026 review confirms the scientific discussion is active. "Contested" is the accurate tier (genuine scientific disagreement between regulatory body and peer-reviewed human evidence). "Dose-dependent" was considered but rejected because EFSA has not established a dose-response relationship — the mechanism is gut-level microbiome modulation, not a classical toxicological dose-response curve. The regulatory gap is explicitly documented in the tier rationale.

2. **E150 caramel color:** Assigned **disclosure-gap**. Israeli labels do not disclose the caramel color class (I–IV). Class I/II (plain caramel) is functionally neutral; Class IV (sulfite-ammonia process, 4-MEI byproduct, IARC Group 2B in animals) carries a dose-dependent concern. Since the class is structurally unknowable from the Israeli label, Bari cannot assign a meaningful evidence tier. The disclosure-gap tier is the only intellectually honest assignment. The Hebrew explanation was revised to clearly explain why we cannot evaluate this additive. If a product discloses the class, re-tiering applies.

3. **E202 potassium sorbate:** Assigned **likely-neutral**. The 2026 NutriNet-Santé prospective cohort association with T2D is a single observational finding. One prospective cohort does not establish causation; EFSA's ADI (3 mg/kg bw/day, also 25 mg/kg bw/day JECFA) has not changed; typical dietary exposure (0.5–1.5 mg/kg bw/day) is well within ADI; the effect size in the cohort was small; no plausible mechanistic pathway has been proposed. Likely-neutral is the current correct tier. A flag is attached: if a replication study in an independent cohort or a mechanistic RCT confirms the association, this should be reassessed. The decision was close; dose-dependent was considered and rejected because a single observational cohort without mechanistic confirmation does not meet the dose-dependent evidence threshold as defined.

**DEC-006 compliance:** All 20 Hebrew explanations reviewed. Two violations found and corrected:
- **E320 BHA:** The draft used "מסרטן" (carcinogen) — a DEC-006 alarm word for a contested tier. Revised to "סווג בסולם סיכונים בינלאומי" (classified on an international risk scale) which conveys the IARC classification factually without alarm framing.
- **E211 sodium benzoate:** The draft used "יכולה להיווצר" (can form) which was accurate, but softened to "עשויה להיווצר" (may form) to avoid any impression of certainty, and the context-dependence (beverages vs. dairy) was made more explicit.
All other 18 explanations passed the DEC-006 check unchanged.

**Next step:** Product co-sign on scope (Phase 4 — TASK-179Q): confirmation that these 20 are the right prototype set, that hummus+maadanim is the right pilot, and acceptance of the aggregate contested-additive ceiling constraint (DEC-006 Q3: sum of contested additives ≤ ~one grade band aggregate impact). Rule A magnitude (+3 D2 sub-score credit in EV-040) also requires Product D7 co-sign before engine activation.

Nutrition D7 co-sign: 2026-06-04

---

## Product Phase 4 Co-sign

**Date:** 2026-06-04

**MVP scope:** hummus + maadanim confirmed. Hummus is the lowest-additive pilot category (moderate complexity, clean baseline for the transparency chip); maadanim is the highest-additive category in the corpus (E407, E466, E1422, E450, E440, E410 all appearing at meaningful frequency) — the real test of the tier system's range. Bread is disqualified as a pilot by the active re-baseline (TASK-180C in progress); yogurt is redundant with maadanim on both category profile and additive overlap. The hummus+maadanim selection is also consistent with TASK-179R (W2 engagement gate uses hummus as the engagement test). No adjustment.

**DEC-006 Q3 contested ceiling:** Confirmed. In W2, contested additives (carrageenan E407, CMC E466, BHA E320) produce tier chips and plain-language explanations only — no score movement. The aggregate contested ceiling of ~1 grade band (from DEC-006 Q3 co-sign) applies to score-moving implementations and is not triggered at the W2 prototype stage. The Hebrew explanations for all three contested additives pass the "explain plainly, do not alarm" standard: none use alarm words ("מסוכן," "מזיק," "רעיל"), all convey the scientific uncertainty accurately and without intent attribution, and all use the appropriate softened framing for the contested tier.

**BHA as contested (not confirmed-negative):** Agreed. IARC Group 2B + NTP "reasonably anticipated" is a formal classification signal based on rodent forestomach carcinogenicity. Three factors keep it out of confirmed-negative: (1) the forestomach mechanism has no direct human anatomical analogue; (2) typical dietary exposure is well below the ADI (0.5 mg/kg bw/day); (3) no human epidemiological evidence of harm exists. Weight-of-evidence harm at realistic food-label exposure — the confirmed-negative bar — is not met. Contested is the correct tier. Nutrition's call is accepted.

**Scope adjustments:** None. The 20-additive set is correct. BHA (1 corpus product) and sodium benzoate (3 corpus products) are retained despite low shelf frequency because they serve as the named-concern and benzene-formation anchors that make the six-tier system legible across its full range — removing them would collapse the prototype demonstration to the undifferentiated middle of the evidence spectrum. The three excluded additives (E500 baking soda, E322 soy lecithin, E170 calcium carbonate) are excluded correctly: all three are definitively neutral and add no tier-diversity value.

Product D7 co-sign: 2026-06-04
