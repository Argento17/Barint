# Magnesium Page — Scientific Assumptions Review
**Author:** Nutrition Agent · **Date:** 2026-06-20 · **Status:** Internal challenge document — candidate prototype only. No published score movement.

This document challenges every scientific assumption behind the magnesium benchmark and consumer page, in plain English. One section per assumption: what it claims, a verdict (SOLID / SHAKY / WRONG), the evidence, and what (if anything) to change.

---

## Assumption 1 — Elemental-load basis
**Plain English:** We score the amount of magnesium printed on the label — not the amount the body actually absorbs. A product that says "300 mg magnesium" gets scored on 300 mg, regardless of whether it's oxide (absorbed at ~4%) or citrate (absorbed at ~30%).

**Verdict: SOLID — with one honest gap the page only partially covers.**

**Why solid:** This is the only coherent choice for a label-based engine. You cannot measure absorption from a label; absorption depends on a person's baseline magnesium status, gut health, food co-ingestion, dose splitting, and time-of-day. No label declares absorbed dose. Scoring elemental-declared dose is what every serious regulatory body (NIH ODS, EFSA) also does — their RDA/AI figures represent intake targets, not absorption targets, because population-level bioavailability is already baked into the requirement calculation.

**The honest gap:** The caveat on the page — "אנחנו מודדים את המגנזיום שעל התווית, לא את מה שנספג בפועל" — is present but buried at the bottom of the category note. The consumer's natural reading of a high elemental dose score is "I will absorb more magnesium." For oxide products especially (MagUp, the three 520 mg oxide products), this creates a genuine risk: a consumer sees "271 mg elemental, score B" and thinks they are getting 271 mg absorbed. The actual absorbed amount from oxide is roughly 10–12 mg at that label dose — about the same as a glass of milk.

**What to change:** The caveat should be promoted into the insight line for every oxide product, not just a footnote on the page. The current MagUp insight line reads: "תמורה גבוהה. הסתייגות אחת — ספיגת אוקסיד נמוכה." That is honest but softens the discrepancy. Consider: "271 מ\"ג מגנזיום יסודי על האריזה — אך אוקסיד נספג בכ-4%, כלומר בפועל כ-10–12 מ\"ג נספגים." That is true, proportionate, and would prevent misread. This is a copy change, not a scoring change.

---

## Assumption 2 — Citrate-first form ranking
**Plain English:** We say citrate is the best-absorbed form with the strongest evidence, and that glycinate/bisglycinate is "tolerability-forward, not the proven absorption winner." Effectively we treat them as tied in score (both rank FORM_PREFERRED = 92) but the benchmark text puts citrate first.

**Verdict: SHAKY — the citrate-vs-glycinate comparison is the weakest link in the form ladder.**

**Why shaky:** The bioavailability evidence for organic salts over oxide is solid (PMID:7815675 showed oxide ~4% vs organic salts ~30%). But the *direct comparative* evidence between citrate and glycinate specifically is thin and inconsistent.

The foundational citation in SUPP-EV-002 (PMID:7815675, Walker 1994) is a 30-year-old crossover study with modest n. It compared citrate and oxide, not citrate and glycinate head-to-head. More recent work (e.g., PMID:30761462, Schuette 2019 lineage) supports bisglycinate having equivalent or superior fractional absorption to citrate in some populations, particularly older adults and those with reduced gastric acid. Glycinate's amino acid chelate structure allows absorption via a peptide transporter pathway (PepT1) that is independent of gastric acid — which means in the large segment of the Israeli population using proton pump inhibitors, glycinate may genuinely outperform citrate.

The benchmark correctly acknowledges "direct human comparative bioavailability evidence is strongest for citrate" — but that claim requires the caveat that most direct citrate-vs-glycinate comparisons have been small (n < 30), short duration, and used different doses, making the head-to-head verdict genuinely uncertain at Moderate confidence, not settled.

The current page presents this as resolved fact. Products with bisglycinate (Altman Bisglycinate, Nutrikar WELL) receive FORM_PREFERRED = 92, same as citrate — so the score itself is defensible. But the copy calling glycinate "tolerability-forward" rather than an "absorbed differently, not necessarily worse" form is slightly unfair to glycinate and slightly overconfident about citrate's primacy.

**What to change:** Relabel the consumer-facing description. "ביסגליצינט — צורה בעלת ספיגה טובה" (the page already says this) is fine. The benchmark note calling glycinate "NOT the proven bioavailability winner" should be softened to "comparative head-to-head human evidence is limited; both citrate and glycinate outperform oxide, relative ranking between them uncertain." The score is unaffected (both = 92 preferred), but the methodology text should not overstate resolution where the science has not delivered it. Confidence on the form ladder = medium, consistent with SUPP-EV-002's own `form_ladder_confidence: "medium-high"` — the "-high" part specifically applies to oxide being poor, not to the citrate-vs-glycinate sub-rank.

---

## Assumption 3 — The effective-dose thresholds (100 mg generic / 200 mg sleep / 400 mg migraine)
**Plain English:** We use three threshold values to judge whether a product delivers "enough" magnesium for its stated purpose. Below 50% of these thresholds = fairy dust (D/49 ceiling). These numbers are the spine of the whole scoring model.

**Verdict: SOLID for migraine (400 mg) and the general threshold direction (100 mg). SHAKY for the sleep threshold (200 mg) — the evidence base for that specific number is weak.**

**Why solid for 400 mg migraine:** The American Headache Society guideline and the 2015 review (Peikert et al., updated) both specifically studied ~400–600 mg magnesium citrate/day for migraine prophylaxis in RCTs. A dose threshold of 400 mg has a real study anchor.

**Why the 100 mg general threshold is defensible:** The US dietary magnesium intake averages roughly 234–268 mg/day from food. The RDA sits at 310–420 mg for adults. A ~50–150 mg supplemental gap is a real and conservative gap estimate. 100 mg as the lower bound of a "gap-closing" dose is reasonable. The benchmark does this right: it calls 100 mg a "gap-closing" dose, not a "therapeutic" dose.

**Why 200 mg for sleep is shaky:** The sleep threshold is the most arbitrary of the three. The benchmark states "200–400 mg/day (no firm target)" and correctly notes there is "no firm target." That is the problem. The systematic reviews (PMID:33865376, PMID:35184264) use heterogeneous doses ranging from 250 to 500 mg elemental/day, primarily in elderly adults. There is no published study that specifically establishes 200 mg as the minimum effective dose for sleep endpoints. The 200 mg figure appears to be a reasonable middle-ground inference, not a study-derived threshold. Using it to judge whether a sleep-claiming product "passes" or "fails" the dose check overstates our precision. A product at 180 mg would score sub-therapeutic on sleep when the evidence does not actually support that 180 mg is meaningfully different from 200 mg for sleep.

**What to change:** For sleep products, the dose threshold should be presented as a range rather than a hard line, and the page should acknowledge the threshold is inference from general supplemental research, not sleep-specific dosing evidence. In practice: a sleep-claiming product at 150–250 mg should not auto-fail the dose check on a hard line of 200 mg. The calibration threshold is defensible as a candidate starting point but should not be presented as settled science. No score change needed now — but the copy on sleep products should not say "עומד ברף הדרוש" (meets the required threshold) as if the 200 mg figure is established; it should say "בטווח המינון שנחקר."

---

## Assumption 4 — "Best value = oxide"
**Plain English:** We say that oxide products (MagUp, three 520 mg products) deliver the best value-per-shekel because they have the most elemental milligrams per shekel. The page explicitly calls them best value on the Israeli shelf.

**Verdict: SHAKY — honest but potentially misleading in its framing, and the page's absorption caveat does not fully neutralize the risk.**

**Why partially true:** The math is correct. Oxide has the highest elemental fraction per compound gram (60.3%), and oxide products are the cheapest on the shelf. If you score elemental mg declared on the label per shekel, oxide wins. The benchmark is transparent about this.

**Why shaky:** "Best value" in common consumer usage means "best outcome per shekel." Absorbed magnesium per shekel is the outcome that matters — not declared elemental per shekel. Oxide at ~4% fractional absorption means that 314 mg declared elemental delivers roughly 12–13 mg absorbed. Citrate at ~30% fractional absorption on a 32 mg elemental product (Altman Citrate, currently scoring D/49 for low dose) delivers roughly 10 mg absorbed. The oxide's actual delivery advantage almost disappears when you correct for absorption.

The category note and row verdicts do mention oxide's low absorption, but never calculate the consequence. The MagUp row verdict says "הגוף מנצל רק חלק מהכמות שעל האריזה" (the body uses only a fraction of the label amount). A consumer will not translate "a fraction" into "roughly 4%." The page never says "כ-4% ספיגה בפועל" (approximately 4% actual absorption). That is the number that would truly inform the decision.

**A specific risk:** A consumer reads the page, sees oxide = best value, buys MagUp for ₪25 instead of Altman Citrate for ₪35, and experiences the same or worse actual magnesium effect because absorbed dose is similar or lower. From a consumer-outcome standpoint this may not actually be best value.

**What to change:** Two changes. First, add the actual absorption percentage to the limiting factors section for every oxide product: "אוקסיד נספג בכ-4% — מתוך 271 מ\"ג על האריזה, כ-10–12 מ\"ג נספגים בפועל." Second, soften "best value" to "best value by label dose-per-shekel" and add a parenthetical: "אם מסתמכים על התווית בלבד." The claim is honest and correct in the engine's own terms — but the consumer framing needs tighter language so it does not imply absorbed-value equivalence.

---

## Assumption 5 — Claim-to-evidence tier assignments
**Plain English:** We assign each health claim a tier: Strong / Moderate / Weak / Insufficient. These tiers affect whether a product can score above 34 (E-ceiling for Insufficient evidence). The current assignments are: immune/energy/fatigue = EFSA-authorized = Moderate; blood pressure = Moderate; sleep = Weak; muscle cramps = Insufficient.

**Verdict: SOLID on blood pressure (Moderate) and muscle cramps (Insufficient). QUESTIONABLE on routing fatigue/energy through blood pressure (Moderate). Correct to hold sleep at Weak rather than Insufficient, but borderline.**

**Blood pressure at Moderate:** Confirmed solid. Multiple meta-analyses (PMID:27402922, 34 RCTs; PMID:41000008) show a consistent, modest BP effect, primarily in hypertensive or low-magnesium subgroups. The effect size is real but small (~2 mmHg SBP). Moderate is the right call: consistent RCT evidence, meaningful limitations (subgroup-dependent, effect size modest). Not Strong because population generalizability is limited and the effect disappears in normotensive well-nourished adults.

**Muscle cramps at Insufficient:** Correct. The Cochrane review (CD009402) specifically concluded that magnesium supplementation is unlikely to provide clinically meaningful relief from idiopathic muscle cramps. This is a genuine Insufficient — there is good-quality research, and it found no effect. The page should never positively signal "cramp relief" for any magnesium product.

**Sleep at Weak, not Insufficient:** This is a genuine borderline call and the dossier acknowledges it ("borderline Weak/Insufficient"). I hold Weak because there is a directional signal in low-certainty systematic reviews — not zero evidence, just thin evidence. Insufficient would mean "no credible human evidence at all," which overstates the null. Weak is defensible, but barely. Re-adjudicate if no higher-certainty SR appears by the 2027 review date.

**Fatigue/energy routed through blood pressure (Moderate): QUESTIONABLE.** The EFSA Article 13 authorization for "magnesium contributes to a reduction of tiredness and fatigue" is real and correctly cited. But routing it to Moderate via the blood pressure endpoint is a stretch. EFSA Article 13 authorizations are not evidence tiers — they are regulatory permissions based on a general recognized relationship. The tiredness/fatigue claim specifically is authorized on the basis of magnesium's role in energy metabolism (ATP synthesis, cofactor in >300 enzymatic reactions), not on blood pressure trials. Routing "fatigue" to the BP meta-analysis citations conflates two mechanistically distinct pathways. The BP evidence does not directly support the fatigue claim. The correct tier for a general fatigue/energy-metabolism claim in replete adults is Weak at best, because human interventional evidence for fatigue endpoints in non-deficient adults is limited. If the intent was to rescue a product from E solely because it carries an EFSA-authorized claim, that is a legitimate structural choice — but it should be explicit rather than disguised as a BP tier routing.

**What to change:** Add a separate claims entry for "fatigue/energy-metabolism" citing the EFSA Article 13 authorization and the cofactor mechanistic pathway, and tier it Weak. Do not route it to Moderate through the blood pressure citations. This means a magnesium product making only a fatigue claim resolves at Weak (score ceiling B, not blocked by E-ceiling). The score effect: a product currently scoring E solely on a fatigue claim would move to D/C range, which is still a meaningful penalty and better reflects evidence. This is a D6 rule proposal requiring D7 co-sign.

---

## Assumption 6 — UL handling (EU 250 vs US/AU 350 mg supplemental)
**Plain English:** Two regulatory bodies give different upper limits for how much supplemental magnesium per day is safe: the EU (EFSA) says 250 mg, the US/NIH says 350 mg. We resolved this by treating 350 mg as the hard veto line and 250 mg as a "soft warning zone."

**Verdict: SOLID in principle; still has an unverified data dependency.**

**Why solid:** The Nutrition D8 ruling that resolved FLAG-2 is scientifically defensible. Both the 250 mg (EFSA) and 350 mg (US IOM) figures are GI-tolerance thresholds, not systemic toxicity ceilings. The adverse event is reversible osmotic diarrhea — genuinely self-limiting and not a toxicological endpoint. Using the lower of two GI-tolerance thresholds as a hard veto would auto-fail any adequately-dosed magnesium product (since the minimum effective dose is 300 mg), which is an absurd scoring outcome. The graded reading — hard veto at 350 mg, soft safety note at 250–350 mg — is the appropriate resolution and is consistent with how the methodology handles reversible vs. toxicological harm.

**The remaining risk:** The safety citations in the dossier are still flagged NEEDS-ENV-VERIFY. The exact current NIH ODS and EFSA primary sheet values have not been re-confirmed by a live data pull. These values are externally maintained; if either regulatory body has revised their supplemental UL, the veto line could be wrong. This is not a design flaw — it is a maintenance gap. Semi-annual re-sync is specified.

**What to change:** Before any product using this engine goes live, the NEEDS-ENV-VERIFY flags on both UL values (NIH ODS 350 mg, EFSA 250 mg) must be resolved against the current primary documents. This is a data integrity gate, not a scoring philosophy change. The graded framework itself needs no change.

**Note on the page:** The current page does not mention the upper limit at all in consumer copy, which is correct — none of the 18 Israeli products scored on this page exceed 350 mg elemental per serving from the label (the highest are the oxide 520 mg compound products, which translate to roughly 314 mg elemental — just within the 350 mg veto). If any product in a future run exceeds 350 mg elemental, the safety note/veto must appear in the product's limiting factors section.

---

## Assumption 7 — The label-truthful-not-lab-verified assumption
**Plain English:** We score what the label says. A Polish assay of 116 EU magnesium supplements found 58.7% were outside legal tolerance for actual magnesium content — and the discrepancy was unrelated to price. We cannot check content without a lab. So our score is "best case, assuming the label is honest."

**Verdict: WRONG as a silent assumption; SOLID as an explicit acknowledged limitation — and the current disclosure is not strong enough.**

**Why this matters:** 58.7% outside legal tolerance is not a small study with a marginal result. If that distribution holds even approximately on the Israeli shelf, then more than half the products we score are being judged on a number that does not reflect what is in the capsule. The current disclosure ("אנחנו מסתמכים על התווית; איננו בודקים במעבדה את התכולה בפועל") states the limitation accurately but presents it in the same tone as a standard caveat. It is not a standard caveat. It is a fundamental limitation that applies to more than half the universe.

The page lists this in the category note alongside the price-comparison disclaimer. A consumer reading the category note will register both as roughly equal in importance. They are not. The label-truthfulness problem is categorically more serious.

**What changes:** Two things. First, the disclosure should be separated, weighted more heavily, and placed higher in the consumer-facing category note — ideally the first caveat, not the last. Suggested Hebrew: "מגבלה מהותית: בדיקת מעבדה אירופאית של 116 תוספי מגנזיום מצאה כי כ-58% לא עמדו בתכולה שעל האריזה — בלי קשר למחיר. אנחנו בוחנים מה שכתוב על האריזה, לא מה שנמדד במעבדה." Second, if and when Bari moves toward lab-verified data partnerships for any category, magnesium supplements should be the first priority — the label-truthfulness gap is uniquely severe here compared to food categories.

This is not a reason to scrap the score. A score built on declared labels is still informative — it tells you what the manufacturer claims, which is itself a meaningful signal (a manufacturer claiming 7 mg elemental is straightforwardly worse than one claiming 271 mg, even before you get to lab verification). But the limitation must be front-and-center, not a footnote.

---

## Assumption 8 — The caps (49 fairy-dust ceiling, 34 insufficient-evidence ceiling)
**Plain English:** Two hard ceilings shape the bottom of the scoring range. Products that deliver less than 50% of the minimum effective dose cannot score above 49 (D grade). Products making claims with insufficient scientific evidence cannot score above 34 (E grade). These cap values were described as "uncalibrated placeholders" in the calibration document.

**Verdict: SHAKY as calibrated numbers; SOLID as structural principles.**

**Why the principle is solid:** Having a hard ceiling for products that cannot deliver a meaningful dose is the right structural choice. A product that delivers 7 mg elemental magnesium (the taurate product) should not score the same as a product delivering 271 mg, even if the 7 mg product uses an elite form with perfect honesty. The fairy-dust ceiling prevents "nice packaging, useless product" from scoring well. Similarly, a ceiling for insufficient-evidence claims prevents wild marketing from inflating a score. Both principles are scientifically justified.

**Why the numbers are shaky:** The calibration document (phase2_calibration_v1.md) is explicit: "Cap 2 fairy-dust ceiling: 49 / §3.2 #2 'approximately D-band' (= D ceiling, 35–49)." The spec says "approximately D-band." The 49 specifically was not derived from a scientific rationale — it was chosen as the top of the D grade band, so that fairy-dust products can reach D-ceiling but no higher. That is internally consistent, but it means the cap value is entirely driven by the grade band boundaries (themselves also candidate), not by evidence about what dose threshold should define "fairy dust" vs "sub-therapeutic."

The fairy-dust fraction itself (0.5 of minimum effective dose) is also a placeholder. The dossier says "§2.2 candidate, verbatim." There is no evidence that 49% of minimum effective dose produces zero effect and 51% produces a meaningful effect. The actual dose-response relationship for magnesium is likely continuous and individual-dependent. A product at 90 mg (90% of the 100 mg general threshold) is meaningfully different from one at 10 mg, but the engine treats both as "sub-therapeutic" in the same band.

**What to change:** The structural principle — fairy dust gets hard-capped below D — should be retained. But the calibration document is honest that these are placeholders, and the public-facing page should not imply these thresholds carry the same evidential weight as, say, the migraine 400 mg threshold (which does have a study anchor). In practice: the 49 and 34 cap values are functionally reasonable for a prototype. They must be revisited before any published score. The review should ask: does sub-50% of minimum effective dose really merit a flat cap, or should the penalty be continuous (dose-response graded penalty)?

One specific concern: the fairy-dust ceiling (49) and the insufficient-evidence ceiling (34) are only one grade band apart. A product making an insufficient-evidence claim scores E regardless of its dose. A product with good evidence but a fairy-dust dose scores D. This means a useless dose of a real compound (e.g., 7 mg elemental oxide) scores better (D/49) than a well-dosed product making an unsupported claim (E/34) — which seems backwards. The taurate product (7 mg elemental, D/49) arguably delivers less value than TRIOMAG (32 mg elemental with a real three-form blend, E/34 due to the honesty claim problem). The relative ordering is debatable. This is a D6/D7 item for the next calibration round.

---

## Summary

**The assumption I am LEAST comfortable defending publicly:**

Assumption 7 — the label-truthfulness problem. If a media outlet or regulatory body challenges this page with the Polish assay data (58.7% outside legal tolerance), we have no defense except "we said it was label-based." That is technically accurate but deeply unsatisfying at scale. A scoring system that rates products on labels when more than half of labels are unreliable is building on a genuinely shaky foundation. The disclosure is not prominent enough to absorb that challenge. This is the one assumption that, if tested publicly, could undermine the credibility of the whole exercise — not because the methodology is wrong, but because the limitation is buried.

**The one thing I would change first:**

Promote the label-truthfulness caveat to the top of the category note, in clear Hebrew, with the 58.7% figure and the "unrelated to price" finding stated explicitly. This is a copy change only — no scoring change, no architecture change. It is the single change that most directly reduces the consumer-harm risk and most honestly represents what Bari can and cannot claim to know about these products.

---

```json
{
  "artifacts": [],
  "counts": {
    "assumptions_reviewed": 8,
    "verdicts_solid": 3,
    "verdicts_shaky": 4,
    "verdicts_wrong": 1,
    "d6_proposals": 1,
    "copy_changes_recommended": 4,
    "score_changes_recommended": 0
  },
  "commands_run": [],
  "not_done": [
    "NEEDS-ENV-VERIFY: NIH ODS 350 mg supplemental UL current value",
    "NEEDS-ENV-VERIFY: EFSA 250 mg supplemental UL current value",
    "D6 proposal for fatigue/energy tier (separate from BP routing) requires D7 co-sign before implementation",
    "Fairy-dust/insufficient-evidence cap ordering anomaly (taurate D > TRIOMAG E) flagged for next calibration round"
  ],
  "spec_conflicts": [],
  "acceptance_test": "N/A — research/analysis deliverable, not a scored build"
}
```
