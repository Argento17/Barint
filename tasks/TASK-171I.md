---
id: TASK-171I
title: Scope the local-brand panel-acquisition build (feasibility + cost)
owner: data-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-03
closed_at: 2026-06-03
work_type: research
depends_on: []
blocks: []
category_id: null
summary: >
  Data feasibility probe + Product cost/recommendation synthesis to decide the local-brand panel-acquisition build. Answer: (1) Super-Pharm PDP coverage % with ingredient panels, (2) brand-site coverage % of market, (3) OCR feasibility photo->structured label, (4) cost estimate in DAYS, (5) expected shelf coverage after acquisition. Empirical testing on real samples; no fabrication; candidate only; feeds the owner build-vs-pause business-case call.
---

# TASK-171I — Scope the local-brand panel-acquisition build

**CLOSED 2026-06-03.** Deliverable: `02_products/supplements/local_brand_acquisition_feasibility_v1.md` (Data probe + Product synthesis). Decision-support; nothing shipped; all candidate.

## The 5 answers (measured)
1. **Super-Pharm PDP panels ≈ 0% structured** — marketing + single-active dose in the name only; no per-active table. Good for identity, not a scoreable panel.
2. **Brand-site + third-party e-tailer coverage ≈ 75–85% of the local shelf** — Altman's own site = clean full panels; the **unlock = Israeli third-party vitamin e-tailers** (vitamins4all/biogaya/klilhateva/vitamania, one generic adapter, redundant). Hole = **Life (SP house brand)**, no independent site.
3. **OCR feasible + accurate on a flat back-label, but a FALLBACK** — the sources missing a text panel (SP/Life) are the *same* ones missing a flat panel image → OCR doesn't close the exact gap. Tier-3 + QA cross-check only.
4. **Cost: ~15–19 eng-days full; MVP subset ~8–10 days** (third-party adapter + Altman + source-priority resolver + QA harness = the whole high-confidence band).
5. **Expected coverage: ~75–85% addressable ≈ ~42–48% net** (up from ~20%/~11% iHerb-only). Hard wall = Life house-brand multi-active residue (~18% addressable) → needs a **manufacturer feed (BD ask, not engineering)**.

## Product recommendation: **BUILD, phased**
Ship the **8–10-day MVP adapter** → run the real corpus (measures the true ~31–37%-net first cut) → *then* decide launch. Don't full-commit before measuring (uncloseable Life residue + ongoing claim-curation/maintenance tax); don't pause (banks a cheap proven unlock for nothing). The MVP is a **measurement instrument, not a launch.**
**Stays gated:** category go-live = separate D10/D1 (not made); launch also needs the EDPG candidate→promote D3/D4 gate on real panels + Nutrition D7. Owner-taste/irreversible item = the launch + maintenance commitment, decided after the MVP corpus exists.

# TASK-171I — Scope the local-brand panel-acquisition build (feasibility + cost)

<!-- opened with new_task.py; fill in context / scope / the deliverable -->
