# Magnesium Form-Absorption Ladder + UL Citation Verification — v1 (TASK-504)

**Status: RETURNED (proposed).** Independent per-citation verification of the
magnesium form-absorption ladder + UL claims flagged as unverified in
`01_framework/nutrition/supplement_guides_science_cosign_v1.md` §1.4, ahead of any
guide copy authorship. Evidence only — no product decision, no scoring change, no
copy drafted here.

**Method.** Every PMID resolved independently via `C:\Bari\integrations\clients\literature.py`
(PubMed E-utilities + Europe PMC) and cross-checked for retraction/integrity via
`crossref.py`. Institutional-source values (NIH ODS, EFSA) checked via `WebSearch`
against the primary fact-sheet/opinion text (direct `WebFetch` to `ods.od.nih.gov`
returned HTTP 403 — the site blocks the fetch tool; verification for NIH ODS
therefore rests on search-indexed quotations of the fact sheet's own text plus
cross-reference against a secondary EFSA/IOM literature trail, not a direct fetch of
the live page — flagged as a residual verification gap in §5). No PMID/DOI was
invented; every identifier below is either the one already in the dossier/co-sign or
was found by, and is disclosed as coming from, an independent PubMed/CrossRef lookup.

**Inputs read:** `01_framework/nutrition/supplement_guides_science_cosign_v1.md`,
`bari-web/src/lib/comparisons/magnesium-page-data.ts` (live v3 copy),
`03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml`,
`03_operations/supplement_engine/proto_v0/benchmark/magnesium_model_v3_bioav_adjusted_dose_spec.md`.

---

## 1. Per-citation verification table — form-absorption ladder

Claim under test: **"Organic magnesium salts (citrate, bisglycinate) are absorbed
more completely than magnesium oxide."** This is the claim `magnesium.yaml`
`forms.citations` (lines 64–71) attaches to `PMID:39770988`, `PMID:30761462`,
`PMID:7815675`, tagged `form_ladder_confidence: "medium-high"`.

| # | PMID | Real? | Correctly attributed? | Design / population | Supports the claim as stated? | Tier (this citation alone) |
|---|---|---|---|---|---|---|
| 1 | **39770988** | Yes — resolves to Pajuelo et al. 2024, *Nutrients* 16(24):4367, "Comparative Clinical Study on Magnesium Absorption and Side Effects After Oral Intake of Microencapsulated Magnesium (MAGSHAPE™) Versus Other Magnesium Sources." Not retracted (CrossRef `is_retracted: false`). | Yes, title/year/journal match the dossier's use. **But see finding 1a below — the DOI our own tool returns for this PMID is wrong.** | Human RCT, double-blind crossover, n=40 healthy adults, single-dose plasma Mg over 6h. Compares a proprietary microencapsulated ingredient (Mg-MS/MAGSHAPE™) against MgO, magnesium citrate (Mg-C), and magnesium bisglycinate (Mg-BG). | **Partially — and the bisglycinate result cuts against the ladder as commonly stated.** Per the abstract itself: plasma Mg rose significantly at some timepoints for both MgO and Mg-C, but **"no significant increase in Mg levels was observed upon the intake of Mg-BG"** — i.e., in this specific human trial, bisglycinate did *not* outperform oxide; it showed no measurable plasma response at all. Only the proprietary MAGSHAPE™ ingredient (the product under commercial evaluation) showed a sustained rise across all timepoints. | **Weak, and specifically weak for the bisglycinate leg of the ladder.** See finding 1b (conflict of interest) below — this further discounts using it as clean support. |
| 2 | **30761462** | Yes — resolves to Ates et al. 2019, *Biological Trace Element Research*, "Dose-Dependent Absorption Profile of Different Magnesium Compounds." Not retracted. | Yes, title/year/journal match. | **Animal study — Balb/c mice**, not human ("administered per orally to Balbc mice," three oral doses, tissue/serum Mg measured). No human arm. | Directionally consistent with organic-salt-favors-absorption (citrate, malate vs. others in mice), but it is **preclinical data extrapolated to a human bioavailability-ranking claim.** | **Insufficient as human evidence; Weak at most as mechanistic/preclinical corroboration.** Hard Rule 4 requires flagging animal data explicitly before it supports a human claim — the dossier does not currently carry this flag; the co-sign does not either. |
| 3 | **7815675** | Yes — resolves to Schuette, Lashner & Janghorbani 1994, *JPEN*, "Bioavailability of Magnesium Diglycinate vs Magnesium Oxide in Patients with Ileal Resection." Not retracted. | Yes, title/year/journal match; this is the strongest of the three for a human, isotope-labeled, head-to-head design. | Human RCT, double-blind crossover, **n=12**, and specifically **patients who had undergone ileal resection** (a malabsorptive surgical population), not general healthy adults. | **Only partially, and only in a subgroup.** For the patient group as a whole, ²⁶Mg absorption from diglycinate (chelate) vs. MgO was **not significantly different** (23.5% vs 22.8%). The chelate advantage (23.5% vs 11.8%, p<.05) appeared **only in the four patients with the most severe pre-existing magnesium malabsorption** — not across the full sample. | **Weak-to-Moderate, population-restricted.** Real, well-designed, but n=12, 1994, and the positive finding is confined to a malabsorption subgroup, not a general-population result. Extrapolating "bisglycinate beats oxide" to a healthy Israeli supplement consumer from this study alone overstates what it shows. |

### 1a. Tooling finding — do not publish a DOI for PMID 39770988

Independently pulling this PMID's DOI through our own `literature.py` client
returned `10.1007/BF00226334` — **this is wrong.** Europe PMC and a direct CrossRef
lookup both confirm the real DOI is `10.3390/nu16244367`. Root cause traced to the
raw PubMed XML: this record has an associated PMC full-text article whose
`<ReferenceList>` embeds dozens of its own references' `<ArticleId>` tags nested
inside the same `<PubmedArticle>` element; `literature.py`'s `pubmed_fetch` selects
DOI via a recursive `.//ArticleIdList/ArticleId` search that is not scoped to the
article's own top-level `ArticleIdList`, so it picks up the *last* matching
`ArticleId` in document order — which belongs to an unrelated 1970s-era reference,
not the paper itself. This is the same class of defect the creatine verification
pass found independently for `PMID:28615996` (`creatine_evidence_cosign_v1.md`
precedent, wrong DOI in PubMed's own metadata linkage) — except here the wrong value
originates from our own client's parsing scope, not PubMed's metadata. **Recommend
whoever owns `integrations/clients/literature.py` scope the DOI lookup to
`PubmedData/ArticleIdList/ArticleId` (the record's own IDs) rather than a
document-wide recursive search** — flagged for awareness; not fixed here (out of
Research Agent's lane; no code changes made).
**Net effect on this task: PMID 39770988 itself is real and correctly identified by
PMID; only its DOI (never cited by the dossier or co-sign) was ever at risk of being
wrong, and no DOI has shipped anywhere. If a DOI is ever added to copy for this PMID,
use `10.3390/nu16244367`, verified independently via Europe PMC + CrossRef.**

### 1b. Conflict-of-interest finding — PMID 39770988

Author affiliations (Europe PMC full record): two of five authors (Negra, Connolly)
are affiliated with **Lubrizol Life Science**, a specialty-ingredients manufacturer;
the study evaluates a trademarked microencapsulated magnesium ingredient
(MAGSHAPE™) against generic MgO/citrate/bisglycinate comparators, with the
proprietary ingredient the only one showing a sustained positive result. Per Research
Agent's Source Hierarchy ("do not cite brand-funded studies without noting the
conflict"), this is an **industry-affiliated comparative study** and should be
labeled as such wherever cited, and should **not** be Bari's basis for ranking
bisglycinate against oxide (a comparator arm in someone else's proprietary-ingredient
study, not a study designed to answer Bari's question).

### 1c. What the primary institutional source actually says — and what it does not

The NIH ODS quote reproduced in `magnesium_model_v3_bioav_adjusted_dose_spec.md` §1.2
and the co-sign — **"Forms of magnesium that dissolve well in liquid are more
completely absorbed in the gut than less soluble forms. Small studies have found
that magnesium in the aspartate, citrate, lactate, and chloride forms is absorbed
more completely and is more bioavailable than magnesium oxide and magnesium
sulfate"** — is confirmed as the fact sheet's actual wording via independent search
(quoted verbatim by multiple independent secondary sources indexing the ODS Magnesium
Health Professional Fact Sheet; direct fetch blocked by the site, see Method above).

**The load-bearing nuance: this sentence names aspartate, citrate, lactate, and
chloride. It does not name glycinate or bisglycinate at all.** Bari's `BAV_TIER_FACTORS`
places bisglycinate in the same HIGH (factor 1.0) tier as citrate, and consumer copy
already states them as an equal pair ("ציטראט וביסגליצינט נספגים טוב יותר מאוקסיד" —
magnesium-page-data.ts line 87). That pairing is not wrong as a *directional*
statement — bisglycinate's absorption-via-dipeptide-transport mechanism is a real,
separately-documented physiological pathway (the basis of PMID 7815675's chelate
hypothesis) — but it is resting on a **different and thinner evidentiary base than
citrate's**, not on the same NIH ODS sentence the copy's framing implies. Citrate has
a direct institutional-source name-check; bisglycinate's support is one small,
population-restricted 1994 human study (subgroup-only positive) plus a 2024 study in
which bisglycinate specifically failed to show a significant plasma response.

---

## 2. Per-citation verification table — UL / safety claims

| Claim in dossier/copy | Source named | Verified? | Correct as stated? | Tier |
|---|---|---|---|---|
| Hard veto / grade-ceiling line: **350 mg/day supplemental elemental Mg** | NIH ODS / US IOM-FNB (`magnesium.yaml` `safety_citations`, tagged `NEEDS-ENV-VERIFY`) | **Yes.** Independently confirmed: the 1997 US Institute of Medicine (IOM) Dietary Reference Intake report set the supplemental-magnesium UL for adults at 350 mg/day, diarrhea as the limiting/critical effect — this figure is what the current NIH ODS Health Professional Fact Sheet still states. | **Correct, and correctly framed as GI-tolerance (diarrhea), not systemic toxicity** — matches the dossier's `ul_governing_decision` framing exactly. | **Strong** — a stable, long-standing, correctly-cited institutional reference value. Recommend the `NEEDS-ENV-VERIFY` tag be cleared for the *value* (350 mg, IOM/NASEM, diarrhea-based); a live re-fetch of the current ODS page text is still worth doing before ship since direct `WebFetch` to `ods.od.nih.gov` is blocked in this environment (see §5). |
| Soft note line: **250 mg/day supplemental elemental Mg** | EFSA (`magnesium.yaml` `ul_note_threshold`, `safety_citations`, tagged `NEEDS-ENV-VERIFY`) | **Yes, the value.** Independently confirmed: the EU Scientific Committee on Food (SCF) 2001 opinion derived a NOAEL of 250 mg/day (mild, transient osmotic-laxative effect) and set the UL at 250 mg/day for readily-dissociable supplemental magnesium salts; this was reaffirmed in the EFSA NDA Panel's 2015 "Scientific Opinion on Dietary Reference Values for magnesium." | **Value correct; framing correct (GI-tolerance/osmotic-diarrhea NOAEL, not toxicity) — matches the dossier exactly.** | **Strong** for the value and framing. |
| **Live copy's specific year attribution: "EFSA (2021)"** — appears twice in `magnesium-page-data.ts` (lines 156, 197: `"EFSA (2021) קבעה ש-250 מ"ג..."`) and twice more without the parenthetical year but referencing the same figure (lines 152, 193) | *(none given beyond "EFSA, 2021")* | **Could not verify.** Three independently-worded searches for an EFSA magnesium UL/opinion dated 2021 returned nothing. The two primary dates that consistently surface are **2001** (original SCF opinion establishing 250 mg/day) and **2015** (EFSA NDA Panel reaffirmation in the magnesium DRV opinion). No 2021 EFSA magnesium opinion was found. | **Likely a wrong year already shipped in live copy.** This is not a form-ladder PMID, but it is squarely a "UL claim" per this task's scope, and it is copy already on the live page, not draft guide copy. | **Flag for correction, not a tier question** — the underlying number (250 mg) and institutional attribution (EFSA) are both correct; only the specific year "2021" is unverifiable and should not be asserted. Recommend citing as "EFSA (2001/2015)" or dropping the year entirely rather than naming an unverifiable one — an unverifiable specific year is worse for credibility than no year, per the citation-fabrication gate this task exists to enforce. |

---

## 3. Bonus cross-check — citation already live in copy (Cochrane cramps null)

Not in this task's named scope but directly adjacent (same page, same
citation-fabrication-gate logic, cheap to verify): `magnesium-page-data.ts` line 308
and the `structure_function_umbrella` mapping both cite **PMID:32956536** for "no
clinically meaningful cramp relief" (Cochrane). Independently verified: real,
resolves to Garrison et al. 2020, *Cochrane Database of Systematic Reviews*,
"Magnesium for skeletal muscle cramps" (Meta-Analysis, Systematic Review), not
retracted, correctly year-stamped ("קוקריין 2020" in copy matches the 2020
publication date exactly). **This one is clean — VERIFIED-primary, correctly
attributed, correctly framed as a null finding.** Included as a positive control:
the verification method above catches real problems (§1, §2) without flagging
everything as suspect.

---

## 4. Bonus cross-check — chemistry identities (pubchem)

`magnesium.yaml`'s `compound_forms_identity` block (CIDs, formulas, molecular
weights, elemental fractions) underlies every product's on-page "compound mass ↔
elemental mg" line in `magnesium-page-data.ts` (e.g., "תרכובת: ~862 מ"ג אוקסיד
מגנזיום... 520 מ"ג מגנזיום יסודי"). Verified independently via
`integrations/clients/pubchem.py`:

| Form | Dossier CID | PubChem CID | Dossier formula/MW | PubChem formula/MW | Elemental fraction check |
|---|---|---|---|---|---|
| Magnesium oxide | 14792 | 14792 ✓ | MgO / 40.305 | MgO / 40.305 ✓ | 24.305/40.305 = 0.6031 ≈ dossier's 0.603 ✓ |
| Magnesium citrate | 6099959 | 6099959 ✓ | C₁₂H₁₀Mg₃O₁₄ / 451.12 | C₁₂H₁₀Mg₃O₁₄ / 451.12 ✓ | 3×24.305/451.12 = 0.1617 ≈ dossier's 0.162 ✓ |
| Magnesium glycinate/bisglycinate | 84645 | 84645 ✓ (both name variants resolve to the same CID) | C₄H₈MgN₂O₄ / 172.42 | C₄H₈MgN₂O₄ / 172.42 ✓ | 24.305/172.42 = 0.1410 ≈ dossier's 0.141 ✓ |

**Clean.** All three chemical identities and elemental-fraction figures that feed the
consumer-facing compound-mass math are correct.

---

## 5. What is cleared for use vs. what needs softening or dropping

### Cleared for use as-is
- **NIH ODS institutional quote** ("forms that dissolve well... aspartate, citrate,
  lactate, chloride... more bioavailable than oxide and sulfate") — independently
  confirmed as the fact sheet's real wording; safe to quote/paraphrase, and it is the
  strongest single piece of support Bari has for the directional claim. Note the
  direct `WebFetch` to the live page returned HTTP 403 in this environment — treat as
  **confirmed via independent secondary corroboration, not a first-party page fetch**,
  and re-confirm with a direct fetch (different tool/session) before this exact
  quote appears verbatim as a "quoted" citation in shipped copy, per the same
  discipline the creatine cosign applied to its own NIH ODS no-UL claim (ship-gate
  item, not a blocker).
- **UL = 350 mg/day (NIH/IOM/NASEM), diarrhea-based** — verified value and framing.
- **UL-soft-note = 250 mg/day (EFSA), osmotic-diarrhea NOAEL, not toxicity** —
  verified value and framing.
- **Citrate absorbs better than oxide (directional, Moderate tier)** — supported by
  the NIH ODS institutional statement; keep as a Moderate, hedged, directional claim
  exactly as the co-sign already framed it. Do not attach an effect-size percentage.
- **Cochrane 2020 cramps-null (PMID 32956536)** — already clean, no action needed.
- **Chemical identities / elemental-fraction math (pubchem-verified)** — safe as-is.

### Needs softening
- **"Bisglycinate absorbs as well as citrate" framing** — the specific PMID support
  for bisglycinate (7815675: population-restricted subgroup finding in n=12
  ileal-resection patients; 39770988: no significant response in the one modern
  healthy-population human trial) is thinner and more mixed than citrate's. Recommend
  the guide keep bisglycinate in the same practical HIGH-absorption *tier band* for
  scoring purposes (the existing calibration-constant architecture explicitly does
  not claim individual absorption percentages, which insulates it from this specific
  finding), but if guide *copy* ever singles out bisglycinate with a "well-absorbed"
  claim independent of the tier badge, it should be hedged as "considered
  well-absorbed via a distinct chelate-transport mechanism" rather than stated with
  the same confidence as the citrate claim, and should not cite PMID:39770988 or
  PMID:30761462 as support for that specific sentence.
- **PMID:30761462 (mouse study)** — usable only as flagged preclinical/mechanistic
  background, never as human evidence, per Hard Rule 4. If retained in the dossier at
  all, its citation should carry an explicit "(animal study)" qualifier — it
  currently does not.
- **PMID:39770988** — if cited in any future copy or dossier update, must disclose
  the Lubrizol Life Science co-authorship (conflict of interest) and should not be
  used to support a bisglycinate-superiority claim, since its own bisglycinate arm
  was null.

### Needs dropping / correcting
- **"EFSA (2021)" in live `magnesium-page-data.ts`** (lines 152, 156, 193, 197) —
  no EFSA magnesium-UL opinion dated 2021 was found across independent searches; the
  real primary dates are 2001 (SCF) and 2015 (EFSA NDA Panel reaffirmation). This is
  copy already shipped, not draft guide copy — flagging for whoever owns that file's
  next edit (Content/Nutrition), since it falls inside this task's named UL-claims
  scope. Recommend "EFSA" with no year, or "EFSA (2001/2015)," not "EFSA (2021)."
- **`magnesium.yaml` `forms.citations` "medium-high" confidence label** — on the
  evidence actually behind these three specific PMIDs (one animal study, one
  population-restricted 12-patient subgroup finding, one industry-affiliated study
  whose bisglycinate arm was null), "medium-high" overstates what the three PMIDs
  themselves show. The **directional claim as a whole** is still reasonably placed at
  Moderate because the independent NIH ODS institutional statement carries real
  weight on its own — but that weight rests on the NIH quote, not on these three
  PMIDs, and the dossier's confidence label should not imply otherwise. Recommend the
  dossier's `form_ladder_confidence` field be split or annotated: Moderate for the
  NIH-named forms (citrate, aspartate, lactate, chloride), Weak-to-Moderate and
  population-qualified for bisglycinate/glycinate specifically. This is a Nutrition
  Agent dossier-annotation call, not something Research is authorized to edit.

---

## Constraints compliance

- No PMID, DOI, product fact, or dose value invented anywhere in this report. Every
  identifier verified is either the one already in the dossier/co-sign, or is
  disclosed explicitly as independently found (the corrected DOI for PMID 39770988,
  §1a).
- Every claim above carries an evidence tier (Strong/Moderate/Weak/Insufficient) or
  an explicit "verified value, flag on attribution" designation — none stated as
  fact without a tier.
- Animal data (PMID:30761462) flagged explicitly, not silently extrapolated to a
  human claim, per Hard Rule 4.
- Conflict of interest disclosed for PMID:39770988 (Lubrizol Life Science
  co-authorship), per the Source Hierarchy's brand-funded-study rule.
- No product recommendation made; no scoring rule touched; no consumer copy
  drafted — only a cleared/needs-softening/needs-dropping classification of
  existing claims and citations, per this task's evidence-only mandate.
- Open Food Facts not used, referenced, or considered anywhere in this report.
- No subagents spawned.
- This is a consult/verification response (RETURNED), not a build. Does not close
  TASK-504.

---

## Return Contract

```json
{
  "task": "TASK-504",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/research/magnesium_form_ladder_verification_v1.md",
      "action": "created",
      "sha256": "a0203f1192b263dd972a5b38e69fc7833289c3d1fa6e06b7809022c357467cf3 — computed pre-this-edit (self-referential: embedding a hash changes the file's own hash by one edit, same caveat as supplement_guides_science_cosign_v1.md's return block). Re-verify with `sha256sum C:\\Bari\\03_operations\\reports\\research\\magnesium_form_ladder_verification_v1.md` at read time."
    }
  ],
  "counts": {
    "form_ladder_pmids_verified_real": "3/3 (source: independent PubMed efetch via literature.py for PMID:39770988, PMID:30761462, PMID:7815675 — all three resolve to real, non-retracted papers matching the dossier's title/year/journal attribution)",
    "form_ladder_pmids_supporting_claim_as_stated_without_caveat": "0/3 (source: §1 table — PMID:39770988's bisglycinate arm was null + industry co-authorship; PMID:30761462 is animal-only; PMID:7815675's positive result is confined to a 4-patient malabsorption subgroup within n=12; denominator = 3 form-ladder PMIDs named in the co-sign)",
    "ul_values_verified_correct": "2/2 (350 mg NIH/IOM supplemental veto line; 250 mg EFSA supplemental soft-note line — both independently confirmed via WebSearch cross-reference against IOM 1997 DRI report content and EFSA SCF 2001 / NDA Panel 2015 opinion content; denominator = 2 UL figures in magnesium.yaml safety block)",
    "ul_citations_with_attribution_defect_found": "1/1 (live copy's 'EFSA (2021)' year attribution in magnesium-page-data.ts, 4 occurrences across 2 distinct sentences — no EFSA magnesium UL opinion dated 2021 found in 3 independent searches; denominator = 1 distinct attribution claim checked)",
    "retracted_papers_found": "0/4 (source: crossref.get_doi is_retracted field, checked for all 4 PMIDs fetched including the bonus Cochrane cross-check)",
    "animal_only_studies_among_form_ladder_citations": "1/3 (PMID:30761462, Balb/c mice — source: PubMed abstract text 'administered per orally to Balbc mice'; denominator = 3 form-ladder PMIDs)",
    "conflict_of_interest_flags_raised": "1/3 (PMID:39770988 — 2 of 5 authors affiliated with Lubrizol Life Science per Europe PMC author-affiliation record; denominator = 3 form-ladder PMIDs)",
    "pubchem_chemical_identities_cross_checked": "3/3 (magnesium oxide CID 14792, magnesium citrate CID 6099959, magnesium glycinate/bisglycinate CID 84645 — all CIDs, formulas, molecular weights, and elemental fractions match the dossier exactly; denominator = 3 compound forms in magnesium.yaml compound_forms_identity)",
    "bonus_live_citation_cross_checked": "1/1 (PMID:32956536, Cochrane cramps review — verified clean, correctly attributed, correctly year-stamped in live copy; denominator = 1 additional already-shipped citation checked as a positive control)",
    "fabricated_or_invented_identifiers_found": "0/0 (none invented by Research in this report; one tooling-side wrong DOI found and disclosed for PMID:39770988, root-caused to literature.py's own parsing scope, not a fabrication by any agent)",
    "claims_cleared_for_use_as_is": "5 (NIH ODS quote pending one direct-fetch reconfirmation, UL=350 NIH/IOM, UL-soft-note=250 EFSA, citrate>oxide directional Moderate claim, Cochrane cramps-null, chemistry/elemental-fraction math — source: §5 'Cleared for use' list)",
    "claims_needing_softening": "3 (bisglycinate-equals-citrate absorption framing, PMID:30761462 animal-data qualifier, PMID:39770988 COI disclosure requirement — source: §5 'Needs softening' list)",
    "claims_needing_dropping_or_correcting": "2 ('EFSA (2021)' year attribution in live copy; magnesium.yaml's 'medium-high' form_ladder_confidence label as currently undifferentiated between citrate and bisglycinate support — source: §5 'Needs dropping/correcting' list)"
  },
  "commands_run": [
    {"cmd": "python -c \"from integrations.clients.literature import pubmed_fetch; pubmed_fetch(['39770988','30761462','7815675','32956536'])\"", "exit_code": 0},
    {"cmd": "python -c \"from integrations.clients.literature import europepmc; europepmc('MAGSHAPE magnesium microencapsulated absorption')\"", "exit_code": 0},
    {"cmd": "python -c \"from integrations.clients.crossref import get_doi; get_doi(...)\" (4 DOIs checked for retraction status)", "exit_code": 0},
    {"cmd": "python -c \"from integrations.clients.http import get; ...\" (raw PubMed efetch XML inspection for PMID 39770988 ArticleId scoping bug)", "exit_code": 0},
    {"cmd": "python -c \"from integrations.clients.http import get_json; ...\" (Europe PMC author-affiliation lookup for PMID 39770988)", "exit_code": 0},
    {"cmd": "python -c \"from integrations.clients.pubchem import get_compound; ...\" (4 compound-identity lookups: magnesium oxide, magnesium citrate, magnesium glycinate, magnesium bisglycinate)", "exit_code": 0},
    {"cmd": "WebFetch https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/", "exit_code": 1, "note": "HTTP 403 — site blocks the fetch tool; substituted with WebSearch cross-reference, disclosed as a residual gap in §5"},
    {"cmd": "WebSearch NIH ODS magnesium absorption-by-form quote + UL 350mg", "exit_code": 0},
    {"cmd": "WebSearch EFSA magnesium UL 250mg SCF 2001 / 2015 opinion", "exit_code": 0},
    {"cmd": "WebSearch EFSA magnesium 2021 opinion (checking the live copy's year attribution)", "exit_code": 0}
  ],
  "not_done": [
    "Direct WebFetch confirmation of the live NIH ODS page text — blocked by HTTP 403 in this environment; confirmed instead via independent secondary-source corroboration of the exact quoted sentence. Recommend a direct re-fetch (different tool/session/IP) before the verbatim NIH quote ships as a cited blockquote in guide copy.",
    "Full-text retrieval of PMID:39770988's funding/COI statement — MDPI blocked WebFetch (403); the conflict-of-interest finding rests on Europe PMC's structured author-affiliation data (Lubrizol Life Science), which is sufficient to raise the flag but a full-text funding-statement quote was not obtained.",
    "Verification of the blood-pressure-claim citations (PMID:27402922, 41000008, 39519450, 22318649, 12160191) reused by the structure_function_umbrella for the עייפות/fatigue Hebrew-label mapping — explicitly out of this task's named scope (form-absorption ladder + UL only); flagged as a candidate follow-up task if that claim path also heads toward consumer guide copy.",
    "No fix applied to the literature.py DOI-scoping bug found in §1a — disclosed for whoever owns integrations/clients, not fixed here (Research Agent builds nothing).",
    "No edit made to magnesium.yaml's form_ladder_confidence label or magnesium-page-data.ts's EFSA(2021) attribution — both flagged as findings for Nutrition/Content to action, not edited by Research."
  ],
  "self_check": "Acceptance test: identify every citation behind the magnesium form-absorption ladder and UL claims (from the co-sign, page data, and model files), independently verify each against PubMed/CrossRef and the NIH ODS/EFSA institutional record, flag any that are missing/wrong-attributed/weaker-than-claimed/unverifiable with an honest tier and a consumer-safe framing recommendation, and never invent an identifier. Result: PASS. All 3 form-ladder PMIDs plus the 2 UL institutional values were independently verified real/correct; none of the 3 form-ladder PMIDs support the stated claim cleanly on inspection (one animal-only, one population-restricted subgroup result, one industry-affiliated study with a null bisglycinate arm) and this is stated plainly rather than smoothed over; the NIH ODS quote itself is confirmed accurate and is identified as the actual load-bearing support, with the specific nuance that it names citrate/aspartate/lactate/chloride but not bisglycinate/glycinate; a live copy attribution error ('EFSA 2021') was caught as a bonus finding squarely inside the UL-claims scope; a positive-control citation (Cochrane PMID:32956536) verified clean, demonstrating the method isn't reflexively flagging everything; a tooling bug (wrong DOI resolution for PC-linked PubMed records) was found, root-caused, and disclosed without being fixed (out of lane) or hidden. No PMID/DOI/product fact invented. No scoring change, no copy drafted, no subagents spawned, OFF not used. Task not closed."
}
```
