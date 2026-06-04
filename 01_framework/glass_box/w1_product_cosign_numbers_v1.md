**Task:** TASK-179E

# Bari Glass Box — Product D7 Co-Sign on the Four Binding Numbers (Wave 1)

**Author:** Product Agent · **Date:** 2026-06-04 · **Wave:** TASK-179, Wave 1
**Co-signs against:** `01_framework/glass_box/d5_d6_rule_spec_v1.md` (TASK-179D, Nutrition Agent)
**Governance honored:** DEC-006 (owner-ratified 2026-06-04) Q1 + Q2.
**Scope of this note:** ratify the *starting* values to build and measure against. No code, no
score movement, no freeze-forever. Exact tuning revisitable after the pilot flag-ON diff.

---

## Verdict in one line

All four numbers are **co-signed outright**. They faithfully implement "conservative-to-demote,
reluctant-to-withhold" and "buy coverage over silence." **Nothing here needs human-owner
ratification** — the posture is already owner-ratified (DEC-006) and these numbers are near-no-op
by construction; none of them changes what a grade *fundamentally claims*. **One conditional**
attaches to the EV append (below): the DEMOTE=60 no-op claim must be *proven*, not asserted, via
the byte-identical-OFF + flag-ON diff on the pilot before go-live (that is a separate gate; it does
not block this co-sign or the registry append).

---

## Number-by-number

### 1. `DEMOTE_CEILING_BOUND = 60` — CO-SIGNED

**Consistent with Q1.** Verified against the live engine: `compute_confidence`
(`score_engine.py` L143–154) bands at exactly `≥80 high / ≥60 medium (no ceiling) / 40–59 low
(ceiling 75) / <40 insufficient (ceiling 50)`. "Below 60 → demote region" is a faithful
*restatement* of the existing edge where ceilings begin to bite. It reuses the live constants
(75/50, `constants.py` L434–435) verbatim. As a band edge, this introduces **no new behavior** —
it names the existing seam.

**Stress test of the "no-op on live" claim — PARTIALLY TRUE, and the spec already says so.**
The bound `60` *in isolation* is a no-op: nothing sitting at confidence 60–74 today gets a ceiling,
and nothing will under this bound either (60–79 is `medium`, ceiling `None`, unchanged). So a
product at confidence 60–74 does **not** change behavior from the bound itself. **But** the spec
(§2.1, §2.4) is honest that flag-ON is *not* byte-identical overall: the new −10/−20 D5 reduction
can push a borderline product's confidence *down across* the 60 or 40 edge into a ceiling it didn't
previously hit. That delta comes from the **reduction term (number 4)**, not from the bound 60.
So the correct framing for the registry: "DEMOTE_CEILING_BOUND=60 is a no-op restatement of the
live band edge; the only ON-vs-OFF score movement comes from the §2.1 reduction and the panel-
absent null flip, both demote-or-null-only, never promotion." **Co-signed, conditional on Data/QA
proving it:** OFF must be byte-identical on the three frozen runs (milk `run_004_recalibrated`,
snack-bars `snk-001=70/B`, bread `real_bread_retail_003_v1`) AND the flag-ON diff must show only
demotions/null-flips — no promotion, no frozen-invariant movement. That is the §4 acceptance test;
it is the pilot's job, not a precondition of this co-sign.

### 2. `NULL_FLOOR = 30`, gated on `severe`-band-AND-confidence<30 (or panel-absent) — CO-SIGNED

**This is the load-bearing "reluctant-to-withhold" number, and it gets it right.** Today
everything `<40` caps at 50 and is labelled `insufficient_data` (L1295–1298). A naive "<40 → null"
rule would withhold a large slice of the shelf (bread saw ~40% unscored) — a direct violation of
"buy coverage over silence." Requiring **both** `confidence < 30` **and** a `severe` disclosure
band means withhold fires only when the data is *both* numerically thin *and* structurally opaque —
a genuine floor-of-observability failure, not a thin-but-readable panel. The 30–39 deep-insufficient
band and the 40–59 low band keep a *capped* grade in `demote` rather than going null. That is
exactly Q1: demote-and-flag carries the normal case; null is rare and reserved. **Co-signed.**

One forward note (not a blocker): the `severe`-AND-<30 conjunction is *deliberately* hard to trip.
If the pilot shows it essentially never fires while panel-absent does all the withholding work, that
is acceptable and on-posture (more reluctant, not less). Revisit only if the pilot surfaces a case
that *should* be withheld but isn't — that's a tuning question for after the flag-ON diff, not now.

### 3 & 4. `D5→D6 reductions: partial −10, severe −20; structural-only = 0` — CO-SIGNED

**This is the cleanest expression of Q2 in the whole spec.** Structural gaps (the `minor` band —
proportions hidden, missing-field that the label format can never close) reduce confidence by **0**.
That is the hinge of "buy coverage over silence": the market floor is not a data fault, so it must
not bleed confidence and demote the whole shelf. Only **closable** opacity — where the manufacturer
*could* have named the additive/E-code and didn't — erodes the engine's trust that it sees the real
formulation, and even then only by a modest −10/−20. The reduction is small enough that D5 acts
*through* confidence (D6) and never becomes a back-door quality penalty on its own axis (Q2: "D5
never moves the grade on its own axis"). The asymmetry (structural 0, closable −10/−20) is the
correct and faithful encoding. The no-double-count guard (G5 names the legacy six but does not
re-deduct, §1.2/§2.1) is the right discipline and I want it held in test. **Both co-signed.**

The endemic-flavoring exclusion (§1.4, EV-036, BSIP2 registry; draft EV-080) is the right call and I explicitly back it: bare
`חומרי טעם וריח` in ~70% of panels must NOT raise the band, or D6 would demote nearly the entire
category — a DISTORTION-001-class category-blind error. Annotate calmly, exclude from band-raising.

---

## EV append authorization (EV-079 … EV-083 → relocated to BSIP2 EV-035 … EV-039)

**Relocation note (TASK-179F):** the five entries were appended to the **BSIP2 engine registry**
`03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.md` as **EV-035…EV-039** (they
are BSIP2 packaged-food scoring rules, not governance BEV- entries). ID mapping: EV-079→EV-035,
EV-080→EV-036, EV-081→EV-037, EV-082→EV-038, EV-083→EV-039. This authorization is unchanged in
substance; only the registry target + ids changed.

**AUTHORIZED to append all five (draft EV-079/080/081/082/083 → EV-035/036/037/038/039) to the
BSIP2 evidence registry as the controlling entries**, on this Product D7 co-sign, **conditional on**:

1. **Nutrition Agent D6/D7 co-sign already in hand** (DEC-006 names D6/D7 as the nutrition gate;
   this Product co-sign satisfies the D7 business/scope half — confirm the Nutrition half is logged
   before the physical append, per the dual-sign rule). Scoring-rule adoption requires BOTH; I do
   not append unilaterally.
2. **One wording correction on EV-038 (draft EV-082) before it lands as controlling:** state explicitly that
   `DEMOTE_CEILING_BOUND=60` is a *no-op restatement of the live band edge*, and that the only
   ON-vs-OFF score movement originates in the §2.1 reduction (EV-037, draft EV-081) and the panel-absent null
   flip — both demote-or-null-only. As drafted, EV-082 risked reading as if the bound itself moves
   behavior. This is a one-line clarity fix, not a numeric change; it does not re-open co-sign. (Applied in the relocated EV-038.)
3. The entries land with **Status flipped DRAFT → adopted-behind-flag** (`BARI_GLASSBOX_D5D6`,
   default OFF), not DRAFT, and not live-active. Adoption is behind-the-flag only until the pilot
   flag-ON diff is reviewed at the separate go-live gate.

The values stay *revisitable after the pilot* by explicit note in each entry — co-signing the
starting values, not freezing them.

---

## Ownership / next steps

- **Nutrition Agent** — confirm the D6/D7 nutrition co-sign is logged, then apply the EV-038 (draft EV-082) one-line
  wording fix and flip EV-035…039 (draft EV-079…083) DRAFT → adopted-behind-flag in the BSIP2 registry. (Owns the EV text.) [DONE — TASK-179F relocation.]
- **Data Agent** — build D5/D6 behind `BARI_GLASSBOX_D5D6` per §1–§4; run the §4 acceptance test
  (OFF = 0-diff on the three frozen runs) as the first gate before any further work.
- **QA Agent** — on the pilot, produce the flag-ON diff and prove the only deltas are demotions +
  `insufficient_data`→`לא נוקד` flips, no promotions, no frozen-invariant movement. This is the
  evidence that retires the "DEMOTE=60 no-op" condition on the co-sign.
- **Product (me)** — hold the separate go-live D10 gate; re-examine the exact −10/−20 and the 30
  floor against the flag-ON diff before live, per the spec's own invitation.

---

## What I am NOT co-signing here

- I am not co-signing go-live. This authorizes build-behind-flag and the EV append only.
- I am not freezing the four numbers. They are the right *starting* values; tuning is open post-pilot.
- I am not approving any consumer-facing surfacing of `disclosure_profile`/`d5_completeness`; that
  is a later D11/D12 frontend-scope decision and is out of scope for this co-sign.

*End of Product D7 co-sign note. Co-sign + EV authorization only — no engine, frontend, or
governance file was modified by this task.*
