---
id: TASK-174
title: "Nutrition Expert Partnership Presentation — boardroom-grade deck for senior-scientist evaluation"
owner: chief-nutrition-officer
status: CLOSED
priority: MEDIUM
created_at: 2026-06-03
completed_at: 2026-06-03
close_reason: "Presentation is in good state"
depends_on: []
blocks: []
category_id: null
work_type: content
roadmap_impact: false
cc_comments:
  - date: 2026-06-03
    flag: fyi
    text: "Deliverable built: 43-slide deck (10 sections + cover + 5 appendix) at presentations/nutrition_partnership/ — Bari_Nutrition_Partnership.pptx (16:9, branded) + _spec.md (slide-by-slide: title/objective/key-messages/visual/notes) + build_deck.py (single source of truth, regenerable). All figures grounded in real artifacts: live frontend corpus (bread 24 A3/B18/C3, cheese ~52, hummus 64, maadanim 84, snacks 18, yogurt 11 → 250+ curated), TASK-170 (10 external clients), TASK-171 (SIE), evidence ids EV-024/EV-029/COV-006, frozen milk run_004. No invented product/nutrition data. NEEDS owner/CNO content review before external use."
  - date: 2026-06-03
    flag: fyi
    text: "Owner review pass v3 (43→25 slides). Applied: (1) page numbers on every slide; (2) slides 1–6 untouched; (3) fixed trust chart (slide 7 — smaller arrow, no text-on-text); (4) MARKETPLACE/commerce added as a 4th pillar across the board (What Bari is, Three-audiences slide, 5yr roadmap Yr4, monetization now 6 stages w/ commerce=step4) — integrity guardrail kept: monetise the transaction never the grade; (5) fixed flywheel infographic (slide 16, clean ring + small arrows); (6) redrew hummus chart as a clear 2-region decision diagram (slide 19); (7) KILLED cereals+dairy examples (old 21–22); (8) explained all cryptic codes in plain English (EV-029/EV-024/COV-006 → described, not coded) on rigor/yogurt/milestones; (9) KILLED Why-We-Win section + moats (old 26–27); (10) rebuilt monetization staircase (slide 25, 6 clean steps); (11) KILLED role-of-expert + opportunities + closing + appendix (old 30–43) per explicit owner instruction (confirmed via question: 'cut exactly as said' — deck now ends on Monetization, no ask/close). Cut slides preserved in source via skip=True (one edit to restore). Sections renumbered 1–6. Validated: 25 slides, master-logo+per-slide logo 25/25, page# 25/25, 12 visuals embedded, 0 overflow. Canonical .pptx now current."
  - date: 2026-06-03
    flag: verify
    text: "OWNER FLAG (non-blocking): deck now ends on the Monetization staircase — there is no closing slide and no explicit role-of-expert / ask, because slides 30–43 were cut on explicit instruction. The original brief called role-of-expert the 'most important section.' If a closing/ask is wanted later, the cut slides are intact in build_deck.py (skip=True) and restore in one edit."
  - date: 2026-06-03
    flag: fyi
    text: "v2 update per owner: (1) Bari logo (faithful wordmark+signal-mark repro in assets/logo_{light,dark}.png) added to the slide MASTER + every one of the 43 slides; (2) 18 real branded VISUALS generated via make_visuals.py (matplotlib, brand palette) and embedded — incl. real-data charts (live grade-distribution per category, yogurt A=0 ceiling, cereals 27.2% fortification) + diagrams (BSIP0→1→2 pipeline, 5yr roadmap, rigor stack, moat flywheel, monetization staircase, expert review loop, 90-day swimlane, EV-029 timeline, closing pyramid). Validated: 0 image overflow, logo on 43/43, master pic=1. Saved as Bari_Nutrition_Partnership_v2.pptx because the canonical .pptx was open/locked in PowerPoint — swap to canonical name once closed (rerun build_deck.py)."
summary: >
  Boardroom-quality slide-by-slide deck for a senior nutrition scientist evaluating a long-term
  Bari partnership. 10 requested sections (Problem, Vision incl. 5-year arc, What We Built,
  Scientific Depth w/ real rulings, Progress, Why We Win, Monetization, Role of Expert,
  90-day Opportunities, Closing) + deep-BSIP appendix. Authored as a single Python source of
  truth that emits BOTH an editable .pptx and a markdown spec (title/objective/key-messages/
  suggested-visual/speaker-notes per slide). Investor-grade tone, rigor-forward, no fluff;
  every number traced to a real repo artifact. Deliverables in presentations/nutrition_partnership/.
---

# TASK-174 — Nutrition Expert Partnership Presentation

## Deliverable
- `presentations/nutrition_partnership/Bari_Nutrition_Partnership.pptx` — 43 slides, 16:9, branded.
- `presentations/nutrition_partnership/Bari_Nutrition_Partnership_spec.md` — full slide-by-slide spec.
- `presentations/nutrition_partnership/build_deck.py` — regenerable single source of truth.

## Grounding (no invented data)
Live frontend corpus counts/grades; TASK-170 (10 live external clients); TASK-171 (SIE);
evidence registry EV-024 (yogurt culture propagation), EV-029 (cheese fat-overwrite),
COV-006 QA guard; frozen milk run_004 (85/A) invariant.

## Open items / next
- CNO/owner content pass for tone + any claim they want softened/strengthened before external use.
- Optional: drop real screenshots into the VISUAL placeholders (comparison page, Command Center).
