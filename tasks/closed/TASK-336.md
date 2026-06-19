---
id: TASK-336
title: Harden Tom-Bari voice-match gate into production checklist
owner: qa-agent
status: CLOSED
priority: MEDIUM
created_at: 2026-06-18
closed_at: 2026-06-19
depends_on: []
blocks: []
category_id: null
close_reason: >
  Orchestrator-verified by full read of content_voice/tom_bari_voice/7_voice_match_gate.md
  (346 lines). DoD met: 5 HARD FAILURES (HF-1 phrase-overuse with a >2/5 sliding-window
  threshold + the 5 named signature moves; HF-2 wrong-mode with numeric thresholds both
  directions, aligned to fingerprint §2; HF-3 generic-review swap test, ≥2 specific-facts
  floor; HF-4 unverified-fact 3-step detection sequenced with file-5 Tier-B; HF-5
  user-facing clutter, grep -c "דורש אימות"=0 in publication) — each with a checkable
  criterion. Compact pass/fail rubric table (8 states). One worked failing→corrected
  cereals example (Hebrew) tripping HF-2A/HF-3/HF-5 and clearing all. Integration point
  sequenced after the file-5 mechanical gates, before the Tom-edit loop, with shelf-level
  HF-1 + publication-mode HF-5 timing. Existing 14 checklist items preserved. Lane =
  C1-Sonnet (completed before session limit). Bonus: HF-1 independently confirms the
  TASK-335 draft's signature-overuse finding.
---

# TASK-336 — Harden Tom-Bari voice-match gate into production checklist

Deliverable: hardened content_voice/tom_bari_voice/7_voice_match_gate.md. CLOSED on verification.
