---
name: banked_assets_dashboard_section
description: "Command Center now has a persistent \"Banked Assets\" section for proven-but-not-launched programs (e.g. SIE) so they never vanish from the roadmap at close"
metadata: 
  node_type: memory
  type: project
  originSessionId: 346019e6-3cc4-4339-8323-105c9db28f4d
---

The Command Center dashboard has a persistent **Banked Assets** section (added 2026-06-04, owner directive — "I want to always see these even if not in progress, this is an important initiative"). Problem it solves: a CLOSED task drops out of every `/roadmap` bucket, so a proven-but-parked program (banked, not launched) becomes invisible. Banked assets now stay on the board forever.

**Source of truth = the registry, not hand-edited JSON.** Tag the task by adding a `banked_asset:` block to its `C:\Bari\tasks\TASK-*.md` frontmatter:
```yaml
banked_asset:
  one_liner: "..."
  why_parked: "..."
  revival_gate: "..."
  reference: "path/to/closure_record.md"
  banked_at: "YYYY-MM-DD"
```
`generate_dashboard.py` → `compute_banked_assets()` collects every task carrying the block into `banked_assets` (in `command_center.json`, `command_center_live.json`, the `--digest`, and the HTML board). Survives CLOSED-task trimming because it's its own top-level section.

First (and currently only) entry: **TASK-171 — Supplement Intelligence Engine (SIE)**, banked 2026-06-03. Canonical record: `03_operations/supplement_engine/SIE_ASSET_AND_CLOSURE.md`. See [[supplement_engine_sie_task171]].

**Why:** strategic assets that are proven but parked on a business-development gate (not an engineering shortfall) must stay visible for revival; the in-flight roadmap buckets structurally hide them.
**How to apply:** to bank a future program, add the `banked_asset:` block to its umbrella task and regenerate. To revive, follow its `revival_gate`.
