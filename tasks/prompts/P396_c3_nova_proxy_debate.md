(route: C3)

# P396 — C3 INDEPENDENT REVIEW: should Bari reduce/eliminate the NOVA proxy?

You are C3 — the independent outside reviewer in a 3-way debate (the other two
voices are Bari's in-house Nutrition Agent and its Adversarial QA / Red-Team gate).
You produce an EVIDENCE-GROUNDED INDEPENDENT OPINION only. You do not produce
production data, you do not close work, you do not write code. Your job is to be the
impartial outside check on an internal proposal.

## Background you need
Bari scores packaged foods 0–100 / A–E on "nutritional architecture." One input signal
is a **NOVA proxy** — an inference of the NOVA 1–4 ultra-processing class from the Hebrew
ingredient text via keyword matching. NOVA feeds several scoring dimensions
(processing_quality, whole_food_integrity) and some caps.

The product owner's standing directive (months old) is: **move away from the NOVA proxy
as far as possible — it has proven too simplistic.** A new failure has reignited this.

## The verified failure (two real product traces, same "cookies" shelf)

PRODUCT A — "פתי בר קלאסי / אסם" (plain Petit Beurre biscuit), FINAL SCORE 21.4 / E
  - sugar 22 g/100g · saturated fat 4 g · 1 Israeli red label (sugar)
  - fat source: unspecified "vegetable oils"
  - NOVA proxy = **4** (confidence 0.55)
  - processing_quality 35 · whole_food_integrity 28 · additive_quality 30 (4 additive categories detected)
  - weighted base 35.4 → after soft penalties (−14) → 21.4

PRODUCT B — "סנדוויץ' עם קרם בטעם שוקו / צ'וקטה" (cream-filled sandwich cookie), FINAL SCORE 26.1 / E
  - sugar 29 g/100g · saturated fat 8.6 g · **2** Israeli red labels (sugar + sat-fat)
  - fat source: **palm oil** · contains a fabricated sugar-fat cream filling, wheat starch, caramel colour
  - hyper-palatable fat+sugar pattern FIRED (an 8-pt penalty Product A escaped)
  - NOVA proxy = **3** (confidence 0.35 — LOW, self-flagged) · category misread as "dessert" (conf 0.51, unstable)
  - processing_quality 56 · whole_food_integrity 56 · additive_quality 66 (only 2 additive categories detected)
  - weighted base 39.1 → after penalties (−13) → 26.1

**The inversion:** Product B is worse on EVERY consumer-facing fact (more sugar, double the
sat-fat, an extra red label, palm oil, a fabricated cream, a fired hyper-palatability flag) —
yet it scores 5 points HIGHER. Root mechanism: B was classified NOVA-3 while the simpler
biscuit A was NOVA-4. That single misclass handed B +21 processing_quality, +28
whole_food_integrity. Two ingredient-parsing artifacts also under-counted B's additives
(its flavouring was written singular "חומר טעם וריח" and missed; its leavening was spelled
chemically and missed) → additive_quality 66 vs 30. The 2-red-label cap on B (cap=45) never
bit, because B's merit score (39.1) was already below 45 — caps are ceilings, not penalties.

Note the owner's nuance: the engine was **honest, not adversarial** — it self-reported NOVA
confidence 0.35 (low) and flagged category instability. It did not hide its uncertainty; it
just didn't act on it.

## The motion under debate
"Bari should structurally reduce or eliminate the NOVA proxy's influence on scores, replacing
it where possible with direct, label-derivable compositional signals (sugar, saturated fat,
fat source/quality, robustly-counted additives, hyper-palatability)."

## Deliver your independent opinion — answer ALL of these, concisely and concretely

1. **Root cause.** Is the NOVA proxy genuinely the root cause of THIS inversion, or is the
   proxy a scapegoat for a deeper architecture choice (NOVA feeding multiple correlated
   dimensions; caps that are non-binding ceilings; brittle keyword parsing)? Apportion it.

2. **The motion itself.** Is eliminating/de-weighting NOVA the right fix, or an over-correction?
   What does NOVA *uniquely* contribute that direct compositional signals do NOT capture (if
   anything)? What concrete NEW failure modes would a direct-compositional engine introduce —
   e.g., could a clean-label but nutritionally poor product, or an additive-heavy but
   low-sugar/low-fat product, now mis-rank the other way?

3. **The honest-uncertainty angle.** The engine already knew NOVA confidence was 0.35. Is the
   smarter fix "kill NOVA" or "make NOVA self-aware — when NOVA confidence is low, down-weight
   its influence and lean on direct compositional signals"? Argue the strongest version of the
   confidence-gating alternative.

4. **Minimal reversible fix.** If you had to stop THIS inversion this week without a wholesale
   re-score of all 12 live categories, what is the smallest, most defensible, reversible change?

5. **Your verdict.** One paragraph: where you land on the motion, your confidence, and the one
   thing you'd most warn the in-house team against.

Be specific and adversarial-minded toward BOTH the NOVA proxy AND the proposal to remove it.
Cite your reasoning. Evidence-only; no code, no data production. ≤900 words.
