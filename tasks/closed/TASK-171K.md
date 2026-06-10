---
id: TASK-171K
title: Hebrew claim-vocabulary fix - dossier umbrella maps
owner: nutrition-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
closed_at: 2026-06-03
cc_reviewed: true
depends_on: []
blocks: []
category_id: null
summary: >
  Nutrition D6 calibration (owner-approved wind-down step 1): expand each of the 15 dossiers' structure_function_umbrella maps to the REAL Hebrew structure/function claims on the Israeli shelf (עייפות/fatigue, ספיגה/absorption, etc. surfaced by the real corpus run) with cited endpoint mappings — incl. EFSA-authorized claims like magnesium->fatigue. Fixes unfair E grades from unmapped Hebrew claims. Candidate; no code; no scraping; improves the banked asset.
---

# TASK-171K — Hebrew claim-vocabulary fix

## CLOSED 2026-06-03 — done + functional + verified
**Nutrition (D6, no code):** expanded `structure_function_umbrella` across the dossiers with Hebrew + EFSA Art.13
claim vocab — **~46 new cited mappings** + cited refusals; 3 dossiers got a first umbrella (vit D3, creatine, omega-3);
caffeine deliberately not authored (Honesty axis, no EFSA claim, mapping "energy"→ergogenic = loophole). Biotin
שיער/עור/ציפורניים kept all-null by design (preserves the loophole-proof cap-1 floor). EFSA-divergence items
(magnesium 'nerve', zinc 'antioxidant', calcium 'muscle', biotin cosmetic) kept consistent with prior ratified D6
(Hebrew mirrors English) — any change needs full D6/D7.

**Orchestrator one-line engine completion (the gating dependency Nutrition surfaced):** the engine tokenizer
`_PUNCT` stripped all non-ASCII → Hebrew tokenized to ∅ → keys inert. Applied the minimal fix
`r"[^a-z0-9֐-׿]+"` (keep the Hebrew Unicode block U+0590–U+05FF) in `score_engine.py`. **Verified:** golden
**17/17 PASS** (no regression — English tokenization unchanged); **`resolve_claim_tier(magnesium, "עייפות")` →
Moderate** (via umbrella, cited), off the wrongful Insufficient/E. *(Not a new sprint — one regex char-class + re-run
existing tests, to make the approved fix functional in the banked asset.)*

**Carried-forward (NOT done — no further sprint per owner):** the 3 first-authored umbrellas (vit D3, creatine,
omega-3) + the tokenizer change are **score-path-creating** → would need **Product D7 + golden re-validation before any
future SHIP**. Recorded in each `change_log` + SUPP-EV. Asset is candidate/banked, so this gates a future revival, not now.

# TASK-171K — Hebrew claim-vocabulary fix - dossier umbrella maps

## Outcome (proposed RETURNED — Nutrition D6, 2026-06-03)

Dossier-authoring only (no code, no scraping, separate tree). Expanded `structure_function_umbrella`
across the SIE dossiers with real Israeli **Hebrew** + **EFSA Article 13** claim vocab, each a **cited
pointer** to an endpoint already tiered in its dossier (no new tiers). All `candidate` /
`should_affect_score_now: false`.

**Coverage:** 11 dossiers got Hebrew/EFSA keys added to an existing umbrella (magnesium, vitamin C, zinc,
iron, calcium, folic acid, B12, melatonin, vitamin E, CoQ10, biotin-as-null); **3 got a first umbrella
authored** (vitamin D3, creatine, omega-3 — score-path-creating, governed like SUPP-EV-006); **caffeine
deliberately NOT authored** (axis is Honesty, no EFSA claim, mapping would be a loophole).

**The corpus fix verified:** `resolve_claim_tier(magnesium, "עייפות")` now → **Moderate** (EFSA
Q-2010-00807 "reduction of tiredness and fatigue" → BP endpoint), off the wrongful E. `"עייפות ותשישות"`
and English `"fatigue"` also → Moderate.

**Gates:** `dossier_loader.load_all()` clean (all 16 load); `run_golden_validation.py` **17/17 PASS**
(no regression).

**⚠ Gating dependency (engine, out of this no-code task):** `score_engine._PUNCT = r"[^a-z0-9]+"` strips
all Hebrew, so Hebrew keys are **inert** until a one-line tokenizer fix preserves the Hebrew Unicode block
(`r"[^a-z0-9֐-׿]+"`). Verified in-memory: with the fix `עייפות`→Moderate; without it, `עייפות`→Insufficient
(magnesium still E). English EFSA keys already resolve. This is a Data engine change with its own D7.

Details + per-active table + EFSA-divergence flags: `evidence_registry/supp_evidence_registry_v1.md`
(TASK-171K addendum); per-dossier `change_log` updated per §5.1.

Proposed status: **RETURNED** (not CLOSED — closing authority is CC/Controller).
