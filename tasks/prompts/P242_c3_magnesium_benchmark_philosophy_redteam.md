# P242 / Magnesium scoring philosophy red-team: absolute benchmark anchor + cap clustering + inclusion (route: C3)

You are the outside-the-family independent reviewer. Give a reasoned second opinion.
You do NOT build, do NOT produce the corpus, do NOT close anything. Evidence + judgment only.
Cite mechanisms/literature where you can. Flag where you are uncertain.

## Context — the Bari Supplement Intelligence Engine (SIE), magnesium category
We scored 19 Israeli-shelf magnesium supplements. The owner (a non-programmer reading
the consumer page) raised three objections. We think they are right; we want your
independent challenge before we change scoring philosophy. These are EDPG/candidate
scores — not published — so changing them is allowed; we want it to be *defensible*.

### How the engine currently scores (the real mechanics)
Per product we compute sub-scores: evidence, dose (elemental-mg adequacy), form
(absorption ladder), honesty (claim vs evidence), safety (UL vetoes). Then
**most-restrictive cap/floor wins**. Two caps dominate magnesium:
- `cap_2_fairy_dust` = hard **D-ceiling of 49** when elemental dose is under-adequate
  or unverifiable. When it fires, the real sub-scores are discarded — the product is
  pinned to exactly 49.
- `cap_1_insufficient_evidence` = hard **E-ceiling of 34** when the on-label claim has
  Insufficient evidence.
Both 49 and 34 are tagged `CALIBRATION-PENDING` in the code — i.e. never calibrated.

Result: the 19 scores are not a spread, they are **cap-pins**: 66.5×1, 62.6×3, 59×2,
58.4×1, **49.0×9**, **34.0×3**. Dose is elemental = (compound mass × form fraction),
e.g. oxide is ~60% elemental, citrate ~16%, bisglycinate ~14%. So the cheap high-mass
oxide products clear the dose bar and land at 62–67, while premium well-absorbed
citrate/bisglycinate products are under-dosed on the Israeli shelf and collapse to the
49 pin. The page therefore "lands entirely on the chemistry compound", and every
low score is the same opaque number with no visible reference point.

## The three forks — rule on each, with reasoning

**FORK A — Absolute best-in-class benchmark anchor.**
The owner wants: "tell me this scores low because, vs a *perfect* product, it falls
behind on X, Y, Z." The engine has NO absolute anchor — a score means "tripped an
internal cap", not "distance below best-in-class".
Q: Is introducing an explicit reference-perfect magnesium (a fixed target: elemental-mg
per dose, form tier, evidence tier, label honesty) — and scoring/explaining every
product as a *distance from that anchor* — methodologically sound? What are the
specific target values for a "reference-perfect" magnesium supplement (elemental mg,
form, evidence, label), grounded in dose-response literature (e.g. RDA ~310–420 mg,
typical clinical doses, the oxide-vs-organic absorption evidence)? Risks?

**FORK B — Cap clustering vs. spread.**
Nine products pinned at exactly 49 erases all differentiation between, say, a 109 mg
malate (decent form, mid dose) and a 21 mg taurate (good form, trivial dose).
Q: Is a flat hard cap defensible here, or should the under-adequate band become a
*graded* range so dose/form/evidence still separate products within it? If graded,
how would you structure it without letting a well-formed-but-underdosed product
masquerade as adequate? (We do NOT want to reward under-dosing.)

**FORK C — Inclusion / relevance.**
The comparison includes combo products that aren't dedicated magnesium supplements:
a Ca/Mg/D3 tablet (magnesium ~100 mg incidental), an ashwagandha+valerian "Balance"
sleep blend, a zinc+B6 "WELL" blend, and tri-form "TRIOMAG"/"nano-liposomal" claim
products.
Q: Should a magnesium comparison include products where magnesium is incidental to a
multi-active formula? Propose a crisp inclusion rule (what stays, what is excluded or
footnoted) that a consumer would find honest.

## Return (to tasks/returns/P242_return.md)
A ruling on A, B, C — each: your recommendation, the reasoning, the literature/mechanism
basis, and the strongest counter-argument to your own position. Plain language where the
owner will read it. End with the single biggest risk you see in the whole approach.
