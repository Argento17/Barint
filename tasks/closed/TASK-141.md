---
id: TASK-141
title: "Cottage/White Cheese governance stress test (must reach B before any scrape)"
owner: product-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-01
completed_at: 2026-06-01
close_reason: "RETURNED block + PO ratification both filed"
depends_on: []
blocks: [TASK-142]
category_id: cheese_spreads
summary: >
  Cottage/white-cheese (cheese spreads) has no governance stress test yet. Per Product Owner decision (locked
  2026-06-01) the category must reach verdict B BEFORE any BSIP0 scrape — same gate cereals passed. Define
  sub-pools (cottage / cream cheese / labaneh / white-quark) per Constitution Sec 2.9, the 'light' threshold
  per Guardrails D6 / Sec 5.2.1, and any endemic distortions per Sec 6.4. Run the standard stress test;
  resolve gaps via targeted amendments (cereals precedent — no new frameworks). Reports verdict to Product Owner.
---

# TASK-141 — Cottage/White Cheese governance stress test

Mirrors the cereals stress-test -> gap-resolution pattern (category_audit_cereals_v1 -> cereals_gap_resolution_v1).
Research Agent supports with evidence; Nutrition rules on sub-pool boundaries + thresholds.

## Required definitions (gaps to close to reach B)
- **Sub-pools** (Sec 2.9 Architectural Divergence): cottage vs cream cheese vs labaneh vs white-cheese/quark
  — these differ structurally (fat, set, fermentation) and should not share one ranking pool by default.
- **'Light' threshold** (Guardrails D6 / claim threshold table 5.2.1): when may a cheese claim "light"/reduced-fat.
- **Endemic distortions** (Sec 6.4): fat-reduction-via-additives or salt as a probable endemic distortion.
- **Fermentation credit** — coordinate with TASK-139B (shared dairy culture vocab).

## Deliverable
`01_framework/governance/cheese_spreads_stress_test_001.md` (+ gap_resolution if verdict < B).
Verdict reported to Product Owner. **Gate: TASK-142 cheese pipeline does not start until verdict >= B.**

## State
Proposes RETURNED on verdict delivery (only Central Controller records CLOSED).

---

## Return block — proposed RETURNED (product-agent, 2026-06-01)

**Deliverable:** `01_framework/governance/cheese_spreads_stress_test_001.md` — full stress test, gap analysis, targeted amendments, reassessment.

**Verdict: B — Yes, with Conditions.** HARD GATE SATISFIED → TASK-142 may proceed once the Section 9 conditions are met. Mirrors the milk dairy precedent (B-with-conditions in one doc), above cereals' C because every framework cheese needs already exists post-cereals/milk — cheese required *calibration*, not new frameworks.

**Four gaps, zero missing-framework:**
1. **Sub-pools (Sec 2.9, SIGNIFICANT):** the granola-calibrated proxies separate the cream-cheese pool but NOT cottage/white-cheese/labaneh (intrinsic dairy fat, not added) — the exact milk Sec 8.1 limitation. Resolved by **Resolution 1**: additive Sec 2.9 amendment adding a *dairy structural divergence axis* (set / protein tier / fermentation / intrinsic-fat tier) + a four-pool cheese standing precedent (Cottage / White-cheese-quark / Labaneh / Cream-cheese-spread; fat tiers = variants, not pools).
2. **'Light' threshold (Sec 5.2.1 / D6, critical-as-condition):** the dominant claim is D6-blocked (no reduced-fat row), identical to milk. Resolved by **Resolution 2**: new 5.2.1 row — **≥25% fat reduction vs. same-sub-pool standard reference** (relative) or ≤3g/100g (absolute). Reference must be the same sub-pool (5% white cheese is the default, not "light" vs itself). **Needs Tom ratification** (framework-level claim threshold per cereals whole-grain precedent).
3. **Endemic distortion — fat-reduction-via-additives + salt (Sec 6.4):** maps to **existing** DISTORTION-006/009/010 (no new entry); two scopes (category-wide sodium/sat-fat = DISTORTION-010; pool-specific light reformulation = 006/009). Sec 6.4 needs **no amendment** — the milk multi-pool clarification is already live. **Resolution 3**: two disclosure texts drafted for Product approval.
4. **Fermentation (coordinate 139B):** RESOLVED by existing work — EV-015 bonus, now *detectable* via TASK-139B/EV-022 culture-vocab; A-ceiling via EV-021/RULING-DAIRY-A-01 (clean live-culture labaneh → A-eligible; stabilizer light cream cheese fails C2). **Resolution 4**: coordination note only.

**Guards honored:** No new frameworks. No published scores changed, no scoring redesigned. All amendments additive. CLAUDE.md frozen invariants untouched.

**Product Owner decisions owned:** (a) ratify reduced-fat/light threshold (Tom); (b) approve two Sec 6.4 disclosure texts; (c) authorize applying Resolution 1 to the Constitution. Until (a), the "light" claim stays D6-blocked (safeguard functioning, not a failure).

**Proposing RETURNED.** Only the Central Controller records CLOSED.

---

## Product Owner ratification — 2026-06-01

All three governance decisions ratified and **applied to the live documents**:
- **Resolution 1 (four dairy pools)** — APPROVED. Applied to Constitution Sec 2.9 (dairy intrinsic-fat divergence axis + cheese-spreads standing precedent: Cottage / White-cheese-quark / Labaneh / Cream-cheese-spread; fat tiers = variants).
- **Resolution 2 (light threshold)** — RATIFIED as **≥25% fat reduction vs. same-sub-pool reference, relative-only** (absolute ≤3g/100g explicitly not used as primary). Applied to Guardrails Sec 5.2.1; also unblocks the milk "light milk" D6 block (defined at dairy level).
- **Resolution 3 (Sec 6.4 disclosure texts)** — both APPROVED (category-wide sodium/sat-fat; pool-specific reduced-fat reformulation); to be wired into the cheese page at TASK-142.

**Gate status:** TASK-142 governance blocker (verdict ≥ B) is **CLEARED**. TASK-142 remains gated only on TASK-139 (dairy calibration) per its own `depends_on`. Central Controller to record CLOSED.
