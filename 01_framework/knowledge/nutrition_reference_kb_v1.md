# Nutrition Reference KB v1

**Classification:** Internal — Nutrition Knowledge (reference layer, NOT scoring)
**Version:** 1.0
**Established:** 2026-06-15
**Owner:** Nutrition Agent
**Status:** Forward-looking reference layer for planned whole-food / combination / expanded
consumer-product categories (owner directive, 2026-06-15).

---

## Charter

This file is a **Bari-owned, provenance-stamped general-nutrition reference**. It is a
**different artifact** from the scoring Evidence Registry
(`03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`).

**What it is for:** accumulating foundational nutrition knowledge ahead of future categories
where it becomes relevant — **fruits, vegetables, whole foods, and food combinations** — and as
a single, citable source of truth for future consumer copy. Owner established this layer
2026-06-15 on the reasoning that Bari will grow beyond packaged foods, and a curated/auditable
KB is worth more than relying on model-internal knowledge.

**Inclusion bar (intentionally relaxed vs. the scoring registry).** For *this* layer we keep an
entry even when a strong nutrition model already knows the fact, **provided** it is foundational
reference for a planned future category. Provenance + a single source of truth are the point.
This deliberately reverses the "drop if the model already knows it" bar — which still governs the
scoring Evidence Registry. We do **not** keep trivia with no plausible future-category use.

**Firewall (unchanged).** Nothing in this file moves a published score. Reference knowledge that
later wants to inform scoring must be **promoted** to an `EV-###` entry in the scoring Evidence
Registry with a primary `source_doi` and **D7 co-sign (Nutrition Agent + Product Agent)**. A
popular-science book flags a finding; it never proves one. (See `off_ban_hard_rule`,
`citations_discipline`.)

---

## Entry schema

| Field | Meaning |
|---|---|
| `id` | `KB-###` |
| `topic` | what it covers |
| `summary` | the reference content |
| `source` | book / author / page (provenance) |
| `source_tier` | `popular_science_secondary` etc. — a popularizer is a pointer, not primary evidence |
| `applies_to_future_categories` | which planned categories this seeds |
| `scoring_relevance` | `none` (reference only) · `future-candidate` (could seed an EV-### later) |
| `consumer_copy_usable` | whether Content Agent may draw on it (still subject to editorial standards) |
| `notes` | caveats, promotion notes |

---

## KB-001 — Dietary minerals: roles + whole-food sources

| Field | Value |
|---|---|
| **id** | KB-001 |
| **topic** | Essential dietary minerals — macro vs. trace, physiological role, and food sources |
| **source** | *The Science of Nutrition: Debunk the Diet Myths and Learn How to Eat Well for Health and Happiness*, Rhiannon Lambert (DK, 2021) — "What Are Minerals?" spread |
| **source_tier** | `popular_science_secondary` — consensus-level textbook content; reliable as reference, not citable as primary evidence |
| **applies_to_future_categories** | fruits, vegetables, whole_foods, food_combinations |
| **scoring_relevance** | none — Bari scores nutritional *architecture* (processing, additives, sugar, sodium, fat quality, fiber), not micronutrient completeness. Minerals are handled *implicitly* via whole-food / matrix-integrity logic. No signal here today. |
| **consumer_copy_usable** | yes — food-source lists are the reusable part for future whole-food category copy (still subject to editorial standards: insight-first, no encyclopedia register) |

**Definition.** Unlike vitamins (organic compounds made by plants/animals), minerals are
**inorganic chemical elements** from soil, rock, or water — absorbed by plants as they grow and
passed up to the animals that eat them. **Macrominerals** (needed in larger amounts): calcium,
chloride, magnesium, phosphorus, potassium, sodium. **Trace minerals** (needed in small amounts):
iodine, iron, selenium, zinc, manganese.

| Mineral | Role (reference) | Whole-food sources |
|---|---|---|
| **Calcium** | Bone & teeth; nervous system, muscle, heart function | milk, yogurt, spinach |
| **Iodine** | Thyroid function & thyroid-hormone production (growth, brain development, bone maintenance, metabolic rate). *Deficiency affects ~⅓ of world population.* | fish, dairy, eggs, seaweed |
| **Iron** | Oxygen-carrying capacity of blood; immune & brain function. *Most common nutritional deficiency worldwide; the only one prevalent in developed countries — >30% have anaemia.* | shellfish, broccoli, red meat, tofu |
| **Magnesium** | Role in 600+ cellular processes — energy production, nervous system, muscle contraction | avocados, nuts, leafy greens |
| **Manganese** | Makes/activates enzymes for chemical reactions (e.g. breaking down food) | bread, nuts, breakfast cereals, green veg |
| **Potassium** | Blood-pressure control, fluid balance, muscle & nerve function | bananas, spinach, potatoes, apricots |
| **Phosphorus** | Strong bones; releasing energy from food | red meat, dairy, fish, poultry, oats, bread |
| **Selenium** | Immune function; protects cells/tissues from damage; reproductive health | Brazil nuts, eggs, meat, fish |
| **Zinc** | Immune system, hormone production, fertility; reduces skin inflammation, wound healing, UV protection | shellfish, red meat, eggs, chickpeas |

**Notes.** Two epidemiological claims worth a primary citation **if** ever promoted toward
scoring/copy authority: iodine deficiency ≈ ⅓ global population; iron deficiency = most common
nutritional deficiency. Sodium/potassium → blood pressure overlaps Bari's existing sodium logic,
but adds nothing to it today. Promotion path to any score move = `EV-###` + D7.

---

## KB-002 — Dried fruit: minerals AND sugars concentrate together

| Field | Value |
|---|---|
| **id** | KB-002 |
| **topic** | Dried fruit as a concentrated source of *both* minerals and fruit sugars (the concentration double-edge) |
| **source** | *The Science of Nutrition*, Rhiannon Lambert (DK, 2021) — dried-fruit spread (goji berries, dates, mango, raisins, figs) |
| **source_tier** | `popular_science_secondary` |
| **applies_to_future_categories** | fruits, dried_fruit, whole_foods, snacks_adjacent |
| **scoring_relevance** | **future-candidate** — when Bari scores a fruit / dried-fruit category, the same drying step that concentrates minerals *also* concentrates sugar (and energy density). A naïve engine could reward mineral density while ignoring sugar density, or penalise sugar while missing the mineral concentration. Flag both, weigh deliberately. NOT a rule today; promotion = `EV-###` + D7. |
| **consumer_copy_usable** | yes — "more minerals, but also more sugar — easy to over-consume" is a clean Bari-style honest-tradeoff line for a future dried-fruit page (subject to no-health-claims: state the architecture, don't advise intake). |

**Reference.** Drying removes water, concentrating everything per gram — minerals *and* intrinsic
fruit sugars (and calories). The book's framing: a more concentrated mineral source than the fresh
equivalent, *"but also of fruit sugars so take care not to over-consume."* Per-fruit reference
labels from the spread: **goji berries** — iron (oxygen transport to tissues); **mango** — calcium
(bones/teeth), iron (immunity), potassium (nerve function).

**Why this is the one keeper in its batch.** It is the only fact in the dried-fruit / supplements /
hydration / digestion set that is *non-obvious as architecture* and *not already modelled*: it names
a concentration tradeoff that directly anticipates a future-category scoring decision. (Contrast:
supplement UL/toxicity is already encoded in the SIE EFSA-TUL ceiling; colonic SCFA absorption is
already encoded in the fiber-fermentability tier EV-006/EV-060; hydration/dehydration is health
advice Bari does not give.)

---

## KB-003 — In-vitro digestion bioavailability (INFOGEST / Caco-2) and the phytate "nutrient trap"

| Field | Value |
|---|---|
| **id** | KB-003 |
| **topic** | Bioaccessibility vs. theoretical nutrient content: INFOGEST static digestion model + Caco-2 intestinal absorption model as predictors of actual mineral and carotenoid uptake; phytic acid as a chelating antinutrient in high-phytate plant matrices |
| **source** | (1) INFOGEST static in-vitro digestion protocol — Minekus et al. (2014), *Food & Function* 5(6):1113–1124 (DOI: 10.1039/c3fo60702j) — the internationally harmonized static digestion model standardizing oral/gastric/intestinal phases for bioaccessibility research. (2) Caco-2 cell monolayer uptake assay — well-established in-vitro intestinal absorption proxy; widely used in food bioavailability literature (no single founding DOI; methodology routinely paired with INFOGEST). (3) Brazilian tropical fruits — carotenoid and anthocyanin bioaccessibility in exotic fruits studied via INFOGEST + Caco-2: *directional, specific study DOI pending confirmation* (TASK-285 research dump cited a Brazilian-fruits bioaccessibility study; DOI not confirmed at time of KB entry — do not cite as primary evidence until verified). (4) Phytic acid (inositol hexaphosphate, IP6) as a mineral chelator: Gupta et al. (2015), *Food Chemistry* 173:814–821 (DOI: 10.1016/j.foodchem.2014.10.069) — reviews phytate reduction strategies and mineral bioavailability impact. |
| **source_tier** | `primary_peer_reviewed` for the INFOGEST protocol DOI and phytate review. `directional_source_pending` for the specific Brazilian-fruits Caco-2 study (DOI unconfirmed). |
| **applies_to_future_categories** | whole_foods, legumes, fruits, vegetables, cereals, food_combinations |
| **scoring_relevance** | **future-candidate** — when Bari scores whole-food / legume / fruit categories, nominal nutrient content from the product label is a ceiling, not a guarantee. Bioavailability is not label-observable (no bioaccessibility % appears on any Israeli product label), and Caco-2 / INFOGEST data are not parseable from BSIP0. **Firewall fully applies: this entry does NOT move any published score and is NOT label-parseable; promotion to scoring action requires EV-### + D7 co-sign.** |
| **consumer_copy_usable** | yes — "high iron on the label doesn't mean all of it reaches the bloodstream" is a Bari-style honest-architecture observation for future legume/whole-grain copy, provided the source-DOI is confirmed before any consumer claim ships. Do not cite the Brazilian-fruits study specifically until the DOI is verified. |

**Core concept.** A food matrix's declared nutrient content (e.g., iron 4 mg/100g on the label) is the
total chemical quantity — not what the gut actually absorbs. The gap between declared and absorbed has
two layers:

- **Bioaccessibility** (release from the matrix during digestion) — measured by INFOGEST static
  digestion, which simulates oral, gastric, and small-intestinal phases to quantify how much of a
  nutrient is released into solution and thus *available* for absorption. This is the most
  standardized in-vitro proxy today.
- **Bioavailability / intestinal uptake** (transport across the epithelium) — measured by Caco-2 cell
  monolayer assays, which add an intestinal transport step on top of bioaccessibility, giving a more
  physiologically grounded estimate of actual cellular uptake.

**Phytate as the principal antinutrient in plant-based high-iron matrices.** Phytic acid (IP6) —
prevalent in legumes, whole grains, seeds, and some cereals — chelates divalent minerals (Fe²⁺,
Zn²⁺, Ca²⁺, Mg²⁺) in the gut lumen, reducing their bioaccessibility substantially. A high-iron
legume with high phytate load can deliver a fraction of its labeled iron as absorbable mineral. The
exact reduction is matrix-specific (moisture, pH, food combination, fermentation, cooking method all
modulate IP6 degradation by endogenous phytase activity).

**Carotenoid and anthocyanin case (Brazilian fruits, directional).** The research dump flagged a
Brazilian-tropical-fruits study applying INFOGEST + Caco-2 to carotenoid and anthocyanin
bioaccessibility. Finding: exotic fruit matrices showed variable but meaningfully lower bioaccessibility
of carotenoids and anthocyanins than their total-extract content suggests — processing, cell-wall
integrity, and lipid co-presence all modulate uptake. This is consistent with the general principle but
the specific DOI is unconfirmed; treat as directional until verified.

**Partial existing engine proxy (gap disclosure).** EV-009 provides a whole-grain structural credit
(intrinsic fiber / intact grain matrix) that implicitly rewards food-matrix integrity — the same
matrix that tends to modulate mineral bioaccessibility. EV-007 distinguishes intrinsic vs. isolated
fiber on mechanistic grounds, which overlaps with the matrix-integrity concept. KB-003 does NOT imply
these are absent; it frames the *bioavailability gap* (nutrient in vs. nutrient absorbed) as a
distinct future-scoring dimension not currently captured by any live EV, because it requires
bioaccessibility inputs that are not label-observable today.

**Firewall.** Nothing in this entry modifies scoring logic, activates a signal, or moves any published
score. Promotion path: confirm Brazilian-fruits DOI → `EV-###` proposal → D7 co-sign (Nutrition Agent
+ Product Agent). The phytate chelation principle itself could seed a future legume/whole-grain
bioaccessibility signal if label-parseable proxy inputs become available (e.g., declared phytate
content, if Israeli labels adopt it).

---

## KB-004 — DIAAS protein-quality classification (FAO bands) and the bioavailability gap

| Field | Value |
|---|---|
| **id** | KB-004 |
| **topic** | Protein quality measured by digestible indispensable amino acid score (DIAAS) rather than crude protein grams: the FAO classification bands, why DIAAS supersedes PDCAAS, and why none of it is per-SKU label-derivable |
| **source** | FAO Expert Consultation on protein quality evaluation (FAO Food and Nutrition Paper 92, 2013) establishing DIAAS using true ileal digestibility; method validation in the growing-pig model and meta-analyses (e.g. *British Journal of Nutrition* DIAAS-vs-PDCAAS comparisons). Owner research dump 2026-06-17 cited the now-established FAO bands. **Specific recent-meta-analysis DOIs pending Research Agent confirmation before any consumer citation.** |
| **source_tier** | `primary_peer_reviewed` for the FAO method; `directional_source_pending` for the specific 2026 meta-analyses cited in the research dump (DOIs unconfirmed) |
| **applies_to_future_categories** | whole_foods, legumes, dairy_protein, plant_protein, protein_bars, food_combinations |
| **scoring_relevance** | **future-candidate** — DIAAS is the correct frame for protein *quality* vs. quantity, but **a per-product DIAAS is NOT label-derivable**: it requires true ileal amino-acid digestibility data that appears on no Israeli label and is not parseable from BSIP0. The most any future engine could do is a coarse **directional proxy** (e.g. animal/dairy ≈ high; fermented/sprouted plant > cooked > raw legume; heat-treated legume > raw) — and doing even that on a live category would **re-rank published protein scores → frozen-invariant tripwire → owner-gated.** Reference frame only today. |
| **consumer_copy_usable** | yes — "more grams of protein doesn't mean more usable protein — quality depends on how digestible the amino acids are" is a clean Bari-style honest-architecture line for a future protein category, **provided** no specific numeric DIAAS or unverified study is cited (no-health-claims: describe architecture, don't prescribe intake). |

**FAO classification bands (reference).** DIAAS <75 → no quality claim permitted; 75–99 → "high quality"; ≥100 → "excellent quality." DIAAS is computed from the **true ileal digestibility of each indispensable amino acid** (measured at the end of the small intestine), scored against the limiting amino acid — unlike legacy PDCAAS, which used faecal digestibility, truncated scores at 1.0, and thereby overstated some lower-quality plant proteins.

**Why it matters as a future frame.** Two products with identical declared protein grams can differ materially in usable protein: a high-protein ultra-processed item with poor amino-acid digestibility vs. a fermented/sprouted whole food whose processing *raises* DIAAS (antinutrient reduction). This is the protein analogue of KB-003's bioaccessibility gap — declared content is a ceiling, not a guarantee.

**Antinutrient interaction (links KB-003).** Phytates and trypsin inhibitors depress plant-protein ileal digestibility; cooking, sprouting, and fermentation degrade them and raise effective DIAAS. So the same matrix that modulates *mineral* bioaccessibility (KB-003) also modulates *protein* quality — a single "processing-modulates-bioavailability" theme spanning both entries.

**Firewall.** Nothing here moves a published score, activates a signal, or re-ranks any live protein category. DIAAS inputs are not label-observable. Promotion path: a label-derivable proxy + `EV-###` + D7 co-sign (Nutrition + Product), and — because it would move *published* scores — owner sign-off under the frozen-invariant tripwire.

---

## KB-005 — UPF food-matrix structural collapse and neo-formed contaminants

| Field | Value |
|---|---|
| **id** | KB-005 |
| **topic** | Ultra-processing harm that is independent of nutrient composition: physical disruption of the food matrix (gastric-transit / satiety effects) and neo-formed process contaminants (acrylamide, lipid-oxidation products) — and the sharp line between what of this is label-derivable and what is not |
| **source** | 2026 peer-reviewed UPF-matrix literature (Imperial College conference data; Monash / São Paulo cohorts, n≈2,100) per owner research dump 2026-06-17. **Specific DOIs pending Research Agent confirmation.** Acrylamide/Maillard and lipid-oxidation chemistry are textbook-consensus food science. |
| **source_tier** | `directional_source_pending` for the 2026 UPF-matrix cohort claims (DOIs unconfirmed); `primary_peer_reviewed` consensus for the neo-contaminant chemistry |
| **applies_to_future_categories** | whole_foods, snacks_adjacent, cereals, bakery, fried_categories, food_combinations |
| **scoring_relevance** | **partly already modelled, partly not implementable.** Matrix-integrity logic, the hyper-palatability detector, and the NOVA/Siga processing proxy (EV-001) already capture much of the *structural* dimension from labels. **Neo-formed contaminants (acrylamide, lipid-oxidation products) are NOT label-derivable** — no Israeli label declares them and they cannot be inferred reliably from ingredient text or a process claim — so that layer is reference-only and cannot move a score. |
| **consumer_copy_usable** | yes, carefully — "processing changes more than the numbers on the panel — it changes the food's structure and how the body handles it" is defensible Bari-style architecture framing for future whole-food vs. UPF copy. Do **not** assert a specific contaminant is present in a specific product (not label-knowable) and do **not** make a health-outcome claim (Hard Rule #5). |

**Two distinct harm layers (reference).**
- **Matrix disruption** — milling, extraction, extrusion, and reconstitution destroy intact cell walls and fibre networks that normally slow gastric transit and blunt the glycaemic/insulin response. Two foods of identical macros can therefore have opposite metabolic kinetics. *This is largely already in the engine* via matrix-integrity + processing proxies; KB-005 does not imply it is absent.
- **Neo-formed contaminants** — high-heat / high-pressure processing generates compounds not present in the raw ingredients: acrylamide (Maillard, in high-temperature starch browning), advanced glycation end-products, and lipid-oxidation products in repeatedly heated/extracted oils. **Not label-observable; reference only.**

**Honest limit / why this is reference, not a new EV.** The structural half is already scored; the contaminant half fails the project-wide eligibility bar (*"only signals observable or inferrable from packaged food labels"* — Evidence Registry core constraint). Adding a "likely-acrylamide" penalty would require inventing a process inference the label does not support — exactly the fabrication the OFF ban and the missing-data-discard rule forbid. If a future category ever carries a declared or independently measured contaminant value, that becomes an `EV-###` candidate; until then it stays here.

**Firewall.** Nothing here moves a published score or activates a signal. Promotion path for any label-derivable sliver: `EV-###` + D7 co-sign (Nutrition + Product).

---

## KB-006 — Iodine fortification (iodized salt): a positive signal Bari does not model, and its collision with the sodium penalty

| Field | Value |
|---|---|
| **id** | KB-006 |
| **topic** | Iodine adequacy as a public-health concern in Israel, the iodized-salt fortification flag as the *only* label-observable proxy (dose is never on-label), and the structural tension between rewarding iodine fortification and Bari's sodium penalty |
| **source** | Ynet Wellness consumer-health article (2026), expert commentary by Mor Meinhardt, director of the nutrition department, Assuta Ashdod Hospital — `https://www.ynet.co.il/wellness/article/skhbnlkmzg`. Underlying epidemiology (global iodine deficiency ≈ ⅓ of population; mild-deficiency thyroid effects) is consensus public-health knowledge; **no µg intake thresholds were given in the article**, and the specific Israeli-prevalence figure was not quantified. |
| **source_tier** | `popular_science_secondary` — a popular-press health piece with named expert commentary; a pointer to consensus epidemiology, not primary evidence. Any quantified IL-prevalence claim needs a primary citation (Research Agent) before it informs copy. |
| **applies_to_future_categories** | salt_seasonings, dairy, eggs, fish_seafood, whole_foods |
| **scoring_relevance** | **none today, and not a clean future-candidate.** Iodine *dose* (µg) is never on an Israeli label, so the scorable value is unscrapable (fails the label-derivability bar; same firewall as KB-003/KB-004 bioavailability). The *one* detectable signal is the binary ingredient flag "מלח מועשר ביוד" / iodized salt — a **positive fortification** signal. Bari does not reward fortification anywhere, and adding a fortification credit would be a **scoring-philosophy change → frozen-invariant tripwire → owner-gated.** It would also **collide with the sodium penalty**: the article itself decouples the benefit from sodium ("switch to iodized salt *without* raising total sodium"), so there is no clean way to express "good iodine" without fighting Bari's existing sodium logic. The only category where the flag could ever be a genuine, defensible differentiator is a future **salt / seasonings** category (iodized vs. plain). |
| **consumer_copy_usable** | reference only — usable as context if a salt category launches ("iodized salt delivers iodine most Israelis under-consume, at the same sodium as plain salt"), but **subject to Hard Rule #5 (no health claims)** — describe the fortification fact, never advise intake for thyroid/pregnancy outcomes. Not relevant to any live category (protein-bars / snacks / granola do not touch iodine). |

**Core point this entry adds beyond [[KB-001]].** KB-001 already lists iodine's role (thyroid) and whole-food sources (fish, dairy, eggs, seaweed) as a reference row. KB-006 records the *non-obvious, engine-relevant* layer: (1) iodine is a fortification signal, a category Bari's architecture has no slot for; (2) its only label proxy is a binary iodized-salt ingredient flag, never a dose; and (3) it structurally conflicts with the sodium penalty — making it a poor scoring candidate even setting the tripwire aside. This is logged so the knowledge isn't lost before a salt/seasonings category exists, not because it is actionable now.

**Israeli relevance.** The article's framing — most Israelis are unaware of iodine's importance and many under-consume it (at-risk: vegans/vegetarians, women of childbearing age, pregnant/breastfeeding) — is the kind of local public-health context that would matter *if and only if* Bari ever scores salt, dairy, or eggs. Until then it is directional context, not a finding.

**Firewall.** Nothing here moves a published score or activates a signal. Promotion path, should a salt/seasonings category ever make the iodized-salt flag a deliberate differentiator: `EV-###` proposal → D7 co-sign (Nutrition + Product) → and, because rewarding fortification changes scoring philosophy, **owner sign-off under the frozen-invariant tripwire.**
