---
document: additive_library_expanded_v1
task: TASK-181A
program: TASK-181 (Glass Box program-of-record) — Wave 3, D4 additive library
phase: Research deliverable — Nutrition tiering (181B) pending
status: RETURNED (proposed; CC close-readiness gate to verify)
created_at: 2026-06-04
owner: research-agent
---

# Additive Library — Expanded v1 (Glass Box W3, D4)

**Purpose.** Expand the W2 24-row prototype additive library
(`additive_prototype_set_v1.md`, TASK-179Q) to the **full set of additives that actually
appear on the displayed Israeli shelves** (the live comparison JSONs), with curated
regulatory evidence per additive. This sheet is the evidence input for Nutrition's tiering
in TASK-181B and Data's wiring in TASK-181D.

**What this document IS:** identity + technological function + EFSA/JECFA/FDA evaluation
references + ADI (where an authority set one) + a one-line factual evidence-state note +
source citation, per additive.

**What this document is NOT:** it assigns **no evidence tiers** (the 6-tier
Strong/Moderate/Weak/Insufficient/Contested-style classification, and the Bari D4
functional/likely-neutral/dose-dependent/contested/disclosure-gap labels, are
**Nutrition's call in 181B**). It moves **no score**, edits **no JSON**, and touches **no
engine code**. Annotate-only research artifact.

**Hard rule honored (CLAUDE.md):** every datum cites a source. Where an evaluation could
not be located it is marked **`EVIDENCE GAP`** and never fabricated.

---

## 1. Coverage report

### 1.1 Scope correction vs the prototype — read this first

The W2 prototype scanned the **full BSIP0 raw corpora** (hummus 55 + maadanim 184 + bread
181 = **420 products**). This W3 task is scoped (per TASK-181A inputs) to the **displayed
comparison corpora** — the JSONs the consumer actually sees:

| Corpus (displayed JSON) | Products | With ingredient text |
|---|---|---|
| `hummus_frontend_v4.json` ("חומוס וממרחים" — incl. matbucha 10, pepper-spread 5, eggplant-spread 7, masabacha 2) | 64 | 62 |
| `maadanim_frontend_v2.json` | 84 | 84 |
| `bread_frontend_v2.json` | 24 | **9** |
| **Total displayed** | **172** | **155** |

**Material finding (flagged for Product/Data):** the displayed `bread_frontend_v2.json`
carries ingredient text for **only 9 of 24** products, and those 9 are all *clean
artisan/sourdough/cracker* breads (flour · sourdough · seeds — `scope_note`: "ניתוח מדף
שופרסל בלבד — לא סקר שוק ישראלי"). **Zero additives are declared in the displayed bread
set.** Consequently the prototype's bread-driven additives — **E282 calcium propionate
(81 raw breads), E481 SSL (63), E472e DATEM (37), E300 ascorbic-acid-as-dough-improver
(106)** — do **not** appear on the *displayed* bread shelf. They are retained in this
library (carried forward from the prototype, sourced) because (a) they are real on the
broader Israeli bread shelf and will return the moment a fuller bread JSON is displayed,
and (b) Data wires the detector once, not per-render. But their **displayed-shelf frequency
is currently 0** and that is recorded honestly in the frequency table.

### 1.2 Prototype carried-forward vs newly added

- **Prototype entries carried forward:** 20 prototype entries (covering 24 E-numbers via
  grouped families — sorbates E200–203, phosphates E450–452, modified-starch E1422/1442,
  caramel E150a–d, benzoates E210–213). All carried forward unchanged in their sourced
  regulatory data.
- **Newly added (observed on the displayed shelf, absent from the prototype 20):
  **16 additives** —
  E160a beta-carotene, E163 anthocyanins, E162 beetroot red, E100 curcumin, E141 copper
  chlorophylls, E333 calcium citrate, E331 sodium citrate, E327 calcium lactate, E296
  malic acid, E270 lactic acid, E401 sodium alginate, E516 calcium sulphate, E500 sodium
  carbonate (as acidity regulator / raising agent), E575 glucono-delta-lactone (GDL),
  E960 steviol glycosides, and the **E1412/E1414 modified-starch variants** (siblings of
  the prototype's E1422/E1442).
- **Total additives in this expanded library: 36** (20 carried + 16 new), spanning **40+
  E-numbers** when grouped families are expanded.

> Note on "newly added": all 16 resolve cleanly in the live OFF additives-taxonomy client
> (`integrations/clients/food_additives.py`) for identity + function class + EFSA-eval
> pointer. They were simply below the prototype's selection cut (count ≥ 8 across ≥ 2
> categories), not absent from the regulatory record.

### 1.3 Per-corpus additive frequency (DISPLAYED shelf — this task's scan)

Counts = number of products in that displayed corpus whose ingredient text declares the
additive (named Hebrew term **or** E-number). Generic-class-only terms ("מייצב",
"חומר משמר" with no named substance) are tracked separately in §1.4 as disclosure gaps,
**not** counted as a specific additive.

| Additive | Hummus (n=62) | Maadanim (n=84) | Bread (n=9) | Displayed total | Categories |
|---|---|---|---|---|---|
| E200–203 sorbates | 54 | 6 | 0 | 60 | 2 |
| E1422/1442/1412/1414 modified starch | 2 | 48 | 0 | 50 | 2 |
| E330 citric acid (+ E331/E333 citrate salts) | 40 | 7 | 0 | 47 | 2 |
| E500 sodium carbonate / baking soda | 36 | 1 | 0 | 37 | 2 |
| E407 carrageenan | 0 | 34 | 0 | 34 | 1 |
| E415 xanthan gum | 13 | 13 | 0 | 26 | 2 |
| E412 guar gum | 7 | 15 | 0 | 22 | 2 |
| E410 locust bean gum | 0 | 18 | 0 | 18 | 1 |
| E440 pectin | 0 | 14 | 0 | 14 | 1 |
| E160a beta-carotene (colour) | 0 | 10 | 0 | 10 | 1 |
| E450–452 / E339 / E341 phosphates | 0 | 10 | 0 | 10 | 1 |
| E333 calcium citrate (tricalcium) | 0 | 5 | 0 | 5 | 1 |
| E322 lecithin | 0 | 5 | 0 | 5 | 1 |
| E471 mono-/diglycerides | 0 | 4 | 0 | 4 | 1 |
| E955 sucralose | 0 | 4 | 0 | 4 | 1 |
| E331 sodium citrate | 0 | 3 | 0 | 3 | 1 |
| E163 anthocyanins (colour) | 0 | 3 | 0 | 3 | 1 |
| E327 calcium lactate | 0 | 3 | 0 | 3 | 1 |
| E950 acesulfame-K | 0 | 3 | 0 | 3 | 1 |
| E960 steviol glycosides | 0 | 2 | 0 | 2 | 1 |
| E162 beetroot red (colour) | 0 | 1 | 0 | 1 | 1 |
| E100 curcumin (colour) | 0 | 1 | 0 | 1 | 1 |
| E141 copper chlorophylls (colour) | 0 | 1 | 0 | 1 | 1 |
| E401 sodium alginate | 0 | 1 | 0 | 1 | 1 |
| E516 calcium sulphate | 0 | 1 | 0 | 1 | 1 |
| E296 malic acid | 0 | 1 | 0 | 1 | 1 |
| E270 lactic acid | 1 | 0 | 0 | 1 | 1 |
| E282 calcium propionate (bread preservative) | 0 | 0 | 0 | **0** | 0 |
| E481 SSL (bread dough conditioner) | 0 | 0 | 0 | **0** | 0 |
| E472e DATEM (bread dough conditioner) | 0 | 0 | 0 | **0** | 0 |
| E300 ascorbic acid (dough improver) | 0 | 0 | 0 | **0** | 0 |
| E466 CMC | 0 | 0 | 0 | **0** | 0 |
| E211 sodium benzoate | 0 | 0 | 0 | **0** | 0 |
| E320 BHA | 0 | 0 | 0 | **0** | 0 |
| E575 GDL | 0 | 0 | 0 | **0** | 0 |

> The seven `0`-on-displayed-shelf rows are **carried forward from the prototype** (sourced)
> and from the broader raw corpora; they are real on the full Israeli shelf but not present
> in the products currently rendered. Marked so Data does not assume they are dead, and so
> Nutrition knows their displayed-shelf impact is currently nil. (E466 CMC, E211 benzoate,
> E320 BHA, E282, E481, E472e all appeared in the prototype's 420-product raw scan but not
> in the 155-product displayed scan; E575 GDL was resolved as a candidate but not detected
> on either shelf — retained only as a near-neighbor of the citrate/acidulant set and may
> be dropped by Nutrition.)

### 1.4 Generic-class-only declarations (disclosure gaps, not counted as named additives)

These bare class terms appear without a named substance and are a D5 disclosure-gap signal,
not a specific additive. Displayed-shelf frequency (hummus / maadanim):

| Generic class term | Hummus | Maadanim |
|---|---|---|
| "מייצב" (stabilizer) — unnamed | 18 | 59 |
| "חומר משמר / חומרי שימור" (preservative) — unnamed | 55 | 6 |
| "מווסת חומציות" (acidity regulator) — unnamed | 43 | 17 |
| "חומרי טעם וריח / ארומה" (flavoring) — unnamed | 5 | 77 |
| "צבע מאכל / צבעי מאכל" (colour) — unnamed | 0 | 26 |
| "מתחלב" (emulsifier) — unnamed | 0 | 10 |
| "ממתיק" (sweetener) — unnamed | 0 | 8 |

These belong to the D5 transparency dimension, not D4 evidence. Listed here for Nutrition's
and Data's awareness only.

---

## 2. Method & sources

- **Shelf-present set:** Python scan of `expansion.ingredients` (a free-text Hebrew string)
  across the three displayed JSONs. Detection by Hebrew named-additive regex + explicit
  E-number regex. (E-numbers are sparse on Israeli labels — most additives are declared by
  Hebrew name, e.g. "קסנטן", "חומצת לימון", "קרגינן" — so name patterns dominate the catch.)
- **Identity + function class + EFSA-evaluation pointer + EFSA over-exposure flag:** the
  live read-only OFF additives-taxonomy client
  `integrations/clients/food_additives.py` (TASK-170), which wraps
  `https://world.openfoodfacts.org/data/taxonomies/additives.json`. **All 40+ codes
  resolved.** This client's documented HONEST LIMIT: it provides identity + class + EFSA-eval
  *pointer*, **not** numeric ADI values and **not** Israel-vs-EFSA approval divergence.
- **Numeric ADI / JECFA / FDA CFR cites:** carried forward from the W2 prototype (each
  already sourced there) for the 20 prototype additives; for the 16 newly-added additives,
  ADI/authority values are from EFSA re-evaluation opinions located by authority web
  research (firecrawl), cited per entry. EFSA OpenFoodTox / JECFA / FDA have **no free
  per-substance REST API wired** — see the wiring-gap finding in §4.
- **No evidence tiers assigned** anywhere in this document.

---

## 3. Additive evidence entries

Format per entry: **E-number · canonical name · Hebrew label(s) on shelf · function ·
EFSA · JECFA · FDA · ADI · evidence-state note (factual) · source.**

### 3.A — Carried forward from the W2 prototype (20 entries)

The full sourced evidence dossiers for these 20 live in
`additive_prototype_set_v1.md` (Entries 1–20) and are **incorporated by reference** —
not reproduced verbatim here. Summary line per entry below; for the long-form evidence
summary, dose signal, and Israeli label behavior, see the prototype. **Tier labels shown
in the prototype are NOT authoritative for 181B** — Nutrition re-tiers the full expanded
set.

| # | E-number | Name | Function | EFSA | JECFA ADI | FDA | ADI (authority/yr) | Evidence-state note (factual) |
|---|---|---|---|---|---|---|---|---|
| 1 | E330 | Citric acid | acidulant / antioxidant synergist | re-eval, no concern | no ADI (GMP) | GRAS 21 CFR §184.1033 | "no ADI necessary" | Krebs-cycle metabolite; no dose-response concern at food-label exposure. |
| 2 | E202 (E200/201) | Potassium sorbate / sorbates | preservative | re-eval; EFSA over-exposure flag = HIGH | 0–25 mg/kg bw/d | GRAS §182.3640/.3089 | EFSA 3 mg/kg bw/d (as sorbic acid) | ADI > typical exposure (0.5–1.5); one 2026 NutriNet-Santé cohort association w/ T2D (observational, unconfirmed). |
| 3 | E300 | Ascorbic acid (vit C) | antioxidant / dough improver | re-eval, no concern | no ADI | GRAS §182.3013 | no ADI (normal nutrient) | As dough improver, oxidized during baking; **0 on displayed bread shelf**. |
| 4 | E1422 (+E1442) | Acetylated distarch adipate / modified starch | thickener / freeze-thaw stabilizer | group eval | "not specified" | GRAS §172.892/.894 | "not specified" | Metabolized as carbohydrate; no dose-response concern. |
| 5 | E282 | Calcium propionate | mould/rope inhibitor (bread) | re-eval, no concern | "not limited" | GRAS §184.1221 | "not specified" | Endogenous SCFA; Tirosh 2019 effect was pharmacological-dose. **0 on displayed bread shelf.** |
| 6 | E481 | Sodium stearoyl-2-lactylate (SSL) | dough conditioner / emulsifier | eval 2012; over-exposure flag = HIGH | 0–20 mg/kg bw/d | GRAS §172.846 | EFSA 20 mg/kg bw/d (2012) | Exposure < ADI; limited independent RCT data. **0 on displayed bread shelf.** |
| 7 | E407 | Carrageenan | thickener / gelling / stabilizer | 2018 re-eval, ADI "not specified", over-exposure flag = HIGH | "not specified" (2014) | GRAS (food-grade) | "not specified" (EFSA 2018) | Active scientific debate: food-grade carrageenan gut/NF-κB mechanistic concern (Bhattacharyya); EFSA finds no concern at use levels. |
| 8 | E471 | Mono-/diglycerides of fatty acids | emulsifier | eval, no concern | "not specified" | GRAS §182.4505 | "not specified" | NutriNet-Santé 2024 emulsifier-cancer association is class-level, observational. |
| 9 | E472e | DATEM | dough conditioner / emulsifier | group eval | "not specified" | GRAS §182.4101 | "not specified" | Sparse independent data; safety basis primarily regulatory. **0 on displayed bread shelf.** |
| 10 | E415 | Xanthan gum | thickener / stabilizer | eval 2017, no concern | "not specified" | GRAS §172.695 | "not specified" | Fermented as fiber-equivalent; neutral-to-positive evidence. |
| 11 | E450/451/452 | Di-/tri-/polyphosphates | emulsifier / buffer | 2019 re-eval; over-exposure flag = HIGH | "not specified" | GRAS (specific salts) | Group ADI 40 mg P/kg bw/d (EFSA 2019) | EFSA 2019 flagged cumulative phosphate intake may approach/exceed ADI in heavy consumers. |
| 12 | E440 | Pectins | gelling / thickener | eval, no concern | "not specified" | GRAS §184.1588 | no ADI (soluble fibre) | Prebiotic soluble fibre; positive evidence profile. |
| 13 | E410 | Locust bean gum | thickener / stabilizer | eval, no concern | "not specified" | GRAS §182.1343 | "not specified" | Carob-seed polysaccharide; classified dietary fibre. |
| 14 | E412 | Guar gum | thickener / water binder | eval, no concern | "not specified" | GRAS §184.1339 | "not specified" | Soluble fibre; occupational (not dietary) respiratory history only. |
| 15 | E955 | Sucralose | sweetener (NNS) | 2026 re-eval | 0–15 mg/kg bw/d | approved §172.831 | EFSA 5 mg/kg bw/d (2026) | EFSA 2026 tightened ADI to 5 (body-weight critical effect); genotoxicity concern not substantiated; T2D cohort association observational. |
| 16 | E950 | Acesulfame-K | sweetener (NNS) | eval 2000 | 0–15 mg/kg bw/d | approved §172.800 | EFSA 9 mg/kg bw/d (2000) | Animal high-dose insulin/microbiome signals; human RCT data limited/inconsistent. |
| 17 | E466 | Carboxymethylcellulose (CMC) | thickener / stabilizer | eval, ADI "not specified" — **predates Chassaing 2021 RCT** | "not specified" | GRAS §182.1745 | "not specified" (pre-2021) | Chassaing 2021 pre-registered human RCT (n=16+16) showed gut-microbiome/SCFA changes at ~15 g/d; EFSA not re-evaluated since. **0 on displayed shelf.** |
| 18 | E150 (a–d) | Caramel colour | colour | 2012 re-eval (class-specific) | class-specific | GRAS §73.85 (plain) | E150c/d 300 mg/kg bw/d; E150a/b no ADI | Israeli label does not disclose class (I–IV); 4-MEI concern is Class III/IV-specific. Class unknowable from label. |
| 19 | E211 (E210–213) | Sodium benzoate | preservative | 2016 re-eval; over-exposure flag = HIGH | 0–5 mg/kg bw/d | GRAS §184.1733 (not w/ ascorbic) | EFSA 5 mg/kg bw/d (2016) | Benzene-formation reaction w/ vit C (beverage-context); EFSA flagged cumulative exposure can approach ADI. **0 on displayed shelf.** |
| 20 | E320 | BHA (butylated hydroxyanisole) | antioxidant (fats) | 2012 re-eval | 0–0.5 mg/kg bw/d | GRAS ≤0.02% fat §182.3169 | EFSA 0.5 mg/kg bw/d (2012) | IARC Group 2B + NTP "reasonably anticipated"; rodent forestomach mechanism, human relevance debated. **0 on displayed shelf.** |

> EFSA over-exposure flags above ("HIGH") are read directly from the OFF taxonomy
> `efsa_evaluation_overexposure_risk` field via the `food_additives` client — they indicate
> EFSA flagged a population subgroup whose intake may exceed the ADI; they are a regulatory
> exposure flag, **not** a tier.

### 3.B — Newly added (observed on the displayed shelf; absent from prototype 20)

#### N1 — E160a Beta-carotene (colour)
- **Hebrew on shelf:** "צבע מאכל (בטא קרוטן)". **Function:** orange/yellow colour.
- **Frequency (displayed):** 10 maadanim.
- **EFSA:** Re-evaluated 2012 (mixed carotenes) / synthetic beta-carotene re-eval — taxonomy
  pointer `doi:10.2903/j.efsa.2016.4434`. EFSA did **not** set a numerical ADI for use as
  a colour; flagged that high supplemental beta-carotene (distinct from colour use) carries
  a separate consideration in smokers.
- **JECFA:** ADI "not specified" (provitamin-A carotenoid). **FDA:** listed colour additive,
  21 CFR §73.95 (beta-carotene).
- **ADI:** no numerical ADI for colour use (EFSA). **Evidence-state note:** normal dietary
  provitamin A; colour-use exposure is low; the smoker/high-dose-supplement signal is a
  supplement-context issue, not a food-colour-exposure conclusion.
- **Source:** OFF taxonomy (EFSA pointer 10.2903/j.efsa.2016.4434); JECFA/FDA per standard
  colour status.

#### N2 — E163 Anthocyanins (colour)
- **Hebrew on shelf:** "צבע מאכל: אנטוציאנין (רכז גזר שחור)" (black-carrot concentrate).
- **Function:** red/purple colour. **Frequency:** 3 maadanim.
- **EFSA:** Re-evaluated 2013 — pointer `doi:10.2903/j.efsa.2013.3145`. SCF did **not**
  derive an ADI; EFSA noted data limitations for grape-skin extract.
- **JECFA:** ADI 2.5 mg/kg bw/day for anthocyanins from grape-skin extract. **FDA:** fruit/
  vegetable juice colours are exempt-from-certification colour additives.
- **ADI:** EFSA/SCF no ADI; JECFA 2.5 mg/kg bw/d (grape-skin extract). **Evidence-state
  note:** plant-pigment colour; sourced here from black-carrot concentrate (a colouring
  food); no safety concern flagged at colour-use exposure.
- **Source:** EFSA opinion 10.2903/j.efsa.2013.3145 (verified web); JECFA grape-skin ADI
  (EFSA opinion text).

#### N3 — E162 Beetroot red / betanin (colour)
- **Hebrew on shelf:** "אדום סלק" / "רכז סלק". **Function:** red colour. **Frequency:** 1 maadanim.
- **EFSA:** Re-evaluated 2015 — pointer `doi:10.2903/j.efsa.2015.4318`. ADI "not specified"
  (no safety concern at reported use levels).
- **JECFA:** ADI "not specified". **FDA:** beet powder, exempt-from-certification colour
  (21 CFR §73.40).
- **ADI:** "not specified" (EFSA 2015). **Evidence-state note:** beet-derived pigment; no
  safety concern at use levels.
- **Source:** EFSA opinion 10.2903/j.efsa.2015.4318 (OFF taxonomy pointer).

#### N4 — E100 Curcumin (colour)
- **Hebrew on shelf:** "כורכומין". **Function:** yellow colour. **Frequency:** 1 maadanim.
- **EFSA:** Re-evaluated 2010 — pointer `doi:10.2903/j.efsa.2010.1679`. **ADI = 3 mg/kg
  bw/day.** EFSA flagged that the ADI may be exceeded by high consumers of curcumin **food
  supplements** (not by colour use in food).
- **JECFA:** ADI 0–3 mg/kg bw/day. **FDA:** turmeric/curcumin colour, exempt-from-
  certification (21 CFR §73.600 turmeric).
- **ADI:** 3 mg/kg bw/day (EFSA 2010; JECFA concordant). **Evidence-state note:** the ADI
  is documented as potentially exceeded via concentrated supplements; food-colour exposure
  is well below it.
- **Source:** EFSA 2010 opinion (10.2903/j.efsa.2010.1679; ADI 3 mg/kg confirmed via EFSA
  colours summary + BfR); OFF taxonomy.

#### N5 — E141 Copper complexes of chlorophylls / chlorophyllins (colour)
- **Hebrew on shelf:** appears within a colour blend "(E-163, בטא קרוטן, כורכומין, E-141,
  אדום סלק)". **Function:** green colour. **Frequency:** 1 maadanim.
- **EFSA:** Re-evaluated 2015 — pointer `doi:10.2903/j.efsa.2015.4151`. ADI not numerically
  established for the chlorophyll group in that opinion; copper-release considered.
- **JECFA:** ADI 0–15 mg/kg bw/day (chlorophyllin copper complexes, sodium/potassium salts).
  **FDA:** not a US-approved colour additive for general food use (note the US/EU divergence).
- **ADI:** EFSA group consideration; JECFA 0–15 mg/kg bw/d. **Evidence-state note:** the
  copper-bearing green colourant; EFSA's 2015 opinion centered on copper exposure
  contribution; **EVIDENCE GAP on a clean single numerical EFSA ADI** — EFSA evaluated as a
  group with copper-release caveats rather than a single figure.
- **Source:** EFSA opinion 10.2903/j.efsa.2015.4151 (OFF taxonomy pointer); JECFA chlorophyllin ADI.

#### N6 — E333 Calcium citrate (tricalcium citrate)
- **Hebrew on shelf:** "סידן (טריקלציום ציטרט)", "קלציום ציטרט" — used as a calcium-
  fortification / sequestrant salt. **Function:** sequestrant / stabilizer / Ca source.
  **Frequency:** 5 maadanim.
- **EFSA:** **No dedicated EFSA URL in the OFF taxonomy (`EVIDENCE GAP` on a discrete EFSA
  citrate-salt opinion).** Citrates are a "permitted at quantum satis" acid-group salt; EFSA
  treats the citric-acid/citrate group together with "no ADI necessary".
- **JECFA:** ADI "not limited" (citric acid and its Na/K/Ca salts). **FDA:** GRAS, 21 CFR
  §184.1195 (calcium citrate).
- **ADI:** "no ADI necessary" / "not limited" (citrate group). **Evidence-state note:**
  calcium salt of citric acid; metabolized as citrate + calcium; no dose-response concern.
- **Source:** JECFA citrate-group "not limited"; FDA §184.1195. EFSA single-opinion `EVIDENCE GAP`.

#### N7 — E331 Sodium citrate
- **Hebrew on shelf:** "סודיום ציטרט", "טרי סודיום ציטרט". **Function:** acidity regulator /
  emulsifying salt / sequestrant. **Frequency:** 3 maadanim.
- **EFSA:** No dedicated EFSA URL in OFF taxonomy (`EVIDENCE GAP` on discrete opinion);
  citrate group "no ADI necessary".
- **JECFA:** ADI "not limited". **FDA:** GRAS, 21 CFR §184.1751 (sodium citrate).
- **ADI:** "no ADI necessary" / "not limited". **Evidence-state note:** sodium salt of
  citric acid; metabolized as citrate; contributes sodium (nutrition-relevant, not a safety
  ADI concern).
- **Source:** JECFA citrate group; FDA §184.1751.

#### N8 — E327 Calcium lactate
- **Hebrew on shelf:** "לקטט" / calcium-lactate fortification context. **Function:**
  acidity regulator / calcium source / firming. **Frequency:** 3 maadanim.
- **EFSA:** No dedicated EFSA URL in OFF taxonomy (`EVIDENCE GAP` on discrete opinion);
  lactate group treated as "no ADI necessary".
- **JECFA:** ADI "not limited" (lactic acid and salts). **FDA:** GRAS, 21 CFR §184.1207.
- **ADI:** "not limited" / "no ADI necessary". **Evidence-state note:** calcium salt of
  lactic acid; lactate is a normal metabolite; no dose-response concern.
- **Source:** JECFA lactate group; FDA §184.1207.

#### N9 — E296 Malic acid
- **Hebrew on shelf:** "חומצה מאלית". **Function:** acidulant. **Frequency:** 1 maadanim.
- **EFSA:** No dedicated EFSA URL in OFF taxonomy (`EVIDENCE GAP` on discrete opinion);
  DL-malic acid permitted, treated as a metabolic acid.
- **JECFA:** ADI "not limited" (L- and DL-malic acid). **FDA:** GRAS, 21 CFR §184.1069.
- **ADI:** "not limited". **Evidence-state note:** Krebs-cycle intermediate (L-malate);
  no dose-response concern; DL-form not recommended for infants (standard caveat).
- **Source:** JECFA malic-acid evaluation; FDA §184.1069.

#### N10 — E270 Lactic acid
- **Hebrew on shelf:** "חומצה לקטית" / "חומצת חלב". **Function:** acidulant / preservative.
  **Frequency:** 1 hummus.
- **EFSA:** No dedicated EFSA URL in OFF taxonomy (`EVIDENCE GAP` on discrete opinion);
  normal fermentation metabolite, "no ADI necessary".
- **JECFA:** ADI "not limited" (L-form). **FDA:** GRAS, 21 CFR §184.1061.
- **ADI:** "not limited". **Evidence-state note:** normal metabolite of carbohydrate
  fermentation; no concern at food-label exposure; D-/DL-form caveat for infants.
- **Source:** JECFA lactic-acid evaluation; FDA §184.1061.

#### N11 — E401 Sodium alginate
- **Hebrew on shelf:** "אלגינט נתרן" / alginate. **Function:** thickener / gelling /
  stabilizer (seaweed-derived). **Frequency:** 1 maadanim.
- **EFSA:** Re-evaluated 2017 — pointer `https://efsa.onlinelibrary.wiley.com/doi/
  10.2903/j.efsa.2017.5049`. ADI "not specified"; no safety concern at use levels (alginates
  E400–E404).
- **JECFA:** ADI "not specified". **FDA:** GRAS, 21 CFR §184.1724.
- **ADI:** "not specified" (EFSA 2017). **Evidence-state note:** brown-seaweed polysaccharide;
  not absorbed intact; soluble-fibre-like; no dose-response concern.
- **Source:** EFSA 2017 alginates opinion (10.2903/j.efsa.2017.5049); FDA §184.1724.

#### N12 — E516 Calcium sulphate
- **Hebrew on shelf:** "גופרת סידן" / calcium-sulphate firming/Ca context. **Function:**
  firming agent / sequestrant / calcium source. **Frequency:** 1 maadanim.
- **EFSA:** No dedicated EFSA URL in OFF taxonomy (`EVIDENCE GAP` on discrete opinion).
- **JECFA:** ADI "not limited". **FDA:** GRAS, 21 CFR §184.1230.
- **ADI:** "not limited" (JECFA). **Evidence-state note:** gypsum; common firming/coagulant
  agent (also tofu coagulant); no dose-response concern; contributes calcium + sulphate.
- **Source:** JECFA calcium-sulphate evaluation; FDA §184.1230.

#### N13 — E500 Sodium carbonates (sodium carbonate / bicarbonate)
- **Hebrew on shelf:** "סודיום קרבונט", "סודה לשתייה", "ביקרבונט". **Function:** acidity
  regulator / raising agent. **Frequency:** 1 maadanim (named); also detected under the
  baking-soda family in hummus (counted under the E500 family row, §1.3).
- **EFSA:** Re-evaluated 2013 — pointer `doi:10.2903/j.efsa.2013.3152`. ADI "not specified";
  no safety concern.
- **JECFA:** ADI "not limited". **FDA:** GRAS, 21 CFR §184.1742 (sodium bicarbonate).
- **ADI:** "not specified" (EFSA 2013). **Evidence-state note:** common leavening/buffer
  salt; contributes sodium (nutrition-relevant); no dose-response safety concern.
- **Source:** EFSA 2013 opinion (10.2903/j.efsa.2013.3152); FDA §184.1742.

#### N14 — E575 Glucono-delta-lactone (GDL)
- **Hebrew on shelf:** "גלוקונו דלתא לקטון" (candidate; **not detected on displayed shelf**
  — count 0). **Function:** acidulant / sequestrant / coagulant.
- **EFSA:** No dedicated EFSA URL in OFF taxonomy (`EVIDENCE GAP` on discrete opinion);
  gluconate group "no ADI necessary".
- **JECFA:** ADI "not limited". **FDA:** GRAS, 21 CFR §184.1318.
- **ADI:** "not limited". **Evidence-state note:** hydrolyzes to gluconic acid; normal
  metabolite; no dose-response concern. **Retained as a candidate only; Nutrition may drop
  it (0 displayed-shelf frequency).**
- **Source:** JECFA gluconate group; FDA §184.1318.

#### N15 — E960 Steviol glycosides (sweetener)
- **Hebrew on shelf:** "סטיביה" / "סטיביול גליקוזידים". **Function:** non-nutritive
  sweetener (plant-derived). **Frequency:** 2 maadanim.
- **EFSA:** First evaluated 2010 — pointer `doi:10.2903/j.efsa.2015.4146` (and 2010 origin);
  EFSA over-exposure flag in OFF taxonomy = **MODERATE** (high-consumer subgroups,
  esp. children, may exceed ADI). **ADI = 4 mg/kg bw/day** (expressed as steviol
  equivalents).
- **JECFA:** ADI 0–4 mg/kg bw/day (steviol equivalents). **FDA:** high-purity steviol
  glycosides are GRAS (FDA has issued multiple GRAS no-objection letters); whole-leaf
  stevia is **not** approved.
- **ADI:** 4 mg/kg bw/day (EFSA 2010, JECFA concordant). **Evidence-state note:** EFSA
  flagged children as a potential over-exposure subgroup; genotoxicity concern resolved
  (not genotoxic). The "natural sweetener" front-of-pack framing is common.
- **Source:** EFSA 2010 (ADI 4 mg/kg, verified web) + 2015 exposure opinion
  (10.2903/j.efsa.2015.4146); JECFA 4 mg/kg; OFF taxonomy over-exposure flag = moderate.

#### N16 — E1412 / E1414 Modified starch variants (distarch phosphate / acetylated distarch phosphate)
- **Hebrew on shelf:** "עמילן מעובד" (often undifferentiated) + explicit "E1412"/"E1414".
  **Function:** thickener / stabilizer. **Frequency:** 2 maadanim (explicit E-number);
  many more fold into the "עמילן מעובד" generic count under the modified-starch family row.
- **EFSA:** Modified-starch group re-evaluated; OFF taxonomy carries no discrete per-variant
  EFSA URL (`EVIDENCE GAP` on a per-variant opinion), but the group conclusion applies.
- **JECFA:** Group ADI "not specified". **FDA:** food-starch-modified, 21 CFR §172.892.
- **ADI:** "not specified" (modified-starch group). **Evidence-state note:** siblings of the
  prototype's E1422/E1442; metabolized as carbohydrate; the same group conclusion applies.
  These are folded into the prototype's modified-starch entry for tiering purposes.
- **Source:** JECFA modified-starch group; FDA §172.892; OFF taxonomy identity.

---

## 4. EFSA / JECFA / FDA wiring-gap finding (for Product, 181C/D)

**Which authority I could query programmatically vs had to web-scrape vs could not reach:**

| Authority / data | Reachable how | Status |
|---|---|---|
| **Identity** (E-number → canonical name, synonyms) | `food_additives` client (OFF taxonomy) + `pubchem.get_compound` | **WIRED & LIVE.** All 40+ codes resolved. |
| **Function class** (preservative/colour/emulsifier…) | `food_additives` client (OFF taxonomy) | **WIRED & LIVE.** |
| **EFSA evaluation *pointer*** (the re-eval DOI/URL) | `food_additives` client (OFF taxonomy `efsa_evaluation_url`) | **WIRED & LIVE** for ~30 of 40 codes; the acid-group salts (E331/E333/E327/E296/E270/E516/E575) and per-variant modified starches carry **no discrete URL** in the taxonomy. |
| **EFSA over-exposure flag** | `food_additives` client (OFF taxonomy `efsa_evaluation_overexposure_risk`) | **WIRED & LIVE** (HIGH on sorbates/benzoate/SSL/carrageenan/phosphates; MODERATE on steviol). |
| **EFSA numeric ADI value** | **NOT wired** — no free per-substance REST API. Had to **web-scrape** EFSA opinion PDFs/summaries (firecrawl) per substance, OR carry forward the prototype's already-sourced numbers. | **GAP — manual/web.** |
| **JECFA evaluations / ADI** | **NOT wired** — no free REST API. Web research against JECFA/INCHEM monograph text. | **GAP — manual/web.** |
| **FDA GRAS / 21 CFR cites** | `openfda` client exists but exposes **enforcement (recalls) + adverse-event** endpoints only — **not** the GRAS/CFR substance list. CFR cites here are from the prototype + standard 21 CFR §182/§184 knowledge, web-verifiable. | **GAP — manual/web** (openFDA client does not cover GRAS substance status). |
| **Israel MoH approval / Israel-specific ADI or divergence** | **NOT wired** anywhere; the `food_additives` client docstring names this as a documented industry-wide gap. | **GAP — unreachable.** |

**Recommendation for Product (181C):** the cheap, high-value wiring is an **EFSA OpenFoodTox
bulk import** (EFSA publishes OpenFoodTox as a downloadable dataset with substance-level
hazard/reference-point data — a one-time import-and-cache, exactly the "import-and-curate,
not live-per-product" model the umbrella specifies) plus a **JECFA monograph index**.
Numeric ADI values are the single most-requested datum the current `food_additives` client
explicitly does **not** provide; closing that with an OpenFoodTox import would remove the
per-substance web-scrape step entirely. The Israel-MoH divergence gap has no free source and
should stay a documented limitation, not a blocked task. **This is a wiring decision for
Product/Data — not actioned in this research wave.**

---

## 5. EVIDENCE GAP register (additives where a datum could not be located — never fabricated)

| Additive | Gap | What was used instead |
|---|---|---|
| E331 sodium citrate | No discrete EFSA opinion URL in taxonomy | JECFA citrate-group "not limited" + FDA §184.1751 |
| E333 calcium citrate | No discrete EFSA opinion URL | JECFA "not limited" + FDA §184.1195 |
| E327 calcium lactate | No discrete EFSA opinion URL | JECFA lactate group + FDA §184.1207 |
| E296 malic acid | No discrete EFSA opinion URL | JECFA "not limited" + FDA §184.1069 |
| E270 lactic acid | No discrete EFSA opinion URL | JECFA "not limited" + FDA §184.1061 |
| E516 calcium sulphate | No discrete EFSA opinion URL | JECFA "not limited" + FDA §184.1230 |
| E575 GDL | No discrete EFSA opinion URL | JECFA gluconate group + FDA §184.1318 |
| E141 copper chlorophylls | No single numerical EFSA ADI (group eval w/ copper caveat) | EFSA 2015 group opinion + JECFA 0–15 mg/kg |
| E1412 / E1414 modified starch | No per-variant EFSA URL | modified-starch group conclusion (JECFA/FDA §172.892) |

For all nine, an authority *did* evaluate the substance (JECFA and/or FDA), so none is left
without any regulatory anchor — the gap is specifically a **missing discrete EFSA numeric
opinion**, recorded honestly rather than invented. These are the prime candidates for an
EFSA OpenFoodTox bulk import (§4) to close.

---

## 6. Handoff to Nutrition (181B) — explicit non-decisions

- **No evidence tiers assigned** in this document. The
  functional/likely-neutral/dose-dependent/contested/disclosure-gap labels shown in the
  *prototype* (`additive_prototype_set_v1.md`) are **not authoritative for the expanded
  set** — Nutrition re-tiers all 36 against this evidence.
- Specific tiering judgments Nutrition must make on the **newly-added** additives:
  - **Colours (E160a, E163, E162, E100, E141):** mostly "no ADI / no concern at colour-use
    exposure," but E100 curcumin and E960 steviol carry numeric ADIs with documented
    over-exposure subgroups (supplements / children) — decide whether that is a
    dose-dependent flag or a context note.
  - **E960 steviol glycosides:** EFSA over-exposure flag = MODERATE (children). Decide tier.
  - **Acid-group salts (citrates/lactates/malic/lactic):** all "not limited"/"no ADI
    necessary"; sodium citrate also contributes sodium (a nutrition-axis, not D4-evidence,
    consideration) — confirm these are functional.
  - **E141 copper chlorophylls:** US/EU divergence (not FDA-approved for general food use) +
    EFSA copper-release caveat — decide whether the divergence is tier-relevant or a D5
    disclosure note.
- The **0-on-displayed-shelf** carried-forward additives (E282, E481, E472e, E300-dough,
  E466, E211, E320, E575) still need tiers (Data wires the detector once), but Nutrition
  should know their current displayed-shelf impact is nil.

---

## 7. Provenance & integrity statement

- **Files scanned (read-only):** `bari-web/src/data/comparisons/hummus_frontend_v4.json`,
  `maadanim_frontend_v2.json`, `bread_frontend_v2.json`.
- **Live client used (read-only):** `integrations/clients/food_additives.py` (OFF additives
  taxonomy) — all 40+ codes resolved for identity/class/EFSA-pointer/over-exposure flag.
- **Web research (authority verification):** EFSA opinion DOIs/summaries for the newly-added
  colours and sweeteners (curcumin ADI 3 mg/kg; steviol ADI 4 mg/kg; anthocyanin SCF-no-ADI
  / JECFA 2.5 mg/kg; beetroot/sodium-carbonate/alginate "not specified").
- **No score moved. No JSON edited. No engine code touched. No evidence tier assigned.**
  This is an annotate-only research artifact under `01_framework/glass_box/`.
- Proposed task status: **RETURNED** for CC close-readiness verification. CC records CLOSED;
  Research does not.
