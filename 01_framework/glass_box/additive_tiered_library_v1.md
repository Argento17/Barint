---
document: additive_tiered_library_v1
task: TASK-181B
program: TASK-181 (Glass Box program-of-record) — Wave 3, D4 additive library
phase: Nutrition tiering deliverable — Nutrition + Product D7 co-sign COMPLETE 2026-06-04
status: RETURNED (proposed; CC close-readiness gate to verify)
created_at: 2026-06-04
owner: nutrition-agent
registry: EV-043 (03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md)
---

# Additive Tiered Library v1 — Glass Box W3 (D4)

**Purpose.** Assign each of the 36 additives in the expanded D4 library
(`additive_library_expanded_v1.md`, TASK-181A) **exactly one** of the EV-041 evidence
tiers. This is the decision 181A explicitly deferred to Nutrition. The tiers drive
**display copy only** — they carry **no headline-grade weight in W3** (annotate-only;
TASK-181 hard boundary). This file is the tier input Data wires in TASK-181D.

**Tier model (frozen, from EV-041 — not redefined here):**
`functional` · `likely-neutral` · `dose-dependent` · `contested` · `disclosure-gap` ·
`confirmed-negative` (+ `unclassified` true-fallback only).

**Hard constraints honored:** No score moved. No JSON edited. No engine code touched.
No tier invented beyond the 181A curated evidence. Every tier cites that evidence + the
registry entry **EV-043**. Product D7 co-sign is **COMPLETE 2026-06-04** (Product Agent,
TASK-181C — scope/maintenance co-sign; see §6) — Nutrition authored these tiers; the co-sign
was not self-certified.

---

## 1. Tier distribution (36 additives)

| Tier | Count | Definition (EV-041) |
|---|---|---|
| functional | 19 | Well-characterised function, broad regulatory acceptance, no safety concern at typical food doses. |
| likely-neutral | 7 | Extensive history of use, no significant safety signal at typical doses; a minor unconfirmed signal may exist. |
| dose-dependent | 5 | Safe at typical food doses; concern arises at high or cumulative exposure. |
| contested | 3 | Mixed/emerging evidence; credible mechanistic or clinical signal without regulatory consensus. |
| disclosure-gap | 1 | Label does not transmit the information needed to assign a tier. |
| confirmed-negative | 0 | Credible weight-of-evidence harm at relevant exposure. **No additive on this shelf meets the bar.** |
| unclassified | 1 | True fallback: the available evidence anchor does not permit a clean tier verdict. |
| **Total** | **36** | |

---

## 2. The 36-row tier table

Format: **E-number · name · function · tier · one-line justification (citing 181A evidence) ·
181A source location.** "181A" = `additive_library_expanded_v1.md`. "P#" / "N#" = that
sheet's entry id.

### 2.A — Carried forward from the W2 prototype (20)

| # | E-number | Name | Function | Tier | Justification (181A evidence) | 181A src |
|---|---|---|---|---|---|---|
| 1 | E330 | Citric acid (+ E331/E333 citrate salts) | acidulant / antioxidant synergist | **functional** | Krebs-cycle metabolite; EFSA "no ADI necessary", JECFA GMP, FDA GRAS; no dose-response concern at food-label exposure. | 181A §3.A #1 |
| 2 | E200–E203 | Sorbates (potassium sorbate) | preservative | **likely-neutral** | EFSA ADI 3 mg/kg & JECFA 25 mg/kg both >> typical exposure (0.5–1.5); one 2026 NutriNet-Santé T2D association is observational, unconfirmed, has not shifted the regulatory consensus. | 181A §3.A #2 |
| 3 | E300 | Ascorbic acid (vit C) | antioxidant / dough improver | **functional** | Normal nutrient, no ADI; as dough improver it is oxidized during baking and not present in finished bread. **0 on displayed bread shelf.** | 181A §3.A #3 |
| 4 | E1422 / E1442 | Acetylated/hydroxypropyl distarch (modified starch) | thickener / freeze-thaw stabilizer | **likely-neutral** | Metabolized as carbohydrate; EFSA/JECFA group ADI "not specified"; well-characterised, no positive harm signal. Prototype tier kept; E1412/E1414 siblings (N16) fold in here. | 181A §3.A #4, N16 |
| 5 | E282 | Calcium propionate | mould/rope inhibitor (bread) | **likely-neutral** | Endogenous SCFA; EFSA/JECFA "not limited"; Tirosh 2019 effect was pharmacological-dose, not confirmed at food exposure. **0 on displayed bread shelf.** | 181A §3.A #5 |
| 6 | E481 | Sodium stearoyl-2-lactylate (SSL) | dough conditioner / emulsifier | **likely-neutral** | EFSA ADI 20 mg/kg; exposure < ADI; emulsifier class carries only class-level observational (NutriNet) signal, not E481-specific. **0 on displayed bread shelf.** | 181A §3.A #6 |
| 7 | E407 | Carrageenan | thickener / gelling / stabilizer | **contested** | EFSA 2018 "no concern" / ADI "not specified", but independent peer-reviewed mechanistic research (Bhattacharyya; NF-κB / gut-barrier) at food-grade concentrations is in genuine, active disagreement (2026 review). | 181A §3.A #7 |
| 8 | E471 | Mono-/diglycerides of fatty acids | emulsifier | **likely-neutral** | EFSA/JECFA ADI "not specified"; structurally identical to normal fat-digestion products; 2024 NutriNet-Santé emulsifier-cancer link is class-level, observational, could not isolate E471. | 181A §3.A #8 |
| 9 | E472e | DATEM | dough conditioner / emulsifier | **likely-neutral** | EFSA/JECFA "not specified"; no DATEM-specific mechanistic concern; evidence base is primarily regulatory + metabolic-stability (sparse independent data, no positive harm signal). **0 on displayed bread shelf.** | 181A §3.A #9 |
| 10 | E415 | Xanthan gum | thickener / stabilizer | **functional** | Fermentation-derived polysaccharide, fermented as fiber-equivalent; EFSA 2017 "not specified"; neutral-to-positive evidence. | 181A §3.A #10 |
| 11 | E450/451/452 | Di-/tri-/polyphosphates | emulsifier / buffer | **dose-dependent** | EFSA 2019 group ADI 40 mg P/kg bw/d and explicit flag that cumulative phosphate intake may approach/exceed ADI in heavy consumers — a documented dose-response pathway. | 181A §3.A #11 |
| 12 | E440 | Pectins | gelling / thickener | **functional** | Soluble dietary fibre, prebiotic; EFSA no ADI; positive evidence profile. | 181A §3.A #12 |
| 13 | E410 | Locust bean gum | thickener / stabilizer | **functional** | Carob-seed polysaccharide, classified dietary fibre; EFSA/JECFA "not specified"; no concern at any food-label exposure. | 181A §3.A #13 |
| 14 | E412 | Guar gum | thickener / water binder | **functional** | Soluble fibre; EFSA/JECFA "not specified"; occupational (not dietary) respiratory history irrelevant to food exposure. | 181A §3.A #14 |
| 15 | E955 | Sucralose | sweetener (NNS) | **dose-dependent** | EFSA 2026 tightened ADI to 5 mg/kg (body-weight critical effect); narrower exposure-to-ADI margin than "not specified" additives + live gut-microbiome / T2D observational discussion; genotoxicity unsubstantiated (so not contested). | 181A §3.A #15 |
| 16 | E950 | Acesulfame-K | sweetener (NNS) | **dose-dependent** | EFSA ADI 9 mg/kg; high-consumer exposure (1–3) non-negligible vs ADI; animal insulin/microbiome signals at high dose + class-level NNS–T2D observational association cross the threshold beyond likely-neutral. | 181A §3.A #16 |
| 17 | E466 | Carboxymethylcellulose (CMC) | thickener / stabilizer | **contested** | Chassaing 2021 pre-registered human RCT (n=16+16) showed gut-microbiome/SCFA changes at food-achievable ~15 g/d; EFSA "not specified" ADI predates it and has not been re-evaluated — substantive regulatory-science gap. **0 on displayed shelf.** | 181A §3.A #17 |
| 18 | E150 (a–d) | Caramel colour | colour | **disclosure-gap** | Israeli label declares "צבע קרמל"/E150 without class; Class I/II neutral, Class III/IV carry the 4-MEI (IARC 2B animal) concern — class is structurally unknowable from the label, so no meaningful tier can be assigned. | 181A §3.A #18 |
| 19 | E210–E213 | Sodium benzoate | preservative | **dose-dependent** | EFSA ADI 5 mg/kg; cumulative exposure can approach ADI; benzene-formation reaction with ascorbic acid is a real (context-dependent) chemical concern, slower in solid/dairy matrices. **0 on displayed shelf.** | 181A §3.A #19 |
| 20 | E320 | BHA (butylated hydroxyanisole) | antioxidant (fats) | **contested** | IARC Group 2B + NTP "reasonably anticipated" on rodent forestomach data (no human analogue); EFSA maintains ADI 0.5 mg/kg; regulatory-vs-classification tension at realistic exposure = contested, not confirmed-negative (no human harm evidence; exposure << ADI). **0 on displayed shelf.** | 181A §3.A #20 |

### 2.B — Newly added (16; observed on the displayed shelf, absent from prototype 20)

| # | E-number | Name | Function | Tier | Justification (181A evidence) | 181A src |
|---|---|---|---|---|---|---|
| 21 | E160a | Beta-carotene | colour | **functional** | Provitamin-A carotenoid; no numerical ADI for colour use (EFSA), JECFA "not specified"; the smoker/high-dose-supplement signal is a supplement-context issue, not a food-colour-exposure conclusion. | 181A N1 |
| 22 | E163 | Anthocyanins (black-carrot conc.) | colour | **functional** | Plant pigment / colouring food; EFSA-SCF no ADI, JECFA 2.5 mg/kg (grape-skin); no safety concern flagged at colour-use exposure. | 181A N2 |
| 23 | E162 | Beetroot red / betanin | colour | **functional** | Beet-derived pigment; EFSA 2015 ADI "not specified" (no concern at use levels); JECFA "not specified". | 181A N3 |
| 24 | E100 | Curcumin | colour | **functional** | EFSA/JECFA ADI 3 mg/kg; the documented over-exposure is via concentrated **food supplements**, not food-colour use — colour exposure is well below the ADI. Numeric ADI noted as a context note, not a dose-dependent trigger (see §3 judgment call 2). | 181A N4 |
| 25 | E141 | Copper complexes of chlorophylls | colour | **unclassified** | No clean single numerical EFSA ADI (group eval w/ copper-release caveat); the only added datum that cannot be cleanly tiered on its anchor. US/EU divergence handled as a D5 note, not a tier move (see §3 judgment call 3). Reason recorded; not guessed. | 181A N5 |
| 26 | E333 | Calcium citrate (tricalcium) | sequestrant / Ca source | **functional** | Citrate group "no ADI necessary" / JECFA "not limited" + FDA §184.1195; metabolized as citrate + calcium; no dose-response concern. EFSA discrete-opinion gap → tiered on JECFA+FDA anchor (judgment call 1). | 181A N6 |
| 27 | E331 | Sodium citrate | acidity regulator / emulsifying salt | **functional** | Citrate group "not limited" + FDA §184.1751; metabolized as citrate. Contributes sodium — a **nutrition-axis** consideration, NOT a D4-evidence one, so it does not change the D4 tier. | 181A N7 |
| 28 | E327 | Calcium lactate | acidity regulator / Ca source | **functional** | Lactate group "not limited" + FDA §184.1207; lactate is a normal metabolite; no dose-response concern. EFSA gap → JECFA+FDA anchor. | 181A N8 |
| 29 | E296 | Malic acid | acidulant | **functional** | Krebs-cycle intermediate (L-malate); JECFA "not limited" + FDA §184.1069; no dose-response concern (DL-form infant caveat is a standard note, not a shelf-additive tier driver). | 181A N9 |
| 30 | E270 | Lactic acid | acidulant / preservative | **functional** | Normal fermentation metabolite; JECFA "not limited" + FDA §184.1061; no concern at food-label exposure. | 181A N10 |
| 31 | E401 | Sodium alginate | thickener / gelling | **functional** | Brown-seaweed polysaccharide, not absorbed intact, soluble-fibre-like; EFSA 2017 ADI "not specified"; no dose-response concern. | 181A N11 |
| 32 | E516 | Calcium sulphate | firming / sequestrant / Ca source | **functional** | Gypsum; JECFA "not limited" + FDA §184.1230; common firming/coagulant (also tofu coagulant); no dose-response concern. EFSA gap → JECFA+FDA anchor. | 181A N12 |
| 33 | E500 | Sodium carbonates / bicarbonate | acidity regulator / raising agent | **functional** | Common leavening/buffer salt; EFSA 2013 ADI "not specified"; no dose-response safety concern. Contributes sodium = nutrition-axis, not a D4 tier driver. | 181A N13 |
| 34 | E575 | Glucono-delta-lactone (GDL) | acidulant / sequestrant / coagulant | **functional** | Hydrolyzes to gluconic acid, normal metabolite; JECFA "not limited" + FDA §184.1318. **0 on either shelf** — Nutrition RETAINS it (does not drop): low maintenance cost, real near-neighbour of the acidulant set, returns the moment a product declares it. | 181A N14 |
| 35 | E960 | Steviol glycosides | sweetener (NNS) | **dose-dependent** | EFSA/JECFA ADI 4 mg/kg + EFSA over-exposure flag MODERATE (children as high-consumer subgroup may exceed ADI at the **sweetener** axis — a genuine use-level signal, unlike colour over-exposure). Consistent with the other two NNS. Genotoxicity resolved (not genotoxic), so not contested. | 181A N15 |
| 36 | E1412 / E1414 | Distarch phosphate / acetylated distarch phosphate (modified starch) | thickener / stabilizer | **likely-neutral** | Siblings of E1422/E1442; modified-starch group ADI "not specified"; metabolized as carbohydrate; the same group conclusion applies. Folds into the modified-starch tier (#4). | 181A N16 |

---

## 3. The four §4 judgment-call groups — explicit resolution

**Judgment call 1 — the 9 EVIDENCE-GAP additives (no discrete EFSA numeric opinion).**
`E331, E333, E327, E296, E270, E516, E575, E141, E1412/E1414`.
For eight of the nine, an authority *did* evaluate the substance — JECFA returned **"not
limited"** and FDA carries a **GRAS / 21 CFR anchor** — and each is a normal metabolic acid
salt (citrate/lactate/malate/lactate/gluconate), a mineral firming salt (calcium sulphate),
or a modified starch metabolized as carbohydrate. These have **no dose-response pathway** at
food-label exposure. **Resolution: all eight → `functional`**, with confidence stated as
**Strong** on the JECFA-"not limited" + FDA-GRAS concordance (the missing datum is only a
*discrete EFSA numeric opinion*, not the absence of any evaluation). The ninth, **E141**, is
the exception — it has no clean single numerical EFSA ADI (group eval with a copper-release
caveat) and so cannot be tiered on its anchor → handled in judgment call 3.

**Judgment call 2 — E100 curcumin & E960 steviol (numeric ADI + over-exposure subgroup).**
The deciding question is *whether the over-exposure occurs at the additive's shelf use, or
in a different consumption context.*
- **E100 curcumin → `functional` (context note, not dose-dependent).** The EFSA-documented
  ADI exceedance is via **concentrated curcumin food supplements**, a separate consumption
  channel; **food-colour use exposure is well below the 3 mg/kg ADI.** The numeric ADI is
  recorded as a context note in the entry, but the over-exposure does not occur at the
  food-colour exposure Bari is scoring — so a dose-dependent tier would mislead. Functional
  is the honest tier for the shelf use.
- **E960 steviol → `dose-dependent`.** Here the over-exposure subgroup (EFSA flag =
  **MODERATE**, children as high consumers) sits on the **same sweetener axis** the additive
  is used for — high-NNS-consuming children can approach the 4 mg/kg ADI through ordinary
  sweetened-product consumption. That is a genuine use-level dose-response signal, identical
  in kind to E955/E950. Dose-dependent, consistent with the rest of the NNS set.

**Judgment call 3 — E141 copper chlorophylls (US/EU divergence + copper caveat).**
Two distinct issues, resolved separately:
- The **US/EU approval divergence** (not FDA-approved for general US food use; permitted in
  EU) is a **jurisdictional approval-status fact, not evidence of harm.** Approval divergence
  belongs to **D5 (disclosure / what-the-label-vs-jurisdiction-says)**, not to a D4
  evidence-tier move. **Resolution: the divergence is a D5 note, NOT a D4 tier move** — D4
  does not penalise an additive for a jurisdictional approval difference.
- The **D4 tier itself**: 181A records **no clean single numerical EFSA ADI** for E141 (EFSA
  2015 evaluated the chlorophyll group with copper-release caveats rather than a single
  figure; JECFA gave 0–15 mg/kg for the copper-complex salts). Because the available anchor
  does not permit a clean food-label tier verdict and Bari does not invent one, **E141 →
  `unclassified`** with the reason recorded (the one true fallback in the set). This is the
  intellectually honest call: not `disclosure-gap` (the *label* discloses E141 fine — the
  *evidence record* is what is incomplete), and not a forced `functional` (the copper caveat
  is a real, unresolved consideration). A future clean EFSA numeric opinion would re-tier it.

**Judgment call 4 — acid-group salts contribute sodium (sodium citrate, sodium carbonate).**
Confirmed **functional** on the D4 evidence axis. The sodium they contribute is a
**nutrition-axis (D1) consideration, not a D4 additive-evidence one** — it is already
captured by the sodium nutrition signal and must not be double-counted as an additive
concern. Recorded in the entries so Data does not conflate the two axes.

---

## 4. Carried-forward prototype reconciliation (kept vs changed)

181A marked the W2 prototype tiers **non-authoritative for the expanded set** and required
re-confirmation. Result of re-confirming all 20 against the expanded evidence:

- **KEPT — all 20 prototype tiers unchanged.** Re-confirmation against the 181A evidence
  reproduced every W2 assignment: 6 functional (E330, E300, E415, E440, E410, E412),
  6 likely-neutral (E200–203, E1422, E282, E481, E471, E472e), 4 dose-dependent
  (E450/451, E955, E950, E211), 3 contested (E407, E466, E320), 1 disclosure-gap (E150).
- **CHANGED — none.** No carried-forward tier was moved.
- **Notes on two that were re-examined closely:**
  - **E282 calcium propionate** and **E1422 modified starch** are metabolite-class members
    (endogenous SCFA / carbohydrate) that could argue for `functional`. They were **kept at
    `likely-neutral`** — the more conservative tier — because each carries a (pharmacological-
    dose, resp. labeling-controversy) footnote that, while not a food-safety concern, keeps
    them just shy of the "no asterisk at all" functional bar. This preserves the D7-co-signed
    W2 assignment and avoids an unmotivated upgrade.
  - **E200–203 sorbates** were re-examined against the 2026 NutriNet-Santé T2D association
    and **kept at `likely-neutral`** (single observational cohort, no mechanism, ADI
    unchanged) with the standing reassess-on-replication flag.

The 16 newly-added additives were tiered fresh (§2.B); they had no prior authoritative tier.

---

## 5. Annotate-only / boundary statement (W3 hard boundary)

- **ANNOTATE-ONLY.** These tiers drive **display copy only**. They carry **no headline-grade
  weight** in W3 — no score formula change, no weight, no penalty, no credit was proposed or
  implied. D4 does not enter the headline grade. Letting additives move the grade is a
  separate, future, owner-gated decision (frozen-invariant tripwire #1) and is out of scope.
- **No score moved. No JSON edited. No engine code touched.** Methodology/governance artifact
  only. OFF = byte-identical (inherited from EV-041 / `BARI_GLASSBOX_W2`).
- **Frozen invariants untouched:** milk run_005_headpin, snack 70/B, bread provenance.
- **Every tier cites the 181A curated evidence + EV-043.** No evidence invented; the one
  additive that could not be tiered on its anchor (E141) is `unclassified` with reason, not
  guessed.

---

## 6. Co-sign

**Nutrition D7 co-sign:** 2026-06-04 (authored these 36 tier assignments + the four §4
judgment-call resolutions + the carried-forward reconciliation).

**Product D7 co-sign: CO-SIGNED 2026-06-04 (Product Agent, TASK-181C).** Scope/maintenance
co-sign — annotate-only, authorizes the 36-row tiered set + the maintenance plan for **DISPLAY
only**; does **NOT** authorize D4 to move any headline grade (separate future owner-gated
decision, frozen-invariant tripwire #1).
- **The tiered set is the right set to commit to.** Distribution 19/7/5/3/1/0/1 = 36 reviewed;
  surface is shelf-present additives, not the E-number space (guardrail held). The 0-on-shelf
  bread additives (E282/E481/E472e/E466/E211/E320/E575) and E575 GDL are correctly RETAINED —
  low marginal maintenance cost, detector stays complete when a fuller bread JSON displays.
- **Sustainability:** the maintenance obligation holds via
  `additive_library_maintenance_protocol_v1.md` (TASK-181C) — annual re-verify + quarterly scan
  + 6 trigger events, staleness surfaced on the Command Center, and a Product go/no-go gate with
  a real FREEZE outcome + a demand-revisit checkpoint that carries the bypassed-W2-gate debt
  (TASK-179X closed by owner override without engagement data).
- **Judgment calls — accepted as authored:**
  - **E141 → `unclassified`:** correct. Honest fallback — the *label* discloses E141 fine (so
    not `disclosure-gap`), the *evidence record* lacks a clean single EFSA numeric ADI (so not a
    forced `functional`). US/EU approval divergence correctly routed to a **D5 note, not a D4
    tier move** — jurisdictional approval status is not evidence of harm. The one true fallback.
  - **E960 steviol `dose-dependent` vs E100 curcumin `functional`:** correct split. The
    discriminator — does over-exposure occur at the additive's **shelf-use axis** or a different
    channel — is the right axis. Curcumin's ADI exceedance is supplement-channel (off the
    food-colour axis → context note, `functional`); steviol's MODERATE over-exposure flag sits on
    the **sweetener axis** the additive is used for (children as high consumers → genuine
    use-level signal, `dose-dependent`, consistent with E955/E950). Accepted.

**Registry:** EV-043, `03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md`.

**Proposed task status:** RETURNED for CC close-readiness verification. CC records CLOSED;
Nutrition does not.
