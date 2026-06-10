---
id: TASK-117
title: Consolidate registry SSOT + relocate governance into the Agent OS
owner: product-agent
status: CLOSED
priority: HIGH
created_at: 2026-05-31
completed_at: 2026-05-31
depends_on: [TASK-116]
blocks: []
category_id: null
summary: >
  Establish C:\Bari\tasks as the single authoritative registry; demote the
  second (markdown) registry to a frozen read-only snapshot; relocate Registry
  Protocol, Registry First, and lifecycle governance into the real Agent OS
  (C:\Bari CLAUDE.md + 01_framework/operations) so all agents load them; add the
  Work Classification model (Conversation Work vs Registry Work). No lifecycle
  redesign, no new states, no enforcement/CI. Includes a Jarvis-style dashboard
  visual restyle (presentation only — no behavior change).
---

# TASK-117 — Registry SSOT consolidation + governance relocation

Architecture-validation follow-up (items 1–4). Governance now lives where agents
load it; the dashboard remains derived from the single registry.
