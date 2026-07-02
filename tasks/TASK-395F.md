---
id: TASK-395F
title: Data-integrity firewall: ingredient-field sanitation gate + provenance contract
owner: data-agent
status: IN_PROGRESS
priority: HIGH
created_at: 2026-06-26
depends_on: []
blocks: []
backlink: "BACKWARD CLEAN DELIVERED by TASK-405 (2026-06-26): 473 BSIP1 files de-polluted via proven sanitize_ingredient_list, pollution 28.6%->14.7%, 8 barcodes verified, 5 flagged-for-rescrape; clean_report.json manifest. RT-3 (חומר משמר lexicon)=TASK-407, owner assigned to other/de-chain chat. REMAINING (de-chain chat): forward C0 sanitation+provenance GATE at one page-generator point; RT-1 WITHHELD->null grade."
category_id: null
summary: >
  Validation triad (C3 + Gemini + Red-Team) BLOCKED the de-chain candidate on DATA QUALITY, not scoring logic. Root finding: 15.1% of products (47/311 with text) have ingredient-field pollution (nutrition-panel/disclaimer/serving text bleeding into the ingredients field, concentrated in cheese); this pollution wrongly drove the single largest mover (cottage 7290014758681 -21.7, real label = milk/salt/calcium = 3 items, parsed as 6) and a ceiling-victim inversion. Two parts: (A) deterministic C0 ingredient-field SANITATION (strip non-ingredient content before parse/confidence) + a detector that FLAGS/escalates still-suspicious fields rather than silently scoring (owner 'raise imperfect reads'); (B) PROVENANCE CONTRACT - every published score persists corpus run_id + FULL flag vector (incl. patches like D4) + engine version, with a C0 gate refusing to publish a score that can't round-trip to its committed hash (fixes the D4-unrecorded / NULL-run_id / wrong-corpus / granola v1-v2 / uncovered-route leaks by construction). Enforce both at ONE page-generator point. Prereq to a trustworthy re-shadow. Also fix RT-1 (WITHHELD string -> null grade) + RT-3 (lexicon gap: add 'חומר משמר' alongside 'חומר שימור').
---

# TASK-395F — Data-integrity firewall: ingredient-field sanitation gate + provenance contract

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
