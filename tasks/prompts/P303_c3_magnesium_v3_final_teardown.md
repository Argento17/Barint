# P303 / Magnesium v3 FINAL determination teardown (route: C3)

Independent adversarial review (ChatGPT). Evidence/advice only — do not build, do not close. **The owner explicitly asked for a fresh C3 teardown of the FINAL state before go-live.** This is the last challenge before a real consumer page is rebuilt and re-published. The whole chain has signed off — your job is to find what they collectively missed. Be ruthless; the page was published-then-pulled once already.

## The full chain (all complete + orchestrator-verified)
1. **Data reconciliation:** label convention "מגנזיום (from/as X) Y מ\"ג ⇒ Y = elemental" for organic salts (citrate/bisglycinate/taurate/malate verified elemental from source labels); oxide 520mg + malate 700mg treated as COMPOUND (chemistry-forced: 520mg elemental would exceed UL; derived oxide elemental = 314mg via 0.603 stoichiometry).
2. **Architecture (owner-chosen):** absorption-adjusted dose. scoring_dose = administered_elemental × bioavailability tier_factor (HIGH citrate/bisgly/glycinate=1.0, MODERATE malate/taurate/hydroxide=0.75, LOW oxide/carbonate=0.35, UNRESOLVED=1.0+ev-penalty −20). Scored vs 100–300mg general-gap band. Weights: dose 0.55 / evidence 0.20 (flat 72 for all known classes) / transparency+safety 0.25. Safety (UL 350mg, EFSA GI note >250mg) on ADMINISTERED mg, never adjusted. Display = administered mg + class only; factor/adjusted-dose internal.
3. **Three prior C3 passes:** P300 (elemental determination = defensible heuristic, score verified-only set), P301 (recommended this absorption-adjusted architecture over a class-modifier patch), P302 (HOLD → LOW 0.45→0.35; everything else endorsed).
4. **Two D7 co-signs (Hard Rule 8):** Product APPROVE-WITH-CONDITIONS (reshuffle proportionate; defer optional taurate penalty; 7 go-live conditions), Nutrition APPROVE-WITH-CONDITIONS (LOW=0.35 clinically defensible; flat evidence base correct; edges fair; safety correct).

## The FINAL verified grades (run 20260623T114522Z.json; B4/C9/D2/E1)
- **B:** Supherb Citrate+B6 250mg (72.8), Altman Bisglycinate 250mg (72.8), Altman Citrate 200mg (68.7), Nutricare WELL bisgly 168mg (66.0)
- **C:** NT-LC hydroxide 190mg cramps-product (63.9), Full-Mag bisgly 122mg (62.2), Tink Malate 136mg (60.6), 3× oxide-314mg / the 520mg bottles (60.0), Nutricare Malate 135mg (59.3), 2× oxide-272mg (57.6)
- **D:** Solgar Cal-Mag oxide+citrate blend (48.9, cap_3), Nutricare Taurate 76mg (46.2)
- **E:** Nutricare Nano bisgly 88mg (34.0, cap_1 unverifiable nano-delivery claim)
- **No score:** Amorphicure, TRIOMAG (label data missing). **Discarded:** Supherb Max 550.

## Tear it apart — attack the weakest assumption
1. **The elemental-vs-compound flip is the foundation of the whole reshuffle.** Identical label grammar "(from/as X) Y mg" is read as ELEMENTAL for organic salts but COMPOUND for oxide (chemistry-forced). The entire "premium forms jump to the top" result rests on this. Is this still the single most fragile link? What one product, if its determination is wrong, would most embarrass the page? Oxide elemental rests on DOMAIN INFERENCE (no resolving panel photo) — is shipping on inference acceptable, or a launch blocker?
2. **Tier factors 1.0 / 0.75 / 0.35 are calibration constants, not absorption fractions.** Is the page honest about this, or does grading-by-a-made-up-multiplier invite a "your 0.35 is arbitrary" attack that the page can't defend? Is there a cleaner defensible basis?
3. **The C-cluster (9 of 16 products, 57.6–63.9).** Over half the shelf lands in one grade band, mixing well-absorbed-low-dose with poorly-absorbed-high-dose. Does this make the page USELESS to a consumer (everything's a C), even if each grade is individually correct? Is a 9-wide C-cluster a finding or a failure?
4. **Flat evidence base (72 for every known class).** Does removing all evidence-strength signal mean a mechanism-only form (taurate) and an RCT-backed form (citrate) are treated as equally evidenced — and is that a defensibility hole?
5. **The reshuffle's consumer message.** The pulled page said ~"nothing on the Israeli shelf is adequate." The new page says "premium forms lead, cheap oxide is mid-tier." Is the NEW message over-correcting — is there a scenario where high-dose oxide is genuinely the right buy (cost, constipation use) that a B/C-by-absorption framing now hides?
6. **What did 3 C3 passes + 2 D7 co-signs collectively MISS?** Name the one thing nobody in the chain challenged.

Return a verdict per point + an explicit GO (proceed to page rebuild) / HOLD (name the blocker) recommendation, and the single product or assumption you'd most want hard evidence on before go-live. End with the return contract.
