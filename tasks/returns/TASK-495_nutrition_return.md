# TASK-495 — Nutrition Agent Return

**Task:** TASK-495 — EV-017 flag-vs-score review: reconcile population-RCT meta vs class-not-tier evidence
**Agent:** Nutrition Agent
**Date:** 2026-07-05
**Proposed status:** RETURNED

---

## Summary of Work

Read all required inputs: TASK-495.md, the Research Agent DOI verification report (task495_ev017_doi_verification_v1.md, orchestrator-verified), the full EV-017 entry in both bsip2_evidence_registry_v1.json and .md, scoring.md (engine architecture), signal_extractor.py (sweetener tier constants), constants.py (SWEETENER_CAP/PENALTY values), and score_engine.py (cap application logic).

Resolved the crux: the Tufts/Mozaffarian meta (PMID 42347889) challenges EV-017's "inter-individual variability" rationale but cannot license a tier-level score move because the paper explicitly pools all NNS as a class and cannot discriminate sucralose/saccharin from stevia/monk-fruit.

**Single recommendation: keep `should_affect_score_now: false` (flag posture). Update the grounds language in the registry to retire the now-invalidated "inter-individual variability" framing.**

Key findings:
- The Tufts meta demonstrates a population-mean cardiometabolic effect, which does retire the variability-only grounds
- Two independent gates exist for a score move: (1) population signal, (2) tier-discriminating evidence. Gate 1 is now Moderate-evidence. Gate 2 is still uncleared — no pre-registered tier-discriminating RCT meta exists
- Option (b), converting to a class-level score, would penalize stevia/monk-fruit equally to sucralose — scientifically unjustifiable given the existing tier evidence base, and would move the engine in the wrong direction
- The live engine already applies `SWEETENER_CAP_A/B/C` and `SWEETENER_PENALTY_A/B/C` as a structural-classification concern, separate from EV-017's dysbiosis-mechanism flag
- Falsifiability condition stated: a pre-registered subgroup RCT meta with sweetener-specific arms would flip this

No code changed. No published score changed. No consumer-facing output changed.

---

## Tripwire Assessment

- Recommendation itself: **no tripwire** — flag/disclosure posture maintained
- Registry language update (grounds correction only): **no tripwire** — Nutrition Agent lane authority
- Any future conversion to `should_affect_score_now: true` or change to SWEETENER_CAP values: **Tripwire 1** — owner + Product Agent co-sign required; not proposed here

---

## Artifacts

| File | Action | Purpose |
|---|---|---|
| `03_operations/reports/nutrition/task495_ev017_flag_vs_score_recommendation_v1.md` | created | Crux resolution memo, recommendation, evidence-weight table, tripwire assessment, falsifiability condition |

---

## Not Done

- Registry language update for EV-017 `should_affect_score_now_reason` — recommended in memo but not implemented here (propose-only scope; no D7 required for this specific change, but held for orchestrator to route as appropriate)
- D7 co-sign with Product Agent — not required for the flag-maintain recommendation; would be required before any future conversion to score-active

---

```json
{
  "task": "TASK-495",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/nutrition/task495_ev017_flag_vs_score_recommendation_v1.md",
      "action": "created",
      "sha256": "af02dd536d18937bc4f86f92e5c9fe83d65c88f4c8236af1e153cbe981ea6afd"
    }
  ],
  "counts": {
    "citations_verified": "3/3 (denominator: citations in EV-017 CORROBORATES + REFINES addenda per DOI verification report task495_ev017_doi_verification_v1.md)",
    "options_evaluated": "2/2 (denominator: spec options a and b; option c explicitly rejected as not applicable)",
    "tripwire_conditions_assessed": "5/5 (denominator: all actions in Section 6 of memo)",
    "live_sweetener_tiers_in_engine": "3/3 (denominator: SWEETENER_CAP_A/B/C in constants.py)",
    "posture_changes_proposed": "0/1 (denominator: EV-017 should_affect_score_now field — maintained false)"
  },
  "commands_run": [
    {"cmd": "(Get-FileHash 'C:\\Bari\\03_operations\\reports\\nutrition\\task495_ev017_flag_vs_score_recommendation_v1.md' -Algorithm SHA256).Hash.ToLower()", "exit_code": 0}
  ],
  "not_done": [
    "EV-017 registry grounds-language update (recommended in memo; not implemented here — propose-only scope; no D7 required for this change but held for orchestrator routing)",
    "D7 co-sign with Product Agent (not required for flag-maintain recommendation; would be required before any future conversion to score-active)"
  ],
  "self_check": "Spec acceptance test: crux resolved head-on (class-level meta cannot license tier-level score move), single recommendation given (no A/B menu), tripwire assessment complete, falsifiability condition stated. Observed: all four elements present in Section 2, 4, 6, 7 of memo respectively. PASS."
}
```
