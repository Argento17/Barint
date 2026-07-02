# Sugar Alcohols / Polyols — Blog Nutrition Spec
**Document:** `sugar_alcohols_blog_nutrition_spec_v1.md`
**Task:** TASK-379
**Role:** D13 Nutrition-accuracy gate — locks what Content Agent may say and what data Frontend renders
**Date:** 2026-06-22
**Corpus source:** `bari-web/src/data/comparisons/protein_combined_frontend_v2.json` (SHA256: 28358739146e4ff660f544817cb42283f9be209c54ecf2e2b18439356e0595bd, generated 2026-06-21)
**Evidence pack:** `02_products/snack_bars/sugar_alcohols_blog_evidence_v1.md` (Research Agent, TASK-379)

---

## Section 1 — Publish-Safe Claim Set

Each claim below is approved for publication. Every claim names its source. Content Agent must not reword the substance — only the Hebrew phrasing.

### APPROVED CLAIMS

**Claim 1.** EU nutrition labeling law (Regulation 1169/2011, Annex XIV) assigns polyols a uniform value of 2.4 kcal/g — approximately 60% of the energy assigned to sugar (4 kcal/g). Swapping sucrose for maltitol therefore simultaneously lowers both "calories" and "sugars" in a nutrition table without reducing total sweetening mass.
- Evidence tier: STRONG
- Source: Regulation (EU) No 1169/2011, Annex XIV (EUR-Lex primary text)
- Framing note: This is an architectural mechanism, not a health claim. Phrase it as: what the label convention allows, not what it "does to the body."

**Claim 2.** Israeli nutrition panels, which follow EU convention, list polyols (כוהלי סוכר) as a sub-line under carbohydrates. A bar can therefore display a low "sugars" figure while carrying a large polyol mass that is not labeled separately with the total weight.
- Evidence tier: MODERATE
- Source: USDA GAIN Reports (Israel, 2018/2019) via secondary regulatory guidance; aligned with EU Reg. 1169/2011. Primary Hebrew MoH text not accessed (see Section 5 on Israeli framing boundary).

**Claim 3.** EU law (Regulation 1169/2011, Annex III) requires that any food product containing more than 10% added polyols by weight must carry the mandatory statement: "excessive consumption may produce laxative effects."
- Evidence tier: STRONG
- Source: Regulation (EU) No 1169/2011, Annex III; European Commission Health Knowledge Gateway (secondary confirmation of exact wording)
- Framing note: This is an architectural transparency claim. State it as: regulators judged the physiological reality significant enough to require an on-pack warning. Do NOT frame as "polyols are dangerous."

**Claim 4.** Maltitol raises blood glucose. It is not glycemically neutral. Its glycemic index (GI) is approximately 35 for crystalline maltitol versus approximately 65 for sucrose. The glycemic impact is lower, but not zero.
- Evidence tier: MODERATE
- Source: Felber JP et al., JPEN 1987 (RCT, n=8); EFSA NDA Panel 2011 Scientific Opinion on sugar replacers and postprandial glycaemia (regulatory endorsement of the lower-glycemic claim)
- Framing note: The EFSA 2011 opinion substantiated the claim "sugar replacers including maltitol produce lower blood glucose rise vs. sugar." That is the defensible architectural claim. Do NOT extend to medical advice for any population.
- Confirmed limit: Maltitol syrup GI (~52) is separately noted in the evidence pack (MODERATE confidence) — if Content Agent uses it, it should flag "syrup form" specifically. This spec conservatively anchors on the crystalline form (~35) as the primary stated value.

**Claim 5.** Polyol GI effects (bloating, flatulence, laxative effects) are dose-dependent and are not visible from the nutrition panel.
- Evidence tier: STRONG for existence and dose-dependence; MODERATE for specific maltitol thresholds
- Source: Lenhart A, Chey WD, Advances in Nutrition 2017 (systematic review, 79 studies). The review establishes ~10 g/day sorbitol as the threshold for mild GI symptoms; for maltitol, the mechanism class is confirmed but per-serving dose data is less precise. Ruskone-Fourmestraux et al. 2003 (RCT, n=12) established a diarrhea threshold at ~92 g/day for healthy adults under dose-escalation conditions — this figure is NOT safe to cite in consumer copy as a typical-use reference; see DROP list below.
- Framing note: Use the Lenhart 2017 systematic review as the citation anchor. The claim "some individuals — particularly those with IBS — may experience GI sensitivity at lower doses" is permitted with a hedge and that citation. Do NOT advise any population on what to consume or avoid.

**Claim 6.** 24 out of 32 protein bars (75%) in the Bari Israeli protein-bar corpus contain maltitol. This is confirmed directly from the scored engine output.
- Evidence tier: STRONG — direct corpus extract, verified against scored JSON
- Source: `protein_combined_frontend_v2.json`, `_scoring_trace.key_signals.maltitol`, all 32 products enumerated
- Note: Product count for the live page is 32 (the meta states `product_count: 32`; the `fix_note` references a prior 33-product corpus before removing 2 WIN barcodes with truncated ingredient lists).

**Claim 7.** Erythritol has a near-zero glycemic index (GI approximately 1) and is the best-tolerated common polyol: approximately 90% is absorbed in the small intestine and excreted unchanged in urine, producing minimal osmotic or fermentation load in the colon.
- Evidence tier: STRONG
- Source: EFSA NDA Panel 2023 re-evaluation of erythritol (E968), EFSA Journal 21(12):e8430; Lenhart & Chey 2017 comparative tolerance data

**Claim 8.** The top-ranked bar in the Bari corpus (חטיף חלבון אגוזי לוז, פנגיאה, score 68.6/B, rank 1) achieves its sweetness from whole-food sources — dates, hazelnuts, almonds — with 17 g/100g sugar from those sources and no maltitol.
- Evidence tier: STRONG — direct corpus extract
- Source: `protein_combined_frontend_v2.json`, id: pb-002, `key_signals.maltitol: false`, `sugars_g: 17.0`, ingredients confirmed from scrape

---

### CLAIMS TO DROP OR SOFTEN

**DROP 1 — Ruskone-Fourmestraux 92 g/day diarrhea threshold as a consumer-facing reference.**
- Why: The 92 g/day figure comes from a dose-escalation study designed to find a threshold — participants were escalated until diarrhea occurred. It is not a "safe upper limit" for typical use. Publishing "92 g is the threshold" in consumer copy would imply misleading safety headroom. A typical maltitol-heavy protein bar can contain 15–30 g per bar (range estimate from ingredient positions in the corpus, not a verified per-SKU figure); the relevant risk window is the mild-symptom range (~10–20 g for sensitive individuals), not the 92 g diarrhea number.
- Safe reword: "At typical single-bar amounts, severe effects are unlikely in most healthy adults, according to the available evidence. Sensitive individuals may notice milder effects at lower amounts." Cite Lenhart & Chey 2017 (systematic review), not Ruskone-Fourmestraux. Do NOT publish the 92 g figure.

**DROP 2 — Maltitol syrup GI ~52 as an undifferentiated primary claim.**
- Why: Evidence pack flags this as MODERATE confidence. The distinction between crystalline and syrup forms is real but requires specificity (stating "syrup form") to be accurate. If Content Agent wants to use this, the safe wording is: "Maltitol in syrup form has a higher glycemic index (approximately 52 vs. 35 for the crystalline form)." Do not use ~52 as the headline GI without the syrup qualifier.
- Decision: Use only the crystalline form GI (~35) as the primary stated value unless Content Agent specifically addresses syrup forms.

**DROP 3 — IBS patients as a named population.**
- Why: Stating "people with IBS should be careful" crosses into medical advice (Hard Rule #5). Lenhart 2017 documents that IBS patients experience symptoms at lower doses — this is a published finding — but Bari cannot direct a health condition audience on consumption decisions.
- Safe reword: "Research suggests that some individuals may be more sensitive to the effects of polyols at lower amounts." No population naming, no dietary instruction.

**DROP 4 — Per-bar polyol gram estimates (e.g., "this bar contains 30 g maltitol").**
- Why: The Israeli nutrition panel does not list total polyol mass on most bars in the corpus. The comparisonContext copy references maltitol's presence qualitatively; it does not state an absolute gram figure. No field in `protein_combined_frontend_v2.json` carries a quantified maltitol gram value per SKU. Publishing a specific gram figure per bar requires a calculation the corpus does not support.
- Decision: Content Agent must not invent a specific polyol gram number per bar. The architectural claim ("the label shows total carbohydrates and a sugar sub-line; polyol mass is not disclosed as a standalone figure") is permitted. The Bari engine detects presence/absence from ingredients text, not from a disclosed polyol gram count — this distinction is architecturally important and the blog can explain it.

---

### Special Rulings

#### Erythritol 2023 Cardiac Signal (Hazen/Witkowski, Nature Medicine 2023)

**Ruling: OMIT from this article.**

Justification:
1. The evidence pack correctly labels this CONTESTED. EFSA's formal 2023 regulatory re-evaluation found no causal relationship between dietary erythritol intake and cardiovascular disease.
2. Independent experts raised substantial confounding concerns: cohort selection (cardiac risk assessment patients, not general population), endogenous erythritol production via the pentose phosphate pathway, and in-vitro doses that were supraphysiological (10× permitted beverage levels).
3. The article's thesis is substitution vs. reduction — not erythritol safety. Erythritol appears in the polyol family comparison table (Chart 1) as a reference point for the favorable end of the tolerance spectrum. That use requires stating erythritol's GI and tolerance profile (both STRONG evidence), not its cardiovascular association.
4. Including the cardiac signal — even with caveats — pulls the piece into health-risk territory that the architectural thesis does not need and that Bari's lane does not support.
5. A single caveat-laden paragraph about an unresolved cardiac signal would require more context than this article format can responsibly carry without becoming a health communication piece.

If in a future piece the question "is erythritol safe?" is the central topic, the Hazen finding can be included with the full EFSA/expert-caveat framing from the evidence pack. Not here.

#### Israeli Laxative-Warning Wording

**Ruling: Cite the principle from EU law; do NOT quote a specific Hebrew warning text.**

What is verified and safe to publish:
- "Israeli labeling regulations, which follow EU convention, require polyols to be listed under carbohydrates on the nutrition panel." (MODERATE — USDA GAIN 2018/2019)
- "Israeli regulations require a warning for products where polyols exceed 10% by weight — broadly equivalent to the EU mandatory statement." (MODERATE — secondary regulatory sources, confirmed as aligned with EU Annex III requirement)

What is not verified and must not be published:
- The exact Hebrew text of the Israeli warning. The evidence pack explicitly states the primary Hebrew MoH legislative text was not accessed. Secondary sources reference slightly different wording ("intestine dysmotility" vs. "laxative effects") without primary-source confirmation.
- Which Hebrew term (כוהלי סוכר vs. רב-כהלים) is the current official term in Israeli labeling law.

Safe framing boundary for Content Agent: Reference the EU regulation by name for the warning requirement; state Israel follows EU convention for the structural labeling rule. If the specific Hebrew warning text is needed on-pack as a visual element (e.g., in a callout graphic), the Adversarial QA gate must confirm it against a physically purchased Israeli product before publication — this is not an evidence-pack task, it is a verification task.

---

## Section 2 — Chart 1 Data: Polyol Family Comparison

These are the final values for Frontend to render. Every cell is publishable as stated. Source is cited per row. These values are locked; Content Agent does not alter them.

| Polyol | E-number | kcal/g (EU label value) | Note on physiological value | Approx. GI (glucose=100) | Digestive tolerance summary |
|--------|----------|------------------------|----------------------------|--------------------------|----------------------------|
| **Maltitol** | E965 | 2.4 | EU label value. Partially absorbed + partially fermented; 2.4 kcal/g is a reasonable approximation of metabolisable energy (unlike erythritol). | ~35 (crystalline form); ~52 (syrup form) | Moderate. Dose-dependent GI symptoms in sensitive individuals at ~10–20 g/day; diarrhea threshold ~92 g/day in healthy adults (not a consumer-facing reference — see Section 1 DROP list). |
| **Sorbitol** | E420 | 2.4 | Same EU label convention. | ~9 | Low tolerance. ~10 g/day: mild symptoms (flatulence/bloating) in healthy adults; ~20 g/day: diarrhea in many adults. Most studied polyol for dose thresholds. |
| **Xylitol** | E967 | 2.4 | Same EU label convention. | ~7–13 | Moderate. Mechanism similar to sorbitol (incomplete small-intestine absorption); dose-dependent bloating. |
| **Erythritol** | E968 | 2.4 (EU label) | Physiological value ~0.2 kcal/g (US FDA convention; rounds to 0 on American labels). The EU label assigns 2.4 kcal/g to all polyols uniformly regardless of metabolisable energy. | ~1 | High tolerance. ~90% absorbed in small intestine and excreted in urine unchanged; minimal osmotic or fermentation load; EFSA applied an exemption from the laxative warning (EFSA 2023). |

**Sources per row (for editorial footnote / source disclosure):**
- kcal/g (all rows): Regulation (EU) No 1169/2011, Annex XIV. EUR-Lex. https://eur-lex.europa.eu/eli/reg/2011/1169/oj/eng
- Erythritol physiological kcal/g: EFSA NDA Panel. EFSA Journal 2023;21(12):e8430. DOI: 10.2903/j.efsa.2023.8430
- Maltitol GI: Felber JP et al. JPEN 1987;11(3):250-254. DOI: 10.1177/0148607187011003250
- Maltitol tolerance: Ruskone-Fourmestraux A et al. Eur J Clin Nutr 2003;57(4):592-595. DOI: 10.1038/sj.ejcn.1601516
- Sorbitol thresholds; comparative tolerance: Lenhart A, Chey WD. Advances in Nutrition 2017;8(4):587-596. DOI: 10.3945/an.117.015560
- Xylitol GI and GI profile: Makinen KK. Int J Dentistry 2016;Article 5967907. DOI: 10.1155/2016/5967907
- Erythritol tolerance and laxative exemption: EFSA NDA Panel 2023 (above)

**Frontend rendering notes:**
- The EU label kcal/g (2.4 for all) is what appears on Israeli nutrition panels. Render this as the primary value.
- For erythritol only, a footnote cell may note "~0.2 kcal/g physiological (FDA)" to explain the discrepancy between label convention and metabolisable energy — this is the architectural transparency point.
- GI values are approximate; display with "~" prefix.
- Do not render the 92 g/day diarrhea threshold figure anywhere in consumer-facing output.

**Unconfirmed cell note:** Xylitol GI range (7–13) is from Makinen 2016 (review; not a single direct RCT). Range is widely cited in regulatory and academic literature. Evidence tier: MODERATE. Mark with standard confidence indicator if the UI carries one.

---

## Section 3 — Chart 2 Data: Substitution vs. Reduction

Six bars selected from the corpus to illustrate the architectural point. All values are pulled directly from `protein_combined_frontend_v2.json`. No values are invented or interpolated.

### Group A — Maltitol-Based (Substitution Architecture)

**Bar A1: WIN חטיף חלבון קרם קרמל**
- Corpus id: pb-013  <!-- corrected 2026-06-22 (TASK-379 QA M-1): was pb-011, which is a different product; pb-013 is the WIN bar (rank 11, 54/C, 1.7g sugar) -->
- Rank: 11 / 32
- Score: 54 / Grade: C
- Sugars (per 100g): 1.7 g
- Maltitol present: YES (`key_signals.maltitol: true`, `polyol_tier: 1`)
- Engine cap fired: `PROTEIN_BAR_MALTITOL_TIER1` (cap 62)
- Note: Ingredients also list sorbitol and erythritol in addition to maltitol. The bar's displayed sugar (1.7 g) is the lowest in the entire corpus. The insightLine from the corpus: "סוכר 1.7 גרם — הנמוך במדף, אבל זה כמעט כולו הממתיק מלטיטול שהחליף סוכר."

**Bar A2: אול אין סופט פיסטוק**
- Corpus id: pb-007
- Rank: 6 / 32
- Score: 55 / Grade: C
- Sugars (per 100g): 4.6 g
- Maltitol present: YES (`key_signals.maltitol: true`, `polyol_tier: 1`)
- Engine cap fired: `PROTEIN_BAR_MALTITOL_TIER1` (cap 62); also `SWEETENER_CAP_C_PROTEIN_BAR` (cap 70); effective cap via `BASE_ENGINE_BINDING_CAP_INHERIT` = 55
- Note: This bar also contains sucralose (E955). The insightLine from the corpus: "סוכר 4.6 גרם נראה מצוין — עד שמגלים שהוא הוחלף במלטיטול ובממתיק מלאכותי."

**Bar A3: פרו שטראוס חטיף חלבון קרמל ואגוזים**
- Corpus id: pb-010
- Rank: 8 / 32
- Score: 54 / Grade: C
- Sugars (per 100g): 3.7 g
- Maltitol present: YES (`key_signals.maltitol: true`, `polyol_tier: 1`)
- Engine caps fired: `PROTEIN_BAR_MALTITOL_TIER1` (cap 62); `SWEETENER_CAP_C_PROTEIN_BAR` (cap 70); `BASE_ENGINE_BINDING_CAP_INHERIT` (effective cap 55)

### Group B — No Maltitol (Real Ingredients or Real Sugar)

**Bar B1: חטיף חלבון אגוזי לוז (פנגיאה)**
- Corpus id: pb-002
- Rank: 1 / 32 — top of shelf
- Score: 68.6 / Grade: B
- Sugars (per 100g): 17.0 g (from whole-food sources: dates, hazelnuts, almonds — confirmed from ingredients field)
- Maltitol present: NO (`key_signals.maltitol: false`, `polyol_tier: null`)
- Engine cap fired: none for maltitol. One base-engine cap exists (`BASE_ENGINE_BINDING_CAP_INHERIT` cap 94.8, never binding). Penalty: `PROTEIN_BAR_GLYCEROL` (-8) for glycerol humectant.
- Note: Despite 17 g/100g displayed sugar — the highest among the non-maltitol group and mid-shelf overall — this bar ranks #1. The insightLine: "חלבון מאגוזי לוז אמיתיים — אבל תוסף ההלחה גליצרול ברשימה מסגיר חטיף מהונדס במפעל."

**Bar B2: טודיי חטיף חלבון בננה שוקולד**
- Corpus id: pb-003
- Rank: 2 / 32
- Score: 61.9 / Grade: C
- Sugars (per 100g): 12.0 g
- Maltitol present: NO (`key_signals.maltitol: false`, `polyol_tier: null`)
- Engine caps fired: none for maltitol. `BASE_ENGINE_BINDING_CAP_INHERIT` at 87.2 (not binding).

**Bar B3: מקס ברנר חטיף חלבון קרמל מלוח**
- Corpus id: pb-033
- Rank: 32 / 32 — last on shelf
- Score: 45 / Grade: D
- Sugars (per 100g): 35.0 g
- Maltitol present: NO (`key_signals.maltitol: false`, `polyol_tier: null`)
- Engine cap fired: `BASE_ENGINE_BINDING_CAP_INHERIT` (cap 45 — binding; engine score 53.6 clipped to 45)
- Note: This bar is the counter-example in Group B — no maltitol, but 35 g real sugar. It scores D not because of substitution but because of high actual sugar. Useful contrast: you can score badly on both ends of the spectrum. The insightLine: "גם הסוכר הכי גבוה במדף וגם הנתרן הכי גבוה — 35 גרם סוכר ו-396 מ\"ג נתרן ל-100 גרם."

### Summary Table for Chart 2

| Bar (display name) | Displayed sugar g/100g | Maltitol? | Score | Grade | Engine cap rule fired |
|--------------------|----------------------|-----------|-------|-------|----------------------|
| WIN קרם קרמל | 1.7 | Yes | 54 | C | PROTEIN_BAR_MALTITOL_TIER1 |
| אול אין סופט פיסטוק | 4.6 | Yes | 55 | C | PROTEIN_BAR_MALTITOL_TIER1 |
| פרו שטראוס קרמל ואגוזים | 3.7 | Yes | 54 | C | PROTEIN_BAR_MALTITOL_TIER1 |
| פנגיאה אגוזי לוז | 17.0 | No | 68.6 | B | None (maltitol) |
| טודיי בננה שוקולד | 12.0 | No | 61.9 | C | None (maltitol) |
| מקס ברנר קרמל מלוח | 35.0 | No | 45 | D | None (maltitol) — real sugar penalty |

**Confirmed from corpus. No values invented.**

**Values confirmed directly from JSON fields:** `nutrition_per_100g.sugars_g`, `_scoring_trace.key_signals.maltitol`, `_scoring_trace.key_signals.polyol_tier`, `_scoring_trace.caps_applied[].rule`, `score`, `grade`.

**Unconfirmed / flagged:**
- Absolute maltitol gram content per bar is NOT available in the corpus (the engine detects presence from ingredient text, not from a disclosed polyol gram figure). Content Agent must not publish a per-bar gram claim.
- WIN bar (pb-013) also contains sorbitol and erythritol in addition to maltitol (confirmed from ingredients text). The headline maltitol signal fires correctly; the multi-polyol nature is a nuance Content Agent may reference if writing a deeper callout on this bar.

---

## Section 4 — Firewall and Framing Guardrails for Content Agent

### Phrasings that cross into health-claim territory (BANNED in consumer copy)

| Banned phrasing | Why banned |
|----------------|------------|
| "מלטיטול מעלה את רמת הסוכר בדם" (maltitol raises your blood sugar) — stated as a personal health consequence | This is medical advice directed at the reader. |
| "אנשים עם סוכרת צריכים להיזהר ממלטיטול" | Named medical population + dietary instruction = medical advice. Hard Rule #5. |
| "כוהלי סוכר גורמים לנזק למעיים" (sugar alcohols cause intestinal damage) | Not supported by the evidence; overstates harm. |
| "ארתיריטול קשור למחלות לב" without extensive caveat | The Hazen finding is contested; EFSA found no causal link. Full omission is the ruling (Section 1). |
| "ציון X מבטיח בריאות" / "ציון B הוא מזון בריא" | Bari scores nutritional architecture, not health outcomes. Scores never imply health claims. |
| "הבחירה הבריאה יותר" (the healthier choice) | Bari does not rank foods by health; it describes structure and labels. |
| "מאכלת פחות קלוריות" / "מורידה סוכר" as a directive | Purchase/consumption instruction = health claim territory. |
| The 92 g/day diarrhea threshold figure stated as a safety limit | Misrepresents the dose-escalation study design; see DROP 1 above. |

### Architectural equivalents that are ALLOWED

| Allowed phrasing (architectural) | Evidence basis |
|----------------------------------|----------------|
| "הסוכר הנמוך על האריזה מגיע מהחלפה, לא מהפחתה" | Direct corpus finding — structural observation |
| "מלטיטול הוא כוהל סוכר שנרשם כחלק מהפחמימות, לא בנפרד" | Regulatory architecture — EU Reg. 1169/2011 Annex XIV |
| "הכוהל הזה מעלה סוכר בדם פחות מסוכר רגיל, אבל לא אפס" | MODERATE evidence (Felber 1987; EFSA 2011 opinion) — state the source |
| "ה-GI של מלטיטול קריסטלי הוא בערך 35, לעומת כ-65 לסוכרוז" | MODERATE evidence — state "approximately" and cite |
| "לפי התקנות האירופיות, מוצר עם יותר מ-10% כוהלי סוכר חייב להצהיר על כך על האריזה" | STRONG — EU Reg. 1169/2011 Annex III |
| "ארתיריטול הוא כוהל הסוכר הסביל ביותר: כ-90% ממנו נספג ומופרש ללא עיכול" | STRONG — EFSA 2023; Lenhart 2017 |
| "ברי מזהה כוהל סוכר ברשימת הרכיבים ומשקף זאת בציון" | Direct engine description — architectural |
| "75% מחטיפי החלבון בניתוח של ברי מכילים מלטיטול" | STRONG — direct corpus count |

### Framework vocabulary firewall (no consumer copy may include these terms)

The following technical/internal terms must not appear in any consumer-facing string, regardless of context:

- NOVA, NOVA-4, NOVA class
- BSIP, BSIP0, BSIP1, BSIP2
- cap, floor, binding cap, engine cap, base engine binding cap
- polyol_tier, polyol tier 1/2
- structural_class, lens, protein_bar_lens
- "scoring engine," "pipeline," "trace"

Permitted consumer-facing terms for the same concepts:
- "כוהל סוכר" or "כוהלי סוכר" (sugar alcohol/s) — fine as descriptive consumer terms
- "מלטיטול" — fine; it is a Hebrew-adopted ingredient name
- "ממתיק" (sweetener) — fine
- "תחליף סוכר" (sugar substitute) — fine
- "הציון" / "דירוג" (score/ranking) — fine; this is what we show on the page

---

## Return Contract

```json
{
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\snack_bars\\sugar_alcohols_blog_nutrition_spec_v1.md",
      "sha256": "TO_BE_VERIFIED_ON_READ",
      "description": "D13 nutrition-accuracy gate spec: publish-safe claims, chart data, framing guardrails for TASK-379 blog explainer"
    },
    {
      "path": "bari-web/src/data/comparisons/protein_combined_frontend_v2.json",
      "sha256": "28358739146e4ff660f544817cb42283f9be209c54ecf2e2b18439356e0595bd",
      "description": "Source corpus — all Chart 2 product values pulled from this file directly"
    }
  ],
  "counts": {
    "claims_safe_to_publish": 8,
    "claims_safe_to_publish_denominator": "numbered claims 1-8 in Section 1 APPROVED CLAIMS",
    "claims_dropped_or_softened": 4,
    "claims_dropped_or_softened_denominator": "DROP 1-4 in Section 1",
    "chart1_rows": 4,
    "chart1_rows_denominator": "maltitol, sorbitol, xylitol, erythritol",
    "chart2_products": 6,
    "chart2_products_denominator": "3 maltitol-based (A1-A3) + 3 no-maltitol (B1-B3) from corpus",
    "values_unconfirmed": 2,
    "values_unconfirmed_denominator": "xylitol GI range (MODERATE, review-derived not single RCT); per-bar maltitol gram content (not available in corpus for any SKU)"
  },
  "commands_run": [
    {"cmd": "Read: sugar_alcohols_blog_evidence_v1.md", "exit": 0},
    {"cmd": "Read: protein_combined_frontend_v2.json lines 1-1096", "exit": 0},
    {"cmd": "Grep: name/score/grade/rank/sugars_g/maltitol/polyol_tier across full JSON", "exit": 0},
    {"cmd": "Read: JSON lines 2950-3464 (ranks 19-22, pb-019 to pb-022)", "exit": 0},
    {"cmd": "Read: JSON lines 4820-5270 (ranks 28-32, pb-029 to pb-033, D-grade bars)", "exit": 0},
    {"cmd": "Read: JSON lines 1574-1730 (WIN bar rank 11-12 detail)", "exit": 0}
  ],
  "not_done": [
    "Exact Hebrew text of Israeli mandatory laxative warning — primary MoH legislative text not accessed in evidence pack or this session; Content Agent must cite EU law for the warning requirement and not quote a specific Hebrew text without primary-source verification",
    "Per-bar maltitol gram quantification — the corpus does not carry a declared polyol mass per SKU; any per-bar gram figure would require either (a) primary label measurement or (b) a corpus engineer deriving it from ingredient order/position heuristics, neither of which is available here",
    "Erythritol cardiac signal ruling (Hazen 2023) — ruled OMIT for this article; if a future standalone piece on erythritol safety is commissioned, this evidence pack section can be activated with full caveat framing"
  ],
  "spec_conflicts": "None detected. The thesis (substitution vs. reduction) stays on the architectural side of Hard Rule #5 throughout. No claim in this spec advises on diet or health outcomes.",
  "acceptance_test": {
    "criterion": "Every figure in Charts 1 and 2 traces to a named source. Every corpus value traces to a specific JSON field. All four special-ruling decisions are unambiguous. The firewall section gives Content Agent a clear allowed/banned taxonomy. The Israeli label section states exactly what is and is not verified.",
    "result": "PASS — each chart cell cites a source; each corpus value references the specific JSON id and field; erythritol cardiac ruling is explicit (OMIT); Israeli warning ruling is explicit (cite EU, do not quote Hebrew text); framework vocab firewall is enumerated"
  }
}
```
