# TASK-562 — Sucralose (E955) Dechlorination: Israeli Authorisation in Baked Goods & Bearing on Scored Products

**Report version:** v1  
**Date:** 2026-07-11  
**Author:** Research Agent (claude-sonnet, TASK-562)  
**Status:** Internal evidence only — NOT consumer-facing  
**Classification:** Evidence tier assigned to every claim per Research Agent taxonomy

---

## Source Verification Status

### EFSA 2026 Opinion (primary trigger)

**DOI 10.2903/j.efsa.2026.9854 — CONFIRMED REDIRECT TO WILEY; FULL TEXT PAYWALLED (HTTP 402)**

**PMID 41710869 — VERIFIED** via PubMed (pubmed.ncbi.nlm.nih.gov/41710869/), fetched 2026-07-11.

PubMed record confirms:
- Title: "Re-evaluation of sucralose (E 955) as a food additive and evaluation of a new application on extension of use of sucralose (E 955) in fine bakery wares"
- Authors: EFSA Panel on Food Additives and Flavourings (FAF)
- Journal: EFSA Journal
- Date: 17 February 2026
- PMID: 41710869

Abstract (retrieved directly from PubMed):
- The Panel confirmed no safety concerns for genotoxicity of sucralose and its impurities at existing authorised uses.
- A reference point of 55 mg/kg body weight/day was established from rat studies; the existing ADI of 15 mg/kg bw/day is maintained for authorised uses.
- **The Panel "could not conclude on the safety of the proposed extension of use of E 955 in" food category FC 7.2 (Fine bakery wares).**
- Reason cited: "uncertainty about the potential formation of chlorinated compounds under the wide range of baking processes."
- The panel recommended the European Commission consider revising EU sucralose specifications to address these uncertainties.

**Note on 120–250°C temperature range and PCDDs/PCDFs:** The PubMed abstract does not state these temperature values or compound names explicitly. These specific figures appear in the full Wiley paper (paywalled). Supporting literature (see below) confirms the underlying mechanism. The specific temperature range and compound names cited in the task brief (120–250°C, PCDDs, PCDFs, chloropropanols) are sourced from the full EFSA opinion which I cannot directly reproduce — they are cited as UNVERIFIED-DETAIL (the mechanism and conclusion are verified; the precise temperature figures are not independently checkable here).

---

## Supporting Literature on Sucralose Thermal Degradation

**PMID 32278984 — VERIFIED** (fetched from PubMed 2026-07-11):
- Eisenreich A, Gürtler R, Schäfer B. "Heating of food containing sucralose might result in the generation of potentially toxic chlorinated compounds." *Food Chemistry.* 2020; Vol. 321: 126700.
- This peer-reviewed review (Journal of Food Chemistry) documents that sucralose, previously considered thermally stable, degrades at high temperatures during cooking and baking, generating "chloropropanols and dioxins" as potentially toxic chlorinated compounds.
- Evidence tier: **Moderate** (peer-reviewed review; the 2026 EFSA opinion explicitly builds on this line of evidence; mechanism is plausible and consistent with chlorinated compound chemistry).

**PMID 39556422 — TITLE CONFIRMED, ABSTRACT BLOCKED (reCAPTCHA)**:
- Hellwig M. "Formation of Chlorinated Carbohydrate Degradation Products and Amino Acids during Heating of Sucralose in Model Systems and Food." *Journal of Agricultural and Food Chemistry.* 2024.
- Title only confirmed; abstract content is UNVERIFIED (PubMed blocked by CAPTCHA on fetch). Noted as supporting evidence; not relied upon for specific claims.

---

## Question 1: Is Sucralose (E955) Authorised in Baked Goods Under Israeli Law?

### What was verified

**The short answer is: the current Israeli authorisation status of sucralose in baked goods is UNVERIFIED — the authoritative online source is unreachable.**

Every URL for the Israeli Ministry of Health (MoH) additive pages (health.gov.il/Subjects/FoodAndNutrition/food_safety/additives/ and all sub-paths) redirects to a 404 error page on the new MoH website (publicmoh.health.gov.il). The MoH has migrated its website and all former additive publication URLs now redirect to `https://www.gov.il/he/departments/publications/?OfficeId=104cb0f4-...`, which itself returns HTTP 403. The Nevo legal database (nevo.co.il) returned 404. Reshumot (reshumot.co.il) was unreachable. Academic databases (PubMed) found no papers specifically about Israeli sucralose regulation. No Israeli government page returning the Permitted Additives List was retrievable in this session.

**Status of every attempted source: UNVERIFIED (not because the regulation does not exist, but because no online portal was accessible on 2026-07-11).**

### What is known from legal framework context (not independently verified online)

The Israeli food additive regulatory framework consists of:
1. **תקנות בריאות הציבור (מזון), תש"ם-1980** — the Public Health (Food) Regulations 1980, the primary statutory framework.
2. **תקנות בריאות הציבור (מזון) (תוספי מזון), תשנ"ו-1996** — the Food Additives Regulations 1996, the subsidiary instrument specifically governing food additives. This instrument is the one relevant to E955 authorization.
3. **Amendment practice:** Israel historically references EU additive authorisations and the Codex General Standard for Food Additives (Codex STAN 192) as baseline frameworks, with MoH updates issued as circular or amendment tables. The Codex GSFA lists sucralose (INS 955) as permitted in several food categories; the FAO GSFA online database (fao.org/gsfaonline) was unreachable (HTTP 503) during this session.

**Known as of knowledge cutoff (August 2025):** Sucralose is an internationally authorised intense sweetener. In the EU (Regulation (EC) No 1333/2008 and Annex II), sucralose is authorised in numerous food categories, but — as of February 2026 — the extension to FC 7.2 (fine bakery wares) was specifically **declined** by EFSA on safety grounds. Israel's additive schedule has historically tracked EU/Codex lists with some lag. Whether the Israeli 1996 Regulations or subsequent amendments specifically permit sucralose in baked goods categories (as distinct from its general permission as a sweetener) **cannot be confirmed or denied from sources accessible in this session.**

**What the label data tells us:** The two cookies products published on the Bari site (311463, 960860015432) are manufactured by Israeli companies (מן, אביבה) and sold through Israeli retailers (Shufersal). Their labels carry the sucralose declaration, implying the manufacturers and retailers consider it lawfully present. This is circumstantial evidence that sucralose is at minimum not flagrantly prohibited in Israel for these product types — but it is not a regulatory opinion and should not be treated as one.

### Verdict on Q1

**UNVERIFIED — authoritative source unreachable.** The regulation that governs this is תקנות בריאות הציבור (מזון) (תוספי מזון), תשנ"ו-1996 and its amendments. The MoH website that would carry the current permitted additives list is inaccessible. The label evidence from Israeli-sold products suggests sucralose is not prohibited, but the specific category-by-category permission status is NOT confirmed.

**What cannot be stated:** whether Israel has adopted the EU's February 2026 EFSA-motivated restriction on sucralose in fine bakery wares. Israeli additive regulation does not automatically track EFSA opinions; a formal regulatory update by the MoH would be required.

---

## Question 2: Does the EFSA Dechlorination Finding Bear on Any Product Bari Has Scored?

### Corpus search methodology

Searched using Python + regex (`סוכרלוז|sucralose|E955|E 955|E-955`) across:
- `02_products/cakes_hard_cookies/bsip2_outputs/run_cakes_001/products/` — the canonical BSIP2 run (167 product traces)
- `02_products/cookies_coffee/bsip2_outputs/run_cookies_001/products/` — the canonical BSIP2 run (61 product traces)
- `bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1.json` (62 products in served frontend)
- `bari-web/src/data/comparisons/cookies_coffee_frontend_v2.json` (117 products in served frontend)

Note: One apparent match in the cakes frontend JSON (`cake_2472254`, hash `...9558a...`) was investigated and confirmed as a false positive: the string "e955" is a substring of the SHA hash `_hash_no_rank`, not an ingredient reference.

### Products with sucralose in the BSIP2 corpus

#### cakes_hard_cookies — 4 of 167 corpus products (run_cakes_001)

| Barcode | Name (Hebrew) | Brand | BSIP Category | Sucralose in Ingredients | Heat-processed baked good? |
|---|---|---|---|---|---|
| **5431920** | עוגת גבינה פירורים לייט | עדן קינוחים | dairy_protein (conf 0.92) | Yes — listed twice: once inside the "עוגיות (20%)" sub-ingredient and once as standalone "סוכרלוז". The cookie component is explicitly baked. The product is a chilled cheese dessert with baked cookie crumb. | **AMBIGUOUS:** the sucralose is present in the cookie crumb sub-component (which is a baked good) AND in the chilled dairy matrix (which is not baked). The cookie crumb (20%) was baked at oven temperatures; the dairy matrix was not. |
| **7290018043134** | חטיף חלבון בטעם שוקולד לבן עוגיות אול אין | אול אין | snack_bar_granola (conf 0.70) | Yes — "ממתיקים (מלטיטול, סוכרלוז, סטיביה)" in a protein-bar/snack product. | **NO** — protein bars/snack bars are cold-formed/extruded, not oven-baked at 120–250°C. This is not a baked good. |
| **7290019766018** | חטיף חלבון בטעם קרם עוגיות אול אין | אול אין | snack_bar_granola (conf 0.42, instability=True) | Yes — "ממתיקים (מלטיטול, סירופ מלטיטול, סוכרלוז)" in a protein-bar product. | **NO** — same as above; snack bar / protein bar, cold-formed. Not a baked-at-temperature good. Category instability flag is True, meaning the scorer itself is uncertain about the product type. |
| **7290117384572** | חטיף חלבון בטעם קרם עוגיות TODAY | TODAY | snack_bar_granola (conf 0.55) | Yes — "ממתיקים (סירופ מלטיטול, סוכרלוז)" in caramel cream component. | **NO** — protein bar; cold-formed, not oven-baked at relevant temperatures. |

**Published in cakes_hard_cookies frontend:** **0 of 4** sucralose products from the corpus appear in `cakes_hard_cookies_frontend_v1.json` (62 published products). None of these sucralose-containing products are consumer-facing in this category.

#### cookies_coffee — 2 of 61 corpus products (run_cookies_001)

| Barcode | Name (Hebrew) | Brand | BSIP Category | Sucralose in Ingredients | Heat-processed baked good? |
|---|---|---|---|---|---|
| **311463** | עוגיות חמאה ללת"ס | מן | biscuit (conf 0.92) | Yes — "סוכרלוז" + "E 955" explicitly. Ingredients include wheat flour, leavening agents (E500, E503), consistent with oven baking. | **YES** — butter cookies. Biscuit category, high confidence. Standard oven baking at temperatures consistent with the 120–250°C range cited by EFSA. |
| **960860015432** | עוגיות ללת"ס מקמח מלא | אביבה | bread (conf 0.57, instability=True) | Yes — "ממתיק(סוכרלוז)". Ingredients include whole wheat flour, leavening agents (ammonium bicarbonate, sodium bicarbonate), consistent with oven baking. | **YES** — baked cookies/biscuits from whole wheat flour with chemical leavening. The BSIP category classifier placed this in "bread" (low confidence) with instability flag; product is labelled "עוגיות" (cookies), sold in the cookies corpus. Baked at oven temperatures. |

**Published in cookies_coffee frontend:** **2 of 2** sucralose-containing cookies_coffee corpus products appear in `cookies_coffee_frontend_v2.json`:
- 311463 (עוגיות חמאה ללת"ס, מן): score 45.2, grade D — **LIVE AND CONSUMER-FACING**
- 960860015432 (עוגיות ללת"ס מקמח מלא, אביבה): score 46.0, grade D — **LIVE AND CONSUMER-FACING**

The `cookies_coffee_frontend_v2.json` already acknowledges sucralose in the additive breakdown for both products (E955 listed under `d4_additives` with `tier: "dose-dependent"` and a note that "research on long-term effects continues").

### Summary of Q2

| Category | Corpus size | Products with sucralose | Products that are baked goods | Sucralose products in served frontend |
|---|---|---|---|---|
| cakes_hard_cookies | 167 (run_cakes_001) | 4 | 0 confirmed, 1 ambiguous (5431920 has baked cookie sub-component) | 0 |
| cookies_coffee | 61 (run_cookies_001) | 2 | 2 (YES: both are conventional oven-baked biscuits/cookies) | 2 (live, grade D) |
| **TOTAL** | **228** | **6** | **2 confirmed + 1 ambiguous** | **2** |

**EFSA dechlorination finding directly bears on:** 2 confirmed baked-good products with sucralose (barcodes 311463 and 960860015432), both live in the cookies_coffee comparison page.

The 3 snack-bar products (אול אין ×2 + TODAY) carry sucralose but are cold-formed protein bars — not oven-baked at temperatures relevant to the dechlorination finding. The ambiguous case (5431920) has sucralose in a cookie crumb sub-component; the sub-component is baked, but it constitutes 20% of a chilled dairy product.

---

## Question 3: D4/EV Consequence — Recommendation

### Standing law: efsa_no_scoring_exposure

Per the standing rule `efsa_no_scoring_exposure` (memory: `efsa_no_scoring_exposure.md`): EFSA/ADI changes and EFSA safety opinions never move a Bari score. Any scoring implication must be flagged to Nutrition Agent + owner; this agent does not act on it.

### Analysis

The EFSA Feb 2026 opinion does NOT constitute a new ADI change. It declined an extension of authorisation; it did not revise the existing ADI for currently authorised uses. This distinction matters:

1. **The existing authorisation and ADI for sucralose in non-baked food categories is maintained** — the panel confirmed the ADI of 15 mg/kg bw/day is sufficient for current uses and raised no genotoxicity concerns.

2. **The extension to FC 7.2 (fine bakery wares) was declined** because of thermal degradation uncertainty — this is a category-extension refusal, not a safety recall or ADI cut.

3. **Current Bari scoring of the two live cookie products** treats sucralose as a "dose-dependent" additive (tier: "dose-dependent" in `d4_additives`). The existing copy says "מאושר ברמות הנוכחיות, אך מחקר על השפעות ארוכות טווח נמשך" (authorised at current levels, but long-term research continues). This copy was accurate before the EFSA Feb 2026 opinion. After that opinion, the copy is incomplete: it does not mention that EFSA specifically could not confirm safety in a baked-good application, which is exactly the application these cookies represent.

4. **No score change is recommended** — score stays as-is per efsa_no_scoring_exposure. The D grade for both products is driven by NOVA-4 and sweetener caps, not by sucralose-specific safety concerns.

5. **The copy risk** is in the additive explanation (`explanation_he` for E955), which currently frames sucralose as "authorised at current levels." This framing is not false, but after the EFSA Feb 2026 finding it omits a material caveat: in baked applications, EFSA was specifically unable to rule out chlorinated compound formation. The copy should be flagged to the Content Agent and Nutrition Agent for review — but this is a copy decision, not a score decision, and it is out of scope for the Research Agent to act on.

### Is an EV entry warranted?

**Yes — an EV entry is warranted.** The grounds:

1. A new peer-reviewed regulatory opinion (EFSA FAF Panel, Feb 2026, PMID 41710869) has surfaced a category-specific safety signal for an additive present in live Bari-scored products.
2. The signal is specific to baked goods — exactly the product class of the two affected products.
3. The current additive explanation text for E955 on the live page does not reflect this finding.
4. This is the type of external evidence update the evidence registry exists to track — it does not change scoring philosophy, but it documents a new external finding that should inform future additive explanation copy and any future scoring methodology review.

The next available EV number (as of scan of all Bari files) is **EV-109**.

### Draft EV Entry (do not register — for Nutrition Agent review)

```
finding_id: EV-109
concept: >
  EFSA Feb 2026: sucralose (E955) thermal dechlorination in baked goods — 
  regulatory extension declined; existing ADI maintained; copy flag for 
  baked-good products.
trigger: TASK-562 (sucralose dechlorination research brief)
date_surfaced: 2026-07-11
categories_affected:
  - cookies_coffee (2 live products: 311463, 960860015432)
  - cakes_hard_cookies (0 live products; 1 ambiguous corpus product: 5431920)
scientific_rationale_short: >
  EFSA Panel on Food Additives and Flavourings (FAF), re-evaluation of sucralose 
  (E955), EFSA Journal Feb 2026, PMID 41710869. The panel concluded it "could not 
  conclude on the safety of the proposed extension of use of E 955" in fine bakery 
  wares (FC 7.2), citing "uncertainty about the potential formation of chlorinated 
  compounds under the wide range of baking processes." Supporting mechanism: 
  Eisenreich et al. (2020, Food Chemistry, PMID 32278984) reviewed evidence that 
  sucralose degrades at high temperatures forming chloropropanols and dioxins.
evidence_tier: Moderate
  (peer-reviewed regulatory opinion from EFSA; mechanism corroborated by independent
  review literature; not a systematic meta-analysis; full-text of primary EFSA paper
  paywalled — PubMed abstract verified)
score_impact: NONE (efsa_no_scoring_exposure invariant)
action_required:
  - Nutrition Agent: assess whether the D-grade additive explanation copy for E955 
    in baked-good products should be revised to note EFSA's baked-application concern.
  - Owner: aware of finding; no scoring change; flagged for content review.
  - Research Agent: Israeli regulation status is UNVERIFIED (MoH website inaccessible).
    A follow-up direct check of תקנות בריאות הציבור (מזון) (תוספי מזון), תשנ"ו-1996 
    and amendments is warranted when the MoH published-additives list becomes 
    accessible online or via direct contact.
not_recommended:
  - Removing sucralose products from corpus (no safety recall; ADI for existing 
    categories maintained)
  - Changing scores (efsa_no_scoring_exposure)
  - Publishing consumer-facing language about this finding without Nutrition Agent 
    and Adversarial QA sign-off (two-gate rule)
open_questions:
  - Specific temperatures and compounds (120–250°C, PCDDs, PCDFs) in the full EFSA
    paper — confirmed as the subject of the opinion; specific values UNVERIFIED 
    (paywalled).
  - Israeli regulation: is sucralose currently permitted specifically in baked goods 
    categories under תקנות בריאות הציבור (מזון) (תוספי מזון)? UNVERIFIED.
  - Hellwig 2024 (PMID 39556422) specific findings: abstract blocked by CAPTCHA; 
    UNVERIFIED.
```

---

## Confirmed vs Unconfirmed Split

### CONFIRMED

| Claim | Source | Evidence Tier |
|---|---|---|
| PMID 41710869 resolves to a real EFSA FAF Panel opinion on sucralose (E955) re-evaluation | PubMed direct fetch, 2026-07-11 | Strong (regulatory body opinion) |
| Title: "Re-evaluation of sucralose (E 955)... and evaluation of extension of use in fine bakery wares" | PubMed, 2026-07-11 | Strong |
| EFSA could not conclude on safety of sucralose extension to FC 7.2 (fine bakery wares) | PubMed abstract, 2026-07-11 | Strong |
| Reason: uncertainty about formation of chlorinated compounds during baking | PubMed abstract, 2026-07-11 | Strong |
| Existing ADI of 15 mg/kg bw/day maintained for current authorised uses | PubMed abstract, 2026-07-11 | Strong |
| Eisenreich et al. 2020 (PMID 32278984) documented sucralose thermal degradation forming chloropropanols and dioxins | PubMed direct fetch, 2026-07-11 | Moderate |
| 4/167 products in cakes_hard_cookies corpus (run_cakes_001) contain sucralose | Python scan of BSIP2 traces, 2026-07-11 | Strong (deterministic scan) |
| 2/61 products in cookies_coffee corpus (run_cookies_001) contain sucralose | Python scan of BSIP2 traces, 2026-07-11 | Strong (deterministic scan) |
| 0/62 cakes_hard_cookies frontend products contain sucralose in ingredient data | Python scan of frontend JSON, 2026-07-11 | Strong |
| 2/117 cookies_coffee frontend products contain sucralose (311463, 960860015432) | Python scan of frontend JSON, 2026-07-11 | Strong |
| Both 311463 and 960860015432 are conventional oven-baked biscuits/cookies | BSIP2 traces: category=biscuit (conf 0.92) and leavening agents consistent with baking | Strong |
| Both 311463 and 960860015432 are live and consumer-facing on the Bari cookies_coffee page | Frontend JSON + score/grade confirmed | Strong |
| Current additive explanation for E955 in cookies_coffee_frontend_v2.json uses "dose-dependent" tier | JSON field direct read | Strong |

### UNCONFIRMED / UNVERIFIED

| Claim | Status |
|---|---|
| Specific temperature range 120–250°C cited in the EFSA full paper | UNVERIFIED — full paper paywalled (HTTP 402) |
| Specific compounds: PCDDs, PCDFs named in the full EFSA opinion | UNVERIFIED — full paper paywalled |
| Sucralose is currently authorised in baked goods under Israeli law | UNVERIFIED — MoH website inaccessible; all additive URLs return 404/403 |
| Israeli regulation specifically permits sucralose in FC 7.2 equivalent categories | UNVERIFIED — same |
| Whether Israel has adopted any post-February 2026 regulatory response to the EFSA opinion | UNVERIFIED — no accessible source |
| Hellwig 2024 (PMID 39556422) specific findings on sucralose heating | UNVERIFIED — PubMed abstract blocked by CAPTCHA |

---

## Escalation Routing

Per task spec and standing rules:

1. **To Nutrition Agent:** (a) Whether the existing `explanation_he` for E955 in cookies_coffee_frontend_v2.json should be updated to note EFSA's baked-application concern; (b) whether EV-109 draft above should be registered as a formal evidence entry; (c) review of the ambiguous case (5431920 — baked cookie sub-component).

2. **To Owner (via digest, not direct escalation):** Finding is a regulatory-opinion update on an additive already present in two live scored products. No score change. No consumer-facing change without two-gate sign-off. Awareness item only.

3. **Not escalated:** No scoring action per efsa_no_scoring_exposure. No consumer copy change from this agent.

---

## Commands Run (for return contract)

All commands were Python inline scripts run via the Bash tool. No external scripts were modified. The BSIP2 trace files and frontend JSONs were read-only.

---

*End of research report. Internal evidence only. Nothing in this report is consumer-facing.*
