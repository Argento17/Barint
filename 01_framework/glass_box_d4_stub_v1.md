# Glass Box D4 — Additive Evidence Dimension (Stub v1)

**Classification:** Internal — Glass Box program (TASK-179)  
**Version:** stub v1  
**Date:** 2026-06-06  
**Owner:** Nutrition Agent  
**Task:** TASK-193 (library seed); TASK-179 (parent program)  
**Status:** Pre-activation. No scoring rule is live. All entries are demand-gated per TASK-179 sequencing (D4 library after D5/D6 + DIAAS ship).

---

## What D4 covers

D4 ("additive MOAT") is the fourth dimension in the Glass Box scoring architecture. It evaluates the additive composition of a product based on the identity and function class of each E-number present, cross-referenced against a tiered evidence library. D4 is a deliberate moat: it is the dimension that makes Bari's additive intelligence hard to replicate from label text alone, because it requires an authoritative, cited, regularly updated reference library — not just E-number counting.

**D4 scores the additive architecture of the food, not the eater.** It never implements per-person ADI × bodyweight calculations. Bari describes the SKU; it does not predict individual exposure (BEV-001; BEV-003e). The D4 output is either an annotation (identity + concern class surfaced to the consumer) or, for entries with a `score_moving_pending_d7` status, a potential scored signal once owner D7 sign-off is obtained.

**Input:** the `food_additives` integration client (`integrations/clients/food_additives.py`) converts a product's `additives_tags` list (sourced from Open Food Facts) into E-number identity, function class, and EFSA evaluation pointer. Paired with `pubchem` for chemical identity disambiguation. This client provides the identity + class + EFSA evaluation pointer only; no ADI numeric value or Israeli-vs-EFSA approval divergence is available without further work (noted as a library limit).

**Output per product:** a list of additive annotations keyed to the tier framework below, surfaced as D4 signals in the consumer explanation layer (Phase 4).

---

## Tier framework and Evidence Registry references

The D4 library is seeded from the "Food additives 1" research document (New Batch, 2026-06-06), which synthesizes EFSA, JECFA, and FDA evaluations across nine additive classes. Four Evidence Registry entries anchor the four tiers:

| Tier | Description | Representative additives | EV-### | D4 Status |
|---|---|---|---|---|
| **Tier 1** | Strong concern — dose-independent sensitivity population; EFSA found high-consumer MOE at risk | Sulfites (E220–228) | BEV-078 | `score_moving_pending_d7` |
| **Tier 2** | Moderate concern — sensitive population signal (hyperactivity in children); EU warning label required | Azo synthetic colorants: tartrazine (E102), Sunset Yellow (E110), Allura Red (E129), Ponceau 4R (E124), Carmoisine (E122) | BEV-079 | `score_moving_pending_d7` |
| **Tier 3 / Emulsifier boundary** | Neutral or annotation-only — approved at use levels with no established human harm; emulsifiers P80/CMC/carrageenan annotate-only (animal signal, 2026 RCT showed ↓SCFA but no rise in inflammation markers) | MSG (E621), sorbates (E200–202), propionates, polyols, acidity regulators; P80 (E432), CMC (E466), carrageenan (E407) | BEV-080, BEV-081 | `annotate_only` |
| **Tier 4** | Beneficial or context-dependent — nutritional value or no safety concern at use levels | Lecithin (E322), natural colorants (beta-carotene E160a, anthocyanins), pectin (E440), bicarbonates (E500) | BEV-081 | `annotate_only` |

---

## Activation gate

**Score-moving entries (BEV-078, BEV-079):** Sulfites and azo synthetic colorants are candidates for a scored D4 rule. Activation requires:
1. A separate, specific scoring rule proposal (co-proposed by Nutrition Agent)
2. Owner D7 sign-off (Nutrition + Product co-sign; either can block)
3. A demand-gate clearance from Product Agent — consumer engagement with the annotation layer must demonstrate demand before converting an annotate-only or pending entry to a scored rule (per TASK-179 sequencing)

**Annotation-only entries (BEV-080, BEV-081):** Tier 3 / emulsifier boundary and Tier 4 additives are informational annotation only. The evidence for P80, CMC, and carrageenan is weak and non-directional as of 2026-06-06; re-evaluation is warranted if stronger human evidence emerges, but this requires a new evidence review and D7 process. These entries do not become score-moving without a new registry entry and co-sign.

**EDPG firewall:** the `food_additives` client and any external source inform the library and calibrate rules (with Evidence Registry citations) but do not feed the engine's score path directly. The engine reads in-house BSIP0 label data only.

---

## What this stub does NOT authorize

- Any change to a published or live score
- Any new scoring rule (each requires a separate D7 co-sign)
- Any consumer-facing claim about additive harm or safety
- Per-person ADI × bodyweight intake logic (permanently excluded — BEV-001; BEV-003e)

---

*Superseded by the full D4 dimension spec when TASK-179 D4 wave ships. Next action: Product Agent to review demand-gate threshold; owner D7 sign-off required per rule before activation.*
