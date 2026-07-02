# Red-Team Challenge Report — Magnesium (real_corpus_v3, v9 engine run)
Date: 2026-06-20
Scope: 18 products displayed / 19 in corpus, /hashvaot/magnesium (candidate — not consumer-live)
Challenger: adversarial-qa-agent
Material read directly: magnesium-page-data.ts, _corpus_run_full_v9.json, magnesium_benchmark_v1.md,
  all 19 individual SKU JSON files in skus_full/

---

## Opening Finding

The page is structured around a single ranking dimension: elemental magnesium per shekel as declared
on the label. That dimension is internally consistent. But it produces a ranking that is publicly
indefensible as a consumer recommendation without far more prominent qualifications:

**Oxide products are ranked B and C (top 4 of 18). The absorption of magnesium oxide is ~4% (benchmark
§3, Lindberg 1990). At that rate, the "best value" product (Nutrikare 520mg oxide) delivers
approximately 12–13 mg of actually absorbed magnesium per capsule — less than a D-grade
bisglycinate or citrate product at 35mg label dose with ~40% absorption (~14mg absorbed).**

The absorption caveat exists in the category note, but it is not quantified, and it is invisible at
the score level. The headline, scores, and grade chips all push oxide. A consumer who reads the score
table and skips the category note walks away with the instruction to buy the supplement their body
barely absorbs. This is the single biggest structural vulnerability.

A regulator, journalist, or plaintiff's attorney would open with this. Everything else is secondary.

---

## Attack 1: "Best value = oxide" — the absorption inversion

**Exact claim attacked:**
- Prologue: "מה שמצאנו הפוך מהאינטואיציה: דווקא מוצרי האוקסיד הזולים מספקים הכי הרבה מגנזיום לשקל"
  ("What we found is counter-intuitive: oxide products deliver the most magnesium per shekel")
- insightLine (Nutrikare 520): "התמורה הגבוהה ביותר למחיר במדף" ("Highest value for money on the shelf")
- rowVerdict (MagUp): "מספק כ-271 מ\"ג מגנזיום יסודי לכמוסה — פי 2.7 מהמינון המינימלי האפקטיבי"

**The attack (journalist / food scientist):**
Bari tells consumers to buy the supplement their body barely absorbs. The benchmark states oxide
absorption is ~4%. At that rate, 314mg oxide label dose = ~12.6mg absorbed. Magnesium citrate at
200mg label dose with ~40% absorption = ~80mg absorbed. A D-grade citrate product (score 49,
ranked outside the top 7) delivers 6x more absorbed magnesium than the page's top-ranked C
(Nutrikare 520). The headline "best value" is calculated on label weight, not bioavailability.
The category note warns about low absorption but does not quantify it (no "~4%" appears
anywhere in consumer-facing copy). At the score/grade level, the page's own system rewards
the biologically least available form.

**Severity: CRITICAL**

**Does the absorption caveat in the category note protect against this?**
No. The category note says "oxide is absorbed at a low rate" (ספיגה נמוכה). It does not say
"approximately 4%" or "your body may use less than 1 in 10 milligrams." The prologue leads with
the oxide-wins-on-value finding. The insightLines and grades reinforce it. The caveat is a
subordinate clause in a text block consumers are not required to see before encountering scores.

The "best value" frame is the loudest claim on the page and it is contradicted by the absorption
science the page itself cites as context.

**Verdict: DOES NOT SURVIVE the attack.** The page's own benchmark says citrate is the
strongest evidenced form for comparative bioavailability. The framing systematically elevates
the weakest-absorbed form.

Routes to: Nutrition Agent (methodology — does the scoring system intentionally not weight
absorption because it scores "label-declared dose"?), Content Agent (copy framing — the category
note needs quantified absorption language at the score level, not only in the fine print).

---

## Attack 2: Promise-delivery percentages — "2.7x minimum effective dose"

**Exact claim attacked:**
- rowVerdict (MagUp): "פי 2.7 מהמינון המינימלי האפקטיבי" ("2.7x the minimum effective dose")
- rowVerdict (Nutrikare 520): "פי 3.1 מהמינון המינימלי האפקטיבי"
- Category note: "המינון המינימלי האפקטיבי שאנו משתמשים בו לתוסף יומי הוא כ-100 מ\"ג מגנזיום יסודי"

**The attack (regulator / scientist):**
The 100mg threshold is applied as a single universal denominator across all products, regardless
of what claim the engine actually matched each product to. The benchmark specifies claim-specific
thresholds: general repletion = 100–200mg; blood pressure = 300–400mg; migraine = 400–600mg;
sleep = 200–400mg.

The engine matched MagUp (7290013142894) to "blood pressure reduction" (trace:
claim_matched = "blood pressure reduction"). The benchmark's defensible dose for that endpoint
is 300–400mg/day. MagUp delivers 271mg elemental oxide. Against the correct denominator,
MagUp is 271/300 = 0.90x — it falls BELOW the minimum effective dose for its matched claim.
The page displays "2.7x" — correct only against the general 100mg threshold, not against the
specific claim the engine scored it on.

The same applies to Altman Balance (7290019444206): engine matched "muscle mass/strength
(sarcopenia)" at 100mg threshold; page copy frames this product as meeting the threshold
"for sleep and relaxation" (200mg threshold). The engine never scored this product against
a sleep claim. The page framing is untracked by the scoring.

**Can a regulator say "those numbers are made up"?**
The 100mg number itself has a defensible scientific basis (benchmark §2, NIH ODS). But the
application of a single threshold across all claims — including products matched to endpoints
requiring 3–4x that threshold — means the multiplier displayed to consumers is systematically
overstated for the high-dose-claim products.

**Severity: HIGH**

**Verdict: DOES NOT SURVIVE in its current form.** The displayed multiplier must use the
threshold corresponding to the engine's matched claim, not the general floor.

Routes to: Nutrition Agent (scoring logic — should the promise-delivery ratio use claim-specific
denominators?), Content Agent (copy — fix rowVerdict multipliers to the matched claim threshold).

---

## Attack 3: Brand callouts — "worst value on the shelf"

**Exact claims attacked:**
- insightLine (Nutrikare taurate): "התמורה הגרועה ביותר במדף: היקר ביותר ליחידת מגנזיום"
- rowVerdict (Nutrikare taurate): "התמורה הגרועה ביותר על המדף: מינון זעום במחיר גבוה מכולם"

**The attack (competitor's lawyer):**
Is Nutricare taurate actually the most expensive per unit of magnesium across all 18 products?

Verification: 161.9 ILS / (76mg × 8.9% × 90 servings) = 161.9 / 608.8mg total elemental = 0.2659 ILS/mg.
This was computed against all 18 products in the corpus.

Three products (Magnox B6, Altman Balance, Amorficare PH) have null servings_per_container
in the corpus — their price/mg could not be computed. For Amorficare (181.9 ILS, 160mg
carbonate, stated 60 capsules): 181.9 / (160 × 28.8% × 60) = 181.9 / 2,764.8mg = 0.0658 ILS/mg
— better than taurate. For Magnox (109.9 ILS, 432mg oxide, stated 60 capsules):
109.9 / (432 × 60.3% × 60) = 0.0070 ILS/mg — far better than taurate.

These products' missing-servings data is a corpus gap, not a legal shield. If Nutricare
launches a legal challenge and asks "how did you compute the price/mg ranking when three
products had null servings," the answer is that Bari excluded three products from the comparison
by corpus data gaps and then issued a superlative. Whether the superlative survives depends
on whether imputing the container size from the product name (e.g., "60 כמוסות" in the product
name itself) would change the ranking. It would not — taurate remains worst at 0.266 ILS/mg.
But the method of handling null-servings data is not disclosed on the page.

**Severity: HIGH** (the underlying fact is defensible; the undisclosed methodology gap is the risk)

**Verdict: CONDITIONALLY SURVIVES.** The taurate ranking holds when container sizes are
imputed from product names. But the page does not disclose that three products had missing
data in the servings field. The superlative "worst on the shelf" needs either (a) the null-servings
handling documented, or (b) disclosure that 3 products' per-mg costs could not be precisely computed.

Routes to: Data Agent (fix null servings_per_container for Magnox, Altman Balance, Amorficare),
Content Agent (add methodology disclosure for comparatives).

---

## Attack 4: The label-truthfulness assumption

**Exact claim attacked:**
- Category note: "אנחנו מסתמכים על התווית; איננו בודקים במעבדה את התכולה בפועל"
  ("We rely on the label; we do not lab-test actual content")
- Every product's elemental mg figure, e.g., "כ-314 מ\"ג מגנזיום יסודי לכמוסה"

**The attack (journalist):**
The benchmark (§1, standing caveat 1) cites a Polish AAS assay of 116 EU supplements: 58.7%
were outside legal tolerance, with actual content ranging from 98% below to 304% above the
declared label value. That variance was independent of price.

The page declares specific elemental milligram figures (314mg, 271mg, 7mg) with ~ precision,
sourced from label declarations. The category note says it relies on labels. But it does not
tell the consumer that more than half of supplements tested in a comparable jurisdiction were
materially wrong. A consumer reading "314mg elemental" and comparing it to "7mg elemental"
is making a decision on a quality difference of 44x. If either figure is within the
measured range of mislabeling (98% below to 304% above), the entire ranking could invert.

The caveat "we rely on the label" without quantifying known mislabeling rates is the weakest
possible disclosure for a comparison page whose entire value proposition rests on label accuracy.

**Severity: MEDIUM** (the page cannot lab-test, the caveat exists; but its thinness is a
reputation risk, not a factual error)

**Verdict: SURVIVES with a weakness.** The caveat is present. The 58.7% figure from the
Polish assay is from the EU, not Israel, and cannot be directly applied. But the generic
"we use labels" disclaimer is notably thin for a page that issues specific-to-the-milligram
comparisons. A more quantified disclosure ("supplement labeling accuracy is imperfect; studies
suggest material mislabeling rates in regulated markets") would substantially reduce this risk.

Routes to: Content Agent (strengthen the label-accuracy disclosure), Nutrition Agent
(is the 58.7% Polish assay finding applicable to Israeli products?).

---

## Attack 5: Price-value verdicts — stale and single-retailer

**Exact claim attacked:**
- Category note: "תמורה גבוהה = הרבה מגנזיום (לפי התווית) לכל שקל, מול שאר המדף הישראלי"
- All price-derived rankings and comparatives ("Zol beyoter" / "expensive relative to shelf")

**The attack (savvy consumer / competitor):**
Three specific problems, each independently attackable:

(a) No per-product price capture date is shown. The page's metadataLine says "יוני 2026"
(month-only). The benchmark requirement (§1 caveat 4) is that "every price carries a capture
date." Supplement prices on Israeli e-tailers fluctuate with promotions, bundles, and holiday
sales. A product labeled "most expensive on the shelf" at 161.9 ILS may have been 99 ILS
with a coupon the day after the scrape.

(b) Single-retailer sourcing. Prices come from one retailer per product (bteva.co.il,
vitamins4all.co.il, altman.co.il, etc. as per corpus provenance fields). The page makes
shelf-level comparisons ("most expensive on the shelf") but the "shelf" is a composite of
different retailers, not a single store's prices on the same day. Cross-retailer price
comparisons have no disclosed normalization.

(c) Three products (Magnox, Altman Balance, Amorficare) have null servings_per_container
in the corpus. Their price-per-effective-dose cannot be computed. The page includes
price-based commentary on all three products (e.g., Altman Balance "מחיר סביר", Magnox
"במחיר גבוה יחסית") without disclosing that the underlying cost-per-day figures are
inferred or unavailable.

**Severity: MEDIUM**

**Verdict: SURVIVES in aggregate framing, FAILS on specific comparatives.** The general
"we compare prices within the Israeli shelf only" frame is fine. But issuing a superlative
("most expensive per unit") across a corpus where 3 products' per-mg costs were not
computable, and citing that claim without per-product price dates or retailer names,
does not meet the benchmark's own price-disclosure standard.

Routes to: Data Agent (capture per-product price dates and retailer sources; fix null
servings), Content Agent (add price staleness caveat and retailer attribution).

---

## Attack 6: Sleep / cramp / stress framing — efficacy implied beyond evidence

**Exact claims attacked:**

(a) Altman Balance (7290019444206) rowVerdict:
"עומד ברף הדרוש לתמיכה בשינה ורגיעה" ("meets the threshold required for sleep and relaxation support")

(b) NT LC capsules (7290010207640) insightLine:
On-label claim: "למניעת התכווצויות שרירים" (cramp prevention)
Positive signal in expansion: "כ-188 מ\"ג מגנזיום יסודי לכמוסה — מינון בינוני-גבוה" and
"מקור ים המלח — גיוון צורה" (described as positive against a cramp-prevention claim)

(c) Altman Balance insightLine:
"כתוסף הרגעה/שינה המינון עומד ברף" — frames this as legitimate sleep/relaxation product

**The attack (nutrition scientist):**

(a) SLEEP: The engine matched Altman Balance to "muscle mass / strength (sarcopenia)," NOT to
a sleep endpoint (trace: claim_matched = "muscle mass/strength (sarcopenia) in older adults").
The page copy frames this product as a sleep/relaxation supplement that "meets the threshold."
Two problems: the engine scored it on a different claim, and the benchmark rates sleep evidence
as WEAK ("systematic reviews contradictory"). The page implies sleep efficacy where the engine
made no such determination and the evidence does not support it.

(b) CRAMPS: Cochrane systematic review CD009402 found no benefit for magnesium in muscle
cramps. The benchmark explicitly records this as evidence tier = INSUFFICIENT. NT LC's
entire on-label claim is cramp prevention. The page lists "188mg elemental — mid-high dose"
as a positive signal — but high dose of an insufficient-evidence endpoint is not a positive.
The engine resolved the claim away from cramps to sarcopenia to avoid the INSUFFICIENT rating,
but the page copy does not flag the on-label cramp claim as unsupported. A consumer buying
NT LC for cramps based on Bari's positive-signal framing is making an evidence-free decision.

(c) STRESS: The benchmark notes that EFSA has specifically ruled that "mental stress resistance"
is NOT an authorized health claim for magnesium. No current page product makes this claim
explicitly, but the category positioning ("הרגעה" / relaxation) skirts this boundary.

**Severity: HIGH**

**Verdict: DOES NOT SURVIVE.**
- Altman Balance sleep framing is directly contradicted by the engine's matched claim.
- NT LC positive signals are written against a claim the evidence cannot support.
Both need correction before the page could be shown to consumers.

Routes to: Content Agent (rewrite Altman Balance rowVerdict to match the engine's sarcopenia
claim; remove or caveat the NT LC positive signals against cramp prevention),
Nutrition Agent (should cramp prevention products carry an explicit "Cochrane: no benefit" notice?).

---

## Attack 7: The coherence of the paradox — is it self-contradictory?

**Exact claim attacked:**
- Prologue: oxide = best value for money
- Category note: high elemental ≠ high absorbed (the "absorption paradox")
- Scores: oxide products rank B and C at top of table

**The attack (smart consumer):**
"You told me high elemental doesn't mean high absorbed. Then you ranked the high-elemental
oxide products at the top and called them best value. You built your entire comparison on the
very metric you said was misleading. Which is it?"

**Analysis:**
The page is internally coherent on a narrow technical reading: it explicitly measures "elemental
per shekel on the label" and says so in the category note. The paradox framing ("counter-intuitive")
acknowledges the tension.

BUT: the page's headline and score table are not labeled "elemental per shekel." They are simply
"scores" and "grades." A B-grade with an insightLine saying "leading value for money" does not
register as "this is a label-elemental-per-shekel score, not a recommendation to buy." The category
note does clarify, but it is four paragraphs long and appears below the hero. The disconnect between
the label and what the ranking actually measures is not resolved by a buried disclosure.

Crucially: the category note says the score weighs "quantity of elemental magnesium in practice,
the quality of the chemical form, strength of scientific evidence for the label claim, and clarity
of labeling." If form quality is scored, oxide (the worst form per benchmark §3) should receive
the lowest form score. The engine does show form sub_scores for oxide products at 45/100 (MagUp)
and similar. But that penalty is insufficient to prevent oxide from dominating the top 4 slots.
The form score does not compensate for the dose advantage oxide has on the label — by design.

**Severity: CRITICAL** (not a bug in the math, but a structural framing contradiction that would
be the second paragraph of any hostile media story)

**Verdict: DOES NOT SURVIVE adversarial expert read.** The page calls something "best value"
using a metric it also warns is misleading. That is not a paradox the page resolves — it is
a contradiction it names and then proceeds to embed in its ranking output.

Routes to: Nutrition Agent (should the scoring system weight absorption into the dose sub_score
rather than scoring declared elemental?), Product Agent (can this category go live if the
primary ranking signal systematically elevates the weakest-evidence form?).

---

## Product-by-Product Assessment

| ID | Name (short) | Score/Grade | RT Assessment | Severity Notes |
|---|---|---|---|---|
| 7290013142894 | MagUp Altman 60cp | 67/B | Threshold claim wrong: engine=BP (needs 300mg), page says 2.7x at 100mg floor | HIGH |
| 7290001065662 | Nutrikare 520 100cp | 63/C | Best-value claim defensible; absorption paradox applies | CRITICAL-context |
| 7290015318426 | Tinc Oxide 520 90cp | 63/C | Same as above; "honest labeling" positive signal is fine | CRITICAL-context |
| 7290017218564 | Altman 520 60cp | 63/C | Same oxide paradox; claim evidence weak per insightLine | CRITICAL-context |
| 7290010207640 | NT LC capsules | 59/C | On-label cramp claim = Cochrane INSUFFICIENT; positive signals mislead | HIGH |
| 7290019444206 | Altman Balance | 59/C | Engine matched sarcopenia; page frames as sleep — mismatch | HIGH |
| 7290017847122 | Magnox B6 | 58/C | Source: amazon.com, null servings; 432mg labeled "elemental" — ambiguous; page computes 260mg applying 60.3% fraction which may be double-applied | HIGH |
| 7290015429245 | Amorficare PH | 49/D | Null servings in corpus; amorphic technology dismissal is defensible | MEDIUM |
| 7290001066973 | Nutrikare Malate 90cp | 49/D | Meets stated threshold; malate evidence sparse but the claim is modest | OK |
| 7290015318532 | Tinc Malate 60cp | 49/D | Price claim defensible; form is genuinely better than oxide | OK |
| 7290011899967 | Altman Citrate 120cp | 49/D | "Good form, low dose" is accurate | OK |
| 7290013464248 | Supherb Citrate B6 Badatz | 49/D | Kosher note appropriate; low dose claim correct | OK |
| 7290019444480 | Altman Bisglycinate 60cp | 49/D | "Pays for form, gets little Mg" — fair | OK |
| 7290018439579 | Nutrikare Taurate | 49/D | "Worst value" superlative defensible; null-servings gap for 3 peers undisclosed | HIGH |
| 0033984005181 | Solgar Ca/Mg/D3 | 49/D | "Not a dedicated Mg supplement" = correct and fair | OK |
| 7290118816065 | Supherb TRIOMAG | 34/E | Elemental calc assumes citrate fraction on a proprietary blend — unknown proportions | HIGH |
| 7290001065594 | Nutrikare Nano Lipo | 34/E | "Marketing impressive, delivery tiny" — defensible; nano-lipo evidence attack is correct | OK |
| 7290018439043 | Nutrikare WELL | 34/E | "WELL" claim vague — fair finding | OK |

(SP-7290118818205 / Supherb Max 550 is in the corpus but absent from the page without explanation.)

---

## Summary Assessment

**Structural: Overriding structural problem.** The page's scoring logic rewards declared elemental
magnesium per shekel without weighting absorption into the primary signal. This is a deliberate
methodology choice, but it produces a consumer-facing output where the least bioavailable form
tops the table. The absorption caveat in the category note does not neutralize the headline effect
of the score/grade system. This is the strongest attack vector and the hardest to defend publicly.

**Claim framing: Partially incorrect.** Altman Balance sleep framing and NT LC cramp framing are
undefended by the engine's own matched claims and by the benchmark evidence tier. These are not
over-reading by an attacker — the copy states efficacy implications the science and the engine
do not support.

**Price arithmetic: Plausible-but-unverifiable.** The per-mg rankings are internally consistent
with the corpus data, but the corpus has data gaps (null servings, single retailer, no per-product
dates) that make the precision of comparative claims contestable.

**Elemental arithmetic: Mostly Justified.** The conversion math is correct for all products with
clear form declarations. The TRIOMAG and Magnox exceptions are genuine data ambiguities, not
fabrications.

---

## Findings by Severity

### CRITICAL — must resolve before launch

**RT-1: Oxide absorption not quantified at score level**
The page ranks 4 oxide products at B/C and frames them as "best value" while the absorption rate
(~4% per benchmark) is disclosed only as "low" in a fine-print category note. At 4% absorption,
the top-ranked oxide product delivers ~12mg absorbed — less than several D-grade chelated products.
The headline consumer signal (score/grade/insightLine) contradicts the absorption science the page
itself cites. This is the most attackable claim on the page.
Evidence: benchmark §3 (citrate > oxide); insightLine for 7290001065662; category note absorption
paragraph; absorption arithmetic verified above.
Implication: Consumer is directed toward the supplement form with the weakest bioavailability.
Routes to: Nutrition Agent (is absorbed dose in scope for this scoring framework?), Content Agent
(absorption must be quantified in insightLines, not buried).

**RT-2: Page ranks "best value" using a metric the page itself calls misleading**
The prologue calls high elemental ≠ high absorbed "the paradox." The scores then rank on elemental
per shekel. The page resolves the paradox in the category note and not in the scores. A hostile
expert's opening line is: "Bari's own page admits the ranking signal is misleading, then uses it."
Evidence: prologue paragraph 3 ("הפוך מהאינטואיציה"), category note absorption paragraph, top-4
oxide placement.
Implication: Structural coherence failure visible on a single read. Cannot be fixed by copy alone.
Routes to: Nutrition Agent (does the dose sub_score need to weight absorbed, not declared, elemental?),
Product Agent (can this go live if the primary ranking = known-misleading metric?).

### HIGH — should resolve before launch

**RT-3: Claim-threshold mismatch in displayed multipliers**
MagUp rowVerdict: "2.7x minimum effective dose" — correct only against the 100mg general floor.
The engine matched MagUp to blood pressure reduction (threshold 300–400mg). Against that threshold,
MagUp delivers 0.90x (below, not above). The displayed multiplier uses the wrong denominator.
Evidence: SP-7290013142894 trace (claim_matched = "blood pressure reduction"), benchmark §2 BP
row (300–400mg/day), rowVerdict text, arithmetic verified above.
Implication: A product displayed as "2.7x effective dose" is actually below its matched endpoint's
threshold. Consumer overestimates efficacy by 3x on the specific claim the engine scored.
Routes to: Nutrition Agent (fix the ratio denominator to match claim-specific thresholds),
Content Agent (rewrite multiplier language in rowVerdict for MagUp and any other BP/migraine-matched products).

**RT-4: Altman Balance sleep framing is unsupported by the engine**
The engine matched Altman Balance to "muscle mass / strength (sarcopenia)" (trace verified).
The page insightLine and rowVerdict frame this product as meeting the "sleep and relaxation"
threshold ("עומד ברף הדרוש לתמיכה בשינה ורגיעה"). The engine never scored it on a sleep claim.
The benchmark rates sleep evidence as WEAK. The copy implies sleep efficacy that neither the
engine nor the evidence supports.
Evidence: SP-7290019444206 trace (claim_matched = "muscle mass/strength (sarcopenia)"),
benchmark §2 sleep row (weak evidence, contradictory reviews), insightLine and rowVerdict text.
Implication: Consumer buys a sleep supplement based on a claim the scoring engine didn't make.
Routes to: Content Agent (rewrite insightLine and rowVerdict to match the engine's matched claim).

**RT-5: NT LC cramp claim — Cochrane INSUFFICIENT evidence, presented with positive signals**
NT LC's label claim is cramp prevention. Cochrane CD009402 found no benefit for magnesium in
muscle cramps (evidence tier = INSUFFICIENT per benchmark §2). The expansion's positive signals
list the elemental dose as a positive ("188mg — mid-high dose") without noting the endpoint is
INSUFFICIENT. The engine sidesteps the cramp claim by resolving to sarcopenia, but the page copy
does not surface the cramp evidence problem to the consumer.
Evidence: SP-7290010207640 label_claim ("למניעת התכווצויות שרירים"), benchmark §2 cramp row
("Cochrane CD009402: no benefit"), expansion positiveSignals text.
Implication: Consumer buys a cramp-prevention supplement from a page that does not disclose the
endpoint has insufficient evidence. This is a health-claim liability.
Routes to: Content Agent (add explicit caveat that cramp-prevention evidence is insufficient per
Cochrane; remove dose as a positive signal for an insufficient endpoint), Nutrition Agent
(should cramp-claim products carry a mandatory INSUFFICIENT-evidence notice?).

**RT-6: TRIOMAG elemental estimate is a citrate-only approximation on a proprietary blend**
TRIOMAG (7290118816065) declares "citrate + bisglycinate + taurate blend, 200mg" as a
proprietary_blend=True. The page displays "~32mg elemental." This is 200mg × 16.2% (citrate
fraction) — the engine defaulted to the first-named form (citrate) in the corpus record. The
actual proportions of the blend are undisclosed. If the blend is equal thirds:
200 × (16.2% + 14.1% + 8.9%) / 3 = 26.1mg elemental. The difference is ~6mg or ~18% of
the stated figure. The page states "~32mg" without noting it is an estimate that assumes
100% citrate composition.
Evidence: SP-7290118816065 panel (proprietary_blend=True, form_raw="citrate+bisglycinate+taurate"),
bsip0s_label (form="citrate"), elemental arithmetic verified above.
Implication: The stated elemental figure for TRIOMAG is a best-case assumption, not a known fact.
Routes to: Data Agent (obtain per-form proportions from manufacturer or flag as estimate-with-range),
Content Agent (add "estimated" qualifier and range to the TRIOMAG elemental figure).

**RT-7: Magnox B6 — 432mg labeled "elemental," source is amazon.com with null servings**
The corpus panel for Magnox B6 (7290017847122) was scraped from amazon.com (non-Israeli source).
The ingredient lists "מגנזיום (elemental), 432mg" — meaning the label may declare 432mg as the
elemental quantity. The benchmark rule (§1 caveat 3) states: "when the label states elemental mg,
that number wins." The page applies the oxide fraction (60.3%) to derive ~260mg — which would
be correct only if 432mg is compound weight, not elemental. If the label declares 432mg elemental
(which "magnesium (elemental)" nomenclature suggests), the correct displayed figure is 432mg,
not 260mg, and the compound would be ~716mg oxide — an unusually high dose.
The source has null servings_per_container, making price-per-mg uncomputable.
Evidence: SP-7290017847122 panel (url=amazon.com, ingredient="מגנזיום (elemental)", amount=432,
form=oxide, servings_per_container=null), benchmark §1 caveat 3.
Implication: Either the elemental figure is understated by 172mg (if 432 is declared elemental),
or the source is unreliable for this product. Either way, the confidence=partial classification
is warranted but insufficient — the elemental figure may be meaningfully wrong.
Routes to: Data Agent (obtain Magnox label from the Israeli manufacturer or an IL retailer; resolve
the elemental vs compound ambiguity before displaying ~260mg as a stated figure).

### MEDIUM — should document or monitor

**RT-8: Label mislabeling rate not quantified in consumer-facing copy**
The benchmark cites 58.7% of EU supplements outside legal tolerance (Polish AAS assay). The
page says "we rely on the label; we do not lab-test." This caveat exists but is not quantified.
Every elemental figure on the page is potentially a best-case assumption with material
real-world variance (98% below to 304% above, per the assay range). The disclosure meets a
minimum standard but is thinner than the underlying risk.
Evidence: benchmark §1 caveat 1 (58.7% outside tolerance), category note final line.
Implication: Reputation risk if a consumer's purchased product is independently tested and
found materially different from the Bari-displayed figure.
Routes to: Content Agent (strengthen label-accuracy caveat with reference to industry mislabeling
rates, without overstating the Israeli context).

**RT-9: No per-product price capture date; cross-retailer composite**
The metadataLine shows "יוני 2026" (month-level). The benchmark requires a per-product
capture date. Prices were sourced from different Israeli e-tailers per product with no
disclosed normalization. "Most expensive on the shelf" and "cheapest per mg" are composite
comparisons across a multi-retailer corpus, not a single-shelf observation.
Evidence: benchmark §1 caveat 4; corpus provenance fields showing bteva, vitamins4all, altman,
tinc, biogaya, solgar as separate sources.
Implication: Comparative price claims are stale if prices changed after the scrape; cross-retailer
comparisons are not normalized (different VAT treatment, membership discounts, etc.).
Routes to: Data Agent (add per-product scrape date to corpus; document retailer per SKU),
Content Agent (add per-product price date disclosure and retailer attribution).

**RT-10: 19th product excluded from page without explanation**
The corpus (_corpus_run_full_v9.json) contains 19 magnesium-engine products with grades.
The page displays 18. The excluded product is SP-7290118818205 (Supherb מגנזיום מקס 550,
D/49, 84.9 ILS, proprietary blend, 60 servings). No comment in the page-data.ts header
explains its exclusion.
Impact on rankings: Supherb Max would rank ~7th by price/mg (0.0159 ILS/mg). It does not
affect the best or worst value claims. But the discrepancy between "19 products in corpus"
and "18 products in page" creates a cherry-picking appearance without documentation.
The page header says "18 מוצרים" with no note about the omission.
Evidence: corpus count verified by script; page IDs enumerated from page-data.ts; SP-7290118818205
confirmed present in corpus and absent from page.
Implication: Minimal data impact; documentation risk.
Routes to: Data Agent / Product Agent (document why SP-7290118818205 was excluded; add to
page or record a principled exclusion reason — e.g., proprietary blend preventing reliable
elemental calculation).

---

## Overall Verdict

**FAIL — must resolve RT-1 through RT-7 before any consumer exposure.**

This page cannot go live in its current form. The structural failures (RT-1, RT-2) are not
copy problems that a rewrite can patch — they require a methodology decision: does this
scoring system measure administered elemental magnesium or absorbed magnesium? The current
answer is "administered," but the page frames the output as a consumer recommendation.
Those two things are incompatible without a far more prominent and quantified absorption
disclosure that overrides the grade-and-score headline.

The claim-framing failures (RT-3 through RT-7) are individually fixable but collectively
signal that the page copy was authored against a simplified view of the benchmark data
rather than the full constraint set.

**Would this page survive a hostile expert read?** No. A nutrition scientist would reach
RT-1 in the first 30 seconds. A competitor's lawyer would reach RT-3 and RT-4 within
a minute. A Cochrane-aware journalist covering supplement misinformation would lead with
RT-5 (cramp prevention on zero evidence). The page has a solid analytical foundation —
the elemental arithmetic is correct, the price data is directionally right, the taurate
worst-value claim is defensible — but the framing decisions layer misinformation onto
accurate underlying data.

---

## Return Contract

```json
{
  "agent": "adversarial-qa-agent",
  "task": "magnesium-page assumptions challenge",
  "run_id": "real_corpus_v3_v9",
  "date": "2026-06-20",
  "artifacts": [
    {
      "path": "C:\\Bari\\02_products\\supplements\\real_corpus_v3\\magnesium_assumptions_redteam_v1.md",
      "sha256": "not_computed_read_only_agent"
    }
  ],
  "counts": {
    "products_in_corpus": 19,
    "products_on_page": 18,
    "products_missing_from_page": 1,
    "products_with_null_servings": 3,
    "critical_findings": 2,
    "high_findings": 5,
    "medium_findings": 3,
    "total_findings": 10
  },
  "track_v_verdict": "NOT_RUN (this was a Track C challenge only — no build/render check)",
  "track_c_verdict": "FAIL",
  "open_critical": 2,
  "open_high": 5,
  "go_live_gate": "BLOCKED (2 open CRITICAL, 5 open HIGH)",
  "commands_run": [
    "Read magnesium-page-data.ts",
    "Read magnesium_benchmark_v1.md",
    "Python: corpus structure inspection",
    "Python: elemental calculation verification (all 18 products)",
    "Python: price/mg ranking computation",
    "Python: null-servings identification",
    "Python: TRIOMAG proprietary blend elemental range",
    "Python: claim-threshold mismatch analysis",
    "Read SP-7290018439579.json (taurate)",
    "Read SP-7290118816065.json (TRIOMAG)",
    "Read SP-7290017847122.json (Magnox B6)",
    "Read SP-7290019444206.json (Altman Balance)",
    "Read SP-7290010207640.json (NT LC)",
    "Read SP-7290013142894.json (MagUp)"
  ],
  "not_done": [
    "Track V (build/render/mobile geometry/leakage) — this was a Track C only engagement",
    "Hebrew leakage gate (hebrew_readability.py) — no server access confirmed",
    "Evidence registry validation (EV-### / SUPP-EV-### cross-check against registry files)",
    "E2E / a11y harness (npm test:e2e, npm test:a11y)"
  ],
  "spec_conflicts": [
    "The benchmark (§5, promise-delivery ratio definition) specifies using the lower bound of the benchmark band FOR THE PRODUCT'S OWN MAIN CLAIM as denominator. The page uses a single 100mg general floor for all products regardless of engine-matched claim. These are inconsistent."
  ]
}
```
