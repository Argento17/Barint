---
id: TASK-528
title: verify_citations.py domain-word heuristic false-positives on non-food/supplement medical literature (GLP-1/incretin body-composition papers)
owner: data-agent
status: IN_PROGRESS
priority: LOW
created_at: 2026-07-08
depends_on: []
blocks: []
category_id: null
summary: >
  The C0 citation-fabrication gate correctly resolves real PMIDs (title/journal/year/author all match) but flags them MISMATCH when the resolved title lacks a nutrition/food domain keyword the heuristic expects -- confirmed false-positive on PMID 41877354 (real 2026 Diabetes Obes Metab paper, Eisa et al., topic = incretin/GLP-1 lean-mass, correctly resolved by the tool itself but mislabeled MISMATCH for lacking food-domain words). Surfaced during TASK-504A RT-2 evidence verification. Not a fabrication-detection failure (0 actual fabrications missed this session) -- a false-positive class on medical/pharma literature adjacent to but not strictly 'food' topically. Fix: broaden the domain-word list or add a medical/pharma-literature allowlist path.
---

# TASK-528 — verify_citations.py domain-word heuristic false-positives on non-food/supplement medical literature (GLP-1/incretin body-composition papers)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
