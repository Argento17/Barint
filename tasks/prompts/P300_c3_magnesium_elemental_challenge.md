# P300 / Magnesium elemental-vs-compound + corrected-model challenge (route: C3)

You are an independent adversarial reviewer (ChatGPT). Challenge a high-stakes data + scoring determination for Bari's magnesium comparison page. **Evidence/advice only — do not build, do not close.** Cite reasoning; flag anything unsafe to ship.

## Background
Bari's magnesium page (18 products) was published then PULLED OFFLINE 2026-06-23. Two bugs surfaced:
1. **Absorbed-vs-administered (confirmed):** the model multiplied elemental × a fixed absorption % to get "absorbed mg," then compared that to clinical-trial thresholds — but trial doses are *administered elemental* mg. Apples-to-oranges; systematically depressed every product.
2. **Elemental-vs-compound (just reconciled):** two internal audits disagreed on whether each product's declared mg is elemental or compound.

## The reconciliation now on the table (challenge THIS)
Determination: the label convention **"מגנזיום (from/as X) Y מ\"ג"** declares **Y = elemental magnesium**, X = source compound. Therefore:
- **Organic-salt products declare ELEMENTAL:** Altman Citrate 200mg, Altman Bisglycinate 250mg, Supherb Citrate+B6 250mg, Nutricare Taurate 76mg, Tink Malate 136mg, Nutricare WELL 168mg, Nutricare Nano 88mg — these are the TRUE elemental doses. The live page WRONGLY converted them DOWN ~6–11× (treating 200mg citrate as compound → 32mg), making good products look near-empty.
- **Oxide + high-compound products declare COMPOUND:** the three 520mg oxide products and Nutricare Malate 700mg — here Y is the compound salt mass (520mg elemental from oxide is physically impossible; 700mg elemental malate is too large for one capsule), so convert via elemental fraction (oxide 0.603 → 314mg; malate → ~108–137mg).
- Orchestrator independently VERIFIED two labels on altman.co.il: Citrate "(From Magnesium Citrate) 200 מ\"ג" and Bisglycinate "(as Magnesium Bisglycinate) 250 מ\"ג" — both elemental.

**Consequence:** premium-form products (citrate/bisglycinate/taurate) the live page ranked LAST become the shelf TOP (good dose 76–250mg elemental AND high-bioavailability form). The "nothing on the Israeli shelf reaches adequacy / all C-D-E" headline largely collapses.

## The corrected model (challenge this too)
Drop the absorbed-mg calculator. Score **administered elemental mg** vs indication thresholds: general dietary gap 100–300mg, blood pressure 300–400mg (modest ~2mmHg effect), migraine 400–600mg (exceeds UL → supervised). Bioavailability shown as CLASSES (high/mod/low/very-low/unknown), not fake-precise mg. Safety block above the table (kidney, UL 350mg, diarrhea, drug interactions). Price per 100mg elemental.

## Your challenge — be adversarial
1. **The wording inconsistency:** identical label form "מגנזיום (X) Y מ\"ג" is read as ELEMENTAL for citrate/bisglycinate but COMPOUND for oxide (chemistry-forced). Is flipping the meaning of identical wording based on plausibility defensible, or a red flag that the whole determination is shaky? How would you make it rigorous / what would you demand to confirm?
2. **The reshuffle:** is it clinically and consumer-defensible that citrate/bisglycinate products jump from bottom to top? Any scenario where this is still wrong?
3. **What could still be wrong** in the elemental reads (e.g., products where the stated mg really IS compound despite the convention)? Which specific products would you insist on a physical-label photo for before scoring?
4. **The indication thresholds** (general gap 100–300, BP 300–400, migraine 400–600) — reasonable, or mis-specified?
5. Anything the two internal audits + the orchestrator's spot-check **missed**.

## References (read if reachable)
- `C:\Bari\02_products\supplements\real_corpus_v3\magnesium_elemental_reconciliation_v1.md` (the authoritative table)
- `C:\Bari\02_products\supplements\real_corpus_v3\magnesium_label_audit_v1.md` (source-label audit)

Return: a verdict per challenge point + an explicit GO / HOLD on whether the elemental determination is solid enough to drive a re-score, and the shortlist of products that must have a physical-label photo first. Do not edit files. End with the return contract.
