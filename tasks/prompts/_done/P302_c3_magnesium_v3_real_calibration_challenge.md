# P302 / Magnesium v3 REAL-numbers calibration challenge (route: C3)

Independent adversarial review (ChatGPT). Evidence/advice only — do not build, do not close. The architecture question is already settled (owner chose absorption-adjusted-dose scoring); this challenge is on the **calibration and the REAL engine output**, before Product D7 co-sign and owner go-live. Challenge hard — this page exists to kill the "oxide ≈ citrate" misconception, and these are the actual grades that would ship.

## What was built (REAL run, not estimate)
The v3 model: scoring `adjusted_dose = administered_elemental_mg × bioavailability_tier_factor`, scored against a 100–300mg general-gap band. Tier factors: **HIGH (citrate/bisglycinate/glycinate) = 1.00, MODERATE (malate/taurate/hydroxide) = 0.75, LOW (oxide/carbonate) = 0.45, UNRESOLVED = 1.00 + evidence-penalty −20.** Pillar weights: dose 0.55 / evidence 0.20 / transparency+safety 0.25. The class factor lives in the DOSE pillar (not evidence) to avoid double-counting; evidence base is a flat 72 for all known classes. Safety (UL 350mg, EFSA GI note >250mg) fires on ADMINISTERED elemental, never on adjusted dose. Consumer display = administered mg + class label only; the factor and adjusted dose are internal. The backwards cross-form monotonicity hard-constraint (v2) was removed.

These factors are framed as **coarse scoring-calibration constants, NOT claimed fractional-absorption percentages** (oxide's real fractional absorption ≈4%; citrate ≈28–32%).

## The REAL grade distribution (trace-derived, n=16 scored; B4/C9/D2/E1)
| Product | Form | Admin elem mg | Class | factor | adj mg | Final | Grade |
|---|---|---|---|---|---|---|---|
| Supherb Citrate+B6 | citrate | 250 | HIGH | 1.00 | 250 | 72.8 | B |
| Altman Bisglycinate 250 | bisglycinate | 250 | HIGH | 1.00 | 250 | 72.8 | B |
| Altman Citrate 200 | citrate | 200 | HIGH | 1.00 | 200 | 68.7 | B |
| Nutricare WELL | bisglycinate | 168 | HIGH | 1.00 | 168 | 66.0 | B |
| NT-LC Anti Leg Cramps | hydroxide | 190 | MODERATE | 0.75 | 142.5 | 63.9 | C |
| Nutricare/Tink/Altman Oxide 520 (×3) | oxide | 314 | LOW | 0.45 | 141.3 | 62.6 | C |
| Full-Mag Hadas | bisglycinate | 122 | HIGH | 1.00 | 122 | 62.2 | C |
| Altman MagUp / Balance (×2) | oxide | 272 | LOW | 0.45 | 122.4 | 61.0 | C |
| Tink Malate | malate | 136 | MODERATE | 0.75 | 102 | 60.6 | C |
| Nutricare Malate | malate | 135 | MODERATE | 0.75 | 101.2 | 59.3 | C |
| Solgar Cal-Mag (oxide+citrate blend) | UNRESOLVED | 100 | — | 1.00 | 100 | 48.9 | D (cap_3) |
| Nutricare Taurate | taurate | 76 | MODERATE | 0.75 | 57 | 46.2 | D |
| Nutricare Nano | bisglycinate | 88 | HIGH | 1.00 | 88 | 34.0 | E (cap_1) |

Grade-separation property test PASS (every oxide < every citrate/bisglycinate ≥200mg). Within-form monotonic.

## Challenge questions — be adversarial
1. **Is LOW=0.45 the right magnitude?** 314mg oxide × 0.45 = 141mg adjusted → C/62.6, only ~1.3pts below Full-Mag bisglycinate-122 (62.2/C) and ~1.6pts above oxide-272 (61.0/C). Given oxide's real fractional absorption is ~4% (≈5–6× lower than citrate), is 0.45 too GENEROUS — does landing high-dose oxide mid-C still under-state how poorly it delivers? Or is C (clearly below every B citrate) sufficient honest signal? Would 0.40 or 0.35 be more defensible, or would that over-punish into false precision?
2. **The big C-cluster (59–64, 9 products) mixes HIGH-class low-dose (Full-Mag bisgly 122 = 62.2) with LOW-class high-dose (oxide 314 = 62.6).** They tie because adjusted doses converge (~122–142mg). Is "these deliver a similar effective amount, the difference is form + label honesty" the right consumer message — or does a bisglycinate tying an oxide re-introduce a muddied "form barely matters here" signal the page is trying to avoid?
3. **Flat evidence base (72 for every known class):** is removing all class signal from the evidence pillar correct (avoids double-count), or does it under-reward forms with genuinely stronger human-comparative evidence (citrate) vs forms placed by mechanism only (taurate, malate)?
4. **Taurate 76mg → D/46.2** (76 × 0.75 = 57mg adjusted, NEAR tier). Defensible that a clean, well-labelled MODERATE-form product lands D purely on low administered dose? Any consumer-fairness or proportionality concern?
5. **NT-LC hydroxide 190mg → C/63.9** — top of the C cluster, just under the B floor. The P301 concern was a cramps-indication product landing B; it now lands C. Resolved, or still risky given it's the single highest non-B?
6. **GO / HOLD:** are these REAL grades calibrated well enough to proceed to Product D7 co-sign + owner go-live, or does a specific tier factor / weight need one more turn before the numbers are defensible in public?

References (read if reachable): `03_operations/supplement_engine/proto_v0/benchmark/magnesium_model_v3_bioav_adjusted_dose_spec.md`, `magnesium_v2_verification_table.csv`.

Return a verdict per question + an explicit GO (proceed to D7) / HOLD (name the exact calibration change) recommendation. End with the return contract.
