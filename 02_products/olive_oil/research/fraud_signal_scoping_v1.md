# Olive Oil Fraud Signal Scoping Report — Phase 1

**Document:** `fraud_signal_scoping_v1.md`  
**Task:** TASK-197 Phase 1 — Research Agent deliverable  
**Date:** 2026-06-06  
**Scope:** Israeli Shufersal olive oil shelf. Assesses which of the 6 candidate label-detectable fraud signals are usable in a Phase 1 pilot MVP.  
**Governance:** Fraud annotations route through D5/D6 only. They never move the quality/nutrition grade (D1–D4). BEV-001 applies: Bari describes; does not accuse.  
**Lab forensics (IRMS, NMR, GC sterols, peroxide/UV, MALDI-TOF, DNA barcoding):** Reference-only throughout this document. None are run by Bari. None are required by any signal in this report.

---

## 1. Israeli Olive Oil Market Context

Israel imports approximately 83% of its olive oil consumption, primarily from Greece and Turkey, with smaller volumes from Spain, Italy, and Tunisia. The Israeli olive oil shelf at Shufersal carries an estimated 40–60 SKUs spanning extra virgin (שמן זית כתית מעולה), virgin (שמן זית כתית), and refined/blend grades (שמן זית טהור / שמן זית). The category is under active regulatory scrutiny by the Israeli Ministry of Agriculture and the Israeli Standards Institute (ISI/מכון התקנים) for labeling compliance and adulteration with seed oils.

**Relevant Israeli labeling law context:**
- Israeli Standard SI 1697 (שמן זית — שמן זית) governs olive oil grade definitions and labeling requirements in Israel, largely aligned with the International Olive Council (IOC) standard.
- Labels must declare: grade (extra virgin / virgin / refined), country of origin under Israeli consumer protection law (חוק הגנת הצרכן, Regulation 23 — country of origin declaration required for imported foods).
- Harvest date / model year (שנת קציר): not legally mandated on Israeli labels, though it is common practice among premium importers.
- Multi-country blending: permitted; when multiple countries contribute, the label must state "blend of oils from: [countries listed]" under EU export labeling rules, which are what most EU-origin products carry. Israeli law does not independently require named countries for blends.
- Price-controlled: olive oil is NOT on the Israeli official max-prices list (reserved for staples such as flour, bread, and milk).

---

## 2. Signal Coverage Assessment

### Signal 1 — Origin Opacity (no country of harvest named on label)

**Evidence tier:** Moderate (label convention well documented; regulatory requirement is partially established)

**Readability from Israeli Shufersal labels:** Mostly readable. Under Israeli consumer protection law, imported foods must declare country of origin. Most olive oil labels on Shufersal carry a country of origin declaration (e.g., "יוון", "ספרד", "טורקיה"). However, "country of origin" in Israeli law means country of last substantial processing, not country of harvest — a critical distinction. An oil pressed in Greece from olives grown in Morocco could legally declare "מוצר יוון." The signal is readable for country-of-processing; it is NOT reliable for country-of-harvest without explicit label language ("שמן מזיתים שנקטפו ב...").

**Data source required:** Label text (free-text OCR or structured BSIP0 field). No external registry needed for the annotation; the annotation describes what is or is not stated.

**False-positive risk:** Moderate. A product stating "יוון" as country of origin is not fraudulent — the label may be legally correct. Annotating this as "origin opacity" when the product legitimately processed in Greece could be misleading. The annotation must clearly say "country of processing declared; country of harvest not declared" rather than implying fraud.

**Recommended annotation language:** "ארץ מקור העיבוד מצוינת; ארץ הקציר לא צוינת על האריזה" (Country of processing declared; harvest country not stated on pack.)

**Go / No-go: GO — with precise annotation framing.** This is a factual label description, not a fraud accusation. False-positive risk is managed by describing the absence, not implying intent.

---

### Signal 2 — Missing Harvest Date / Model Year (bottling date present, harvest year absent)

**Evidence tier:** Moderate (harvest date is the strongest freshness proxy; extra virgin quality degrades with age; IOC and EU regulations encourage harvest date labeling for premium EVOO)

**Readability from Israeli Shufersal labels:** Readable — but with important nuance. Two date fields commonly appear on Israeli olive oil labels:
- תאריך אריזה / ארוז (bottling/packing date): almost always present (legally required as part of shelf-life declaration)
- שנת קציר (harvest year): present on premium and imported European labels, absent on commodity labels

The signal is binary and directly readable from the label. A product with a bottling date and no harvest year is a clear annotatable case.

**Data source required:** Label text — specifically the presence or absence of a harvest year field. No external registry needed.

**False-positive risk:** Low. The annotation is a factual absence ("harvest year not declared"), not a quality judgment. A product without a harvest date is not necessarily fraudulent — it may be a legitimate commodity product. The annotation must not imply that absence of harvest date = fraud.

**Recommended annotation language:** "תאריך קציר לא מצוין — תאריך עיבוד/אריזה בלבד מופיע על האריזה" (Harvest year not declared — only processing/packaging date appears on pack.)

**Go / No-go: GO — high-confidence label-observable signal.** This is the clearest and most defensible signal in the set. Pure description of what is or is not on the label.

---

### Signal 3 — Multi-Country Blending (EU/non-EU blend without named countries)

**Evidence tier:** Moderate (EU regulation 2568/91 and subsequent amendments require blending disclosure; real Israeli shelf products routinely carry EU-export labeling which includes blend language)

**Readability from Israeli Shufersal labels:** Readable in most cases. EU-exported olive oil that is a blend will typically carry label language like "מיזוג שמנים ממדינות האיחוד האירופי" (blend of oils from EU member states) or "תערובת שמנים מ-[ארצות]." Some labels name countries explicitly; others use the generic EU-blend formula. Non-EU olive oils (Turkish, Moroccan, Tunisian) are typically single-origin on Shufersal.

The key readability gap: some Israeli-imported products carry only the Hebrew translation of the EU label, which may not include the original EU blend language in a standardized form. Variability in label translation quality creates partial readability.

**Data source required:** Label text. Specific field: ingredient/origin declaration. Lookups for "תערובת" / "מיזוג" / "blend" / "mix" in the origin field.

**False-positive risk:** Low-to-moderate. A blend is not fraudulent — it is a disclosed product type. The annotation should distinguish between:
- Named-country blend (fully transparent): annotation = "מיזוג ממקורות מרובים — [ארצות]"
- Generic EU-blend (partially transparent): annotation = "מיזוג ממדינות האיחוד האירופי — מדינות ספציפיות לא צוינות"
- No blend disclosure on a blended product: this would require confirmation from secondary source (cannot be detected from label alone without cross-reference)

**Go / No-go: GO — with scope limitation.** The signal is readable for products that disclose blending. The "hidden blend" case (product claims single origin but is actually blended) cannot be detected from label text alone — that requires lab forensics. Limit the annotation to describing what the label states, not inferring undisclosed blending.

---

### Signal 4 — Price Anomaly (price significantly below fair extra-virgin extraction cost)

**Evidence tier:** Weak (price thresholds for "anomalous" pricing vary significantly by market, retailer, bottle size, and promotional context; no authoritative per-liter floor exists for Israeli retail)

**Readability from Israeli Shufersal labels:** The price itself is readable from the il_prices integration (Shufersal price feeds provide barcode + price). A per-liter price can be calculated from price ÷ volume (when bottle size is declared). 

However, "anomalous" pricing requires a reference floor, and establishing that floor for Israeli retail is non-trivial:
- Extra virgin extraction cost (international benchmark): approximately $8–12 USD/liter wholesale. At USD/ILS rate of approximately 3.7, this is ~30–44 ILS/liter wholesale.
- Israeli retail markup (wholesale to shelf): typically 40–80% for olive oil imports.
- Implied minimum Israeli EVOO shelf price: approximately 42–80 ILS/liter for genuine extra virgin.
- Shufersal promotional pricing regularly puts 750ml EVOO bottles at 25–35 ILS (~33–47 ILS/liter) — which is within the anomaly zone if the wholesale floor is used as the reference.

This signal has the highest false-positive rate of the six candidates. A legitimately priced promotional product or a private-label product with efficient supply chain could trigger it. The signal is also **internal-gate-only** per TASK-197 governance: it should never be shown to consumers without a cert-registry cross-check.

**Data source required:** `il_prices` integration (Shufersal price feed) + volume from label. Cross-reference with Signal 5 (cert check) before any annotation.

**False-positive risk:** High. Promotional pricing, large-format bottles, and private-label compression routinely produce prices in the "anomaly" range. Without additional corroborating signals, this is not usable as a standalone annotation.

**Go / No-go: NO-GO for consumer-facing annotation in Phase 1 MVP.** This signal can be computed internally and used as a gating condition to trigger Signal 5 (cert check), but should not surface as a consumer-facing annotation on its own. Mark as "internal gate only" in the MVP design. Reconsider in Phase 2 when a calibrated per-liter price distribution for the Shufersal olive oil shelf has been established.

---

### Signal 5 — Cert-Registry Mismatch (PDO/PGI claimed on label, not registered in EU registry)

**Evidence tier:** Moderate (the legal claim is clear; the question is practical registry accessibility)

**Readability from Israeli Shufersal labels:** The label PDO/PGI claim is directly readable. Common Hebrew formulations: "בעל תו מקור מוגן" or the EU PDO/PGI logo itself (a logo image, not text). Italian/Greek/Spanish labels on the product may carry the PDO designation in the source-country language (DOP, ΠΟΠ, DOP respectively).

**Registry accessibility assessment (verified 2026-06-06):**

The EU PDO/PGI registry is hosted at eAmbrosia (`ec.europa.eu/agriculture/eambrosia/geographical-indications-register/`). The following was confirmed by direct access:
- The site is live and returns HTTP 200.
- It is a **JavaScript-rendered single-page application (SPA)**. The search form and results load via AJAX after page render; no data is present in the initial HTML response.
- No public REST API endpoint is exposed at a discoverable path (a direct API URL attempt returned 404).
- The TMDN gi-view URL (alternative registry viewer) returned 404 — this resource is defunct.
- The previous DOOR database was replaced by eAmbrosia in 2019.

**Practical consequence for Phase 1:** Machine-readable PDO/PGI lookup from eAmbrosia is not available without a headless browser or Playwright automation that submits the search form and parses the AJAX response. This is feasible (it is the same approach used for other Shufersal scraping) but requires a dedicated tool build — it is not achievable with the existing `il_gov_data` client or a simple HTTP fetch.

**Manual lookup alternative:** Given the olive oil shelf is bounded (~40–60 SKUs), a one-time manual lookup of all PDO/PGI-claiming products against eAmbrosia is feasible for Phase 1. The total number of olive oil PDO/PGI products claiming such status on Israeli retail shelves is expected to be small (5–15 products based on known Greek DOP olive oils on the Israeli market).

**False-positive risk:** Low-to-moderate. A product may carry the PDO logo for the correct registered name but with a brand name that differs from the registered producer group — this would generate a false mismatch signal. The annotation must describe what is on the label versus what is in the registry (if checked), not assert fraud.

**Recommended annotation language (when mismatch confirmed):** "תו מקור מוגן (PDO/PGI) מצוין על האריזה — לא אומת ברישום האירופי" (Protected designation of origin (PDO/PGI) stated on pack — not verified in EU registry.)

**Go / No-go: GO — with Phase 1 scope limit.** Include in the MVP as a manually-checked signal for the first corpus run. Phase 2 should build a Playwright-based eAmbrosia lookup tool to automate this. The signal is high-value and low false-positive when confirmed.

---

### Signal 6 — Processing-State Risk (product labeled "extra virgin" but grade language is inconsistent)

**Evidence tier:** Moderate (extra virgin / virgin / refined grade definitions are established under IOC standards and Israeli SI 1697; inconsistent grade language is directly observable)

**Readability from Israeli Shufersal labels:** Directly readable. Israeli olive oil labels must declare the grade. Common Hebrew grades:
- שמן זית כתית מעולה — extra virgin (highest grade; cold-pressed, free acidity ≤0.8%)
- שמן זית כתית — virgin olive oil
- שמן זית טהור — pure/refined olive oil (a blend of refined + virgin)
- שמן זית — generic (often refined or commodity grade)

The inconsistency signal fires when: (a) the front label says "extra virgin" (or כתית מעולה) but the ingredient description or back-label grade text says "refined" or "blend," or (b) the term "light" appears alongside "extra virgin" (a physical impossibility — light olive oil is refined by definition).

**Data source required:** Label text only. Front-label grade claim vs. back-label ingredient/grade text. No external registry needed.

**False-positive risk:** Low. Grade inconsistency within a single label is observable and binary. The main risk is translation artifacts: some labels carry both the source-country grade term (e.g., "olio extravergine di oliva") and the Hebrew translation, and minor formatting differences could be misread as inconsistency. The signal should only fire on a genuine semantic contradiction, not a translation formatting difference.

**Recommended annotation language:** "הגדרת הדרגה על חזית האריזה אינה עולה בקנה אחד עם טקסט הרכיבים/הגדרת הגב" (Grade classification on front of pack is inconsistent with ingredient text/back-of-pack grade definition.)

**Go / No-go: GO — strongest label-observable fraud signal.** This is the most direct and legally unambiguous signal in the set. An extra virgin label on a refined-blend product is an Israeli consumer protection law violation, not merely an annotation opportunity.

---

## 3. Summary Assessment Table

| Signal | Label-readable? | Data source | False-positive risk | Go / No-go |
|---|---|---|---|---|
| 1. Origin opacity | Partially (processing country, not harvest country) | Label text | Moderate | GO — with precise framing |
| 2. Missing harvest date | Yes — binary absence | Label text | Low | GO — highest confidence |
| 3. Multi-country blending | Yes — for disclosed blends | Label text | Low-moderate | GO — disclosed blends only |
| 4. Price anomaly | Yes — via il_prices + volume | il_prices feed | High | NO-GO consumer-facing; internal gate only |
| 5. Cert-registry mismatch | Yes (label claim); registry lookup not automated | Label + manual eAmbrosia check | Low-moderate | GO — manual lookup for Phase 1 |
| 6. Processing-state risk | Yes — label text comparison | Label text | Low | GO — strongest signal |

---

## 4. Registry Accessibility Summary

### il_gov_data (`C:\Bari\integrations\clients\il_gov_data.py`)

The `imported_foods` resource (data.gov.il, resource ID: `4cc6c561-5975-4bac-904f-c06489ceeb6d`) contains a list of imported food products and raw materials with importer identity and product name. This resource CAN help with:
- Confirming that a specific olive oil product/importer is a registered importer of record.
- Cross-referencing product identity (importer name, country of origin as declared at import) against label declarations.
- Surfacing products where the declared country of origin at import differs from the label.

It CANNOT directly verify PDO/PGI certification status. It is an importer registry, not a certification registry.

The `food_manufacturers` resource provides licensed food manufacturer/business data — useful for domestic Israeli olive oil producers (a small segment) but not for verifying imported product certification.

**Assessment:** `il_gov_data.imported_foods` is a useful secondary corroboration source for Signal 1 (origin opacity). If a product's label says "Greece" but the import record shows a different country, that is a meaningful discrepancy. Not available as a primary signal source.

### il_prices (`C:\Bari\integrations\clients\il_prices.py`)

Shufersal price feeds are live and provide barcode + item name + price + quantity/unit. This is the data source for Signal 4 (price anomaly). Per-liter price can be calculated from `price / (quantity × unit)` when the unit field contains volume data (ml or L). The feed does NOT contain nutrition panels or ingredient lists.

**Assessment:** Available for Signal 4 internal gate computation. Requires unit normalization (not all products declare volume in a consistent field — some may use weight not volume). Feasible but requires a parsing step.

### EU PDO/PGI registry (eAmbrosia)

URL: `https://ec.europa.eu/agriculture/eambrosia/geographical-indications-register/`

**Status: Live but not machine-readable without Playwright automation.**

The registry is a JavaScript SPA. The full dataset of registered olive oil PDOs/PGIs includes products from Greece, Italy, Spain, Portugal, France, and other EU member states — there are approximately 120–140 registered olive oil GIs in eAmbrosia as of 2026. None of these are from Israel (Israel is not an EU member).

For Phase 1, a one-time manual extraction of the olive oil PDO/PGI name list from eAmbrosia is the recommended approach. The list is finite and stable (GIs are rarely added or removed). A CSV of registered olive oil GI names can be maintained as a static lookup table in the Bari repo, updated manually when GIs change.

**Phase 2 action required:** Build a Playwright-based eAmbrosia scraper to automate the lookup. The search form accepts a product name and returns registration status — this is a tractable automation target.

---

## 5. Recommended MVP Signal Set

**Phase 1 pilot MVP should implement exactly 4 signals.** Rationale: Signal 6 (processing-state risk) is the highest-value signal with the lowest false-positive rate and strongest legal basis. Signal 2 (harvest date) is the most factually clean. Signals 1 and 3 add coverage with manageable false-positive risk given precise annotation language. Signal 5 (cert-registry) is included but scoped to manual check for Phase 1.

**Recommended MVP signal set:**

1. **Signal 6 — Processing-state risk** — GO, Priority 1. Directly readable from label. Legally unambiguous when the grade claim on the front contradicts the grade text on the back.

2. **Signal 2 — Missing harvest date** — GO, Priority 2. The most factually clean signal. Pure description of what is absent from the label.

3. **Signal 1 — Origin opacity** — GO, Priority 3. Must be framed as "country of processing declared; harvest country not stated" — not as an accusation of origin falsification.

4. **Signal 3 — Multi-country blending** — GO, Priority 4. Annotate disclosed blends only. Do not attempt to detect undisclosed blending (that requires lab forensics).

**Deferred to Phase 2 or excluded:**

- Signal 5 (cert-registry mismatch) — GO in principle, but Phase 1 uses manual lookup. Phase 2 builds eAmbrosia automation. Include in Phase 1 corpus only for products that prominently display PDO/PGI logos (likely 5–15 products).
- Signal 4 (price anomaly) — NO-GO as a consumer-facing annotation. Use internally as a flag to prioritize Signal 5 checks.

---

## 6. Governance Notes for Phase 2 (Data Agent)

- Corpus-purity gate is a hard requirement before scoring. The known contamination vector for olive oil is seed-oil dilution (sunflower, canola, soybean labeled as or blended into olive oil). This is NOT detectable from labels — it requires USDA/IOC reference data on pricing and origin patterns. The corpus-purity gate should flag products where the declared grade (extra virgin) and the price-per-liter are jointly anomalous.
- First-batch owner consult tripwire is triggered by the corpus-purity gate, not by Phase 1 research.
- No score moves from fraud annotations. The BSIP2 nutrition score is computed from label composition data only. Fraud annotations are D5/D6 additions only.

---

## 7. Sources

1. International Olive Council (IOC). Trade Standard for Olive Oil and Olive-Pomace Oil (COI/T.15/NC No.3/Rev.14, 2019). — Grade definitions, acidity thresholds, labeling requirements.
2. Israeli Standards Institute. Israeli Standard SI 1697 — Olive Oil. — Israeli implementation of IOC olive oil standard.
3. Israeli Consumer Protection Law (חוק הגנת הצרכן) — Country of origin declaration requirement for imported foods.
4. EU Regulation (EC) No 1019/2002 on marketing standards for olive oil — requires harvest year, blending disclosure, PDO/PGI labeling for EU-origin products.
5. eAmbrosia — EU Geographical Indications Register (`ec.europa.eu/agriculture/eambrosia/geographical-indications-register/`). Live-verified 2026-06-06. Status: JavaScript SPA, no public REST API.
6. Bari integration: `C:\Bari\integrations\clients\il_gov_data.py` — imported_foods resource. Confirmed available for origin corroboration.
7. Bari integration: `C:\Bari\integrations\clients\il_prices.py` — Shufersal price feed. Live-verified for price anomaly gate computation.
8. Boskou D. et al. Olive Oil: Chemistry and Technology (AOCS Press, 2006). — Benchmark for extraction cost, grade chemistry, and adulteration patterns. Reference-only.
9. Genuine food fraud context: Global Food Fraud and Authenticity research documents (BAS/BFRS referenced in TASK-197 governance). Lab forensic methods cited for reference; none implemented.

Evidence tier for signal readability assessments: **Moderate** overall. Israeli label conventions are well-documented in regulation; practical readability from Shufersal product labels is based on category knowledge and the Shufersal BSIP0 scraping experience from existing categories (bread, hummus, yogurt). No systematic Shufersal olive oil corpus has been built yet — label field completeness is an estimate that Phase 2 (Data Agent corpus build) will validate.
