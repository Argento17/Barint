# Return: P246

> ⚠️ **STATUS: RETURNED-UNVERIFIED.** Raw agent output captured by the router.
> Nothing here is accepted, closed, or true until the ORCHESTRATOR verifies every
> claim against artifacts (Return Contract v1). The router never closes.
> (Law added after P35 was face-value-closed with contradictions inside it.)

| Field | Value |
|---|---|
| Prompt file | `tasks\prompts\P246_c3_magnesium_assumptions_challenge.md` |
| Model | `openai/gpt-5.5` |
| Started | 2026-06-20T09:07:49.259115+00:00 |
| Finished | 2026-06-20T09:12:10.670397+00:00 |
| Exit code | 0 |

---

## Output

```
# Independent Review: Magnesium Comparison Page Assumptions

Role: outside-the-family reviewer. Scope: challenge assumptions in plain English. No scoring changes. No product data invention. No Open Food Facts.

Bottom line: the page can be honest and useful, but only if it stops implying that "more elemental magnesium on the label" equals "better magnesium delivered to the body." The label is the only practical starting point, but the consumer-facing language must repeatedly say: this is a label-based comparison, adjusted for form where evidence allows, not a lab-verified absorbed-dose ranking.

## 1. Score the magnesium on the label, not what is absorbed

Verdict: SHAKY, but usable if framed carefully.

The evidence: supplement labels normally state elemental magnesium or a magnesium compound amount. That is observable, comparable, and auditable. Actual absorption is not directly observable from the package. It varies by form, dose size, stomach acidity, food, baseline magnesium status, gut disease, and probably individual need. So a page cannot honestly calculate the exact amount absorbed by each buyer.

But stopping at label elemental magnesium is also dangerous. Magnesium oxide can show a very high elemental number because oxide is magnesium-dense by weight, yet it is poorly soluble and often less bioavailable than organic salts. Human comparative work supports the broad direction: oxide is generally worse than citrate and chelated/organic forms. One cited trial in ileal-resection patients compared magnesium diglycinate with magnesium oxide and found similar average absorption in the whole small group, but better absorption and tolerability for diglycinate in the subgroup with the poorest oxide absorption; this is useful but not a clean general-population ranking study (Schuette 1994, PMID:7815675). The local registry also cites human bioavailability evidence for oxide below citrate/glycinate, but the total evidence base is not large or perfectly consistent.

Judgment: label-based scoring is honest only if it is presented as "declared dose" or "label dose," not as "what your body gets." If the page says or implies absorbed benefit, it overclaims.

What I would change: keep elemental magnesium as the primary auditable number, but rename it clearly: "label-declared elemental magnesium." Add a second consumer note beside oxide and other low-solubility forms: "High label magnesium does not mean high absorption." Do not claim exact absorbed milligrams unless the page labels it as a rough illustration, not a score.

## 2. "Best value" = most elemental magnesium per shekel

Verdict: WRONG if shown as the main "best value" result. SHAKY if shown as a narrow "label mg per shekel" metric.

The evidence: this assumption is the most consumer-misleading one. Magnesium oxide can look excellent on elemental milligrams per shekel because it is cheap and magnesium-dense. But oxide is also the form most likely to disappoint if the consumer thinks they are buying absorbable magnesium. Some studies and reviews cite very low fractional absorption for oxide, sometimes around 4%, while citrate and other soluble/organic salts often perform better. The exact percent is not stable across studies, populations, and methods, but the direction is consistent enough: oxide is a poor-bioavailability form compared with citrate and many chelates.

The absorbed-magnesium picture in plain English:

- Oxide: lots of magnesium printed on the label, cheap, but relatively poorly absorbed and more likely to act as an osmotic laxative at higher doses.
- Citrate: usually better dissolved and better supported by direct human comparison than oxide; it can also loosen stools.
- Glycinate/bisglycinate: marketed as gentle and often plausible as a better-tolerated option; human head-to-head evidence versus citrate is thinner than marketing suggests.

A simple example shows the trap. If a product gives 300 mg elemental magnesium as oxide and only a small fraction is absorbed, while another gives 150 mg as citrate/glycinate with meaningfully higher absorption, the cheaper oxide product may not be the better physiological value. The precise numbers are uncertain, but the "oxide wins because label mg is high" logic is not robust.

Judgment: "elemental mg per shekel" is a price-density metric, not a value metric. Calling it "best value" without a form caveat invites a journalist to say: "Your top value pick is the form many sources call least absorbed." That criticism would be fair.

What I would change: rename the metric to "cheapest label magnesium" or "lowest cost per labeled elemental mg." Create a separate "practical value" badge that requires both adequate label dose and acceptable form. Oxide can still be called cheap, but should not be crowned "best value" unless the text says "best value by label milligrams only, not by likely absorbed magnesium."

## 3. Citrate ranked above glycinate/bisglycinate

Verdict: SOUND in a narrow evidence-ranking sense, but overconfident if phrased as citrate is clearly biologically superior.

The evidence: citrate has better direct human comparative evidence than glycinate for general supplement bioavailability, especially compared with oxide. Glycinate/bisglycinate has plausible mechanisms and a tolerability story, and there is some human evidence, but much of the consumer-market certainty around "glycinate is best absorbed" is stronger than the clinical evidence.

The important nuance: the cited diglycinate-vs-oxide trial was in 12 patients with ileal resection, not healthy consumers. It did not show a clean whole-group superiority for diglycinate over oxide, though it did show advantages in the subgroup with poor oxide absorption and better tolerability (PMID:7815675). That supports "glycinate may be useful/gentle," not "glycinate is proven absorption champion." For citrate, the direct comparative evidence against oxide is more straightforward in many summaries, but the page should still avoid sounding certain about exact superiority over glycinate.

Judgment: it is fair to rank citrate above glycinate if the criterion is "stronger direct human comparative evidence." It is not fair to imply citrate is definitely better for every person or that glycinate is mostly marketing fluff. Glycinate may be a very reasonable product choice, especially for tolerability.

What I would change: write: "Citrate has the cleaner direct evidence base; glycinate/bisglycinate is a strong tolerability-forward alternative. We do not treat glycinate as proven superior to citrate." That is defensible and fair.

## 4. Minimum effective-dose thresholds: 100 mg general, 200 mg sleep, 400 mg migraine; below 50% treated as ineffective

Verdict: SHAKY but mostly defensible as practical thresholds, not hard biological cutoffs.

The evidence: 100 mg/day for general supplementation is a reasonable gap-closing number, not a clinical treatment threshold. Adult magnesium requirements are usually discussed around total daily intake from food plus supplements, not supplement-only intake. A 100 mg supplement can help close a dietary gap for some people, but it is not a magic minimum.

For blood pressure, stronger RCT/meta-analysis evidence clusters around higher supplemental doses. A 2016 meta-analysis of 34 randomized, double-blind, placebo-controlled trials found median magnesium dose 368 mg/day for 3 months and suggested around 300 mg/day was enough to raise serum magnesium and modestly lower blood pressure by about 2 mmHg systolic and 1.8 mmHg diastolic (Zhang 2016, PMID:27402922). That supports 300-ish mg for a blood-pressure claim, not 100 mg.

For sleep, 200 mg is a pragmatic low bar, not a proven threshold. A 2021 systematic review/meta-analysis in older adults found only three RCTs, 151 participants, moderate-to-high risk of bias, and low to very-low quality evidence; sleep onset latency improved in pooled analysis, but the authors explicitly said the literature is substandard for confident recommendations (Mah 2021, PMID:33865376). So a 200 mg sleep threshold is a judgment call.

For migraine, 400 mg/day is defensible as a lower-end clinical benchmark. Migraine reviews and headache practice commonly discuss oral magnesium in the 400-600 mg/day range, though trials are mixed and some authors argue for broad use while others are more cautious (for example Mauskop 2012, PMID:22426836; Sun-Edelstein 2009, PMID:19271946). So "400 mg minimum for migraine" is more defensible than the sleep threshold, but it should be claim-specific and not treated as universal.

The "below 50% is ineffective" rule is the weakest part. Biology rarely has a cliff at 50%. A product with 49% of a threshold is not categorically different from 51%. But as a consumer scoring rule, it is reasonable to say: if a product delivers less than half of the page's own minimum benchmark for its own promise, it should not score well.

Judgment: the thresholds are acceptable as practical consumer benchmarks if labeled as "benchmark minimums," not proven cutoffs. The 50% rule is a policy choice, not science.

What I would change: show the thresholds as bands: general gap support 100-200 mg, sleep 200-400 mg with weak evidence, migraine 400-600 mg with moderate evidence. Replace "ineffective" with "unlikely to deliver the promised use at the labeled dose" or "far below our benchmark."

## 5. If labels are often wrong, what is a label-based score worth?

Verdict: SOUND as a limitation, but dangerous if hidden.

The evidence: the page cites an assay finding 58.7% of EU magnesium supplements outside legal tolerance, with actual content ranging from far below to far above label and discrepancy independent of price. I did not independently verify the exact assay paper in this pass, so I would cite it only with full bibliographic details before publication. But the general point is highly plausible: supplement labels are not lab assays, and price does not guarantee content accuracy.

Judgment: a label-based score is still worth something because consumers buy from labels. It can assess whether the product even claims to provide a meaningful dose, names the form, stays under safety ceilings, and avoids unsupported claims. But it cannot prove what is inside the bottle. The honest framing is: "This is the best-case comparison if the label is truthful."

What I would change: put a visible caveat near the score, not buried in methodology: "We do not lab-test products. Scores assume the label is accurate. Independent assays have found many magnesium supplements miss their label amounts, so this is a label-quality score, not a purity guarantee." If the 58.7% statistic is used, cite the exact study title, journal, year, assay method, and legal tolerance definition.

## 6. Evidence tiers: energy/fatigue and immune strong because EFSA-authorized; migraine moderate; sleep and cramps weak/insufficient

Verdict: MIXED. Migraine moderate is sound. Sleep weak is sound. Cramps insufficient is sound. Energy/fatigue and immune as "strong" because EFSA-authorized is SHAKY to WRONG depending on wording.

The evidence: EFSA-authorized health claims are important. They mean a regulatory authority accepted a cause-and-effect relationship for a nutrient function under specified conditions. For magnesium, EFSA has authorized claims such as contribution to normal energy-yielding metabolism, reduction of tiredness and fatigue, electrolyte balance, normal muscle function, normal nervous system function, and maintenance of normal bones/teeth. That supports label compliance and biological plausibility.

But EFSA authorization is not the same as strong clinical evidence that a replete adult taking a magnesium supplement will feel more energy, improve immunity, sleep better, or perform better. Nutrient-function claims often mean "magnesium is necessary for this normal body function," not "extra magnesium improves this outcome in everyone." That distinction matters a lot for consumer trust.

Immune = strong is especially suspect for magnesium. Magnesium has roles in normal physiology, but broad "immune support" supplement claims are often vague and not equivalent to proven reduction in infections or better immune outcomes in ordinary consumers. If the page treats immune as strong simply because of EFSA-style nutrient-function logic, I would downgrade or heavily qualify it.

Migraine = moderate is reasonable: there is mechanistic plausibility, common guideline/practice use, and some trial/review support, but the evidence is mixed and not a slam dunk. Sleep = weak is right given the small, biased evidence base (PMID:33865376). Cramps = insufficient/weak is right, especially for ordinary nocturnal leg cramps in older adults: the 2020 Cochrane review concluded magnesium is unlikely to provide clinically meaningful cramp prophylaxis for older adults with skeletal muscle cramps (PMID:32956536).

Judgment: the page should separate "authorized nutrient-function claim" from "proven consumer benefit." EFSA is a regulatory floor for permitted wording, not a magic stamp of real-world supplement efficacy.

What I would change: classify EFSA nutrient-function claims as "authorized/physiological" rather than "strong" unless there is direct supplementation outcome evidence. Use plain labels: "Authorized normal-function claim" versus "Clinical outcome evidence." Downgrade broad immune support for magnesium unless a specific, cited clinical endpoint is shown.

## 7. Hard ceilings: too-low dose caps around 49/100; unsupported claim caps around 34/100

Verdict: SOUND as consumer-protection policy, but too blunt if every underdosed product gets the same score.

The evidence: a product that does not provide enough magnesium for its own claim should not get a good score just because it uses a nice form or has clean marketing. A product making an unsupported claim should be capped even harder. That is a defensible consumer-protection design.

But a flat low-dose cap can erase useful information. A product with 5 mg elemental magnesium and a product with 140 mg are not equally weak, even if both are below the benchmark. The local recalibration notes already identify this problem: a single 49 pin collapses very different underdosed products into one bucket. That is not a science problem; it is a communication/scoring-resolution problem.

The unsupported-claim cap around 34 is more defensible. If the product's main promise is not supported, more magnesium should not rescue the score unless the page changes the claim being assessed. Otherwise a product could make a nonsense sleep/stress/liposome claim and still look acceptable because it has a lot of elemental magnesium.

Judgment: hard ceilings are reasonable, but the low-dose ceiling should be graded. Unsupported claims can remain a hard E-style cap.

What I would change: keep a hard cap for unsupported claims. Replace the flat too-low-dose cap with a graded "far below benchmark" band, so consumers can see the difference between tiny-dose products and almost-adequate products. Use words like "below benchmark" instead of "ineffective" unless the evidence truly supports no effect.

## The assumption most likely to embarrass the project

The biggest embarrassment risk is assumption 2: "best value = most elemental magnesium per shekel."

Why: it lets cheap magnesium oxide win while the page itself knows oxide is poorly absorbed. A journalist or scientist could fairly say: "Your best-value recommendation rewards the least bioavailable form because you counted label magnesium, not useful magnesium." That attack is easy to understand, easy to quote, and damaging to consumer trust.

Assumption 6 is the second risk: treating EFSA-authorized nutrient-function claims as "strong evidence" of consumer benefit. A scientist could say: "EFSA authorization means the nutrient is needed for a normal function, not that this supplement improves that outcome in non-deficient people." That criticism is also fair.

## The one fix I would prioritize

Fix the value language first.

Do not call oxide "best value" without qualification. Split the metric into two labels:

- "Cheapest labeled magnesium": price per declared elemental mg.
- "Best practical value": adequate dose plus acceptable form plus claim support, with a visible warning that absorption is estimated only qualitatively.

This one change protects the project from the most obvious attack while preserving the useful price information. It also makes the page easier for a normal consumer to understand: cheap label magnesium is not always good magnesium.

## Short source notes

- Schuette SA, Lashner BA, Janghorbani M. Bioavailability of magnesium diglycinate vs magnesium oxide in patients with ileal resection. JPEN. 1994. PMID:7815675.
- Zhang X et al. Effects of Magnesium Supplementation on Blood Pressure: A Meta-Analysis of Randomized Double-Blind Placebo-Controlled Trials. Hypertension. 2016. PMID:27402922.
- Mah J, Pitre T. Oral magnesium supplementation for insomnia in older adults: a systematic review and meta-analysis. BMC Complement Med Ther. 2021. PMID:33865376.
- Garrison SR et al. Magnesium for skeletal muscle cramps. Cochrane Database Syst Rev. 2020 update. PMID:32956536.
- Mauskop A, Varughese J. Why all migraine patients should be treated with magnesium. J Neural Transm. 2012. PMID:22426836. Note: opinionated review; useful, not definitive.
- Sun-Edelstein C, Mauskop A. Role of magnesium in the pathogenesis and treatment of migraine. Expert Rev Neurother. 2009. PMID:19271946.
- EFSA magnesium Article 13 health-claim opinions/register: useful for permitted nutrient-function wording, but not identical to direct proof of supplement benefit in already-replete consumers.

## RETURNED

Changed file:

- `03_operations/supplement_engine/proto_v0/benchmark/magnesium_assumptions_c3_v1.md`: full independent plain-English review of the seven assumptions.

Verify:

- `03_operations/supplement_engine/proto_v0/benchmark/magnesium_assumptions_c3_v1.md:1` confirms the output exists at the requested benchmark path.
- `03_operations/supplement_engine/proto_v0/benchmark/magnesium_assumptions_c3_v1.md:20` starts the assumption-by-assumption review.
- `03_operations/supplement_engine/proto_v0/benchmark/magnesium_assumptions_c3_v1.md:130` identifies the highest embarrassment-risk assumption and priority fix.

--- SSE Events ---
  server.connected: {}
  session.created: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.next.agent.switched: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44963b2001lB4V6CwWIeumEO", "timestamp": "2026-06-20T09:07:55.442Z", "agent": "build"}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "user", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "time": {"created": 1781946475442}, "age
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "text", "text": "You are the outside-the-family independent reviewer. A consumer comparison page rates Israeli magnesium\nsupplements. 
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee449654f001Gs9O0ecIwvEjIN", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "id": "msg_ee449
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee4497ca3001vK2xDGJO6bCh0p", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "snapshot
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee4497e86001jYtO19UG7IMluA", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": "I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": "\u2019ll"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " review"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " relevant"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " context"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " source"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " files"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " first"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " then"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " write"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " assessment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " directly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " requested"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " markdown"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " path"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " return"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " same"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " text"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": " here"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "partID": "prt_ee4497e86001jYtO19UG7IMluA", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee4497e86001jYtO19UG7IMluA", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44981b2001qwcjOtinXalq8N", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  todo.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "todos": [{"content": "Inspect magnesium benchmark context and existing assumptions", "status": "in_progress", "priority": "high"}, {"content": "Draft i
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "todowrite", "callID": "call_DN9jroqezJHlSgnoXN0QiSLs", "state": {"status": "running", "input": {"todos": [{"content": 
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "todowrite", "callID": "call_DN9jroqezJHlSgnoXN0QiSLs", "state": {"status": "completed", "input": {"todos": [{"content"
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee4498cfc001S3j8vFMGyWhQLG", "reason": "tool-calls", "snapshot": "b511395b4330fe5445a1e0a6dc781a1f0e93ef0a", "messageID": "msg_ee449
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee449654f001Gs9O0ecIwvEjIN", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44991d8001FF6LkM3e5pZMUP", "messageID": "msg_ee449654f001Gs9O0ecIwvEjIN", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee449654f001Gs9O0ecIwvEjIN", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44991e6001r2NUUzZA5mc0E5", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee4499df7001CRdXMF2k1EtQZW", "messageID": "msg_ee44991e6001r2NUUzZA5mc0E5", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "snapshot
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449a7e6001OKQVtFSHzFvowj", "messageID": "msg_ee44991e6001r2NUUzZA5mc0E5", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "glob", "callID": "call_78Vl7qCFWSvk9aW8y4LTHzr1", "state": {"status": "running", "input": {"pattern": "03_operations/s
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449a7f10017zw6l2fJn7lbAk", "messageID": "msg_ee44991e6001r2NUUzZA5mc0E5", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "grep", "callID": "call_1VKhPmWFT2sTejv0RsnYqP9L", "state": {"status": "running", "input": {"pattern": "magnesium|citra
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "glob", "callID": "call_78Vl7qCFWSvk9aW8y4LTHzr1", "state": {"status": "completed", "input": {"pattern": "03_operations
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "grep", "callID": "call_1VKhPmWFT2sTejv0RsnYqP9L", "state": {"status": "completed", "input": {"pattern": "magnesium|cit
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449aef70011bJMkmbe6qyU3N", "reason": "tool-calls", "snapshot": "a5cd155d9cdbae72d8e19ffe3939d6e8b07a17ae", "messageID": "msg_ee449
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44991e6001r2NUUzZA5mc0E5", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44991e6001r2NUUzZA5mc0E5", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee449b35a001E05kphQhxIjUB7", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449bb61001aLGOOMfltpoWuD", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "snapshot
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449bec40017432U8HzZ6d2Rb", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": "**Assessing requirements**\n\nI"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " see"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " produce"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " assessment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " seems"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " reading"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " some"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " benchmarks"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " good"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " first"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " step"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " I'm"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " thinking"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " about"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " what"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " specific"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " aspects"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " consider"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " while"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " doing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " assessment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " how"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " benchmarks"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " will"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " help"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " me"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " process"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " want"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " ensure"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " I'm"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " thorough"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " accurate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": "\u2019ll"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " take"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " my"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " time"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " gather"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": " proceeding"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449bec40017432U8HzZ6d2Rb", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449bec40017432U8HzZ6d2Rb", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449c5e1001TuicJafHSCM2JO", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " found"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " local"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " registry"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " notes"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " including"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " existing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "-par"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "adox"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " concerns"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " cited"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " PM"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "IDs"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "\u2019ll"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " cross"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "-check"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " primary"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "/public"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " where"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " possible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " writing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " requested"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " output"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " reviewer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " judgment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " rather"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " repo"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "-in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "ternal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": " change"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "partID": "prt_ee449c5e1001TuicJafHSCM2JO", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449c5e1001TuicJafHSCM2JO", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449cfdf001E3wa4rjH1fc9Sy", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "read", "callID": "call_NRei6Pia2ZsZlPh2SmO7fzOQ", "state": {"status": "running", "input": {"filePath": "C:\\Bari\\03_o
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449d018001ZkbEea0dhCdUGU", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "read", "callID": "call_NRei6Pia2ZsZlPh2SmO7fzOQ", "state": {"status": "completed", "input": {"filePath": "C:\\Bari\\03
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "read", "callID": "call_9VHeJcOV0a1f41sBbNcUVHVQ", "state": {"status": "running", "input": {"filePath": "C:\\Bari\\03_o
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449d0dd001whc40GeJOjzVXh", "messageID": "msg_ee449b35a001E05kphQhxIjUB7", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "read", "callID": "call_1sWLte15PLtLTAk8fZ1SOkIx", "state": {"status": "running", "input": {"filePath": "C:\\Bari\\03_o
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "read", "callID": "call_9VHeJcOV0a1f41sBbNcUVHVQ", "state": {"status": "completed", "input": {"filePath": "C:\\Bari\\03
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "read", "callID": "call_1sWLte15PLtLTAk8fZ1SOkIx", "state": {"status": "completed", "input": {"filePath": "C:\\Bari\\03
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449d5c7001UIkeHqlRE2Y0p9", "reason": "tool-calls", "snapshot": "a5cd155d9cdbae72d8e19ffe3939d6e8b07a17ae", "messageID": "msg_ee449
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee449b35a001E05kphQhxIjUB7", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee449b35a001E05kphQhxIjUB7", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee449da6c001UrE8bFBHWxEQqO", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449e4340018EqB5AAgp9ZbTD", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "snapshot
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449e653001rWiKxghguyzwvc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": "**Gathering citations**\n\nI"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " make"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " sure"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " have"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " right"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " web"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " citations"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " my"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " sounds"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " sources"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " NIH"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " maybe"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " even"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " Pub"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": "Med"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " pages"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " find"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " credible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " relevant"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " Using"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " these"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " well"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": "-known"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " resources"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " will"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " help"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " ensure"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " provide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " reliable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " just"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " ensure"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " I'm"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " checking"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " right"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " pages"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " accurate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": " citations"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449e653001rWiKxghguyzwvc", "field": "text", "delta": "!"}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449e653001rWiKxghguyzwvc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449ed59001aizQ6zvBGdkXmU", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "\u2019m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " going"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " treat"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "-author"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "ized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " regulatory"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " automatically"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " clinical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " proof"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " benefit"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " main"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "\u2019m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " seeing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " \u201c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "\u201d"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " metric"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "-per"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "-s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "he"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "kel"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " crown"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " even"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " when"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " likely"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " much"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " lower"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "-sol"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "ubil"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "ized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": " salts"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "partID": "prt_ee449ed59001aizQ6zvBGdkXmU", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449ed59001aizQ6zvBGdkXmU", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449faf6001q0EGr9eg79XEPo", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_2D15nPgE4taAXoHRElL0vT3Z", "state": {"status": "running", "input": {"url": "https://ods.od.
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449fb13001Al9lYWAganhCTQ", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_gyCOhtInuqcTUD0S23bdAHL7", "state": {"status": "running", "input": {"url": "https://pubmed.
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449fb3c001pRAroITzyCC61O", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_M1r2SkWPo8IIi4Ne1eJbwzrT", "state": {"status": "running", "input": {"url": "https://pubmed.
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449fb47001LaOYmEUH5JzIal", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_Yjdi5oo928KQMRubqmeQCNMz", "state": {"status": "running", "input": {"url": "https://pubmed.
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee449fb4f001ncsA1yl4ohWXmB", "messageID": "msg_ee449da6c001UrE8bFBHWxEQqO", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_gUDZD0lWxNKI4enboHnsTc98", "state": {"status": "running", "input": {"url": "https://pubmed.
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_M1r2SkWPo8IIi4Ne1eJbwzrT", "state": {"status": "completed", "input": {"url": "https://pubme
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_gyCOhtInuqcTUD0S23bdAHL7", "state": {"status": "completed", "input": {"url": "https://pubme
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_Yjdi5oo928KQMRubqmeQCNMz", "state": {"status": "completed", "input": {"url": "https://pubme
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_gUDZD0lWxNKI4enboHnsTc98", "state": {"status": "completed", "input": {"url": "https://pubme
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_2D15nPgE4taAXoHRElL0vT3Z", "state": {"status": "error", "input": {"url": "https://ods.od.ni
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a07190013zdDBS9bIW3m2A", "reason": "tool-calls", "snapshot": "a5cd155d9cdbae72d8e19ffe3939d6e8b07a17ae", "messageID": "msg_ee449
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee449da6c001UrE8bFBHWxEQqO", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee449da6c001UrE8bFBHWxEQqO", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a16d7001queHI9Kr83rIIo", "messageID": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "snapshot
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a1fdc001LvH3f2pUmeJxav", "messageID": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a1fdc001LvH3f2pUmeJxav", "messageID": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a307b001CHbjMJlaRCmAy9", "messageID": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_95Y369XPzcys91wtUbmcg0Lv", "state": {"status": "running", "input": {"url": "https://pubmed.
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a30890018MRVGYKpUGR7UF", "messageID": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_YTEyjsDGOIwGKC6xx95l85MP", "state": {"status": "running", "input": {"url": "https://pubmed.
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a3094001h6RLFykARe6vpc", "messageID": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_X8XOAEwahS6RTgAtyrVhVZaS", "state": {"status": "running", "input": {"url": "https://pubmed.
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a30bc0017Y2UwNUtUVVHRh", "messageID": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_PGXWrNRbHJnATgSRvCqd2FVN", "state": {"status": "running", "input": {"url": "https://efsa.on
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a30c6001gyEkZQoFf0mbX0", "messageID": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_l8ez3HUu1VrXkecpRzAhvY4O", "state": {"status": "running", "input": {"url": "https://www.efs
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_YTEyjsDGOIwGKC6xx95l85MP", "state": {"status": "completed", "input": {"url": "https://pubme
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_l8ez3HUu1VrXkecpRzAhvY4O", "state": {"status": "completed", "input": {"url": "https://www.e
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_PGXWrNRbHJnATgSRvCqd2FVN", "state": {"status": "error", "input": {"url": "https://efsa.onli
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_X8XOAEwahS6RTgAtyrVhVZaS", "state": {"status": "completed", "input": {"url": "https://pubme
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "webfetch", "callID": "call_95Y369XPzcys91wtUbmcg0Lv", "state": {"status": "completed", "input": {"url": "https://pubme
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a3925001Q2aX2p0DMPc0Yn", "reason": "tool-calls", "snapshot": "a5cd155d9cdbae72d8e19ffe3939d6e8b07a17ae", "messageID": "msg_ee44a
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44a0bb6001IAyqkkbkcR0kvY", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44a3d72001M7Z9h0tCcS3amS", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a4e1a0015Vi0nJRWHGv7wh", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "snapshot
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a51c9001c4QySq4uzwKLAr", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "**Ensuring directory existence**\n
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "\u2019m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " planning"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " apply"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "_patch"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " add"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " first"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " ensure"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " directory"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " exists"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " check"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " using"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " glob"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " see"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "\u2019s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " already"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " there"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "\u2019s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " important"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " run"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " into"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " errors"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " later"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "\u2019ll"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " double"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "-check"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " everything"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " set"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " up"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " correctly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " proceeding"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " This"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " little"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " step"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " save"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " me"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " headache"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " down"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " let"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "\u2019s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " make"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " sure"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " do"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": " right"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a51c9001c4QySq4uzwKLAr", "field": "text", "delta": "!"}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a51c9001c4QySq4uzwKLAr", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": "I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": "\u2019m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " writing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " assessment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " now"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " standalone"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " reviewer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " memo"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": "\u2019m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " changing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " any"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " logic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " using"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " OFF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": "-and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": "jud"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": "gment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "partID": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a66d0001uvb6J5XLR9T7Kn", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44a6706001hTQez7a2U874jG", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "apply_patch", "callID": "call_soiJvzIXdm1MWdRW1ry5iq8M", "state": {"status": "running", "input": {"patchText": "*** Be
  file.edited: {"file": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\benchmark\\magnesium_assumptions_c3_v1.md"}
  file.watcher.updated: {"file": "C:\\Bari\\03_operations\\supplement_engine\\proto_v0\\benchmark\\magnesium_assumptions_c3_v1.md", "event": "add"}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "apply_patch", "callID": "call_soiJvzIXdm1MWdRW1ry5iq8M", "state": {"status": "completed", "input": {"patchText": "*** 
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44ba7dc001pLIOSRs9tXviNc", "reason": "tool-calls", "snapshot": "221b30bc0bb78de79c022c484bbe67e546352ca2", "messageID": "msg_ee44a
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44a3d72001M7Z9h0tCcS3amS", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bb074001PRkxQJK1xpuLCn", "messageID": "msg_ee44a3d72001M7Z9h0tCcS3amS", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44a3d72001M7Z9h0tCcS3amS", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44bb097001h1fGRa5BVfJ9do", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bbbf6001g20ccthQnQB7wE", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "snapshot
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bc10600107Z4jwICtl7vLV", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " assessment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " file"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " written"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": "\u2019ll"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " verify"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " saved"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " content"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " returning"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " full"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " text"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": " here"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "partID": "prt_ee44bc10600107Z4jwICtl7vLV", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bc10600107Z4jwICtl7vLV", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bc38b001ABxzi7w6ZTG3P0", "messageID": "msg_ee44bb097001h1fGRa5BVfJ9do", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  todo.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "todos": [{"content": "Inspect magnesium benchmark context and existing assumptions", "status": "completed", "priority": "high"}, {"content": "Draft ind
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "todowrite", "callID": "call_ui07fZO2ppoq79NmEfVDYa8v", "state": {"status": "running", "input": {"todos": [{"content": 
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "todowrite", "callID": "call_ui07fZO2ppoq79NmEfVDYa8v", "state": {"status": "completed", "input": {"todos": [{"content"
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bce7f0019l5XKg2huJzMOO", "reason": "tool-calls", "snapshot": "221b30bc0bb78de79c022c484bbe67e546352ca2", "messageID": "msg_ee44b
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44bb097001h1fGRa5BVfJ9do", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44bb097001h1fGRa5BVfJ9do", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44bd2a9001JFJl6GTuTu6wSj", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bdb70001P0QfGsqw09sfay", "messageID": "msg_ee44bd2a9001JFJl6GTuTu6wSj", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "snapshot
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44be1a20015WV6SO2p91hd30", "messageID": "msg_ee44bd2a9001JFJl6GTuTu6wSj", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "read", "callID": "call_OQQY8SyCQeOks1FWKKcCs7Lx", "state": {"status": "running", "input": {"filePath": "C:\\Bari\\03_o
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "read", "callID": "call_OQQY8SyCQeOks1FWKKcCs7Lx", "state": {"status": "completed", "input": {"filePath": "C:\\Bari\\03
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bea9f001PyM6sjlh2TyXcd", "reason": "tool-calls", "snapshot": "221b30bc0bb78de79c022c484bbe67e546352ca2", "messageID": "msg_ee44b
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44bd2a9001JFJl6GTuTu6wSj", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44bd2a9001JFJl6GTuTu6wSj", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44beefe001QVkjM5XimFltlG", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bf899001x84FYEITEASEBZ", "messageID": "msg_ee44beefe001QVkjM5XimFltlG", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "snapshot
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bfc0b001HDXdm2sHCfHfMJ", "messageID": "msg_ee44beefe001QVkjM5XimFltlG", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bfc0b001HDXdm2sHCfHfMJ", "messageID": "msg_ee44beefe001QVkjM5XimFltlG", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44bfeb6001NBbCDjlcIrpIcI", "messageID": "msg_ee44beefe001QVkjM5XimFltlG", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  todo.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "todos": [{"content": "Inspect magnesium benchmark context and existing assumptions", "status": "completed", "priority": "high"}, {"content": "Draft ind
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "todowrite", "callID": "call_ZONpPrw5BGioCCheuZfJNU32", "state": {"status": "running", "input": {"todos": [{"content": 
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"type": "tool", "tool": "todowrite", "callID": "call_ZONpPrw5BGioCCheuZfJNU32", "state": {"status": "completed", "input": {"todos": [{"content"
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44c089d001LloS73JYH4Dnqr", "reason": "tool-calls", "snapshot": "221b30bc0bb78de79c022c484bbe67e546352ca2", "messageID": "msg_ee44b
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44beefe001QVkjM5XimFltlG", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44beefe001QVkjM5XimFltlG", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44c0cfc001sz7ws4RPYyoVda", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44c16c3001BiG64RzqjvANNm", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "snapshot
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44c199c001AE5lijZkWxciSj", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "#"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Independent"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Review"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Comparison"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Ass"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "um"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ptions"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Role"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " outside"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-family"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " reviewer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Scope"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " challenge"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assumptions"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plain"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " English"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " No"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " changes"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " No"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " data"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " invention"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " No"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Open"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Food"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Facts"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Bottom"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " line"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " honest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " stops"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " implying"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "more"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " equals"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " delivered"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " body"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " practical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " starting"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " point"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-facing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " language"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " must"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " repeatedly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " say"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-based"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " comparison"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " adjusted"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " where"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " allows"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " lab"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "verified"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ranking"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " what"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Verd"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ict"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " SH"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "AK"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Y"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " usable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " framed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " carefully"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labels"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " normally"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " state"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " compound"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " amount"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " observable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " comparable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " aud"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "itable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Actual"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " directly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " observable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " package"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " varies"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " size"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " stomach"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " acidity"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " food"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " baseline"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " status"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " gut"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " disease"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " probably"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " individual"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " need"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " So"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cannot"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " honestly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " calculate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " exact"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " amount"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " each"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " buyer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "But"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " stopping"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dangerous"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " show"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " very"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " number"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-d"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ense"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " weight"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " yet"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " poorly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " soluble"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " often"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " less"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bio"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "available"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " organic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " salts"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Human"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " comparative"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " work"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supports"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " broad"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " direction"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " generally"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " worse"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " che"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "lated"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "organic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " forms"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " One"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cited"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " trial"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ile"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "al"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-re"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "section"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " patients"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " compared"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dig"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " found"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " similar"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " average"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " whole"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " small"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " group"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " toler"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ability"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dig"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " subgroup"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " poorest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clean"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " general"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-pop"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ulation"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ranking"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " study"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Sch"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "u"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ette"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "199"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "781"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "567"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ")."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " local"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " registry"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cites"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " human"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bio"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "availability"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " below"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/g"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " total"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " base"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " large"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " perfectly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consistent"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Jud"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-based"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " honest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " presented"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "decl"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ared"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ",\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "what"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " your"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " body"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " gets"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " says"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " implies"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benefit"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "What"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " change"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " keep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " primary"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " aud"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "itable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " number"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rename"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clearly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-de"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "clared"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Add"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " second"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " note"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " beside"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " other"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " low"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-sol"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ub"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ility"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " forms"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "High"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mean"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Do"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " exact"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mill"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "igrams"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labels"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rough"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " illustration"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " most"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " she"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "kel"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Verd"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ict"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " WRONG"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " shown"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " main"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " result"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " SH"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "AK"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Y"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " shown"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " narrow"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " she"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "kel"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " metric"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assumption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " most"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "leading"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " look"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " excellent"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mill"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "igrams"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " she"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "kel"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cheap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-d"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ense"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " But"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " most"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " likely"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " disappoint"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " thinks"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " they"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " buying"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorb"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "able"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Some"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " studies"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " reviews"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cite"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " very"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " low"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fractional"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sometimes"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "%,"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " while"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " other"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " soluble"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "organic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " salts"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " often"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " perform"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " exact"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " percent"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " stable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " across"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " studies"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " populations"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " methods"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " direction"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consistent"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " enough"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " poor"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-b"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "io"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "availability"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " compared"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " many"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " che"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "lates"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-mag"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "nesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " picture"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plain"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " English"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Ox"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " lots"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " printed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cheap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " relatively"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " poorly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " likely"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " act"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " osm"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "otic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " lax"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ative"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " higher"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " doses"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Citr"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " usually"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dissolved"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supported"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " direct"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " human"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " comparison"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " loosen"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " stools"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Gly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/b"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " marketed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " gentle"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " often"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plausible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-t"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "oler"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ated"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " option"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " human"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " head"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-head"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " versus"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " thinner"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " marketing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " suggests"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " simple"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " example"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " shows"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " trap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " gives"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "300"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " small"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fraction"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " while"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " another"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " gives"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "150"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/g"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " meaning"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "fully"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " higher"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cheaper"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " physiological"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " precise"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " numbers"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " uncertain"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " wins"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " high"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " logic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " robust"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Jud"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "element"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "al"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " she"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "kel"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " price"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-density"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " metric"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " metric"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Calling"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cave"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "at"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " invites"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " journalist"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " say"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Your"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " top"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " pick"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " many"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sources"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " call"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " least"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " criticism"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fair"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "What"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " change"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rename"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " metric"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "che"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "apest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "lowest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cost"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labeled"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Create"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " separate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "pr"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "actical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " badge"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " requires"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " both"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " adequate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " acceptable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Ox"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " called"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cheap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " crowned"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " text"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " says"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mill"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "igrams"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " likely"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\"\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Citr"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ranked"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " above"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " glyc"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/b"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Verd"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ict"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " SOUND"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " narrow"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-ranking"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sense"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "conf"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ident"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " phr"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ased"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clearly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " biolog"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ically"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " superior"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " direct"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " human"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " comparative"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " glyc"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " general"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bio"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "availability"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " especially"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " compared"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Gly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/b"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plausible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mechanisms"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " toler"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ability"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " story"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " there"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " some"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " human"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " much"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-market"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " certainty"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " stronger"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clinical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " important"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nuance"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cited"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dig"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-v"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " trial"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " was"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "12"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " patients"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ile"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "al"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " re"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "section"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " healthy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumers"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " did"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " show"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clean"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " whole"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-group"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " superiority"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dig"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " though"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " did"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " show"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " advantages"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " subgroup"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " poor"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " toler"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ability"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "PM"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "781"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "567"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ")."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supports"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/g"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ent"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "le"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ",\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " proven"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " champion"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " For"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " direct"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " comparative"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " against"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " straightforward"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " many"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " summaries"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " avoid"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sounding"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " certain"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " about"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " exact"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " superiority"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " over"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " glyc"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Jud"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fair"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rank"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " above"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " glyc"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " criterion"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "strong"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "er"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " direct"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " human"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " comparative"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fair"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " imply"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " definitely"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " every"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " person"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " glyc"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mostly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " marketing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fluff"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Gly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " may"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " very"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " reasonable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " choice"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " especially"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " toler"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ability"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "What"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " change"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " write"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "C"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "itrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cleaner"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " direct"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " base"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " glyc"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/b"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " toler"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ability"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-forward"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " alternative"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " We"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " do"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " treat"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " glyc"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " proven"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " superior"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " citrate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fair"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Minimum"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " effective"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " thresholds"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " general"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " migraine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " below"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "50"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " treated"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ineffective"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Verd"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ict"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " SH"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "AK"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Y"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mostly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " practical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " thresholds"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " hard"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " biological"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cut"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "offs"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/day"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " general"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplementation"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " reasonable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " gap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-cl"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "osing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " number"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clinical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " treatment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Adult"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " requirements"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " usually"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " discussed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " total"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " daily"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " intake"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " food"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plus"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplements"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-only"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " intake"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " help"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " close"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dietary"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " gap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " some"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " people"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " minimum"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "For"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " blood"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " pressure"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " stronger"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " R"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "CT"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/meta"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-analysis"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clusters"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " higher"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " doses"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "201"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " meta"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-analysis"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "34"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " randomized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " double"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-bl"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ind"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " placebo"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-controlled"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " trials"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " found"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " median"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "368"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/day"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " months"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " suggested"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "300"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/day"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " was"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " enough"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " raise"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " serum"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " modest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " lower"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " blood"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " pressure"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " by"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " about"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mm"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Hg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " syst"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "olic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "8"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mm"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Hg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " di"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ast"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "olic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Z"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "hang"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "201"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "274"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "029"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "22"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ")."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supports"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "300"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-ish"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " blood"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-pressure"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "For"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " pragmatic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " low"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bar"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " proven"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "202"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " systematic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " review"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/meta"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-analysis"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " older"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " adults"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " found"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " three"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " R"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "CT"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "151"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " participants"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " moderate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-high"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bias"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " low"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " very"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-low"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " quality"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " onset"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " latency"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " improved"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " pooled"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " analysis"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " authors"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " explicitly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " said"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " literature"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sub"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "standard"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " confident"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " recommendations"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Mah"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "202"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "338"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "653"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "76"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ")."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " So"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " judgment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " call"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "For"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " migraine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/day"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " lower"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-end"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clinical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Mig"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "raine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " reviews"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " headache"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " practice"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " commonly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " discuss"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oral"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "600"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/day"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " range"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " though"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " trials"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mixed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " some"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " authors"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " argue"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " broad"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " while"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " others"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cautious"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " example"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Ma"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "usk"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "op"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "201"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "224"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "268"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "36"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Sun"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-E"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "del"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "stein"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "192"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "719"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ")."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " So"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " minimum"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " migraine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-specific"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " treated"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " universal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "below"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "50"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ineffective"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rule"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " weakest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " part"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Biology"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rarely"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cliff"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "50"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "%."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "49"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " threshold"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " categor"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ically"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " different"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "51"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "%."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " But"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " scoring"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rule"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " reasonable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " say"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " delivers"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " less"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " half"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "'s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " own"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " minimum"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " its"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " own"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " promise"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " well"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Jud"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " thresholds"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " acceptable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " practical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benchmarks"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labeled"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " minimum"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ",\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " proven"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cut"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "offs"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "50"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rule"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " policy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " choice"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " science"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "What"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " change"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " show"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " thresholds"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bands"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " general"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " gap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " support"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " weak"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " migraine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "400"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "600"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " moderate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Replace"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ffective"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "unlikely"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " deliver"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " promised"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labeled"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "far"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " below"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " our"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\"\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labels"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " often"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " wrong"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " what"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-based"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " worth"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "?\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Verd"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ict"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " SOUND"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " limitation"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dangerous"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " hidden"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cites"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assay"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " finding"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "58"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EU"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplements"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " outside"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " legal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " tolerance"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " actual"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " content"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ranging"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " far"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " below"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " far"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " above"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " discrepancy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " independent"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " price"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " did"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " independently"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " verify"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " exact"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assay"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " paper"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " pass"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cite"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " full"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bibli"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ographic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " details"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " before"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " publication"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " But"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " general"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " point"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " highly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plausible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labels"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " lab"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assays"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " price"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " guarantee"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " content"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " accuracy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Jud"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-based"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " worth"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " something"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumers"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " buy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labels"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assess"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " whether"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " even"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " provide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " meaningful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " names"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " stays"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " safety"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ceilings"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " avoids"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unsupported"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " But"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cannot"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " prove"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " what"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " inside"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bottle"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " honest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " framing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "This"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-case"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " comparison"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " truthful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\"\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "What"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " change"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " put"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " visible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cave"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "at"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " near"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " buried"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " methodology"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "We"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " do"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " lab"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-test"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Scores"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assume"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " accurate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Independent"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assays"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " have"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " found"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " many"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplements"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " miss"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " their"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " amounts"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-quality"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " purity"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " guarantee"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "58"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "%"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " statistic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " used"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cite"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " exact"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " study"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " title"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " journal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " year"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assay"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " method"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " legal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " tolerance"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " definition"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " tiers"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " energy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/f"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "at"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "igue"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " immune"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-author"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " migraine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " moderate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cramps"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " weak"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ins"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ufficient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Verd"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ict"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " MIX"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ED"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Mig"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "raine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " moderate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sound"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " weak"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sound"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ram"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ps"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " insufficient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sound"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Energy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/f"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "at"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "igue"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " immune"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "strong"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-author"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " SH"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "AK"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Y"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " WRONG"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " depending"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " wording"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-author"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " health"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " important"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " They"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mean"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " regulatory"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " authority"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " accepted"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cause"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-effect"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " relationship"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nutrient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " specified"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " conditions"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " For"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " authorized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " such"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " contribution"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " normal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " energy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-y"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ield"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " metabolism"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " reduction"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " tired"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ness"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fatigue"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " electrolyte"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " balance"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " normal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " muscle"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " normal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nervous"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " system"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " maintenance"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " normal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bones"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "te"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "eth"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supports"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " compliance"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " biological"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plaus"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ibility"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "But"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " authorization"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " same"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clinical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " re"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "plete"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " adult"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " taking"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " will"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " feel"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " energy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " improve"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " immunity"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " perform"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Nutr"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " often"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mean"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "mag"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "nesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " necessary"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " normal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " body"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ",\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "extra"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " improves"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " outcome"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " everyone"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " distinction"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " matters"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " lot"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " trust"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Imm"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "une"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " especially"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " suspect"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " roles"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " normal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " physiology"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " broad"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "immune"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " support"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " often"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " vague"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " equivalent"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " proven"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " reduction"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " infections"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " better"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " immune"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " outcomes"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ordinary"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumers"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " treats"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " immune"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " strong"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " simply"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-style"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nutrient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " logic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " downgrade"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " heavily"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " qualify"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Mig"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "raine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " moderate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " reasonable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " there"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mechan"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "istic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plaus"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ibility"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " common"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " guideline"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/pr"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "actice"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " use"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " some"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " trial"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/re"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "view"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " support"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mixed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " slam"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dunk"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " weak"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " right"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " given"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " small"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " biased"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " base"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "PM"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "338"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "653"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "76"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ")."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ram"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ps"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " insufficient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "weak"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " right"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " especially"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ordinary"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " noct"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "urnal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " leg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cramps"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " older"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " adults"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "202"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Co"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "chr"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ane"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " review"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " concluded"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unlikely"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " provide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clinically"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " meaningful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cr"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "amp"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " prophyl"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "axis"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " older"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " adults"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " skeletal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " muscle"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cramps"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ("}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "PM"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "329"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "565"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "36"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ").\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Jud"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " separate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "authorized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nutrient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "pro"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ven"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benefit"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " regulatory"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " floor"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " permitted"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " wording"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " stamp"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " real"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-world"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " efficacy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "What"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " change"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " classify"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nutrient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "authorized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "phys"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "i"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ological"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rather"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " than"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "strong"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " there"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " direct"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplementation"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " outcome"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Use"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plain"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labels"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Authorized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " normal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " versus"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Clinical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " outcome"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Dow"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ng"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "rade"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " broad"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " immune"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " support"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " specific"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cited"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clinical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " endpoint"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " shown"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "7"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Hard"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ceilings"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-low"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " caps"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "49"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unsupported"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " caps"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "34"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "100"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Verd"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ict"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " SOUND"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-pro"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "tection"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " policy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " blunt"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " every"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "d"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "osed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " gets"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " same"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " does"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " provide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " enough"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " its"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " own"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " get"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " good"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " just"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " uses"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nice"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " clean"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " marketing"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " making"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " an"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unsupported"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " capped"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " even"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " harder"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-pro"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "tection"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " design"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "But"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " flat"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " low"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " erase"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "140"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " equally"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " weak"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " even"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " if"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " both"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " below"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " local"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " recal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ibration"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " notes"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " already"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " identify"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " problem"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " single"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "49"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " pin"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " collaps"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "es"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " very"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " different"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " under"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "d"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "osed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " into"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bucket"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " science"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " problem"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " communication"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/sc"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "oring"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-resolution"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " problem"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unsupported"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " around"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "34"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " defens"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " If"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "'s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " main"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " promise"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supported"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " more"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rescue"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " score"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " changes"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " being"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assessed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Otherwise"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " product"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " could"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " make"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nonsense"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " sleep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/st"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ress"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/l"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ip"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "osome"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " still"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " look"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " acceptable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " has"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " lot"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Jud"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "gment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " hard"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ceilings"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " are"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " reasonable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " low"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ceiling"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " graded"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Unsupported"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " remain"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " hard"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " E"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-style"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "What"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " change"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " keep"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " hard"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unsupported"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Replace"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " flat"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " too"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-low"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " graded"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "far"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " below"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " band"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " so"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumers"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " can"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " see"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " difference"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " between"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " tiny"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " almost"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "adequ"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " products"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Use"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " words"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " like"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "below"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " instead"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ffective"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " unless"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " truly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supports"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " no"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " effect"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assumption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " most"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " likely"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " embarr"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ass"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " project"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " biggest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " embarrassment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assumption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ="}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " most"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " she"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "kel"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\"\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Why"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " it"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " lets"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cheap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " win"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " while"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " itself"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " knows"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " poorly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorbed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " journalist"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " or"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " scientist"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " could"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fairly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " say"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Your"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " recommendation"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " rewards"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " least"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " bio"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "available"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " because"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " you"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " counted"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " attack"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " easy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " understand"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " easy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " quote"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " damaging"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " trust"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Ass"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "umption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " second"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " risk"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " treating"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-author"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nutrient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claims"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " as"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "strong"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " evidence"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benefit"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " scientist"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " could"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " say"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " authorization"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " means"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nutrient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " needed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " normal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " this"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " improves"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " outcome"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " non"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-def"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "icient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " people"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " That"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " criticism"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fair"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " The"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " I"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " would"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " prioritize"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Fix"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " language"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " first"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Do"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " call"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " without"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " qualification"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Split"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " metric"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " into"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " two"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labels"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Che"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "apest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " labeled"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " price"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " per"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " declared"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " elemental"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " mg"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " \""}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Best"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " practical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " value"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " adequate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dose"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plus"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " acceptable"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " form"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plus"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " support"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " visible"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " warning"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " that"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " absorption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " estimated"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " only"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " qualit"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "atively"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "This"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " one"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " change"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " protects"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " project"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " from"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " most"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " obvious"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " attack"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " while"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " preserving"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " price"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " information"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " It"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " also"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " makes"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " page"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " easier"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " normal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumer"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " understand"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cheap"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " label"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " is"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " always"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " good"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Short"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " source"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " notes"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Sch"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "u"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ette"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Lash"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ner"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " BA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " J"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ang"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "hor"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "b"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ani"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " M"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Bio"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "availability"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " dig"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ly"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "inate"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " vs"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " oxide"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " patients"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " ile"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "al"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " re"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "section"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " JP"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "EN"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "199"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "4"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "781"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "567"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "5"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Zhang"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " X"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " et"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " al"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Effects"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ation"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " on"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Blood"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Pressure"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Meta"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Analysis"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Random"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ized"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Double"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-Bl"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ind"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Place"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "bo"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-Control"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "led"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Trials"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Hy"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "pertension"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "201"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "6"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "274"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "029"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "22"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Mah"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " J"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " P"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "itre"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " T"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Oral"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplementation"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " insomnia"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " older"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " adults"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " a"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " systematic"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " review"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " meta"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-analysis"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " B"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "MC"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Complement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Med"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Ther"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "202"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "338"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "653"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "76"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " G"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "arrison"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " SR"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " et"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " al"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " skeletal"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " muscle"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " cramps"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Co"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "chr"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ane"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Database"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " S"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "yst"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Rev"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "202"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " update"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "329"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "565"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "36"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Ma"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "usk"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "op"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Var"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ugh"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ese"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " J"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Why"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " all"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " migraine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " patients"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " should"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " be"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " treated"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " with"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " J"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Neural"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Trans"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "201"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "2"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "224"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "268"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "36"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Note"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " opinion"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ated"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " review"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ";"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " definitive"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Sun"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-E"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "del"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "stein"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " C"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Ma"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "usk"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "op"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " A"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Role"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " path"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ogenesis"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " treatment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " migraine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Expert"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Rev"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Neuro"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ther"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "200"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "9"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " PMID"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "192"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "719"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "46"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " EF"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "SA"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " magnesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " Article"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " "}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "13"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " health"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "claim"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " opinions"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/register"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " useful"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " for"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " permitted"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " nutrient"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-function"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " wording"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ","}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " but"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " not"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " identical"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " direct"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " proof"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " supplement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benefit"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " in"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " already"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-re"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "plete"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " consumers"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "##"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " RETURN"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ED"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Changed"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " file"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "03"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_operations"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "upp"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "lement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_engine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/pro"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_v"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ag"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "nesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_ass"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "um"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ptions"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_v"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".md"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "`:"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " full"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " independent"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " plain"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-English"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " review"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " of"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " seven"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assumptions"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "Verify"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":\n\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "03"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_operations"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "upp"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "lement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_engine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/pro"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_v"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ag"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "nesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_ass"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "um"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ptions"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_v"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".md"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " confirms"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " output"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " exists"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " at"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " requested"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " path"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "03"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_operations"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "upp"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "lement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_engine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/pro"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_v"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ag"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "nesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_ass"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "um"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ptions"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_v"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".md"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "20"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " starts"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assumption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-by"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-ass"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "umption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " review"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".\n"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " `"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "03"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_operations"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/s"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "upp"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "lement"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_engine"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/pro"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "to"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_v"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "0"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "benchmark"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "/m"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ag"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "nesium"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_ass"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "um"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "ptions"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_c"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "3"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "_v"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "1"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ".md"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": ":"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "130"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "`"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " identifies"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " the"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " highest"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " embarrassment"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "-risk"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " assumption"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " and"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " priority"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": " fix"}
  message.part.delta: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "partID": "prt_ee44c199c001AE5lijZkWxciSj", "field": "text", "delta": "."}
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44c199c001AE5lijZkWxciSj", "messageID": "msg_ee44c0cfc001sz7ws4RPYyoVda", "sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "type": "
  message.part.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "part": {"id": "prt_ee44d2d6a001OzRKcGxYZbPwn2", "reason": "stop", "snapshot": "221b30bc0bb78de79c022c484bbe67e546352ca2", "messageID": "msg_ee44c0cfc00
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44c0cfc001sz7ws4RPYyoVda", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "msg_ee44c0cfc001sz7ws4RPYyoVda", "parentID": "msg_ee44963b2001W7kANzsKC6dxgp", "role": "assistant", "mode": "build", "agent": "build", "
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "busy"}}
  session.status: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "status": {"type": "idle"}}
  session.idle: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc"}
  session.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"id": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "slug": "swift-rocket", "projectID": "e7f90f8a5abbaca924c7d1983e3ba702c9bbf643", "directory": "C:\\Bari
  session.diff: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "diff": []}
  message.updated: {"sessionID": "ses_11bb6a19fffeZ2Nb8X9OGWOhhc", "info": {"role": "user", "time": {"created": 1781946475442}, "agent": "build", "model": {"providerID": "openai", "modelID": "gpt-5.5"}, "summary": {"dif
```

---

## CHANGED-FILES (git status delta)

### Before dispatch

```
M 02_products/supplements/real_corpus_v3/run_full.py
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984003101.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984005181.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984010642.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020573.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020580.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984037250.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-712179581913.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065594.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065662.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001066973.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001186237.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001471845.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943212.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943700.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437273.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437563.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290008111041.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010035984.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010207640.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010318230.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899127.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899967.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012056741.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497643.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497650.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760204.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760266.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760761.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760853.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760891.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142146.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142894.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464248.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464897.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013465535.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318426.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318433.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318532.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429177.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429245.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429290.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765572.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765985.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417197.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417227.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218328.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218366.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218526.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218564.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218809.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017242170.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243368.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243450.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017399638.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017490601.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017847122.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365243.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365359.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439043.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439579.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439623.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444183.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444206.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444312.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444374.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444480.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019918011.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449414.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449421.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290109317199.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290111594342.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113826052.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113828728.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290114965279.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290115971873.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118814061.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118816065.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118818205.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-783495578741.json
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/iron.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/zinc.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md
 M 03_operations/supplement_engine/proto_v0/golden_corpus/fixtures.py
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-dangerous-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-noevidence-creatine-fatloss_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-wasted-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-FAIL-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-PASS-creatine-5g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-FAIL-omega3-brain_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-PASS-omega3-tg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-FAIL-mg-oxide_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-PASS-mg-glycinate_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-FAIL-caffeine-blend_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-PASS-caffeine-200_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R1-vague-evidenced-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R2-vague-snakeoil_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R3-overspecific-false-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-CTRL-d3-50k-weekly_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-FAIL-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-PASS-d3-2000_trace.json
 M 03_operations/supplement_engine/proto_v0/run_golden_validation.py
 M 03_operations/supplement_engine/proto_v0/src/constants.py
 M 03_operations/supplement_engine/proto_v0/src/dossier_loader.py
 M 03_operations/supplement_engine/proto_v0/src/score_engine.py
 M bari-web/next.config.ts
 M tasks/DISPATCH_BOARD.md
 M tasks/TASK-356.md
?? 02_products/snack_bars/_build_return_contract.py
?? 02_products/snack_bars/_check_borderlines.py
?? 02_products/snack_bars/_check_v5.py
?? 02_products/snack_bars/_verify_v5.py
?? 02_products/snack_bars/bsip2_outputs/run_snacks_task360_phase3_20260620_083413/
?? 02_products/snack_bars/bsip2_outputs/run_snacks_task360_phase3_20260620_083413_fix/
?? 02_products/snack_bars/fix_phase3_frontend.py
?? 02_products/snack_bars/observations_bsip0/shufersal/run_snacks_task360_phase3_20260620_083413/
?? 02_products/snack_bars/phase3_fix_summary_20260620_110619.json
?? 02_products/snack_bars/run_task360_phase3.py
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v4.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v5.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v6.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v7.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v9.json
?? 02_products/supplements/real_corpus_v3/_qa_report.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_nutrition_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_redteam_v1.md
?? 02_products/supplements/real_corpus_v3/qa_audit.py
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v2.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_value_framing_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v6.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v7.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v8.md
?? 03_operations/bsip1/run_snacks_task360_phase3_20260620_083413/
?? 03_operations/shadow/goldset/
?? 03_operations/supplement_engine/proto_v0/benchmark/
?? 03_operations/supplement_engine/proto_v0/golden_corpus/traces/RT7-H1-elemental-form-none-overdose_trace.json
?? 03_operations/supplement_engine/proto_v0/magnesium_benchmark_recalibration_proposal.md
?? _devserver.log
?? _tmp_hc_fields.py
?? _tmp_hc_orig.py
?? _tmp_mg_audit.py
?? _tmp_mg_audit2.py
?? _tmp_mg_audit3.py
?? _tmp_mg_audit4.py
?? _tmp_mg_audit5.py
?? _tmp_mg_audit6.py
?? _tmp_score_review.py
?? _tmp_snack_orig.py
?? _tmp_snack_review.py
?? _tmp_tink_detail.py
?? _tmp_v8_analysis.py
?? _tmp_v8_check.py
?? _tmp_v8_zinc.py
?? affected_set_spine.json
?? bari-web/src/app/hashvaot/magnesium/
?? bari-web/src/components/comparisons/magnesium-comparison-page.tsx
?? bari-web/src/data/comparisons/bread_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/bread_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cereals_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cheese_frontend_v4_gates_report.md
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/hard_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/hummus_frontend_v5_gates_report.md
?? bari-web/src/data/comparisons/juices_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/milk_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v3_STAGING.json
?? bari-web/src/data/comparisons/snacks_frontend_v3_STAGING_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v5.json
?? bari-web/src/lib/comparisons/magnesium-page-data.ts
?? dev_server_log.txt
?? integrations/clients/lnhpd.py
?? integrations/clients/tga.py
?? "research/Magnesium Oral Supplements Worldwide Benchmark.pdf"
?? tasks/TASK-349.md
?? tasks/TASK-357.md
?? tasks/TASK-358.md
?? tasks/TASK-359.md
?? tasks/TASK-361.md
?? tasks/TASK-361A.md
?? tasks/prompts/P233_c2_goldset_candidate_extract.md
?? tasks/prompts/P234_c3_goldset_methodology_redteam.md
?? tasks/prompts/P235_c1_nutrition_goldset_phase0.md
?? tasks/prompts/P236_c1cursor_goldcheck_harness.md
?? tasks/prompts/P237_c1grok_goldset_seed_encode.md
?? tasks/prompts/P238_c1gemini_goldset_schema_validator_ci.md
?? tasks/prompts/P239_c2_sie_sa_traceability_audit.md
?? tasks/prompts/P240_c3_sie_broaden_sources_research.md
?? tasks/prompts/P241_c2_magnesium_elemental_arithmetic_check.md
?? tasks/prompts/P242_c3_magnesium_benchmark_philosophy_redteam.md
?? tasks/prompts/P243_c2_magnesium_delivery_arithmetic_recheck.md
?? tasks/prompts/P244_c3_eu_magnesium_shelf_hunt.md
?? tasks/prompts/P245_c3_zinc_worldwide_benchmark.md
?? tasks/prompts/P246_c3_magnesium_assumptions_challenge.md
?? tasks/returns/P233_return.md
?? tasks/returns/P234_return.md
?? tasks/returns/P239_return.md
?? tasks/returns/P240_return.md
?? tasks/returns/P241_return.md
?? tasks/returns/P242_return.md
?? tasks/returns/P243_return.md
?? tasks/returns/P244_return.md
?? tasks/returns/P245_return.md
?? tasks/returns/P258_voice_redteam.md
?? tasks/returns/P261_hc_voice_redteam.md
?? tasks/returns/P265_snacks_v3_voice_redteam.md
?? test_acceptance.py
```

### After dispatch

```
M 02_products/supplements/real_corpus_v3/run_full.py
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984003101.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984005181.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984010642.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020573.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984020580.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-0033984037250.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-712179581913.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065594.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001065662.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001066973.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001186237.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001471845.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943212.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290001943700.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437273.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290006437563.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290008111041.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010035984.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010207640.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290010318230.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899127.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290011899967.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012056741.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497643.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012497650.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760204.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760266.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760761.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760853.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290012760891.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142146.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013142894.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464248.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013464897.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290013465535.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318426.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318433.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015318532.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429177.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429245.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015429290.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765572.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290015765985.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417197.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290016417227.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218328.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218366.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218526.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218564.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017218809.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017242170.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243368.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017243450.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017399638.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017490601.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290017847122.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365243.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018365359.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439043.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439579.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290018439623.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444183.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444206.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444312.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444374.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019444480.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290019918011.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449414.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290103449421.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290109317199.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290111594342.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113826052.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290113828728.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290114965279.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290115971873.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118814061.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118816065.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-7290118818205.json
 M 02_products/supplements/real_corpus_v3/skus_full/SP-783495578741.json
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/iron.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/magnesium.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_dossiers/zinc.yaml
 M 03_operations/supplement_engine/proto_v0/evidence_registry/supp_evidence_registry_v1.md
 M 03_operations/supplement_engine/proto_v0/golden_corpus/fixtures.py
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-dangerous-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-noevidence-creatine-fatloss_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/ARCH-wasted-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-FAIL-creatine-1g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/DOSE-PASS-creatine-5g_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-FAIL-omega3-brain_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/EV-PASS-omega3-tg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-FAIL-mg-oxide_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/FORM-PASS-mg-glycinate_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-FAIL-caffeine-blend_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/HON-PASS-caffeine-200_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R1-vague-evidenced-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R2-vague-snakeoil_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/R3-overspecific-false-mg_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-CTRL-d3-50k-weekly_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-FAIL-d3-50k_trace.json
 M 03_operations/supplement_engine/proto_v0/golden_corpus/traces/SAFE-PASS-d3-2000_trace.json
 M 03_operations/supplement_engine/proto_v0/run_golden_validation.py
 M 03_operations/supplement_engine/proto_v0/src/constants.py
 M 03_operations/supplement_engine/proto_v0/src/dossier_loader.py
 M 03_operations/supplement_engine/proto_v0/src/score_engine.py
 M bari-web/next.config.ts
 M tasks/DISPATCH_BOARD.md
 M tasks/TASK-356.md
?? 02_products/snack_bars/_build_return_contract.py
?? 02_products/snack_bars/_check_borderlines.py
?? 02_products/snack_bars/_check_v5.py
?? 02_products/snack_bars/_verify_v5.py
?? 02_products/snack_bars/bsip2_outputs/run_snacks_task360_phase3_20260620_083413/
?? 02_products/snack_bars/bsip2_outputs/run_snacks_task360_phase3_20260620_083413_fix/
?? 02_products/snack_bars/fix_phase3_frontend.py
?? 02_products/snack_bars/observations_bsip0/shufersal/run_snacks_task360_phase3_20260620_083413/
?? 02_products/snack_bars/phase3_fix_summary_20260620_110619.json
?? 02_products/snack_bars/phase3_fix_summary_20260620_110807.json
?? 02_products/snack_bars/run_task360_phase3.py
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v4.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v5.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v6.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v7.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v8.json
?? 02_products/supplements/real_corpus_v3/_corpus_run_full_v9.json
?? 02_products/supplements/real_corpus_v3/_qa_report.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_nutrition_v1.md
?? 02_products/supplements/real_corpus_v3/magnesium_assumptions_redteam_v1.md
?? 02_products/supplements/real_corpus_v3/qa_audit.py
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_page_v2.md
?? 02_products/supplements/real_corpus_v3/red_team_magnesium_value_framing_v1.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v3.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v6.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v7.md
?? 02_products/supplements/real_corpus_v3/red_team_sie_v8.md
?? 03_operations/bsip1/run_snacks_task360_phase3_20260620_083413/
?? 03_operations/shadow/goldset/
?? 03_operations/supplement_engine/proto_v0/benchmark/
?? 03_operations/supplement_engine/proto_v0/golden_corpus/traces/RT7-H1-elemental-form-none-overdose_trace.json
?? 03_operations/supplement_engine/proto_v0/magnesium_benchmark_recalibration_proposal.md
?? _devserver.log
?? _tmp_hc_fields.py
?? _tmp_hc_orig.py
?? _tmp_mg_audit.py
?? _tmp_mg_audit2.py
?? _tmp_mg_audit3.py
?? _tmp_mg_audit4.py
?? _tmp_mg_audit5.py
?? _tmp_mg_audit6.py
?? _tmp_score_review.py
?? _tmp_snack_orig.py
?? _tmp_snack_review.py
?? _tmp_tink_detail.py
?? _tmp_v8_analysis.py
?? _tmp_v8_check.py
?? _tmp_v8_zinc.py
?? affected_set_spine.json
?? bari-web/src/app/hashvaot/magnesium/
?? bari-web/src/components/comparisons/magnesium-comparison-page.tsx
?? bari-web/src/data/comparisons/bread_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/bread_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/brined_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cakes_hard_cookies_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/cereals_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/cheese_frontend_v4_gates_report.md
?? bari-web/src/data/comparisons/cookies_coffee_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/granola_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/hard_cheeses_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/hummus_frontend_v5_gates_report.md
?? bari-web/src/data/comparisons/juices_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/milk_frontend_v1_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v2_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v3_STAGING.json
?? bari-web/src/data/comparisons/snacks_frontend_v3_STAGING_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v3_gates_report.md
?? bari-web/src/data/comparisons/snacks_frontend_v5.json
?? bari-web/src/lib/comparisons/magnesium-page-data.ts
?? dev_server_log.txt
?? integrations/clients/lnhpd.py
?? integrations/clients/tga.py
?? "research/Magnesium Oral Supplements Worldwide Benchmark.pdf"
?? tasks/TASK-349.md
?? tasks/TASK-357.md
?? tasks/TASK-358.md
?? tasks/TASK-359.md
?? tasks/TASK-361.md
?? tasks/TASK-361A.md
?? tasks/prompts/P233_c2_goldset_candidate_extract.md
?? tasks/prompts/P234_c3_goldset_methodology_redteam.md
?? tasks/prompts/P235_c1_nutrition_goldset_phase0.md
?? tasks/prompts/P236_c1cursor_goldcheck_harness.md
?? tasks/prompts/P237_c1grok_goldset_seed_encode.md
?? tasks/prompts/P238_c1gemini_goldset_schema_validator_ci.md
?? tasks/prompts/P239_c2_sie_sa_traceability_audit.md
?? tasks/prompts/P240_c3_sie_broaden_sources_research.md
?? tasks/prompts/P241_c2_magnesium_elemental_arithmetic_check.md
?? tasks/prompts/P242_c3_magnesium_benchmark_philosophy_redteam.md
?? tasks/prompts/P243_c2_magnesium_delivery_arithmetic_recheck.md
?? tasks/prompts/P244_c3_eu_magnesium_shelf_hunt.md
?? tasks/prompts/P245_c3_zinc_worldwide_benchmark.md
?? tasks/prompts/P246_c3_magnesium_assumptions_challenge.md
?? tasks/returns/P233_return.md
?? tasks/returns/P234_return.md
?? tasks/returns/P239_return.md
?? tasks/returns/P240_return.md
?? tasks/returns/P241_return.md
?? tasks/returns/P242_return.md
?? tasks/returns/P243_return.md
?? tasks/returns/P244_return.md
?? tasks/returns/P245_return.md
?? tasks/returns/P258_voice_redteam.md
?? tasks/returns/P261_hc_voice_redteam.md
?? tasks/returns/P265_snacks_v3_voice_redteam.md
?? test_acceptance.py
```

### Delta

### New / modified since dispatch
  ?? 02_products/snack_bars/phase3_fix_summary_20260620_110807.json
