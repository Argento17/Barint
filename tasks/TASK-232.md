---
id: TASK-232
title: "Salty-snacks v4 golden-standard QA audit — leakage, propagation, rank-order/protein sanity, copy compliance"
owner: qa-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-10
depends_on: [TASK-228]
blocks: []
roadmap_impact: true
work_type: qa-audit
---

# TASK-232 — Salty-snacks v4 golden-standard QA audit

Owner: "check with our golden standards. this is really off." Audit the shipped salty-snacks v4
(`bari-web/src/data/comparisons/salty_snacks_frontend_v4.json`, page `/hashvaot/salty-snacks`)
against the QA Agent pre-launch checklists (leakage / drift / rank-order / propagation / build).

## Known defects to confirm + anything else (be exhaustive)
- LEAKAGE: "NOVA 4" appears in consumer `limitingFactors` copy (banned term) — confirm scope across corpus.
- RECOMMENDATION: bottomLine "עדיף לבחור..." (prescriptive) on ~13 products — confirm.
- DATA: garbled ingredients (במבה יום הולדת), English ingredients (פריכיות תירס), null sodium on
  a salty snack (אפרופו 50 ג'), 8 duplicate Bamba SKUs, brand field garbage (Some/Same/اوسم).
- SCORING SANITY: 2 products at exactly 0/E incl. a decent-macro health cracker (פיטנס קרקר דק סלק
  — 6.5g fiber/12g protein yet 0/E). Run the rank-order sanity check; flag inversions. The owner
  also challenges that protein is under-rewarded in this category — verify against ≥3 known-better pairs.
- DISPLAY: metric bar values were rendering unrounded (7.66666666666667) + overlapping — a fix was
  applied (`formatMetricValue` in comparison-metric-column.tsx); confirm the fix renders correctly.
- Run the offline `hebrew_readability.is_clean` gate on all consumer strings.

## Output
A PASS / CONDITIONAL PASS / FAIL verdict with itemized failures (exact values, product IDs). Per
QA Hard Rules: do not fix, do not redesign — identify and route. This audit defines the bar the
TASK-230 (copy) + TASK-231 (data) + TASK-229 (scoring) remediations must clear before re-QA.

## Acceptance criteria
- [ ] Leakage checklist run; every "NOVA"/framework instance itemized with product ID
- [ ] Recommendation-language instances itemized
- [ ] Rank-order sanity (≥3 known-better pairs) incl. the protein-reward challenge — inversions flagged
- [ ] Score propagation + build/route checks run
- [ ] Verdict issued with named blockers routed to owning agents
