# P301 / Magnesium recalibration + dose-vs-absorption architecture challenge (route: C3)

Independent adversarial review (ChatGPT). Evidence/advice only — do not build/close. This is the central scoring-philosophy question for Bari's magnesium page; challenge hard.

## Story so far
The magnesium page was pulled offline. Old model compared ABSORBED mg to ADMINISTERED clinical doses (bug) and understated 7 organic-salt products' elemental dose ~6×. The corrected v2 model (D7-approved) scores on **administered elemental mg** vs a general-gap band (dose pillar weight 0.40) + a **bioavailability CLASS** modifier (evidence pillar) + safety; absorbed-mg is removed from consumer display. First real engine run produced a defect: a 314 mg oxide (LOW class, ~4% absorbed ≈ 13 mg) scored **B/69**, TYING a 250 mg citrate (HIGH class, ~27% absorbed ≈ 68 mg, B/70) — "oxide ≈ citrate," the misconception the page exists to kill.

## The proposed recalibration (challenge THIS)
Strengthen the class modifiers: HIGH +8→+10, MODERATE +3→+5, LOW 0→**−14**, UNRESOLVED −5→**−20**. Result: all 5 oxide products **B→C** (oxide-314 = C/64.9), citrate stays B/70.6 — a clean ONE-band separation at equal dose. New dist (16 scored): B:5 C:8 D:1 E:1.

Nutrition states the weight structure **cannot** produce a two-band separation at equal dose while satisfying a monotonicity constraint Product imposed: **oxide at 270+ mg must stay ABOVE bisglycinate at 88–122 mg.** That constraint forces oxide-272 (63.2) > Full-Mag bisglycinate-122 (62.9) by only **+0.3 pts**.

## Challenge questions
1. **Is one-band separation (oxide C / citrate B at equal dose) enough** to honestly convey "form/absorption matters," or is it still too weak given oxide delivers ~5× less absorbed magnesium?
2. **Is the monotonicity constraint itself backwards?** It forces a 272 mg oxide (~11 mg absorbed) to outrank a 122 mg bisglycinate (~27 mg absorbed). On absorbed-magnesium grounds the bisglycinate arguably delivers MORE usable magnesium. Should a well-absorbed lower-administered-dose product be allowed to rank ABOVE a high-administered poorly-absorbed one? Is the +0.3 margin a sign the constraint is fighting the science?
3. **Architecture:** is "administered elemental + weak class modifier" the right model, OR should the score use a **bioavailability-ADJUSTED dose** (administered × an absorption-tier factor) — which lets absorption properly drive the grade while still being DISPLAYED as a class, not a fake-precise "absorbed X mg"? The original assessment banned fake-precise absorbed-mg DISPLAY, not absorption-driven SCORING. Which architecture is more defensible?
4. NT LC Hydroxide 190 mg (MODERATE) moves C→B under the recal — defensible?
5. **GO / HOLD:** ship the recalibration (one-band) as the re-build basis, or escalate the architecture question (absorption-adjusted dose) before building?

References (read if reachable): `03_operations/supplement_engine/proto_v0/benchmark/magnesium_v2_bioav_recalibration_spec.md`, `magnesium_model_v2_final_spec.md`, `magnesium_v2_verification_table.csv`.

Return a verdict per question + an explicit GO (ship recal) / HOLD (escalate architecture) recommendation with the single most defensible model for a consumer page whose whole point is "form matters." End with the return contract.
