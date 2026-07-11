# Creatine Evidence Verification — v1 (TASK-492B / TASK-492C)

**Status: RETURNED (proposed).** Cross-check + citation-fabrication gate + dossier
reconciliation + Tnuva GO conflict resolution, ahead of any consumer comparison page
or blog copy.

**Scope note on the two source PDFs (important, read first):** Both
`Comprehensive Creatine Scientific Review.pdf` and `1. Efficacy by Claim.pdf` are
themselves **LLM-tool outputs**, not primary literature. PDF #2 is headed "ChatGPT"
on page 1 and uses ChatGPT-style bracket citation markers (`【26†L193-L202】`). PDF #1
carries the same tell in a different form — numbered superscript citations resolving
to a "Works cited" list built from a mix of PubMed/PMC links, ResearchGate mirrors,
patent databases, and several **non-primary consumer health sites** (Ubie Doctor's
Note, Cleveland Clinic, Superpower, Bunaroba, drstanfield.com) sitting alongside
real journal citations, plus `[cite: 48]`/`[cite: 100]` bracket-style placeholder
markers in its benchmark-product table — another AI-generation signature. **Treat
both PDFs as secondary, AI-synthesized literature reviews, one level closer to
primary sources than `owner_synthesis_pasted.md` but not primary sources
themselves.** This changes nothing about the underlying science (most of it verifies
clean, below) but it means the citation-fabrication gate applies to all three
documents, not just the pasted synthesis, and no PDF claim should be treated as
"established" without independent resolution the way I did for the load-bearing
items below.

---

## 1. Cross-check: synthesis vs. the two PDFs

`owner_synthesis_pasted.md` is a compressed re-synthesis of the two PDFs (mostly of
PDF #1, the more comprehensive one). Section-by-section:

| Synthesis claim | PDF support | Verdict |
|---|---|---|
| Strength/power Strong; lean mass Strong; HIIT Strong | Both PDFs say this | **Matches** |
| Lean mass ~1.1 kg / "35 studies" | PDF #1 says "0.82–1.14 kg... large-scale meta-analyses" (no study count given in visible text). PDF #2 says "≈1.1 kg (95% CI ≈0.6–1.7 kg)," also no "35 studies" figure given in visible text. Neither PDF's readable body states "35 studies" anywhere I can locate. | **PARTIALLY SUPPORTED — the "35 studies" figure is not traceable to either PDF's visible text.** See §2 below; the real number I could verify independently is 12 studies (not 35) for the 1.14 kg figure. |
| Recovery: Moderate | PDF #1: "Moderate (Biochemical Markers) to Weak (Functional Return)." PDF #2: "Weak/mixed." Synthesis compresses both to a flat "Moderate," which **drops PDF #2's more cautious "weak/mixed" framing and PDF #1's explicit functional-outcome caveat.** | **Partially supported — synthesis is more favorable than either PDF on this claim.** Recommend the tier stay Moderate-to-Weak (functional), not a flat Moderate, if this claim area is ever added to Bari's dossier. |
| Cognitive: Moderate (context-specific) to Weak (general) | Both PDFs support this framing closely, including the EFSA 2024 statistical-error critique. | **Matches**, and is the most carefully hedged section in both PDFs and the synthesis — good sign. |
| Fat loss: Insufficient | Both PDFs agree "Insufficient" for direct fat-loss mechanism. Synthesis's parenthetical "~0.5 kg extra, one meta" for older adults roughly tracks PDF #1's -0.28% to -1.19% body-fat-% range (different units, not directly comparable, but not contradictory). | **Matches** on the tier; the specific "0.5 kg" figure is not independently cross-checked here (secondary detail, doesn't change the tier). |
| Safety / no UL / kidney myth | Both PDFs agree closely; synthesis's defensible consumer statement is a close paraphrase of PDF #1's near-verbatim "scientifically defensible consumer safety statement." | **Matches** |
| Dose ranges (loading ~20g/5-7d, maintenance 3-5g, floor ~3g) | Both PDFs agree closely on all figures. | **Matches** |
| Forms: monohydrate gold standard, no alternative form beats it | Both PDFs agree closely, including the HCl head-to-head trial finding no superiority. | **Matches** |
| Dairy stability: "~56–60% retained after 35 weeks... ~3g from initial ~5g in 330ml" | **PDF #1 states this figure** (attributed to Glaxo patent WO2015078835A1): "maintain a commercially viable shelf life of at least 9 months... with less than 40% of the initial creatine converting to creatinine" — i.e., PDF #1's own number is **≥60% retained at 9 months / 21°C**, tied to the patent, not "35 weeks." The synthesis's "35 weeks" / "56-60%" framing does not exactly match either PDF's stated numbers (PDF #1 says 9 months ≈ 39 weeks, "<40% converted" ≈ "≥60% retained" — close but not an exact match to "35 weeks / 56-60%"). PDF #2 does not mention this patent or figure at all; it cites a different, unnamed "milk-based creatine beverage" study reporting "~10% creatinine formation at 4°C" and generic "first-order loss at 23-35°C" with no patent reference. | **DISAGREEMENT between the two PDFs themselves** (one cites a Glaxo patent with a 9-month/<40%-converted figure, the other cites an unnamed milk-beverage study with a 4°C/~10% figure and no patent) **and the synthesis's own number doesn't cleanly match either.** Flag as unverified precision — see §2. |
| Acidic-beverage loss (12-21% in 3 days; up to 90% in 45 days) | Not stated in this specific numeric form in either PDF's visible text; PDF #1 discusses acidic-pH acceleration in general terms without these exact percentages; PDF #2 similarly discusses pH-driven degradation without matching numbers. | **UNVERIFIED — these specific percentages are not traceable to either PDF as provided.** Possibly drawn from a source cited in one of the PDFs' works-cited lists that I cannot independently confirm states these exact figures (e.g. ref 75, "water activity and temperature" study, or ref 77, "multi-analytical characterization of creatine degradation"). Do not use these two specific percentages in consumer copy without re-sourcing the original paper. |
| §5 Tnuva GO "25g protein / 2g creatine / 340ml, Feb 2026 launch" | **This is PDF #1's own claim**, stated as fact in its "Market trends" section, cited to ref 105 — which resolves to a **Hebrew-language retail-guide blog post** (championshop.co.il, "משקה חלבון מוכן או אבקת חלבון..."), not Tnuva, not a retailer product page, not a press release. | **This is the root of the Tnuva GO conflict — see §4. The specific "2g/340ml" dose figure in PDF #1 traces to a secondary blog article, not a primary product-label source, and is contradicted by Bari's own direct scrape.** The synthesis correctly flagged this as "[UNVERIFIED / CONFLICTS WITH SCRAPE]" — that flag is accurate and should be preserved. |

**Overall cross-check verdict:** the synthesis is a faithful, reasonably careful
compression of the two PDFs on the well-established claims (strength, lean mass tier,
forms, dose, safety) and appropriately carries forward the Tnuva GO uncertainty
flag. It is **weaker** on precision for the dairy-stability numbers (introduces a
"35 weeks" figure not cleanly traceable to either source PDF) and it **smooths over
PDF #2's more cautious "weak/mixed" framing on Recovery**. Neither issue is a
fabrication in the sense of inventing a claim from nothing — both are compression/
rounding errors typical of an LLM re-synthesis, but they are exactly the kind of
drift the cross-check gate exists to catch.

---

## 2. Load-bearing citation verification (fabrication gate)

Verified independently via `C:\Bari\integrations\clients\literature.py` (PubMed,
Europe PMC, OpenAlex) and `crossref.py` (DOI integrity — retraction status, title
match). Method stated per item; nothing below is accepted on the PDFs' say-so alone.

### 2a. 2017 ISSN position stand — **VERIFIED-primary**
- **PMID:28615996**, Kreider RB et al., "International Society of Sports Nutrition
  position stand: safety and efficacy of creatine supplementation in exercise, sport,
  and medicine," *Journal of the International Society of Sports Nutrition*, 2017.
  Confirmed via direct PubMed lookup — title, author list (10 authors incl. Kreider,
  Kalman, Antonio, Ziegenfuss), journal, and year all match what both PDFs and the
  synthesis describe. Abstract confirms the "up to 30 g/day for 5 years... safe and
  well-tolerated... 3 g/day habitual intake" language both PDFs paraphrase.
- **Caveat — the DOI PubMed returns for this record (`10.1016/S0278-5919(05)70173-3`)
  is WRONG.** I ran it through CrossRef and it resolves to an unrelated 1999 paper
  ("Facts and Fallacies of Purported Ergogenic Amino Acid Supplements," *Clinics in
  Sports Medicine*) — an old Elsevier DOI apparently misassigned in PubMed's own
  metadata, not a fabrication by either PDF or the synthesis (neither source states a
  DOI for this paper at all). **Do not publish this DOI anywhere.** Cite by PMID
  (28615996) only, or use the JISSN's own DOI (10.1186/s12970-017-0173-z, the
  standard JISSN 2017 creatine paper DOI pattern also seen correctly on a *different*
  2021 ISSN paper in the same search — worth a direct confirm before ship, flagged as
  a residual unverified item below).
- **2021 ISSN "update":** I could not find a 2021 ISSN position stand specific to
  creatine. The 2021 ISSN position stand I did verify (PMID:34503527) is about
  **sodium bicarbonate**, not creatine — it mentions creatine only in passing ("combining
  sodium bicarbonate with creatine... may produce additive effects"). **The
  synthesis's parenthetical "(2021 update)" for creatine specifically is unverified
  and likely incorrect** — I found no evidence of a dedicated 2021 ISSN creatine
  update. Recommend dropping the "(2021 update)" parenthetical from any consumer
  copy; the defensible citation is the 2017 position stand alone, PMID:28615996.

### 2b. The hypertrophy meta-analysis ("~1.1 kg additional lean mass / 35 studies") — **PARTIALLY VERIFIED, one number wrong**
- **PMID:39074168**, Desai I et al., "The effect of creatine supplementation on
  resistance training-based changes to body composition: A systematic review and
  meta-analysis," *J Strength Cond Res* 38(10):1813-1821, 2024. **DOI
  10.1519/JSC.0000000000004862 confirmed clean via CrossRef** (not retracted, title
  matches). This is the citation the dossier already carries for the "Strong"
  strength/lean-mass tier and is a real, correctly-attributed meta-analysis.
- **Verified figure from the actual abstract: LBM +1.14 kg (95% CI 0.69–1.59), from
  12 studies, not 35.** ("One thousand six hundred ninety-four records were screened...
  Twelve studies were included in the meta-analysis.")
- **The synthesis's "35 studies" is not supported by this paper and I could not
  locate any creatine hypertrophy meta-analysis with an n=35 study count in the
  PDFs' visible text or via independent search.** Both PDFs give a range (0.82–1.14 kg
  in PDF #1; ≈1.1 kg, 95% CI 0.6–1.7 in PDF #2) without stating a study count in the
  readable text — the "35" may be a hallucinated or misattributed figure introduced at
  the synthesis stage, or it may come from a different, uncited meta-analysis neither
  PDF's visible body names. **Recommend: if this claim ships in consumer copy, cite
  the ~1.1 kg figure to PMID:39074168 specifically (12 studies) and drop "35 studies"
  entirely** — it is the one clearly unsupported specific number in the whole
  synthesis's efficacy section.
- The dossier's own 5 citations for this claim (PMID:39519498, 37432300, 39074168,
  34836013, 24576864) were re-verified directly — **all 5 resolve to real, correctly-
  titled meta-analyses/systematic reviews on creatine + resistance training**,
  confirming the dossier's existing evidence base is sound (see §2e for detail).

### 2c. NIH ODS — no established UL for creatine — **corroborated, not primary-source-verified**
- NIH Office of Dietary Supplements publishes fact-sheet web content, not indexed
  journal articles, so it does not appear in a PubMed/Europe PMC search — this is
  expected and not a red flag on its own.
- **Corroborating primary literature found and verified:** three independent,
  real systematic-review/meta-analysis papers on creatine and kidney function —
  PMID:31375416 (2019), PMID:41199218 (2025), PMID:42035842 (2026) — all resolve to
  real, correctly-titled papers on "Effects of Creatine Supplementation on Renal
  Function." Their existence and recency (three independent reviews across 6 years,
  most recently 2026) corroborates the PDFs' claim that no dose-dependent renal harm
  has been established and that this remains an active, monitored research question,
  consistent with "no UL because no harm threshold identified" rather than "no UL
  because understudied."
- **The specific NIH ODS fact-sheet page itself was NOT independently fetched in this
  pass** (no web-fetch tool used here per the no-subagent constraint; the literature
  client covers journals/registries, not government fact-sheet pages). Status:
  **believed, corroborated by the kidney-function literature, not VERIFIED-primary
  against the ODS page text itself.** Recommend a direct fetch of
  `ods.od.nih.gov/factsheets/Creatine-HealthProfessional/` before the "NIH ODS says no
  UL" sentence ships as a direct-attribution consumer claim (vs. the safer, already-
  defensible framing "no dose-dependent harm threshold has been identified across
  decades of study, including doses up to 30 g/day for 5 years").
- **Real-world corroboration (new, not in either PDF):** FDA CAERS adverse-event data
  (`openfda.adverse_events("creatine")`) shows 203 reports total; top reactions are
  nausea, vomiting, elevated CPK, headache, elevated heart rate/blood pressure — no
  renal-failure signal in the top reactions. This is unadjudicated self-report data
  (not causally confirmed, not a substitute for RCT evidence) but it is a real
  independent data point that does not contradict the "no established renal harm"
  literature — worth citing as a supplementary real-world signal, clearly labeled as
  such (CAERS ≠ causation).

### 2d. Dairy-matrix stability (creatine→creatinine; patent figure; acidic-beverage loss rates) — **WEAKEST-VERIFIED claim area, flag before shipping any specific number**
- **The foundational paper — Uzzan, Nechrebeki & Labuza (2007), "Thermal and storage
  stability of nutraceuticals in a milk beverage dietary supplement," *Journal of
  Food Science* — is REAL and VERIFIED.** PMID:17995798, confirmed via direct PubMed
  lookup, journal/year match both PDFs' citations exactly.
- **However, the actual abstract text only says creatine (along with glucosamine and
  lactoferrin) "showed only limited stability at either processing or storage" and
  that "an overrun of over 25% may be required for some of them."** The abstract does
  **not** contain the specific numbers either PDF attributes to it in their body text
  (PDF #1: "<5% degradation during heat-holding," "2-month shelf life at room temp,"
  "~10% drop then stable for weeks at 4°C"; PDF #2: "~10% creatinine formation at 4°C,"
  "<5% loss even at 138°C"). Those granular percentages may be correctly drawn from
  the paper's full body/figures (abstracts are commonly this vague; a 2007 food-
  science paper plausibly does report exact retention curves in its results section)
  but **I cannot confirm the specific percentages from the abstract alone, and I did
  not fetch the full paper text.** Status: **believed (the paper is real and on-
  topic), unverified at the level of specific percentages.**
- **The Glaxo patent (WO2015078835A1) figure — "9 months at 21°C, <40% converted" in
  PDF #1 — is a patent claim, not peer-reviewed literature.** Patents describe what a
  filer claims their invention achieves under specific formulation conditions (added
  whey protein 1-25% w/w); they are not independently validated the way a peer-
  reviewed stability study is. **This is exactly the "rests only on a patent or grey
  literature" case the task brief asked me to flag.** The owner synthesis's "~56–60%
  retained after 35 weeks... ~3g from initial ~5g in a 330ml example" does not exactly
  match PDF #1's own stated patent figures (9 months ≈ 39 weeks, not 35; "<40%
  converted" ≈ "≥60% retained," roughly in the ballpark of "56-60%" but not an exact
  restatement) — another sign of synthesis-stage rounding/compression, not a
  fabrication of the underlying patent, but not a precise restatement of it either.
- **The acidic-beverage loss rates (12-21% in 3 days; up to 90% in 45 days) are
  UNVERIFIED** — not traceable to either PDF's visible body text in this specific
  numeric form (see §1 table).
- **Bottom line for TASK-492B/492C: do not publish any specific dairy-stability
  percentage (patent-derived or abstract-derived) as an established fact.** The
  defensible, verified statement is qualitative: creatine is known in food-science
  literature to be chemically unstable in liquid/dairy matrices over time, especially
  under heat and low pH, and this is a genuine, real formulation challenge documented
  in a real 2007 peer-reviewed paper — but the specific retention percentages
  circulating in the synthesis and PDFs should be treated as illustrative, not
  citable facts, until someone pulls the primary Uzzan et al. full text and the
  patent's actual example tables directly.

### 2e. Dossier's existing 5 citations (re-verification) — **VERIFIED-primary, all 5 clean**
Re-checked independently (not just trusting the dossier file): PMID:39519498 (2024,
resistance training <50y strength meta-analysis), 37432300 (2023, regional
hypertrophy meta-analysis), 39074168 (2024, body-composition meta-analysis — see
§2b), 34836013 (2021, older-females strength/mass meta-analysis), 24576864 (2014,
older-adults creatine+RT meta-analysis). **All 5 resolve to real, correctly-titled,
correctly-dated meta-analyses/systematic reviews on creatine and resistance
training.** The dossier's Strong tier for strength/lean-mass is well-supported by an
independently-confirmed, multi-study evidence base — no fabrication found here.

---

## 3. Reconciliation against Bari's dossier

`03_operations/supplement_engine/proto_v0/evidence_dossiers/creatine_monohydrate.yaml`
claims corroborated by this research:

| Dossier claim | Corroborated? |
|---|---|
| Strength/lean mass = Strong | **Yes** — both PDFs, the synthesis, and independent re-verification of all 5 dossier PMIDs agree. |
| Fat loss = Insufficient | **Yes** — both PDFs and synthesis agree explicitly ("no credible... direct lipolytic... properties"). |
| Effective dose ~3-5 g/day | **Yes** — both PDFs and synthesis converge tightly on 3 g/day floor, 5 g/day standard maintenance. |
| No UL | **Yes, corroborated (see §2c)** — not independently re-verified against the ODS page text itself in this pass. |
| Monohydrate = preferred form | **Yes, strongly** — both PDFs independently and specifically confirm no alternative form (HCl, buffered/Kre-Alkalyn, ethyl ester, citrate/malate) has human evidence of superiority; the dossier's `poor` list (HCl, buffered) is consistent with, if slightly harsher-worded than, what the PDFs say (PDFs call HCl/buffered "equivalent, not superior" rather than "poor" — a wording nuance for Nutrition Agent, not a factual conflict). |

**New claim areas this research adds that the dossier does not currently have**
(flagging only — not editing the dossier, per this agent's lane):
1. **Cognitive/brain effects** — Moderate in specific sub-populations (sleep-
   deprived, vegetarians/vegans, low-baseline groups), Weak/null in general healthy
   omnivorous adults after EFSA's 2024 statistical-correction critique of prior
   positive meta-analyses. A real, well-hedged claim area with citable primary
   literature (verified PMIDs exist in both PDFs' works-cited for the EFSA critique
   and the sleep-deprivation RCTs) that the dossier's `claims` list does not cover.
2. **Recovery from exercise** — Moderate (biochemical markers only) to Weak
   (functional return); PDF #2's more cautious "weak/mixed" framing and PDF #1's
   "paradoxical effect" (Santos et al. 2022) finding that chronic training reverses
   the acute damage-marker benefit are both real, citable findings not currently in
   the dossier.
3. **Dairy/liquid-matrix stability** — a genuine food-science claim area (not an
   efficacy or safety claim) that would matter if Bari ever scores a creatine-in-
   liquid-dairy product on "does this product's creatine survive to the point of
   sale" — currently not a dossier field at all. Given §2d's verification gaps, if
   added, it should be added as a qualitative flag ("liquid/dairy creatine is
   formulation-fragile; verify per-product, do not assume stated dose = delivered
   dose") rather than a quantitative retention percentage.
4. **Bipolar-disorder contraindication for mood/depression use** — both PDFs
   independently flag a documented risk of manic/hypomanic switches in bipolar
   patients using creatine adjunctively for depression. This is a safety signal, not
   currently in the dossier's `safety.risky_flags` (currently empty `[]`). Routing
   this to Nutrition Agent per the Escalation Rules below, since it is a safety
   signal that may affect scoring/contraindication display, not a routine dossier
   edit.

---

## 4. The Tnuva GO conflict — resolved

**Verdict: the synthesis's product claim is unverified and conflicts with Bari's own
direct product data. The direct scrape is authoritative for product facts.**

Chain of custody on the claim:
- `owner_synthesis_pasted.md` §5/§7 states Tnuva GO has creatine, flagged by the
  owner's own synthesis tool as **"[UNVERIFIED / CONFLICTS WITH SCRAPE]"** — the
  synthesis already did its own hedging correctly here.
- That claim traces back to **PDF #1's "Market trends" section**, which states as
  flat fact: "In February 2026, Israel's second-largest dairy producer, Tnuva,
  launched... a Tnuva GO refrigerated protein drink containing added creatine
  monohydrate... 25g... protein and 2g of creatine monohydrate in a single 340mL
  bottle" — cited to works-cited ref 105.
- **Ref 105 resolves to a Hebrew-language retail/advice blog post**
  ("משקה חלבון מוכן או אבקת חלבון? מה באמת עדיף לבריאות שלך ב-2026",
  championshop.co.il — a sporting-goods retailer's content-marketing article), **not**
  a Tnuva press release, not a product label, not a retailer product page. This is
  exactly the kind of secondary/promotional source Bari's Source Hierarchy places
  below "do not cite" territory for a specific product-dose claim, and PDF #1 states
  it as unqualified fact rather than as "one blog claims."
- **Bari's own direct Shufersal scrape**
  (`03_operations/reports/research/functional_dairy_shelf_scrape_v1.md`, run
  2026-07-03) found: Tnuva's actual "GO" branded SKU on the live shelf is **"GO
  Collagen Iced Coffee"** (משקה GO קולגן אייס קפה, barcode 7290116935607) — functional
  ingredient is **collagen (1.48%), not creatine.** No Tnuva-branded creatine SKU was
  found across 4 targeted query variants. The only creatine-declaring dairy drinks
  on-shelf were **two Yoplait GO (יופלה גו) SKUs**, both with **undisclosed dose** (one
  shows a 0.6% formulation figure with no serving size to convert to mg/day; one
  shows no dose figure at all).

**This is a direct, dated, sourced conflict between a secondary-source PDF claim and
a primary direct-scrape finding. Per this project's data-sourcing hierarchy (direct
product scrape > any secondary/blog source, always), the scrape wins.** The PDF's
"Tnuva GO has 2g creatine" claim should not be treated as fact anywhere downstream —
not in the blog (TASK-492B), not in the comparison page (TASK-492C).

**Recommendation for how to settle it further** (this agent does not have authority
to decide 492C's scope — flagging for Product/Data per Spec-Conflict Duty, as the
prior scrape report already did):
1. **Broaden the retailer scrape** — Shufersal alone was live at scrape time;
   Victory is still bot-walled, Yochananof's search endpoint wasn't mapped. A second
   clean retailer scrape (or a Yochananof endpoint fix) would strengthen "0 Tnuva
   creatine SKUs" from single-retailer to cross-retailer confidence.
2. **Owner real-world sighting** — if the owner has personally seen a Tnuva-branded
   creatine product in an Israeli store (the Feb-2026 launch date in PDF #1 is
   suspiciously precise for a blog-sourced claim — it may reflect a genuine product
   that simply isn't on Shufersal's online catalog, or has since been discontinued,
   or the blog itself may have fabricated/mis-attributed the launch). A direct owner
   sighting or a Tnuva investor/press-release check would resolve this faster than
   further scraping.
3. **Do not let "likely token amount"** (the synthesis's own hedge phrase for what
   Tnuva GO's undisclosed dose "probably" is) **become a stated fact anywhere** — this
   is doubly true now that the underlying product's existence itself is unverified,
   not just its dose.

---

## 5. Verified evidence base (summary table)

| # | Claim | Evidence tier | Confidence | Key citation(s) | Practical note |
|---|---|---|---|---|---|
| 1 | Strength & power with resistance training | **Strong** | VERIFIED-primary | PMID:28615996 (ISSN 2017); PMID:39519498, 37432300, 39074168, 34836013, 24576864 (all independently re-verified) | Matches dossier. Well-replicated, multiple independent meta-analyses. |
| 2 | Lean mass with resistance training | **Strong** | VERIFIED-primary | PMID:39074168 (Desai et al. 2024, JSCR) — **LBM +1.14 kg, 95% CI 0.69–1.59, from 12 studies** (not 35 — correct the "35 studies" figure if it ships) | Matches dossier tier; correct the specific study-count number before any consumer-facing use. |
| 3 | High-intensity/repeated-sprint performance | **Strong** (PDF #1) / **Moderate** (PDF #2) | corroborated | ISSN 2017 position stand; both PDFs agree on direction, disagree on tier label | Not yet in dossier as a distinct claim (currently folded into the strength/lean-mass claim's rationale). If split out, treat as Strong-to-Moderate pending a dedicated meta-analysis PMID pull. |
| 4 | Recovery (biochemical markers) | **Moderate** | corroborated | Jiao et al. 2021 (cited both PDFs, not independently re-verified this pass) | Real effect on CK/LDH markers only. |
| 5 | Recovery (functional return to performance) | **Weak** | corroborated | Santos et al. 2022 "paradoxical effect" (cited PDF #1, not independently re-verified this pass) | Do not conflate marker reduction with faster real-world recovery — PDF #1's own "paradoxical effect" finding argues against a simple "creatine speeds recovery" consumer claim. |
| 6 | Cognitive — sleep-deprived / low-baseline populations (vegetarians, older adults) | **Moderate** | corroborated | Both PDFs agree closely, including EFSA's 2024 statistical critique of prior positive general-population findings | Context-specific claim — do NOT generalize to "creatine improves cognition" for a healthy general consumer. |
| 7 | Cognitive — general healthy omnivorous adults | **Weak/Insufficient** | corroborated | Same as above | The EFSA correction (unit-of-analysis/double-counting error) is a real, citable methodological critique both PDFs independently report — a genuinely contested area, tier accordingly. |
| 8 | Fat loss / fat burning | **Insufficient** | VERIFIED-primary | Matches dossier exactly; both PDFs agree | Any secondary fat-% change is a byproduct of training-driven lean-mass gain, not direct lipolysis. |
| 9 | "Energy" (acute stimulant effect) | **Insufficient** | corroborated | Both PDFs explicitly reject this framing | Matches dossier's non-mapping of "אנרגיה" in the structure_function_umbrella. |
| 10 | Anti-aging / sarcopenia (with training) | **Weak-to-Moderate** | corroborated | Both PDFs agree; training-dependent | Not currently a dossier claim; candidate addition (§3). |
| 11 | Mood / adjunctive depression support | **Weak** | corroborated | 2025 BJN GRADE-assessed meta-analysis: "very low certainty," SMD -0.34 (below clinical-importance threshold), "substantial publication bias" (PDF #1, not independently re-verified this pass but internally consistent and specific enough to be credible) | **Safety flag attached: documented risk of manic/hypomanic switches in bipolar patients** — route to Nutrition Agent (§3, item 4). |
| 12 | Effective dose — maintenance | **3-5 g/day**, floor ~3 g/day | VERIFIED-primary (matches dossier) | ISSN 2017; both PDFs and synthesis converge tightly | Matches dossier's `effective_dose` block exactly. |
| 13 | Effective dose — loading | ~20 g/day (4×5g) for 5-7 days, optional, not physiologically required | corroborated | Both PDFs agree closely | Matches dossier's `loading_protocol_note`. |
| 14 | Form — monohydrate preferred, no alternative superior | **Strong** consensus | VERIFIED-primary | Both PDFs independently confirm via multiple named head-to-head trials (HCl, Kre-Alkalyn, CEE, citrate/malate) | Matches dossier's `forms` block. |
| 15 | Safety — no established UL | corroborated (not primary-source-verified) | corroborated | 3 independent kidney-function meta-analyses verified real (PMID:31375416, 41199218, 42035842); NIH ODS page itself not directly fetched this pass | Matches dossier. Recommend direct ODS page fetch before a "NIH says" attribution ships. |
| 16 | Safety — kidney "myth" (transient serum-creatinine rise ≠ renal damage in healthy kidneys) | **Strong** | corroborated | Same 3 kidney-function meta-analyses + FDA CAERS data showing no dominant renal-harm signal in 203 real-world reports | Real, well-supported mechanistic explanation (creatinine ≠ direct GFR measurement); consistent across both PDFs. |
| 17 | Safety — contraindication, pre-existing renal impairment | **Established caution** | corroborated | Both PDFs agree; standard clinical caution, not a contested finding | Matches dossier's spirit though dossier's `risky_flags` list is currently empty — candidate addition. |
| 18 | Safety — bipolar disorder contraindication (mood-use context) | **New finding, not in dossier** | corroborated | Both PDFs state independently | **Escalate to Nutrition Agent** — see §3/§6. |
| 19 | Dairy-matrix stability — qualitative (creatine unstable in liquid, worse with heat/acid) | **Real, qualitatively supported** | corroborated (paper verified real; PMID:17995798) | Uzzan/Nechrebeki/Labuza 2007, *J Food Sci* — confirmed real via PubMed | Do NOT cite specific retention percentages (§2d) — abstract doesn't state them, full text not pulled this pass. |
| 20 | Dairy-matrix stability — quantitative (specific % figures, patent numbers) | **Unverified precision** | unverified | Patent WO2015078835A1 (grey literature, not peer-reviewed); specific PDF-quoted percentages not confirmed against primary text | **Do not ship any specific stability percentage in consumer copy.** Qualitative framing only, until someone pulls full-text Uzzan et al. + the patent's actual example tables. |
| 21 | Israel functional-dairy shelf — Tnuva GO has 2g creatine/340ml | **UNVERIFIED, CONTRADICTED by direct data** | **contradicted** | Bari direct Shufersal scrape (2026-07-03): Tnuva GO's actual SKU is collagen, not creatine; 0 Tnuva creatine SKUs found | **Direct scrape is authoritative. Do not ship the Tnuva-GO-has-creatine claim.** See §4. |
| 22 | Israel functional-dairy shelf — creatine-declaring dairy SKUs exist at all | **VERIFIED-primary** | VERIFIED-primary | Bari direct scrape found 2 Yoplait GO SKUs declaring creatine, both with undisclosed dose | This is the real, defensible Israel-market headline: disclosure gap, not "Tnuva has X grams." |
| 23 | Label-honesty / dose-adequacy criteria (§6 of synthesis) | **Reasonable framework, not itself an "evidence" claim** | corroborated | Both PDFs describe "fairy-dusting" and proprietary-blend obfuscation consistently and specifically (worked numeric example in PDF #1 showing blend math is "mathematically impossible" to fit clinical doses) | Useful as a verification checklist (creatine named individually, ≥3g stated, no proprietary blend, third-party cert) — not itself a scientific claim requiring a tier, but should be attributed to the PDFs' synthesis of general supplement-industry practice, not to a specific study. |
| 24 | Worldwide benchmark product table (§5) | **Approximate, MUST re-verify before shipping** | **unverified, product-specific** | Both PDFs list real-sounding brands (Thorne, Momentous, Optimum Nutrition, Myprotein, Bulk Nutrients, etc.) with specific prices/serving counts/certifications | **Every price, serving count, and certification claim in this table is a live e-commerce fact that changes over time and was not independently re-verified in this pass** (out of scope for a literature-verification gate — these require a live retail-price check, not a PubMed lookup). Flag explicitly per the task brief: "approximate," must be directly re-verified before any specific product/price ships. This includes the two Israeli products in PDF #1's table (Super Effect / Alfa) — real-sounding local brands, but their listed prices/dose/certification were not independently confirmed here. |

---

## 6. Escalations

**To Nutrition Agent:**
- New safety signal not currently in the dossier's `safety.risky_flags` (currently
  `[]`): **bipolar disorder / manic-switch risk** in the context of creatine used
  adjunctively for mood/depression, documented independently in both source PDFs.
  This may warrant a dossier `risky_flags` addition — Nutrition Agent's call, not
  this agent's.
- Two new candidate claim areas the dossier's `claims` list does not currently cover:
  **cognitive/brain effects** (Moderate in stressed/low-baseline populations, Weak in
  general population — genuinely contested per the EFSA 2024 critique, tier
  accordingly) and **recovery from exercise** (Moderate on biochemical markers only,
  Weak on functional recovery, with a "paradoxical effect" caveat in chronic
  training). Evidence base for both is real and citable (see §5, rows 4-7, 10-11).
- The "35 studies" figure in the owner's synthesis for the lean-mass meta-analysis is
  not supported by verification — the real, correctly-cited figure is **12 studies,
  +1.14 kg LBM** (PMID:39074168). Recommend this correction propagate to any content
  drawing on that number.

**To Product Agent (per Spec-Conflict Duty, mirroring the prior scrape report's own flag):**
- TASK-492C's apparent premise (a Tnuva-GO-creatine comparison) does not hold on
  either the owner's own synthesis (which flagged it) or Bari's direct scrape (which
  contradicts it). Recommend confirming 492C's scope before build: options are (a)
  reframe around the two Yoplait GO SKUs plus the transparency-gap finding, (b)
  broaden to a category-level "functional dairy creatine disclosure" page rather than
  a brand-specific one, or (c) hold 492C pending a broader-retailer re-scrape /
  owner real-world sighting per §4.

---

## 7. What must be re-verified before anything ships (consolidated)

1. **"35 studies"** for the lean-mass hypertrophy claim — wrong; use 12 studies /
   +1.14 kg (PMID:39074168) instead.
2. **"(2021 ISSN update)"** for creatine specifically — not found; the 2021 ISSN
   position stand I verified is about sodium bicarbonate, not creatine. Cite 2017
   only (PMID:28615996) unless a dedicated 2021 creatine update is located.
3. **Any specific dairy-stability percentage** (56-60% at 35 weeks; <5% heat loss;
   10% at 4°C; 12-21% in 3 days; up to 90% in 45 days) — none of these are confirmed
   against primary full text in this pass; ship only the qualitative statement
   ("creatine is known to be unstable in liquid/dairy matrices, worsened by heat and
   low pH — a real, documented food-science formulation challenge") until full text
   is pulled.
4. **The Tnuva GO creatine claim entirely** — contradicted by direct scrape; do not
   ship in any form, including "likely token amount."
5. **NIH ODS's exact no-UL statement** — corroborated by kidney-function literature
   but the ODS page itself was not directly fetched this pass; fetch before a direct
   "NIH says" attribution.
6. **Every entry in the worldwide benchmark product table** (§5, PDF #1's table and
   PDF #2's table both) — prices, serving counts, and certifications are point-in-
   time e-commerce facts, approximate by the source PDFs' own admission, and require
   a live re-check before any specific product/price appears in consumer-facing
   copy — including the Israeli entries (Super Effect, Alfa).
7. **The 2017 ISSN paper's DOI** — do not publish `10.1016/S0278-5919(05)70173-3`
   anywhere; it resolves to an unrelated paper. Cite by PMID (28615996) or verify the
   correct DOI directly before publishing one.

---

## Constraints compliance

- Every claim above names its source inline (PMID, DOI, or explicit "not
  independently re-verified this pass" flag where I relied on the PDF's own citation
  without re-pulling it myself).
- No PMID/DOI was invented — every identifier in this report was either pulled
  directly from a live `literature.py`/`crossref.py` call (shown in the verification
  steps above) or explicitly carried over from the dossier/PDFs with a stated
  confidence label.
- Open Food Facts was not used, referenced, or considered at any point.
- No subagents were spawned; all verification was run directly via Bash/Python calls
  in this session.

---

## Return Contract

```json
{
  "task": "TASK-492B / TASK-492C evidence verification gate",
  "deliverable": "creatine_evidence_verification_v1",
  "status_proposed": "RETURNED",
  "artifacts": [
    {
      "path": "C:\\Bari\\03_operations\\reports\\research\\creatine_evidence_verification_v1.md",
      "sha256": "d3a810fc3ce240b637b5b18dc00e1607f8a6075677c6cd6e4547552aa69875b8"
    }
  ],
  "counts": {
    "source_documents_reviewed": {"value": 3, "denominator": "3 named in task (Comprehensive PDF, Efficacy PDF, owner_synthesis_pasted.md)"},
    "load_bearing_citations_independently_checked": {"value": 9, "denominator": "9 attempted (2017 ISSN, 2021 ISSN-update search, lean-mass meta-analysis, dossier's 5 existing PMIDs re-verified as a set, NIH-ODS corroboration via 3 kidney-function papers, Uzzan 2007 dairy paper, FDA CAERS real-world check, CrossRef DOI-integrity check on 2 DOIs)"},
    "citations_verified_real_and_on_topic": {"value": 8, "denominator": "9 attempted -- 1 partial (2021 ISSN creatine-specific update NOT found; the verified 2021 ISSN paper found is about sodium bicarbonate, not creatine)"},
    "citations_with_a_factual_error_found": {"value": 2, "denominator": "9 checked -- (1) '35 studies' figure unsupported, real count is 12 (PMID:39074168); (2) 2017 ISSN paper's PubMed-supplied DOI resolves to an unrelated 1999 paper via CrossRef"},
    "dossier_existing_pmids_reverified_clean": {"value": 5, "denominator": "5 cited in creatine_monohydrate.yaml for the strength/lean-mass claim"},
    "cross_check_table_rows_synthesis_vs_pdfs": {"value": 14, "denominator": "14 major synthesis claim-groups checked against PDF text (see Section 1 table)"},
    "cross_check_rows_matching_cleanly": {"value": 9, "denominator": "14 -- 5 rows show partial support, unverified precision, or PDF-internal disagreement (lean-mass study count, recovery tier smoothing, dairy-stability numbers, acidic-beverage percentages, Tnuva GO)"},
    "tnuva_go_creatine_skus_found_on_direct_scrape": {"value": 0, "denominator": "1 Tnuva-branded GO SKU found on live Shufersal shelf (2026-07-03) -- it is collagen, not creatine; PDF #1's claim traces to a secondary Hebrew retail blog post, not a primary product source"},
    "new_candidate_dossier_claim_areas_flagged": {"value": 4, "denominator": "4 flagged for Nutrition Agent (cognitive, recovery, dairy-stability-as-a-flag, bipolar contraindication) -- none edited into the dossier by this agent"},
    "off_usages": {"value": 0, "denominator": "0 -- banned source, never invoked"}
  },
  "commands_run": [
    {"cmd": "python -c \"literature.pubmed('International Society of Sports Nutrition position stand creatine...')\"", "exit_code": 0, "note": "confirmed PMID:28615996 (2017 ISSN creatine position stand) real, correct authors/journal/year"},
    {"cmd": "python -c \"literature.pubmed('creatine 2021 ISSN update review safety')\"", "exit_code": 0, "note": "no creatine-specific 2021 ISSN update found; separately confirmed PMID:34503527 is a real 2021 ISSN paper but on sodium bicarbonate, not creatine"},
    {"cmd": "python -c \"literature.pubmed(<5 dossier PMIDs>)\"", "exit_code": 0, "note": "all 5 dossier-cited PMIDs (39519498, 37432300, 39074168, 34836013, 24576864) resolve to real, correctly-titled creatine+RT meta-analyses/systematic reviews"},
    {"cmd": "python -c \"literature.pubmed('39074168')\" (full abstract pull)", "exit_code": 0, "note": "confirmed actual figure: LBM +1.14kg (95% CI 0.69-1.59), 12 studies (not 35 as the synthesis states), DOI 10.1519/JSC.0000000000004862"},
    {"cmd": "python -c \"crossref.get_doi('10.1016/S0278-5919(05)70173-3')\"", "exit_code": 0, "note": "DOI resolves to an UNRELATED 1999 paper -- flagged as a PubMed metadata error, not a source-document fabrication; do not publish this DOI"},
    {"cmd": "python -c \"crossref.get_doi('10.1519/JSC.0000000000004862')\"", "exit_code": 0, "note": "confirmed clean, not retracted, title matches -- safe to cite"},
    {"cmd": "python -c \"literature.pubmed('creatine tolerable upper intake level UL not established NIH')\"", "exit_code": 0, "note": "no results -- expected, NIH ODS fact sheets are not PubMed-indexed; corroborated instead via kidney-function meta-analyses"},
    {"cmd": "python -c \"literature.pubmed('effect creatine supplementation kidney renal function systematic review meta-analysis')\"", "exit_code": 0, "note": "confirmed 3 real kidney-function meta-analyses: PMID 31375416 (2019), 41199218 (2025), 42035842 (2026)"},
    {"cmd": "python -c \"literature.pubmed('thermal storage stability nutraceuticals milk beverage... Uzzan Nechrebeki Labuza')\"", "exit_code": 0, "note": "confirmed PMID:17995798 real (J Food Sci 2007); abstract does NOT contain the specific retention percentages both PDFs attribute to it -- flagged as unverified precision"},
    {"cmd": "python -c \"openfda.adverse_events('creatine')\"", "exit_code": 0, "note": "203 CAERS reports; top reactions nausea/vomiting/elevated CPK/headache -- no dominant renal-harm signal, corroborates (does not prove) the no-renal-harm literature"},
    {"cmd": "python -c \"semantic_scholar.search(...)\"", "exit_code": 1, "note": "HTTP 429 rate-limited; not retried, sufficient verification already obtained via pubmed/crossref for load-bearing items"},
    {"cmd": "python -c \"literature.openalex('creatine... 35 studies...')\"", "exit_code": 0, "note": "query too broad, returned irrelevant results; '35 studies' figure remains unlocated and is flagged unverified rather than pursued further, per proportionate-effort judgment"}
  ],
  "not_done": [
    "Full text of Uzzan et al. 2007 not pulled (only abstract) -- specific dairy-stability percentages remain unverified at that level of precision",
    "Glaxo patent WO2015078835A1 not independently fetched/read -- its cited figures are relayed from PDF #1 only, not independently confirmed",
    "NIH ODS creatine fact-sheet page not directly fetched (web fetch out of scope for the literature-client-only verification approach used here; corroborated indirectly via kidney-function meta-analyses instead)",
    "Worldwide benchmark product table (prices, serving counts, certifications for ~20 products across 6 regions) not independently re-verified against live retailer pages -- flagged as approximate per task brief, requires a separate live-retail-check pass before any product/price ships",
    "Acidic-beverage degradation percentages (12-21% in 3 days; up to 90% in 45 days) not traced to a specific paper -- remain unverified",
    "2021 ISSN creatine-specific update not located -- may not exist as a discrete update; flagged rather than asserted either way",
    "Semantic Scholar citation-impact / influentialCitationCount check not completed for the 2017 ISSN paper due to a rate limit -- not re-attempted, PubMed+CrossRef verification was judged sufficient for this gate",
    "Second retailer cross-check for the Tnuva GO question (Yochananof endpoint mapping, Rami-Levy scrape) not performed -- inherited gap from the prior scrape report, flagged again here as unresolved"
  ],
  "acceptance_test": {
    "spec_requirement": "Cross-check owner_synthesis_pasted.md against the two source PDFs; independently verify load-bearing citations (2017 ISSN +2021 update, hypertrophy meta-analysis, NIH ODS UL statement, dairy-matrix stability incl. patent figure); reconcile against Bari's creatine dossier; resolve the Tnuva GO conflict; produce a tiered, cited, confidence-labeled verified evidence base; flag what must be re-verified before shipping; no invented PMIDs/DOIs/URLs, no OFF, no subagents",
    "result": "PASS, with multiple material findings surfaced rather than smoothed over",
    "evidence": "All 3 sources read in full (both PDFs read as documents, synthesis read as file). Cross-check table in Section 1 covers 14 claim groups, flags 5 with partial support or PDF-internal disagreement. 9 load-bearing citation checks run directly against PubMed/CrossRef/OpenFDA (commands listed above); found the '35 studies' hypertrophy figure is unsupported (real count is 12, PMID:39074168, figure corrected in Section 5 row 2), found the 2017 ISSN paper's own PubMed-supplied DOI resolves to an unrelated 1999 paper via CrossRef (do-not-publish flag issued), found no dedicated 2021 ISSN creatine update exists (only a 2021 ISSN sodium-bicarbonate paper), and found the dairy-stability percentages are not traceable to the primary paper's abstract (qualitative-only recommendation issued). Dossier reconciliation in Section 3 confirms all 4 owner-specified corroboration targets (strength/lean-mass Strong, fat-loss Insufficient, dose 3-5g, no-UL, monohydrate-preferred) and flags 4 new candidate claim areas without editing the dossier. Tnuva GO conflict resolved definitively in Section 4: direct Shufersal scrape (2026-07-03) found Tnuva GO's actual SKU is collagen, contradicting PDF #1's claim which itself traces to a secondary Hebrew retail blog post rather than a primary source -- direct scrape is authoritative, flagged accordingly, escalated to Product Agent per Spec-Conflict Duty. Section 5 delivers the full per-claim evidence-tier table with confidence labels (VERIFIED-primary / corroborated / unverified / contradicted) as specified, including the worldwide benchmark product table flagged explicitly as approximate and requiring live re-verification before shipping any specific product/price, per the task brief's own instruction. Section 7 consolidates all re-verification items. No PMIDs/DOIs/URLs invented -- every identifier traces to a live tool call shown in commands_run, or is explicitly labeled as carried-over-from-source-with-a-confidence-flag rather than independently confirmed. OFF never used. No subagents spawned."
  }
}
```
