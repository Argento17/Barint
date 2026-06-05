---
name: project-bsip0-structure
description: BSIP0 project-level directory layout and architectural separation rules
metadata: 
  node_type: memory
  type: project
  originSessionId: 41dec126-e15e-427c-a7d2-e5e93bc10a54
---

Canonical project root: `C:\Bari\bsip0_scrape\`

```
C:\Bari\bsip0_scrape\
  bsip_freezes\          # immutable milestone snapshots — bsip0_v0_2\, bsip0_v0_3\, ...
  carrefour\             # retailer-specific runtime, scripts, and outputs only
  yohananof\             # retailer-specific runtime, scripts, and outputs only
  bsip0_core\            # (future) shared utilities imported by all retailers
  schemas\               # canonical BSIP schema/contract definitions
  docs\                  # architecture reviews, changelogs, contracts
  retailer_capabilities\ # one YAML per retailer (living copies, updated on each freeze)
```

**Why:** Frozen BSIP versions are project-level artifacts, not retailer-local runtime outputs.

Rules:
1. `bsip_freezes/` — immutable only. Never write runtime output here.
2. Retailer folders (`carrefour/`, `yohananof/`) — retailer-specific scripts and outputs only.
3. `docs/` — architecture reviews, changelogs. Not per-retailer READMEs.
4. `retailer_capabilities/` — one YAML per retailer (e.g. `carrefour.yaml`). Living copies updated on each freeze.
5. `schemas/` — canonical BSIP schema contracts only.
6. Do NOT nest `outputs/frozen/runtime/temp/` deeply inside retailer folders.

**Why:** Approved in session, May 2026. Previous structure had `carrefour/outputs/frozen/bsip0_v0_2/` which was wrong — freezes belong at the project root.

Freeze scripts (e.g. `06_freeze_v0_2.py`) must:
- Set `PROJECT_ROOT = Path(__file__).resolve().parent.parent` (step up from retailer dir)
- Write to `PROJECT_ROOT / "bsip_freezes" / VERSION`
- Place living copies at `PROJECT_ROOT / "retailer_capabilities" / "RETAILER.yaml"` and `PROJECT_ROOT / "docs" / CHANGELOG`
