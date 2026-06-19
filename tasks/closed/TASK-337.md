---
id: TASK-337
title: Nutrition claim-safety review of Tom-Bari voice system
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-18
closed_at: 2026-06-19
depends_on: []
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified by full read of content_voice/tom_bari_voice/reviews/
  nutrition_claim_safety_review_v1.md (629 lines, complete). DoD met: all 5 checks answered
  (§9 acceptance table, all PASS); 5 buckets populated (24 approved / 14 needs-product-data /
  5 needs-scientific-source / 13 banned+replacements / 10 publication rules P-1..P-10);
  all 6 grey-zone descriptors ruled with safe forms (פחמימה ריקה → BANNED, replace with
  "בעיקר פחמימה קלה"+numbers; שומן רווי גבוה/סוכר גבוה safe WITH per-100g number; מעובד/מתועש
  safe WITH structural anchor; חלש תזונתית safe WITH named dimensions); E471 "קשר לסרטן"
  block confirmed AND a new data-path gap surfaced (additive-burden EV-003/019 engine data
  could leak EFSA annotations → R-1). Review-only: artifact is a single markdown file, NO
  score/constant/engine/config touched (tripwire-1 clear). Cross-validates TASK-335 (P-7:
  grade-E cannot be Positive — exactly what the draft did). Recommendations R-1..R-4
  (edits to files 5/2) correctly NOT applied — routed to follow-up TASK-338.
---

# TASK-337 — Nutrition claim-safety review of Tom-Bari voice system

Deliverable: reviews/nutrition_claim_safety_review_v1.md. CLOSED on verification. Follow-up:
R-1..R-4 firewall-hardening edits → TASK-338.
