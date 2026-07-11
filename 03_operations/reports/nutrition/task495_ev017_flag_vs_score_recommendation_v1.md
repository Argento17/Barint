# EV-017 Flag-vs-Score Recommendation
## Does the Tufts/Mozaffarian meta invalidate `should_affect_score_now: false`?

**Author:** Nutrition Agent
**Date:** 2026-07-05
**Task:** TASK-495
**Status:** PROPOSE-ONLY — no score change; tripwire assessment below

---

## 1. The Crux — Stated Directly

The 2026-07-03 REFINES addendum posed the right question but left it open. This memo resolves it.

**EV-017's `should_affect_score_now: false` rests on two independent grounds:**

1. **Variability ground:** "High inter-individual variability prevents population-level algorithmic penalisation."
2. **Tier-resolution ground** (implicit, now made explicit): EV-017's actionable content is a *tier split* — sucralose/saccharin flagged, stevia/monk-fruit neutral. A scoring rule that only penalizes the flagged tier requires tier-discriminating evidence. A rule that penalizes all sweeteners equally requires evidence of class-level harm at the population mean.

The Tufts/Mozaffarian meta (PMID 42347889 / DOI 10.1007/s11883-026-01429-9, Current Atherosclerosis Reports 28:65, 2026-06-25) **challenges the first ground** but **cannot license a move on the second ground.** These are independent gates; both must be cleared for a score change.

**The recommendation is: keep `should_affect_score_now: false`. Do not convert to a score.**

---

## 2. Why the "Inter-Individual Variability" Rationale Needs to Be Replaced

The Tufts meta demonstrates a **population-mean effect** across 21 adult RCTs: raised fasting insulin and HbA1c with a trend toward worse insulin sensitivity, observed across the pooled NNS group vs noncaloric controls. This is not confined to a responder subgroup.

That result directly invalidates the *specific framing* in `should_affect_score_now_reason`: "High inter-individual variability prevents population-level algorithmic penalisation."

The Research Agent (verified 2026-07-05) correctly classifies this as Moderate tier (narrative review + meta-analysis container; PubMed pub type: Review, not standalone systematic review/meta-analysis; no PRISMA registration signal in available press coverage). It is below the Strong tier of a registered Cochrane-style systematic review. It is nonetheless the highest-quality population-level synthesis to date for NNS cardiometabolic outcomes.

**The "inter-individual variability" language must be retired as a grounds statement.** It is no longer accurate. The replacement honest grounds statement is:

> "A class-level population signal exists (Moderate evidence, Tufts/Mozaffarian 2026), but the signal cannot discriminate sweetener tiers. EV-017's operative content is a tier split (sucralose/saccharin vs stevia/monk-fruit); a scoring rule requires either (a) tier-discriminating evidence to move sucralose/saccharin only, or (b) defense of penalizing stevia/monk-fruit equally. Neither is currently supportable. Flag/disclosure posture maintained."

This is a **registry language update only** — it does not change the posture, the flag state, or any score. It corrects the grounds to reflect the current evidence.

---

## 3. Evidence-Weight Table

| Evidence source | DOI / PMID | Design | Tier | Class-level signal? | Tier-level signal? | Weight for flag-vs-score decision |
|---|---|---|---|---|---|---|
| Suez et al. landmark human intervention (prior, pre-addenda) | (not re-verified here — prior evidence base) | Human RCT, n=~7 | Moderate-Strong | Partial (sucralose/saccharin arms) | Partial (sucralose/saccharin only; stevia not tested) | Supports sucralose/saccharin flag |
| Frontiers/Concha Celume mouse intergenerational (2026-06-18 addendum) | 10.3389/fnut.2026.1694149 | Animal (mouse, 3 generations) | Weak | No (animal only) | Partial (sucralose vs stevia divergence — but animal) | Weak; suggestive of tier divergence |
| UK Biobank Sun et al. cohort (2026-06-18 addendum) | 10.1186/s12933-024-02333-9 / PMID 38965574 | Observational cohort, n=133,285 | Moderate | Yes (NNS class) | No (pooled "artificial sweeteners") | Moderate for class signal; zero for tier |
| Tufts/Mozaffarian (2026-07-03 REFINES addendum) | 10.1007/s11883-026-01429-9 / PMID 42347889 | Narrative review + 21-RCT meta-analysis | Moderate | Yes — raised insulin + HbA1c across pooled NNS | **Explicitly NO** — paper's own stated limitation: "grouping them together may obscure the full picture" | Moderate for class signal; zero for tier |

**Aggregate verdict:**
- Class-level harm signal: Moderate (two independent arms — UK Biobank observational + Tufts RCT meta)
- Tier-level signal (sucralose/saccharin ≠ stevia): Weak-to-Moderate (prior human RCTs for sucralose/saccharin; Frontiers mouse data suggestive but animal; NO population-level tier-discriminating RCT meta)

---

## 4. The Three Options — One Recommendation

**Option (a): Keep flag, don't score.** The flag/disclosure posture for `sweetener_microflora_disruption_risk` remains `should_affect_score_now: false`. Update the grounds language to retire the invalidated "inter-individual variability" framing. No score changes.

**Option (b): Convert to score at class level.** This would mean applying a penalty to ALL non-nutritive sweeteners — including stevia (E960) and monk fruit — equally. The engine already has `SWEETENER_CAP_A = 75` and `SWEETENER_PENALTY_A = 8` for Tier A (stevia/monk-fruit). Converting at class level would mean either (i) collapsing tiers and treating stevia like sucralose, or (ii) tightening `SWEETENER_CAP_A` and `SWEETENER_PENALTY_A` to match Tier C values. This is not defensible. The existing evidence base, including the Frontiers mouse study showing divergent sucralose/stevia effects and the landmark human intervention studies, supports tier differentiation. Collapsing tiers to honor a class-level meta would be **less accurate than the current engine**, not more.

**Option (c): Something else.** Not proposed.

### Recommendation: Option (a).

Keep `should_affect_score_now: false`. Update `should_affect_score_now_reason` in the registry to replace the invalidated "inter-individual variability" language with the tier-gap explanation above. No scores change, no caps change, no penalties change.

**Rationale:**

1. The Tufts meta challenges the variability framing but does not provide tier-discriminating evidence. The two conditions for a score move are independent: clearing one does not license the move.

2. The engine already applies a tiered sweetener scoring system (`SWEETENER_CAP_A/B/C`, `SWEETENER_PENALTY_A/B/C`). The distinction between EV-017's `should_affect_score_now: false` and the live engine caps is precise: the live caps express the structural classification concern (processed food using synthetic sweeteners is architecturally different from whole food); EV-017's flag addresses the specific *gut dysbiosis mechanism*. These are not the same claim. The gut dysbiosis flag does not need to convert to a score to be live in the engine — the broader sweetener architecture is already active.

3. A class-level score move would penalize stevia and monk fruit products equally to sucralose products. The existing evidence base does not support this. The Frontiers mouse study (weak, animal) actually shows *divergent* intergenerational effects between sucralose and stevia, which is directionally supportive of the current tier split. Collapsing tiers in response to a class-level meta would move the engine in the wrong direction scientifically.

4. The correct next evidence threshold is a pre-registered human RCT or systematic review with sweetener-specific subgroup arms (sucralose alone vs stevia alone vs saccharin alone). Until that exists, the tier structure is based on the best available evidence and should be preserved.

---

## 5. Relationship to the Live Engine's `SWEETENER_CAP` Constants

An important clarification for the D7 record:

EV-017's `should_affect_score_now: false` applies specifically to the signal `sweetener_microflora_disruption_risk` — the gut-dysbiosis scoring channel. It does **not** mean sweeteners have zero scoring impact in the live engine.

The live engine already applies `SWEETENER_CAP_A = 75`, `SWEETENER_CAP_B = 73`, `SWEETENER_CAP_C = 70` and corresponding penalties. These operate as a **structural classification concern** (a product that uses high-intensity synthetic sweeteners instead of natural food sweetness is architecturally different from a whole-food product), not as a dysbiosis-mechanism scoring channel.

This distinction is correct and should be preserved. The Tufts meta strengthens the case that the cap hierarchy is directionally right. It does not justify collapsing the tiers. It does not justify removing the caps. It does not justify a new additional scoring penalty for the dysbiosis mechanism specifically.

---

## 6. Tripwire Assessment

| Action | Tripwire fires? | Reason |
|---|---|---|
| Update `should_affect_score_now_reason` language in evidence registry (prose-only grounds update) | **No** | Registry language correction within Nutrition Agent lane; no score, cap, penalty, or consumer-facing published output changes |
| Keep `should_affect_score_now: false` | **No** | Status quo |
| Any change to `SWEETENER_CAP_A/B/C` or `SWEETENER_PENALTY_A/B/C` values | **Yes — Tripwire 1** | Would change published scores; requires owner + Product Agent co-sign |
| Converting `sweetener_microflora_disruption_risk` to `should_affect_score_now: true` | **Yes — Tripwire 1** | Would change published scores (new signal activation); requires owner + Product Agent co-sign |
| Collapsing sweetener tiers (treating stevia = sucralose in engine) | **Yes — Tripwire 1** | Published score change across many affected products |

**The recommendation in this memo (option a) does NOT trip any tripwire.** The only implementation required is a registry grounds-language update — Nutrition Agent lane authority.

Any future proposal to convert to score, change the caps, or collapse the tiers would require: EV-### entry, D6 proposal (Nutrition Agent), D7 co-sign (Nutrition + Product Agent), and owner review (Tripwire 1).

---

## 7. Falsifiability Condition

This recommendation flips to score-active under the following conditions:

**For a tier-level score move (sucralose/saccharin flag, not stevia):**
A pre-registered systematic review or meta-analysis with sweetener-specific subgroup arms — sucralose alone, saccharin alone, stevia alone, erythritol alone, each vs noncaloric control in human adults — showing statistically separable effect sizes between the flagged tier and the neutral tier. Minimum: Moderate evidence tier (PRISMA-registered or equivalent methodological transparency). This would enable a D6/D7 proposal to tighten `SWEETENER_CAP_C` / `SWEETENER_PENALTY_C` relative to `SWEETENER_CAP_A` / `SWEETENER_PENALTY_A`, justified by the dysbiosis mechanism specifically.

**For a class-level score move (all NNS penalized equally):**
A strong-tier systematic review (registered, PRISMA, not narrative-container) showing class-level harm at the population mean, WITHOUT tier-discriminating evidence — and a defensible scientific position that stevia/monk-fruit carry the same gut-dysbiosis risk as sucralose/saccharin. Given current evidence direction (animal + human data both showing tier divergence), this scenario is unlikely without overturning the existing tier evidence base.

---

## 8. Required Registry Update (Nutrition Agent Lane — No Tripwire)

The following change to `bsip2_evidence_registry_v1.json` EV-017 is within Nutrition Agent lane authority and does not require D7 co-sign because it is a grounds-language correction, not a scoring rule change:

**Current `should_affect_score_now_reason`:**
> "High inter-individual variability prevents scoring application; implement as a consumer flag only"

**Proposed replacement:**
> "A Moderate-evidence class-level RCT meta-signal now exists (Tufts/Mozaffarian 2026, PMID 42347889 — 21 RCTs, raised insulin/HbA1c across pooled NNS). The 'inter-individual variability' rationale is retired. The remaining gate is tier-resolution: EV-017's operative content is a sucralose/saccharin-flag-vs-stevia/monk-fruit-neutral tier split; the Tufts meta explicitly pools all NNS as a class and cannot discriminate tiers. A scoring rule requires tier-discriminating evidence (pre-registered subgroup RCT meta). Until that exists, implement as consumer flag only."

**Note:** This registry update is a Nutrition Agent lane action. It corrects the grounds statement to be scientifically accurate without changing any score, cap, penalty, or consumer-facing output. It may be implemented directly without D7 co-sign. It should be done before the next evidence scan cycle to prevent the outdated "inter-individual variability" rationale from misleading future reviewers.

---

*Nutrition Agent — PROPOSE-ONLY. No score changed. No file other than this memo written. Registry language update recommended; no D7 required for that update. Any move to convert `should_affect_score_now` to `true` is Tripwire 1 — owner + Product Agent co-sign required.*
