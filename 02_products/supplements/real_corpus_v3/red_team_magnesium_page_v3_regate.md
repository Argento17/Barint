# Red-Team Re-Gate Report — Magnesium Comparison Page v3 (Post-Patch)
Date: 2026-06-23
Scope: 19 products, /hashvaot/magnesium
Challenger: adversarial-qa-agent (re-gate — v3 CONDITIONAL PASS patch verification)
Prior report: C:\Bari\02_products\supplements\real_corpus_v3\red_team_magnesium_page_v3.md
Authoritative score source: C:\Bari\02_products\supplements\real_corpus_v3\_corpus_run_full_v10.json
Page data file: C:\Bari\bari-web\src\lib\comparisons\magnesium-page-data.ts

---

## D10 Gate Verdict: CONDITIONAL PASS — NOT GO

**Track V: PASS** (19/19 score propagation correct; all arithmetic confirmed; leakage clean; OFF ban clean)
**Track C: 0 CRITICAL open | 1 HIGH open (RT-7, unchanged) | 1 new MEDIUM (RT-7b) | 3 MEDIUM carry-forward | 1 LOW carry-forward**

**Consumer launch: NO-GO.** RT-7 (image identity for 2 products) remains unresolved. A new panel-vs-page capsule count discrepancy for Tink 520 (RT-7b, MEDIUM) also emerged from the patch itself. Both must be resolved before Product Agent can issue go/no-go. See Findings section.

---

## Patch Verification Results

### Patch 1 — RT-NEW-1: Altman Citrate 120 false-equivalence claim

**Prior state (v3):** rowVerdict said "9 mg absorbed is exactly the same as cheap oxide products." limitingFactors said "same quantity as oxide." Both were factually wrong: oxide products deliver 19–43% more absorbed mg than this citrate at ~9 mg.

**Patch claim:** rowVerdict and limitingFactors rewritten to state the TRUE relationship: oxide products deliver MORE (11–13 mg), not the same; the small dose erases citrate's form advantage; at ₪167 it is poor value. First rowVerdict paragraph (200 mg citrate → 32 mg elemental → ~9 mg) preserved.

**Verification — arithmetic:**
- 200 mg citrate × 16.2% = 32.4 mg elemental × 27% = 8.75 mg absorbed (~9 mg): CONFIRMED in page
- Oxide comparison: MagUp (450 mg × 60.3% × 4% = 10.85 mg, ~11 mg), Nutricare/Tink/Altman 520 (520 mg × 60.3% × 4% = 12.54 mg, ~13 mg). Page states "11–13 מ\"ג נספגים": CONFIRMED CORRECT (11 and 13 are valid endpoints)
- The claim "יותר מהמוצר הזה, למרות שאוקסיד נחות כצורה" is factually precise: oxide inferior as form, but delivers more absorbed mg due to higher compound dose. DEFENSIBLE.

**Verification — copy (current page):**
- rowVerdict paragraph 1: "כתוב על האריזה 200 מ\"ג ציטראט — כלומר בערך 32 מ\"ג מגנזיום יסודי. ציטראט נספג בכ-27%, כך שהגוף מקבל לנטילה היומית המומלצת בקירוב 9 מ\"ג." — INTACT AND CORRECT
- rowVerdict paragraph 2: "מחיר ₪167 — מהגבוהים במדף. מוצרי האוקסיד הזולים במדף מספקים 11–13 מ\"ג נספגים — יותר מהמוצר הזה, למרות שאוקסיד נחות כצורה. המינון הקטן מוחק את יתרון הציטראט, ובמחיר הזה התמורה גרועה." — CORRECT
- limitingFactors[1]: "כ-9 מ\"ג נספגים — פחות מאשר מוצרי האוקסיד הזולים במדף (11–13 מ\"ג נספגים)" — CORRECT (reversed from prior false-equivalence)
- insightLine: "ציטראט נספג בכ-27% — אך המינון קטן מדי. כ-9 מ\"ג נספגים, ₪167. תמורה גרועה." — CORRECT
- Old false-equivalence phrases ("בדיוק כמה שנספג", "אותה כמות כמו") NOT FOUND in file.

**Verification — no חשוב opener:** rowVerdict opens with "כתוב על האריזה..." — no חשוב opener. PASS.
**Verification — no framework leakage:** No cap_, binding_constraint, sub_score, or BSIP terms in consumer strings. PASS.
**Naturalness (F1/F2):** F1=4-5 ("המינון הקטן מוחק את יתרון הציטראט" — active verb, native structure; "ובמחיר הזה התמורה גרועה" — punchy closing). F2=5 (clear verdict with numbers and comparison). T1–T7 tells: none found. PASS.

**Patch 1 verdict: CONFIRMED CORRECT AND COMPLETE.** The false-equivalence is fixed. The new copy is factually correct, carries numbers, reads as natural native Hebrew, contains no translationese tells, no חשוב opener, no framework leakage.

---

### Patch 2 — RT-7: Tink Oxide 520 name correction (60 → 90 כמוסות)

**Prior state (v3):** Product name showed "520 60 כמוסות." Claim was that barcode 7290015318426 is the 90-capsule SKU at every Israeli retailer; "60" was a data error.

**Patch claim:** Name now reads "טינק מגנזיום אוקסיד 520 90 כמוסות." No other string for this product claims 60 capsules.

**Verification — page name:** Page line 167: `name: "טינק מגנזיום אוקסיד 520 90 כמוסות"` — CONFIRMED UPDATED TO 90.
**Verification — no 60 reference in product section:** Searched content from id "7290015318426" to next product entry. No "60 כמוסות" found in the Tink 520 section. PASS.
**Corpus name_he:** v10 corpus `name_he` = "טינק מגנזיום אוקסיד 520  90 כמוסות" (note double-space artifact). Consistent with 90-count. CONFIRMED.

**NEW FINDING (RT-7b — MEDIUM):** The panel source data (bteva.co.il scrape, URL: https://www.bteva.co.il/tink-magnesium-oxide-520) still records `product_name = "טינק מגנזיום אוקסיד 520 60 כמוסות"` and `servings_per_container = "60"`. The corpus name_he was updated to 90, but the underlying panel was not updated. This creates a data integrity discrepancy:

- v10 corpus name_he: 90 כמוסות
- v10 corpus panel product_name: 60 כמוסות
- v10 corpus panel servings_per_container: 60
- Page data.ts name: 90 כמוסות

If the actual product barcode 7290015318426 is the 60-count SKU (as the panel source states), then the name correction went in the wrong direction: the page now displays an incorrect product count, and the tinc.co.il image URL (catalog_941469-l.jpg) may be for the 60-count, not the 90-count. This compounds the existing RT-7 image-identity finding.

Routes to: data-agent (independently verify count for barcode 7290015318426 from TINC brand site or another Israeli retailer source before consumer launch).

**Patch 2 verdict: PARTIALLY CONFIRMED.** Name was changed on page — that is factual. But the underlying panel source contradicts the change and was not updated. RT-7 (image identity) remains open; the name change adds a new capsule-count discrepancy to the same product. See RT-7b finding below.

---

### Patch 3 — Magnox B6: ingredients and rowVerdict fix

**Prior state (v3):** The prior report's arithmetic check confirmed Magnox B6 was being scored correctly. The patch described here is:
- rowVerdict now reads "432 מ\"ג אוקסיד — כלומר בערך 260 מ\"ג מגנזיום יסודי"
- ingredients no longer label 432 mg as elemental

**Verification — ingredients field:** Page ingredients: "מגנזיום (magnesium oxide), 432 מ\"ג; ויטמין B6" — CONFIRMED. Does NOT say elemental. PASS.
**Verification — rowVerdict:** "כתוב על האריזה 432 מ\"ג אוקסיד — כלומר בערך 260 מ\"ג מגנזיום יסודי. אוקסיד נספג בכ-4% — הגוף מקבל לנטילה היומית המומלצת בקירוב 10 מ\"ג." CONFIRMED.
**Arithmetic: 432 × 60.3% = 260.5 ≈ 260 ✓. 260.5 × 4% = 10.42 ≈ 10 ✓.** Matches engine ceiling 40.68 (back-calc: absorbed = 6 + (40.68−35) × 7/9 = 10.42 mg). PASS.
**No elemental label in consumer strings:** Searched entire Magnox B6 section for "אלמנטלי" and "(elemental)". None found in consumer-facing strings. PASS.

**PRE-EXISTING CONCERN (not new, upgraded to HIGH for explicit acknowledge-before-launch flag):**

The v10 panel `bsip0s_label.actives[0]` shows `display_name = "מגנזיום (elemental)"`, `form = oxide`, `amount = 432`, with `oxide_misleading_true = True`. The `oxide_misleading_note` states: "oxide form with non-trivial elemental dose — 'high elemental magnesium' framing is technically true but misleading." This means the **product itself labels 432 mg as elemental magnesium** (a common but confusing Israeli supplement labeling practice where manufacturers print the elemental amount, not the compound weight).

If Magnox B6's Israeli label states 432 mg elemental magnesium (oxide), then:
- The correct absorbed-mg chain would be: 432 mg elemental × 4% = 17.28 mg absorbed (~17 mg), not ~10 mg
- The engine treated 432 mg as compound (oxide compound × 60.3% = 260 mg elemental), confirmed by ceiling back-calc = 10.42 mg
- If the product is 432 mg elemental: engine absorbed-mg = **wrong**, score would be C/~55, not D/40
- The page copy "432 mg oxide → ~260 mg elemental → ~10 mg absorbed" would be **factually wrong** if 432 is already elemental

This is not introduced by Patch 3. Patch 3 made the page internally consistent with the engine's compound interpretation. The FINAL_v1 document explicitly flags this: "Amazon source: geographically questionable; re-verification recommended before consumer-facing deployment." The concern predates this re-gate session.

Severity escalation note: In the v3 report this was subsumed under the Magnox provenance footnote. It now deserves explicit HIGH acknowledgment at launch time because the `oxide_misleading_true` flag means the product **advertises 432 mg elemental** — which is exactly the basis the engine used to apply `oxide_misleading_true`. If the engine's compound-vs-elemental interpretation is wrong, this is not just a copy issue but a score error. Routes to: data-agent (verify Israeli label: is 432 mg the compound weight or the elemental weight?), nutrition-agent (confirm correct computation path).

**Patch 3 verdict: CONFIRMED CORRECT relative to engine's interpretation.** The copy is internally consistent and the arithmetic chain is correct for the compound interpretation. However, the underlying compound-vs-elemental question for the actual Israeli product is OPEN and must be resolved before consumer launch (pre-existing flag, now raised to HIGH acknowledgment level).

---

### Patch 4 — Header comment cites v10

**Prior state (v3):** Line 3 of magnesium-page-data.ts cited `_corpus_run_full_v9.json` as source of truth (stale comment — actual scores matched v10).

**Verification — line 3 (0-indexed line 2):**
`// Source of truth: C:\Bari\02_products\supplements\real_corpus_v3\_corpus_run_full_v10.json` — CONFIRMED UPDATED TO V10. PASS.

**Residual defect:** Line 6 (0-indexed line 6) still reads:
`// v0.3.1 (SUPP-EV-030 v2). Grade range: C (1) · D (12) · E (6) = 19 total. 0 A/B.`
Actual current engine version is v3.1 (SUPP-EV-030 v3). The engine version reference in line 6 was NOT updated. This is a non-consumer-facing maintenance defect (LOW severity), carried forward from the v3 report's RT-NEW-4 finding.

**Patch 4 verdict: PARTIALLY CONFIRMED.** Line 3 updated to v10 — CORRECT. Line 6 engine version still says v0.3.1/SUPP-EV-030 v2 — still stale. Non-consumer-facing; does not block launch. Routes to: frontend-agent.

---

## Track V — Verification

### V-1: Score Propagation — Full 19/19

| Barcode | v10 Score | Page Score | Delta | v10 Grade | Page Grade | Grade Match | Result |
|---|---|---|---|---|---|---|---|
| 7290001066973 | 58.5 | 58 | −0.5 | C | C | PASS | PASS |
| 7290118818205 | 49.0 | 49 | 0.0 | D | D | PASS | PASS |
| 0033984005181 | 45.2 | 45 | −0.2 | D | D | PASS | PASS |
| 7290010207640 | 44.4 | 44 | −0.4 | D | D | PASS | PASS |
| 7290001065662 | 43.4 | 43 | −0.4 | D | D | PASS | PASS |
| 7290015318426 | 43.4 | 43 | −0.4 | D | D | PASS | PASS |
| 7290017218564 | 43.4 | 43 | −0.4 | D | D | PASS | PASS |
| 7290013464248 | 41.4 | 41 | −0.4 | D | D | PASS | PASS |
| 7290019444206 | 41.2 | 41 | −0.2 | D | D | PASS | PASS |
| 7290013142894 | 41.2 | 41 | −0.2 | D | D | PASS | PASS |
| 7290017847122 | 40.7 | 40 | −0.7 | D | D | PASS | PASS |
| 7290011899967 | 38.5 | 38 | −0.5 | D | D | PASS | PASS |
| 7290019444480 | 37.2 | 37 | −0.2 | D | D | PASS | PASS |
| 7290015429245 | 34.5 | 34 | −0.5 | E | E | PASS | PASS |
| 7290001065594 | 34.0 | 34 | 0.0 | E | E | PASS | PASS |
| 7290018439043 | 34.0 | 34 | 0.0 | E | E | PASS | PASS |
| 7290015318532 | 32.6 | 32 | −0.6 | E | E | PASS | PASS |
| 7290018439579 | 30.0 | 30 | 0.0 | E | E | PASS | PASS |
| 7290118816065 | 28.8 | 28 | −0.8 | E | E | PASS | PASS |

**19/19 PASS. Max delta −0.8 (integer display rounding). Grade distribution C=1, D=12, E=6. No regressions.**

### V-2: Arithmetic Regression — 14/14 calculable products

All 14 absorbed-path products: elemental and absorbed-mg arithmetic chains verified against engine trace ceiling back-calculations. No discrepancies vs prior v3 report. **14/14 PASS.**

### V-3: Sort Order

C band: 1 product — trivially correct.
D band (absorbed-path): NT LC (44.4) > 520s×3 (43.4) > Supherb Citrate (41.4) > MagUp=Balance (41.2) > Magnox (40.7) > Altman Citrate 120 (38.5) > Altman Bisglycinate (37.2) — PASS.
D band (hidden-composition, last): Max 550 (49) then Solgar (45) — PASS.
E band: Amorphicure (34.5) > Nano=WELL (34.0) > Tink Malate (32.6) > Taurate (30.0) > TRIOMAG (28.8) — PASS.

**Sort order: 3/3 bands PASS.**

### V-4: Leakage Check

Framework terms (cap_, BSIP, NOVA, structural_class, binding_constraint, sub_score, fairy, absorbed_ceiling) checked in consumer-facing strings (code comments stripped). **All 8 checked: CLEAN.**
OFF references: 0. Image domains: vitamins4all.co.il, teva-call.co.il, altman.co.il, solgar.co.il, biogaya.co.il, tinc.co.il — all OFF-free.

**Leakage: PASS. OFF ban: PASS.**

### V-5: Draft Disclaimer Status

"ציונים אלו טרם אושרו לפרסום צרכני" present in both categoryNote and methodologyLines. robots:noindex guard not inspected in this session (confirmed present in v3 prior report). **Draft status: IN PLACE.**

### Track V Verdict: PASS

One LOW non-consumer-facing residual: line 6 engine version comment still says v0.3.1/SUPP-EV-030 v2 (should be v3.1). Routes to: frontend-agent.

---

## Track C — Adversarial Challenge

### CRITICAL findings: 0

### HIGH findings open: 2

**RT-7 (HIGH, carry-forward from v1/v2/v3 — UNCHANGED):**

Two products with unverifiable image identities:
- 7290013142894 (Altman MagUp): image at altman.co.il UUID filename (`_i/bd7e8878-3115-4e63-9646-d28e5d617979.webp`) — no barcode anchor. Grade D/41. Image identity NOT independently verified.
- 7290015318426 (Tink Oxide 520): image at tinc.co.il catalog ID (`catalog_941469-l.jpg?637595154336530000`) — no barcode anchor. Grade D/43. Name patch changed 60→90 capsules but the catalog image was NOT re-verified for the 90-count SKU. If this is the 60-count catalog image, the displayed product image is wrong.

The panel source for Tink 520 (bteva.co.il) still records 60-count. If the image at tinc.co.il is for the 60-count SKU, then both the product name (90) AND the image are mismatched with the panel-identified product.

Routes to: data-agent.

**RT-7b-HIGH — New: Tink 520 panel/page capsule count discrepancy**

This is a direct finding from Patch 2 verification. The v10 corpus panel for barcode 7290015318426 records:
- `panel.product_name`: "טינק מגנזיום אוקסיד 520 60 כמוסות"
- `panel.servings_per_container`: "60"
- Source: bteva.co.il

The page and corpus name_he both now say 90 כמוסות. The panel source was NOT updated.

The patch justification ("every Israeli retailer shows 90-count") is an external claim that cannot be verified from the artifacts alone. The only in-corpus panel data points to 60-count. This is not a framing ambiguity — it is a data discrepancy about the physical product on shelf. A consumer who buys Tink Oxide 520 based on the "90 כמוסות" label may receive a 60-count package if the panel source is correct.

Severity: HIGH — potential consumer-facing product identity error (60 vs 90 capsule count affects price-per-dose reasoning).

Routes to: data-agent (verify barcode 7290015318426 capsule count from TINC brand site tinc.co.il directly, and from a second Israeli retailer; confirm servings_per_container before launch).

**RT-NEW-Magnox-HIGH — Pre-existing, now raised to explicit acknowledge-before-launch level:**

The v10 bsip0s_label for barcode 7290017847122 (Magnox B6) shows `oxide_misleading_true = True` with note: "oxide form with non-trivial elemental dose — 'high elemental magnesium' framing is technically true but misleading." The panel ingredient name is "מגנזיום (elemental), 432 mg, form=oxide." This flag exists because the product ADVERTISES 432 mg as elemental magnesium.

The engine treated 432 mg as the oxide compound weight (confirmed: ceiling back-calc = 10.42 mg absorbed = 432 × 60.3% × 4%). The page copy follows: "432 mg oxide → ~260 mg elemental → ~10 mg absorbed."

If the Israeli product label actually states 432 mg elemental magnesium (as the panel ingredient name suggests), then:
- The page copy "432 mg oxide → 260 mg elemental" is factually wrong (the label says elemental, not oxide compound)
- The actual absorbed calculation would be: 432 mg elemental × 4% = 17.28 mg (~17 mg, not ~10 mg)
- The score should be ~C/55, not D/40 — a grade change
- The `claimShortfallFlag` "~כ-10 מ\"ג נספגים" and `absorbedMgPill` "נספג: ~כ-10 מ\"ג" would be wrong

The Amazon provenance (not an Israeli source, per FINAL_v1 explicit flag) makes this unresolvable from the current corpus. Panel `ingredient_list_raw` = None (no raw label text available for disambiguation).

This is NOT introduced by Patch 3. But it must be explicitly acknowledged before consumer launch given the direct consumer-facing impact (absorbed-mg number and grade shown on page could be wrong by a factor of ~1.7× if the label is elemental-first).

Routes to: data-agent (obtain Magnox B6 label from Israeli source — Super-Pharm, Yochananof, or brand site — to confirm whether 432 mg is the compound weight or the elemental weight), nutrition-agent (confirm correct computation path).

### MEDIUM findings open: 3

**RT-9 (MEDIUM, carry-forward — UNCHANGED):** Magnesia (5 products), Life brand (3 products), and other brands not in corpus are not disclosed on the page. Routes to: content-agent, product-agent.

**RT-11 (MEDIUM, carry-forward — UNCHANGED):** Three products at D/43 (7290001065662, 7290015318426, 7290017218564). Tie-break order not disclosed. Routes to: product-agent, data-agent.

**RT-NEW-3 (MEDIUM, carry-forward from v3 — UNCHANGED):** "חשוב לדעת"/"חשוב להבין" openers appear 4× total (prologue line 4, categoryNote scope explainer, Malate rowVerdict, NT LC rowVerdict). Below gate-failure threshold (F1=4 confirmed across the full page); naturalness gate passes. Stylistic flag for content-agent at next revision pass.

### LOW findings open: 1

**RT-NEW-4 (LOW, carry-forward — PARTIALLY RESOLVED, residual):** Line 3 now correctly cites v10 (RESOLVED). Line 6 engine version still reads v0.3.1/SUPP-EV-030 v2 (OPEN). Non-consumer-facing. Routes to: frontend-agent.

---

## Acknowledge-Before-Launch Items

These items do not trigger a NO-GO on their own but must be explicitly acknowledged by Product Agent before any go-live directive:

1. **RT-7 (HIGH):** Image identity for Altman MagUp (UUID) and Tink Oxide 520 (catalog ID) NOT independently verified. Requires data-agent verification from brand/retailer page source.
2. **RT-7b (HIGH):** Tink Oxide 520 capsule count: page says 90, panel source says 60. Requires data-agent verification from TINC brand site or second Israeli retailer.
3. **RT-NEW-Magnox (HIGH):** Magnox B6 compound-vs-elemental ambiguity: engine treats 432 mg as compound, but the product may label 432 mg as elemental. If elemental, the absorbed-mg figure and score are wrong. Requires data-agent verification of Israeli label.
4. **RT-9 (MEDIUM):** Brand omission: Magnesia and Life brands not in corpus; no disclosure on page.
5. **RT-11 (MEDIUM):** Tie-break within D/43 band not disclosed.
6. **RT-NEW-3 (MEDIUM):** Naturalness: "חשוב לדעת"/"חשוב להבין" 4× total.

---

## Summary: What Changed vs v3 Prior Report

| Finding | v3 Status | Re-gate Status |
|---|---|---|
| RT-NEW-1 (HIGH): Altman Citrate 120 false-equivalence | OPEN | RESOLVED — copy factually correct |
| RT-7 (HIGH): Image identity 2 products | OPEN | STILL OPEN — not changed |
| RT-7b (HIGH): Tink 520 panel/page count discrepancy | Not present | NEW from Patch 2 |
| RT-NEW-Magnox (HIGH): Magnox B6 compound/elemental ambiguity | Subsumed in provenance note | RAISED TO HIGH explicit acknowledgment |
| RT-9 (MEDIUM): Brand omission | OPEN | STILL OPEN |
| RT-11 (MEDIUM): Tie-break disclosure | OPEN | STILL OPEN |
| RT-NEW-3 (MEDIUM): Naturalness routine openers | OPEN | STILL OPEN |
| RT-NEW-4 (LOW): Stale header comment | OPEN | PARTIALLY RESOLVED (line 3 fixed, line 6 still stale) |
| Patch 4 header: line 3 v10 citation | Defect | RESOLVED |
| All 19 scores: propagation | 19/19 PASS | 19/19 PASS (no regressions) |
| All 14 arithmetic chains | 14/14 PASS | 14/14 PASS (no regressions) |
| Sort order | PASS | PASS |
| Leakage | PASS | PASS |

---

## Return Contract JSON

```json
{
  "agent": "adversarial-qa-agent",
  "task_ref": "REGATE-magnesium-page-v3-post-patch",
  "run_date": "2026-06-23",
  "prior_reports": [
    "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\red_team_magnesium_page_v3.md"
  ],
  "authoritative_corpus_source": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\_corpus_run_full_v10.json",
  "page_data_source": "C:\\Bari\\bari-web\\src\\lib\\comparisons\\magnesium-page-data.ts",
  "artifacts": [
    {
      "path": "C:\\Bari\\bari-web\\src\\lib\\comparisons\\magnesium-page-data.ts",
      "purpose": "primary page data — all consumer strings, patch verification",
      "sha256": "not computed"
    },
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\_corpus_run_full_v10.json",
      "purpose": "authoritative score source — 19 magnesium products, panel data, trace",
      "sha256": "not computed"
    },
    {
      "path": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\benchmark\\magnesium_absorbed_scoring_FINAL_v1.md",
      "purpose": "scoring authority — absorption fractions, ceiling table, v3.1 grade changes",
      "sha256": "not computed"
    },
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\skus_full\\SP-7290015318426.json",
      "purpose": "Tink Oxide 520 SKU — panel source, capsule count, bsip0s_label",
      "sha256": "not computed"
    },
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\skus_full\\SP-7290017847122.json",
      "purpose": "Magnox B6 SKU — oxide_misleading_true flag, compound vs elemental disambiguation",
      "sha256": "not computed"
    }
  ],
  "counts": {
    "products_verified": "19 of 19",
    "score_propagation_pass": "19 of 19 (max delta -0.8, all grades match)",
    "arithmetic_verified": "14 of 14 calculable products",
    "leakage_items_clean": "8 of 8 framework terms",
    "off_images": "0 of 19",
    "sort_order_bands_correct": "3 of 3",
    "patches_verified": "4 of 4",
    "patches_fully_resolved": "2 of 4 (Patch 1 RT-NEW-1 RESOLVED; Patch 4 line 3 RESOLVED)",
    "patches_partially_resolved": "2 of 4 (Patch 2 name updated but panel/count discrepancy new; Patch 4 line 6 still stale)",
    "critical_findings_open": 0,
    "high_findings_open": 3,
    "medium_findings_open": 3,
    "low_findings_open": 1,
    "high_findings_resolved_since_v3": 1,
    "high_findings_new_since_v3": 2
  },
  "commands_run": [
    {"cmd": "python3 — v10 corpus structure inspection", "exit_code": 0},
    {"cmd": "python3 — extract engine_output for 4 patch barcodes", "exit_code": 0},
    {"cmd": "python3 — RT-NEW-1 arithmetic verification (citrate 8.75mg vs oxide 10.85-12.54mg)", "exit_code": 0, "result": "oxide delivers 19-43% more absorbed mg — patch copy is CORRECT"},
    {"cmd": "python3 — Magnox B6 compound/elemental analysis (ceiling back-calc = 10.42mg)", "exit_code": 0, "result": "engine treats 432mg as compound; oxide_misleading_true flag shows product advertises elemental"},
    {"cmd": "python3 — Tink 520 SKU panel inspection (bteva.co.il)", "exit_code": 0, "result": "panel says 60-count, page says 90-count — discrepancy"},
    {"cmd": "python3 — full 19/19 regression score table", "exit_code": 0, "result": "19/19 PASS, no grade changes"},
    {"cmd": "python3 — leakage check on consumer strings (comments stripped)", "exit_code": 0, "result": "8/8 framework terms CLEAN"},
    {"cmd": "python3 — naturalness T1-T7 on patched Altman Citrate 120 copy", "exit_code": 0, "result": "F1=4-5, F2=4-5, PASS"},
    {"cmd": "python3 — חשוב לדעת/חשוב להבין frequency count", "exit_code": 0, "result": "4 total (2+2), unchanged from v3"},
    {"cmd": "python3 — Patch 2 Tink name + 60-capsule reference check", "exit_code": 0, "result": "name confirmed 90; no 60 in section; panel still says 60"}
  ],
  "not_done": [
    "npm run build not re-run (no build-system changes introduced by patches; prior confirmed exit 0)",
    "E2E / Playwright not run (dev server HTTP 200 confirmed in v3; no route changes)",
    "Independent retailer verification for Tink 520 capsule count (RT-7b) — requires data-agent",
    "Independent retailer verification for Magnox B6 Israeli label compound vs elemental (RT-NEW-Magnox) — requires data-agent",
    "Image identity verification for Altman MagUp and Tink 520 (RT-7) — requires data-agent",
    "run_gates.py not invoked (supplement category not registered in gate suite)"
  ],
  "spec_acceptance_test": {
    "result": "CONDITIONAL PASS — NO-GO for consumer launch",
    "critical_open": 0,
    "high_open": 3,
    "d10_gate": "Track V fully green. Track C: 0 CRITICAL, 3 HIGH open. Consumer launch requires all 3 HIGH resolved (RT-7 image identity, RT-7b Tink count, RT-NEW-Magnox elemental disambiguation).",
    "patch_1_rt_new1": "RESOLVED — false-equivalence corrected, copy factually correct and natural",
    "patch_2_rt7_name": "PARTIAL — name updated to 90 on page, but panel says 60; new discrepancy RT-7b raised",
    "patch_3_magnox": "CONFIRMED relative to engine interpretation — but underlying compound/elemental ambiguity raised to HIGH",
    "patch_4_header": "PARTIAL — line 3 v10 citation fixed; line 6 engine version still stale (LOW, non-consumer-facing)",
    "score_regression": "PASS — 19/19 no changes",
    "arithmetic_regression": "PASS — 14/14 no changes",
    "naturalness_gate": "PASS — F1=4, F2=4 overall; patched Altman Citrate 120 copy F1=4-5, F2=4-5"
  }
}
```
