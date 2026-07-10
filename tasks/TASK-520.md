---
id: TASK-520
title: Ingredient-text truncation/malformed-bracket defects in protein_combined, juices, hummus, cookies_coffee
owner: data-agent
status: IN_PROGRESS
priority: MEDIUM
created_at: 2026-07-05
depends_on: []
blocks: []
category_id: null
summary: >
  Discovered as a side-effect of fixing a false-positive in validate_comparison_page.py's ingredient gate (crackers merge, 2026-07-05): protein_combined_v2 has multiple ingredient strings truncated at exactly 300 chars mid-word (fixed-length scrape/store cap suspected); juices_v3 barcode 7290019056355 and hummus_v5 barcode 7290105964564 plus some cookies_coffee_v2 records have malformed unbalanced-paren nests, never closed. These end on a Hebrew letter with no trailing separator so the current gate (old or fixed) doesn't catch them -- found by a QA agent manually inspecting strings, not by an automated check. Needs: (1) root-cause the 300-char cap in protein BSIP0/BSIP1 storage, (2) fix the malformed-paren scrapes for the specific flagged barcodes, (3) consider whether the ingredient gate needs a new unclosed-paren/fixed-length-cut check as a separate, reviewed enhancement (deliberately not added inline to avoid scope creep in the gate-tooling fix that found this).
---

# TASK-520 — Ingredient-text truncation/malformed-bracket defects in protein_combined, juices, hummus, cookies_coffee

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
