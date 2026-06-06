# Olive Oil D5/D6 Annotation Spec v1

**Classification:** Internal — Olive Oil + Authenticity Pilot (TASK-197)
**Version:** v1
**Date:** 2026-06-06
**Owner:** Nutrition Agent
**Task:** TASK-197, Phase 3
**Status:** Approved for consumer-facing implementation. Owner tripwire `authenticity_annotation_gate` CLEARED (2026-06-06). Phase 5 (Frontend) unblocked pending `go_live` tripwire (separate owner decision).

---

## 1. Purpose and Scope

This document defines the annotation schema for olive oil authenticity and transparency
signals routed through the Glass Box D5 (Transparency) and D6 (Confidence) dimensions.
It covers what signals are annotated, how they are populated, what consumer-facing Hebrew
copy is permitted, and the hard governance fence separating these annotations from the
D1–D4 quality-scoring dimensions.

This spec covers the Israeli retail olive oil shelf (initial corpus: Shufersal, with
Carrefour and Yochananof as Phase 2 expansion targets).

---

## 2. Governance Fence — Authenticity/Transparency Signals Are Sealed from D1–D4

**This is the architectural constraint that governs the entire document. It is stated
once here and is not negotiable in implementation.**

| Quality dimension | Signal input permitted | Fraud/authenticity signal permitted |
|---|---|---|
| D1 — Nutrition | BSIP0 nutrition panel | **NEVER** |
| D2 — Ingredient evidence | BSIP1 ingredient list | **NEVER** |
| D3 — Processing | NOVA proxy, processing state | **NEVER** |
| D4 — Additive evidence | E-number classification | **NEVER** |
| **D5 — Transparency** | Label completeness, disclosure | **YES — annotation only** |
| **D6 — Confidence** | Verification state, claim plausibility | **YES — annotation only** |

**Consequence:** A product with an opaque origin, a missing harvest date, a Turkish-origin
flag, or any other authenticity annotation carries exactly the BSIP2 grade its D1–D4
signals earn. The authenticity annotation layer does not depress or inflate that grade by a single
point. The annotation surfaces in the D5/D6 expansion section; the collapsed leaderboard
row shows only the D1–D4 quality grade.

This fence is required by BEV-001 ("ברי מתאר. לא ממליצה") and the TASK-197 hard constraint:
"Fraud annotates; grade does not move."

---

## 3. D5 (Transparency) Signal Definitions

D5 signals describe what is or is not declared on the product label. All D5 signals are
annotation-only. None trigger a score change.

---

### D5-OO-001 — Origin Opacity

**Signal name (internal):** `origin_opacity`
**Signal class:** D5 (Transparency)
**Annotation type:** Negative annotation (absence of expected disclosure)

**Definition:** The product label does not name a country of harvest for the olives. A
country-of-packing or country-of-distribution is not equivalent. The signal fires when the
label identifies where the oil was *bottled or packaged* but not where the olives were
grown and pressed.

**Distinction from country-of-origin field:**
EU and Israeli labeling regulations require that olive oil from a single country name that
country as country of origin. When olives come from multiple countries, the label must state
"blend of olive oils from different countries" or list them. A label that names only a
packing country (e.g., "packed in Italy" when the olives may originate elsewhere) activates
this signal. A label that names the harvest country explicitly does not activate this signal,
even if the country carries other risk signals.

**Observability:** Readable from the BSIP0 label extraction. Populated by the BSIP1
enricher field `olive_harvest_country` vs. `olive_packing_country`.

**Status:** Confirmed. Consumer-facing copy approved below (Section 5).

**Governance:** BEV-001 applies — annotation describes a labeling absence, does not assert
any quality failure or adulteration.

---

### D5-OO-002 — Harvest Date

**Signal name (internal):** `harvest_date_absent`
**Signal class:** D5 (Transparency)
**Annotation type:** Negative annotation (absence of disclosure)

**Definition:** The product label does not state the olive harvest year or campaign year.
Extra virgin olive oil quality degrades with time from harvest; the harvest date is the
single most informative freshness indicator available on a label. Its absence limits the
consumer's ability to assess freshness independently.

**Observability:** Readable from BSIP0 extraction field `harvest_date_stated` (boolean).

**Status:** Confirmed — category-level finding (2026-06-06)

The Shufersal re-scrape (Phase 2 Updated, 2026-06-06) returned 13 clean olive oil products.
0/13 state a harvest date — 100% absence, exceeding the ≥80% threshold defined in the
original pending-validation clause. The finding is no longer a per-product annotation
candidate: it is a category-level transparency note, surfaced in the `categoryNote` slot
on the comparison page rather than as a per-product negative annotation.

The schema slot (`harvest_date_stated`) remains in the enricher. Per-product annotation
logic is not applied. Consumer-facing Hebrew copy is finalized below (Section 5).

**Consumer-facing copy:** FINALIZED (see Section 5 — D5-OO-002 category note).

---

### D5-OO-003 — Multi-Country Blending Disclosure

**Signal name (internal):** `multi_country_blend`
**Signal class:** D5 (Transparency)
**Annotation type:** Neutral annotation (factual disclosure of blending practice)

**Definition:** The product is explicitly labeled as a blend of olive oils from more than
one country of origin, or from both EU and non-EU origins. This is a legal and common
practice. The annotation is factual, not negative — it surfaces what the label already
states, because some consumers do not read this disclosure.

**This annotation is neutral.** Multi-country blending is not associated with authenticity
failure. The annotation's purpose is to make visible a disclosure that is legally required
but often printed in small type. It does not imply lower quality.

**Observability:** Readable from BSIP0 extraction. Field: `origin_blend_disclosed` (boolean)
+ `origin_blend_countries` (list of country codes).

**Status:** Confirmed. Consumer-facing copy approved below (Section 5).

**Governance:** Because this annotation surfaces something the label already states (not
an inference or an accusation), it sits squarely within BEV-002 (structural description —
documentable label facts, always defensible).

---

### D6-OO-003 — Turkish Origin Confidence Qualifier

*(Reclassified from D5-OO-004 on 2026-06-06: the harvest country IS stated on the label —
no transparency gap exists. The annotation expresses Bari's confidence limit, a D6 function.)*

**Signal name (internal):** `origin_turkey`
**Signal class:** D6 (Confidence)
**Annotation type:** Confidence qualifier (research-backed traceability limit)

**Definition:** The product's country of harvest is Turkey (ISO: TR). Published international
trade compliance research documents elevated variability in olive oil standards conformance
for Turkish-origin oils. This is a population-level statistical finding — it does not assert
that any individual product is non-conforming. Bari uses this finding to qualify its
confidence in the origin claim, not to characterize the specific product.

**Why D6 (not D5):** The origin is stated on the label (Turkey) — there is no transparency
gap. The annotation describes a limit on Bari's ability to independently verify origin
authenticity, which is a confidence dimension, not a disclosure dimension.

**Evidence base:** Global Food Fraud and Authenticity research doc (peer-reviewed synthesis,
cited by the owner as reliable, 2026-06-06). Turkey appears in multiple published trade
compliance surveillance datasets. Evidence Registry entry: BEV-083 (Section 7).

**Signal activation:** `olive_harvest_country = "TR"` (case-insensitive). Only fires when
harvest country is explicitly confirmed "TR" from label data — never inferred.

**Status:** APPROVED (owner directive, 2026-06-06); reclassified D5→D6 on owner review
2026-06-06. Consumer-facing copy updated and approved (Section 5).

**Governance:**
- BEV-001: The annotation qualifies Bari's confidence in the claim — it does not accuse the
  product or brand of adulteration.
- Language must use confidence-limit framing. The annotation must NOT use words like
  "מזויף," "מסולף," or alarm framing that accuses a named brand.
- The annotation is surfaced in D6 expansion only — never in the collapsed leaderboard row.
- A Turkish-origin product receives the same quality grade from D1–D4 as any other product
  with equivalent nutritional structure.

---

## 4. D6 (Confidence) Signal Definitions

D6 signals describe what Bari can and cannot verify about a product's claims. All D6
signals are annotation-only. None trigger a score change.

---

### D6-OO-001 — PDO/PGI Certification Verification

**Signal name (internal):** `pdo_pgi_verification_status`
**Signal class:** D6 (Confidence)
**Annotation type:** Verification state annotation

**Definition:** Some olive oils carry Protected Designation of Origin (PDO) or Protected
Geographical Indication (PGI) certification marks (EU: DOP/IGP; Hebrew: הגנה על מקור /
הגנה גיאוגרפית). These certifications guarantee that the oil was produced, processed, and
prepared in a defined geographical area under registered quality standards.

The EU maintains the eAmbrosia registry of all registered PDO/PGI food names. However,
eAmbrosia has no public REST API as of 2026-06-06. Cross-referencing a label's cert claim
against the registry requires scraping the HTML interface of:
`https://ec.europa.eu/agriculture/eambrosia/geographical-indications-register/`

**Annotation logic:**
- If the product declares a PDO/PGI mark on its label → `pdo_pgi_claimed: true`
- If the claimed name is found in a scraped snapshot of eAmbrosia → `pdo_pgi_verified: true`
- If the claimed name is NOT found → `pdo_pgi_verified: false` (mismatch annotation fires)
- If the label does not claim PDO/PGI → no annotation (absence of cert is not a concern
  for oils that do not claim one)

**Status:** `Phase 2 — requires scrape of eAmbrosia cert pages`

The Phase 2 corpus showed zero PDO/PGI claims across 258 records (gov import registry).
This may reflect the registry's limited label data rather than the actual shelf composition.
The live Shufersal re-scrape is required to determine whether PDO/PGI claims appear on
Israeli retail labels. Until then:

- Schema slots `pdo_pgi_claimed` and `pdo_pgi_verified` are reserved in the enricher.
- The eAmbrosia scrape infrastructure must be designed (by Data Agent) before this signal
  can fire.
- No consumer-facing annotation is generated for this signal until Phase 2 infrastructure
  is in place.

**Consumer-facing copy:** HELD pending Phase 2 infrastructure.

**Governance:** BEV-002 (structural description only — the annotation describes the label
claim and the registry match result, not a quality judgment).

---

### D6-OO-002 — Processing-State Plausibility Risk

**Signal name (internal):** `processing_state_risk`
**Signal class:** D6 (Confidence)
**Annotation type:** Confidence qualification (structural inferability limit)

**Definition:** "Extra virgin" olive oil is the highest quality grade of olive oil,
defined by free acidity ≤0.8% and the absence of sensory defects, as verified by
chemical and organoleptic tests. This cannot be verified from a product label alone.
When a product carries the "extra virgin" claim but provides no origin specificity,
no harvest date, and no cert mark — conditions that make independent verification
essentially impossible — this represents a structural limit on Bari's ability to confirm
the claim rather than an assertion that the claim is false.

**This signal expresses a confidence limit, not an accusation.** It is the D6 equivalent
of the "insufficient panel" confidence state in BSIP2: the data architecture prevents
verification, not proof of non-conformance.

**Activation condition:** The signal fires when ALL of the following are true:
1. The product claims "extra virgin" (שמן זית כתית מעולה or equivalent).
2. `origin_opacity` = true (D5-OO-001 fired).
3. No harvest date is stated (`harvest_date_stated` = false).
4. No PDO/PGI certification is present (`pdo_pgi_claimed` = false).

When only one or two conditions are present, the signal does not fire — those are handled
by the individual D5 signals above.

**Status:** Confirmed. All required upstream fields are now populated (D5-OO-001 firing logic
confirmed; harvest date confirmed structurally absent from Shufersal shelf; D5-OO-002
elevated to category note 2026-06-06).

**Monitoring condition:** If this signal fires on ≥70% of the shelf's extra virgin products
at any corpus expansion, it is elevated from per-product annotation to a category-level
`categoryNote` (same treatment as D5-OO-002). Evaluate firing rate before enabling
per-product rendering at each corpus expansion.

**Consumer-facing copy:** Approved below (Section 5), conditional on the above fields.

**Governance:** BEV-001 and BEV-003h ("not a health certification body") apply. The
annotation qualifies confidence in the claim; it does not constitute a finding of adulteration or non-conformance.

---

## 5. Approved Hebrew Consumer Copy

All Hebrew annotation text below is factual, third-person, and uses no alarm language.
Maximum two lines per annotation. None of these texts may appear in the collapsed leaderboard
row — they are expansion-section text only (D5/D6 drawer or expansion panel).

The language constraint is strict: no word meaning "fake," "adulterated," "contaminated,"
"suspicious," or "questionable quality" may appear.

---

### D5-OO-001 — Origin Opacity copy

> **מקור הזיתים לא מצוין על האריזה**
> רשום היכן השמן נארז, אבל לא ידוע מאיזה מדינה הגיעו הזיתים.

Translation gloss: "The origin of the olives is not stated on the packaging. It is noted
where the oil was packaged, but the country where the olives were grown is not indicated."

---

### D5-OO-003 — Multi-Country Blending copy

> **מיזוג שמנים ממדינות מרובות**
> השמן מורכב מזיתים ממדינות שונות, כפי שמצוין על האריזה.

Translation gloss: "Blend of oils from multiple countries. The oil is composed of olives
from different countries, as stated on the packaging."

---

### D6-OO-003 — Turkish Origin Confidence Qualifier copy

> **מקור הזיתים: טורקיה — ודאות אותנטיות מוגבלת**
> מחקרי ציות במסחר הבינלאומי מצביעים על שונות רבה יחסית בעמידה בתקנים בשמן זית ממקור טורקי. ברי מציינת זאת כהסתייגות אמינות — לא כממצא על המוצר הספציפי.

Translation gloss: "Olive origin: Turkey — limited authenticity certainty. International
trade compliance research indicates relatively high variability in standards conformance
for Turkish-origin olive oil. Bari notes this as a confidence qualifier — not as a
finding about this specific product."

---

### D6-OO-002 — Processing-State Plausibility Risk copy

> **כתית מעולה: ברי לא יכולה לאמת מהתווית**
> המוצר מסומן "כתית מעולה" אך אינו כולל מקור קציר, תאריך קציר, או תעודת הגנה מוכרת. אלה הם הנתונים שמאפשרים אימות עצמאי של הסיווג.

Translation gloss: "Extra virgin: Bari cannot verify from the label. The product is
labeled 'extra virgin' but does not include harvest origin, harvest date, or a recognized
protection certificate. These are the data points that enable independent verification
of the classification."

---

### D5-OO-002 — Harvest Date (category note)

This copy goes into the `categoryNote` slot on the olive oil comparison page, identical
in placement and visual treatment to the yellow caveat box used on other category pages
(e.g., cheese-spreads). It is not a per-product annotation.

> **תאריך הקציר אינו מופיע על שמני הזית בשוק הישראלי**
> תקן התיוג הישראלי אינו מחייב ציון שנת הקציר — ולכן כל שמני הזית הכתיים שנסרקו לא כללו מידע זה. תאריך הקציר הוא האינדיקטור הנגיש ביותר לרעננות השמן, ואנו מציינים את העובדה שהוא אינו מפורסם.

Translation gloss: "Harvest date does not appear on olive oils in the Israeli market. Israeli
labeling standards do not require stating the harvest year — as a result, none of the extra
virgin olive oils scanned included this information. The harvest date is the most accessible
indicator of oil freshness, and we note the fact that it is not published."

---

### Held copy (pending infrastructure)

| Signal | Reason held |
|---|---|
| D6-OO-001 (PDO/PGI mismatch) | Pending: eAmbrosia scrape infrastructure not yet built. |

---

## 6. Signal Coverage Summary

| Signal ID | Dimension | Type | Status | Consumer copy |
|---|---|---|---|---|
| D5-OO-001 — Origin opacity | D5 | Negative annotation | Confirmed | Approved |
| D5-OO-002 — Harvest date absent | D5 | Category-level note | Confirmed (2026-06-06) — 0/13 Shufersal products; category `categoryNote` | Approved (category note) |
| D5-OO-003 — Multi-country blend | D5 | Neutral annotation | Confirmed | Approved |
| D6-OO-003 — Turkish origin confidence qualifier | D6 | Confidence qualifier (research-backed) | APPROVED (owner, 2026-06-06); reclassified D5→D6 2026-06-06 | Approved |
| D6-OO-001 — PDO/PGI verification | D6 | Verification state | `Phase 2 — requires eAmbrosia scrape` | HELD |
| D6-OO-002 — Processing-state risk | D6 | Confidence qualification | Confirmed (partially pending D5-OO-002) | Approved |

---

## 7. Evidence Registry Entry — BEV-083

*(Formal entry appended to `evidence_registry_v1.md`. Reproduced here for traceability.)*

**BEV-083**
**Topic:** Turkish-origin olive oil as a confidence qualifier annotation signal
**Summary:** Peer-reviewed food fraud surveillance research documents Turkey as a
high-prevalence origin for adulterated or non-conforming olive oil in international trade.
This is a population-level statistical finding across multiple surveillance datasets —
not a per-product laboratory finding. Bari uses this signal as a D6 confidence qualifier:
products where `olive_harvest_country = TR` receive the `origin_turkey` annotation,
surfaced in the D6 expansion drawer with approved factual Hebrew copy. The signal does not
move D1–D4 scores. Evidence tier: Moderate (B) — peer-reviewed synthesis with consistent
direction but reliant on surveillance-dataset methodology. Owner-approved 2026-06-06 as a
reliable source.
**Source:** Global Food Fraud and Authenticity research doc (New Batch, 2026-06-06;
peer-reviewed synthesis); owner directive 2026-06-06 confirming source reliability.
**Status:** Accepted — `annotate_only`
**Impact:** Interpretation (D5 annotation)
**Task:** TASK-197

---

## 8. Enricher Field Specification

The BSIP1 enricher must populate the following fields for olive oil products. These are
additive to the standard enricher output — they do not replace any existing field.

| Field name | Type | Source | Notes |
|---|---|---|---|
| `olive_grade_claimed` | string | BSIP0 label | "extra_virgin" / "virgin" / "refined" / "pomace" / null |
| `olive_harvest_country` | string (ISO 3166-1 alpha-2) | BSIP0 label | Country where olives were harvested; null if not stated |
| `olive_packing_country` | string (ISO 3166-1 alpha-2) | BSIP0 label | Country where oil was bottled/packaged |
| `harvest_date_stated` | boolean | BSIP0 label | true if a harvest year or campaign year appears on label |
| `harvest_date_value` | string or null | BSIP0 label | e.g. "2024/2025" or "2025"; null if `harvest_date_stated` = false |
| `origin_blend_disclosed` | boolean | BSIP0 label | true if label explicitly states multi-country blend |
| `origin_blend_countries` | list[string] | BSIP0 label | List of ISO country codes from blend disclosure; empty list if not applicable |
| `pdo_pgi_claimed` | boolean | BSIP0 label | true if a PDO/PGI/DOP/IGP mark is present |
| `pdo_pgi_name_claimed` | string or null | BSIP0 label | Name of the designation claimed (e.g., "Kalamata PDO") |
| `pdo_pgi_verified` | boolean or null | eAmbrosia scrape | null until Phase 2 infrastructure built; true/false after verification |
| `acidity_pct_stated` | float or null | BSIP0 label | Free acidity % if stated; null otherwise |

**Derived annotation fields** (computed by the annotation engine from the enricher fields
above, not scraped directly):

| Derived field | Logic |
|---|---|
| `d5_origin_opacity` | true if `olive_harvest_country` is null AND `olive_packing_country` is not null |
| `d5_harvest_date_absent` | Confirmed category-level finding (2026-06-06). Computed as NOT `harvest_date_stated`. Not applied as a per-product annotation batch rule — surfaces as `categoryNote` instead. |
| `d5_multi_country_blend` | same as `origin_blend_disclosed` |
| `d6_origin_traceability_qualifier` | true if `olive_harvest_country` = "TR" |
| `d6_pdo_pgi_mismatch` | true if `pdo_pgi_claimed` = true AND `pdo_pgi_verified` = false |
| `d6_processing_state_risk` | true if all four conditions in D6-OO-002 definition are met |

---

## 9. Implementation Constraints

1. **All signal classes approved for consumer-facing implementation.** The `authenticity_annotation_gate`
   tripwire was cleared by the owner on 2026-06-06. Phase 5 (Frontend) is unblocked pending
   the `go_live` tripwire (separate owner decision).

2. **EDPG firewall holds.** The research doc (Turkish-origin traceability/authenticity data) calibrates the
   annotation rule. The rule itself is verified against in-house BSIP0 label data
   (`olive_harvest_country`). The external source never feeds the annotation engine directly.

3. **No lab forensics.** IRMS, NMR, GC, DNA barcoding, and any other lab-based detection
   method are permanently excluded. This spec is label-observable signals only.

4. **Hebrew only, consumer-facing.** All annotation text surfaces in Hebrew. The internal
   field names and this spec document use English for engineering clarity; no English copy
   appears in the consumer interface.

5. **No score movement.** Implementation teams must be explicitly blocked from wiring any
   D5 or D6 field into the D1–D4 score calculation path. This constraint must be enforced
   at the engine level, not by convention.

---

## 10. Open Items for Phase 5

| Item | Owner | Status |
|---|---|---|
| Harvest date (D5-OO-002) | — | RESOLVED — confirmed category-level note (2026-06-06); copy finalized in Section 5 |
| Per-product authenticity annotation go/no-go | Owner | CLEARED (2026-06-06) — `authenticity_annotation_gate` |
| eAmbrosia scrape infrastructure | Data Agent | Phase 2 dependency; PDO/PGI signal held until built |
| PDO/PGI consumer copy | Nutrition + Content Agent | Requires eAmbrosia infrastructure (held) |
| Category go-live | Owner | `go_live` tripwire — separate owner decision; Frontend draft to be prepared first |

---

*Phase 4 complete. Next action: Frontend Agent — Phase 5 implementation. go_live tripwire
(owner) is the remaining gate before the category page goes live.*
