---
id: TASK-562
title: Sucralose heat-dechlorination: Israeli authorisation in baked goods + bearing on scored products
owner: nutrition-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-07-10
depends_on: []
blocks: []
category_id: null
summary: >
  Raised by Red-Team RT-1 (TASK-557, 2026-07-10). EFSA Feb 2026 (DOI 10.2903/j.efsa.2026.9854, PMID 41710869) declined to extend sucralose to fine bakery wares, citing dechlorination at 120-250C forming PCDDs/PCDFs/chloropropanols. Bari's corpus carries sucralose in cakes_hard_cookies and cookies_coffee. Open questions: (1) is sucralose authorised in baked goods under ISRAELI law? (2) does the dechlorination finding bear on any product Bari has scored? (3) any D4/EV consequence? Deliberately EXCLUDED from the consumer guide because neither the hazard nor a reassurance is publicly defensible today. NOT to be published anywhere until answered. Nutrition co-owns with Research.
---

# TASK-562 — Sucralose heat-dechlorination: Israeli authorisation in baked goods + bearing on scored products

<!-- opened with new_task.py; fill in context / scope / the deliverable -->

## Research phase DELIVERED + orchestrator-verified (2026-07-11, unattended run)
Report: `03_operations/reports/research/task562_sucralose_dechlorination_v1.md` (C0 PASS exit 0).
- **Q1 Israeli authorization: UNVERIFIED** — governing reg identified (תקנות בריאות הציבור (מזון)
  (תוספי מזון), תשנ"ו-1996) but every MoH additive sub-page 404/403s post-migration; honest unknown,
  no inference. Label evidence (2 Israeli products with sucralose sold via Shufersal) = circumstantial.
- **Q2 corpus bearing: 6 products carry sucralose** (4/167 cakes corpus, 2/61 cookies corpus).
  **2 are LIVE consumer-facing oven-baked cookies on /hashvaot/cookies-coffee: 311463 (עוגיות חמאה
  ללת"ס, 45.2/D) + 960860015432 (עוגיות ללת"ס מקמח מלא, 46.0/D)** — orchestrator independently
  re-scanned the live JSON: exactly 2/117, barcodes/grades match. 3 protein bars = cold-formed, not
  published; 1 ambiguous (baked sub-component 20%, not published).
- **Q3: EV-109 draft written in the report** (not registered). No score exposure (efsa_no_scoring_exposure
  stands). Copy flag: existing E955 additive explanation ("dose-dependent, authorised at current levels")
  does not reflect EFSA's baked-application finding — needs Nutrition review, then two-gate if copy changes.
- PMID 41710869 verified live; DOI resolves (paywalled — temperature/compound details marked
  UNVERIFIED-DETAIL, honest split).
**NEXT (owner of task = nutrition-agent): adjudicate EV-109 registration + the E955 copy flag.
Nothing published; guide exclusion stands. → owner digest (2 live D-grade products implicated).**

## Dispatch log
- 2026-07-11 03:xx (unattended orchestrate run) — dispatched Research Agent (claude-sonnet pin,
  background). Capability = EVIDENCE-RESEARCH; **fallback activation logged (Router v5 Layer-0
  inv. 6): primary Codex --search SKIPPED — trigger = unattended-run operating constraint; the
  activated fallback IS the router's stated fallback (Research Agent, sonnet).** Read-only
  evidence report; EFSA/ADI never moves a score (standing law) — any scoring implication is
  flag-only for Nutrition + owner.
