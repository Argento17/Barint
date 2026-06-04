---
id: TASK-179Q
title: "Glass Box W2 — additive prototype research: ~20 shelf-frequent additives, evidence dossiers, tier co-sign"
owner: research-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-04
depends_on: [TASK-179]
blocks: []
category_id: null
roadmap_impact: true
work_type: execution
cc_reviewed: 2026-06-04
completed_at: 2026-06-04
cc_comments:
  - flag: fyi
    date: 2026-06-04
    note: >
      All 4 phases complete. additive_prototype_set_v1.md (57KB, 743 lines) verified:
      420-product frequency scan across hummus/maadanim/bread, 20 additive dossiers with
      full EFSA/PubChem/literature evidence, all 20 tiers assigned by Nutrition
      (6 functional / 6 likely-neutral / 4 dose-dependent / 3 contested / 1 disclosure-gap /
      0 confirmed-negative), DEC-006 violations corrected (BHA + benzoate), Nutrition co-sign
      + Product D7 co-sign both in file. Three flagged gaps resolved: CMC→contested (Chassaing
      2021 RCT regulatory lag documented), caramel color→disclosure-gap (class I vs IV not
      disclosed on Israeli labels), potassium sorbate→likely-neutral (2026 cohort noted,
      EFSA ADI unchanged, reassessment flag attached). MVP scope hummus+maadanim confirmed.
      BHA contested (not confirmed-negative) confirmed. Product D7 co-sign complete 2026-06-04.
      Roadmap impact: additive_prototype_set_v1.md is the methodology foundation; the W2
      prototype build cannot open until this + TASK-179R are both closed. 179R is CLOSED.
      This task gates the W2 prototype build task (not yet opened).
summary: >
  W2 research phase of Glass Box. No code in this task. Research identifies ~20 additives
  appearing most frequently across the hummus + maadanim + bread BSIP0 corpora (data in hand),
  builds per-additive evidence dossiers via PubChem + EFSA OpenFoodTox + literature client
  (TASK-170), and Nutrition assigns each to one of the 6 evidence tiers. Nutrition + Product
  co-sign the tier sheet. Output: additive_prototype_set_v1.md (20 additives, tier, evidence
  summary, one-line Hebrew consumer explanation draft per additive). This is the methodology
  foundation the W2 prototype build cannot start without.
---

# TASK-179Q — Glass Box W2: additive prototype research

Part of TASK-179 (Glass Box). Runs in parallel with TASK-179P (W1.5 DIAAS) and
TASK-179R (W2 engagement gate spec). The prototype build task opens only after this
task and TASK-179R are both complete and the engagement gate spec is accepted.

**No code, no score movement in this task.**

## Scope

### Phase 1 — Frequency scan (research-agent)
Extract the ~20 most shelf-frequent additives from existing BSIP0 corpora:
- Hummus (TASK-150 / batch_run_hummus corpus)
- Maadanim (TASK-149 / batch_run_maadanim corpus)
- Bread (real_bread_retail_003_v1)
Cross-reference against existing ingredient_taxonomy.py named-additive list (TASK-133).
Target: 20 additives that (a) appear on ≥ 3 products in the combined corpus and
(b) span at least 4 different evidence tiers to make the prototype tier system visible.

### Phase 2 — Evidence dossiers (research-agent)
For each of the ~20 additives, build a structured dossier:
- Identity: E-number, IUPAC name, common Hebrew name
- Function: technological role (emulsifier / preservative / color / texture / etc.)
- Evidence: EFSA OpenFoodTox evaluation + JECFA (if applicable) + FDA GRAS status +
  1–3 key literature citations via literature client (PubMed/EuropePMC/OpenAlex)
- Dose signal: is there a meaningful dose-response at realistic food exposure?
- Israeli label disclosure: does the Israeli label name it explicitly or hide it
  behind a category term (e.g., "חומר מייצב")?

### Phase 3 — Tier assignment (nutrition-agent)
Nutrition assigns each additive to one of the 6 evidence tiers:
1. **confirmed-negative** — weight-of-evidence harm at realistic exposure (e.g., trans fat)
2. **contested** — genuine scientific disagreement, not manufactured doubt
3. **dose-dependent** — safe at label-typical exposure, concern at high/repeated dose
4. **functional** — nutritional / fermentation / preservation role with neutral/positive evidence
5. **likely-neutral** — no meaningful evidence of harm or benefit at label-typical exposure
6. **disclosure-gap** — insufficient evidence to classify; Israeli label hides identity

For each additive: tier + one-sentence rationale + one-line Hebrew consumer explanation draft.
Hebrew explanations: plain language, no attribution of intent, no alarm framing for
contested/dose-dependent (consistent with DEC-006 posture).

### Phase 4 — Co-sign (nutrition-agent + product-agent)
Nutrition co-signs the full tier sheet. Product co-signs for MVP scope confirmation
(are these 20 the right set? is hummus+maadanim the right pilot?) and accepts/adjusts
the aggregate contested-additive ceiling constraint (DEC-006 Q3: sum of contested
additives ≤ ~1 grade band aggregate impact).

## Guardrails
- No code or engine changes in this task.
- No intent attribution in Hebrew explanations (confirmed by Content before W2 build).
- Tier assignments must be evidence-anchored; each requires ≥ 1 registry-level source.
- Product co-sign is required before the W2 prototype build opens.
- Pilot category (hummus + maadanim) confirmed in W0; adjust only if Product calls it here.

## Deliverables
1. `01_framework/glass_box/additive_prototype_set_v1.md` — Research + Nutrition
   - 20 additives × (identity / function / tier / evidence summary / Hebrew draft)
2. Nutrition co-sign (signature block in the doc)
3. Product co-sign (MVP scope + pilot category confirmed)

## Return block (when complete)
Research returns frequency scan + dossiers to Nutrition. Nutrition returns tier sheet to
Product for co-sign. Final return to orchestrator with additive_prototype_set_v1.md
co-signed and ready to hand to the W2 prototype build task.
