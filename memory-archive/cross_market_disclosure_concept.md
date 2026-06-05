---
name: cross-market-disclosure-concept
description: "Glass Box Wave 3 candidate — surface external market disclosure gaps (added sugar, protein source, sweetener identity) as a trust/confidence feature; no score movement; matching-precision spike required before any roadmap commitment"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3286383b-7366-418e-ae10-fd8bd578bf37
---

**Cross-Market Disclosure** = a D5 external-corroboration annotation that surfaces what an equivalent US/EU product discloses that the Israeli label does not. Approved concept, Wave 3 candidate, no implementation now.

**Why:** explict D5/D6 enrichment — Israeli label stays authoritative, no score or grade changes, no identity assertion. Framed as a **trust feature**, not transparency: "Bari found additional information elsewhere. Bari is not claiming the products are identical. Bari is not changing the score. Bari is showing its work." Strengthens methodology credibility.

**Governance posture (owner-ratified, 2026-06-04):**
- Non-disclosure never moves the headline grade (DEC-006 Q2 holds)
- Routes only through D6 confidence (annotate + demote flag, never a quality penalty)
- Never attributes intent ("לא נוקד" framing, not "היצרן מסתיר")
- EDPG firewall applies: external data = candidate, quarantined, never scoring input

**Use-case ranking (owner-confirmed):**
1. Added sugar — US mandates Added Sugars line; Israeli labels collapse to total
2. Protein-source composition — supplements/protein powders ("תערובת חלבונים" → whey/collagen/pea split)
3. Sweetener identity — generic polyol vs named NNS (dose-dependent D4 tier)
4. Additive specificity — "צבעי מאכל" → named E-numbers (feeds D4 disclosure-gap tier)
5. Proprietary blends / flavor systems

**Infrastructure already available (TASK-170):** DSLD (US supplement labels), OFF (multi-market panels), il_gov_data (imported-foods identity), PubChem (additive identity), provenance stamping (fetched_at).

**Entry gate (hard requirement before any wave commitment):** matching-precision spike on ~50 supplement/protein SKUs via DSLD + il_gov_data + OFF. If false-match rate is not extremely low, **terminate the concept** — precision is load-bearing.

**Roadmap position:**
- Not Wave 1 (would break W1's cheap/unfalsifiable/label-only property)
- Not Wave 2 (unrelated to additive prototype)
- Wave 3 candidate — conditional on D5/D6 live + engagement instrumented + spike passing
- First implementation surface: SIE (supplements) — highest value density, cleanest US data (DSLD), "proprietary blend" concealment is endemic

**Current priority is unaffected:** D5 Transparency → D6 Confidence → protein-quality/DIAAS → additive prototype (all Wave 1/W1.5/W2).

**Why:** Relates to [[glass_box_engine_program_task179]], [[supplement_engine_sie_task171]], [[external_integration_layer_task170]].
**How to apply:** When SIE advances toward W3-readiness, surface this concept for the matching-precision spike. Do not allocate work or create a sub-task until that gate.
