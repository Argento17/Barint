---
id: TASK-338
title: Apply Nutrition claim-safety hardening R-1..R-4 to voice firewall (files 5/2)
owner: content-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-19
closed_at: 2026-06-19
depends_on: []
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified by grep/read of both artifacts. R-1 additive-data-path Tier-B bullet
  present in 5_banned_phrases_and_claims.md §2 (grep EV-003/EV-019 = 1); R-2 never-bullet
  present in 2_voice_fingerprint.md §6 (grep "EFSA evaluation pointers" = 1); R-3 פחמימה ריקה
  banned-row present in file 5 §1 table; R-4 new §4 "Publication-mode additional requirements"
  with 10/10 P-rules present (grep "^### P-" = P-1..P-10, faithful to review §7). Existing
  content in both files preserved (verified — §1 table, §2 Tier-A/B, §3 gate order, file-2
  §1-§8 all intact). NO score/engine/config/product-JSON touched (the dirty 03_operations
  additive_burden + bari-web gates_report paths predate this conversation; not 338's).
  Tripwire-1 clear. Lane = C1-Sonnet (owner approved Sonnet for these voice cases; session
  limit had reset).
---

# TASK-338 — Apply Nutrition claim-safety hardening R-1..R-4 to voice firewall (files 5/2)

Deliverable: hardened files 5 + 2. CLOSED on verification. The voice firewall now blocks the
additive-data-path leak (engine EFSA/risk annotations) and carries explicit publication-mode rules.
