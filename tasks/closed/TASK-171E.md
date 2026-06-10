---
id: TASK-171E
title: Claim-resolution amendment (v1.3) - vague structure/function claims
owner: nutrition-agent
status: CLOSED
priority: HIGH
created_at: 2026-06-03
closed_at: 2026-06-03
cc_reviewed: true
depends_on: []
blocks: []
category_id: null
roadmap_impact: true
summary: >
  Author methodology v1.3: replace the §2.1 'vague claim -> Insufficient' default with claim-resolution via an authored dossier umbrella-map (moderate posture); add §5 structure_function_umbrella schema; confirm §2.4 Honesty catches over-specific over-promises; populate magnesium's umbrella map with cited endpoints; specify 3 golden fixtures (vague-but-evidenced / vague-snake-oil / over-specific-false-claim). Nutrition D6 author -> Data implements engine -> Product D7 co-sign. Moves the real magnesium PoC E->B. Owner-approved posture: moderate (fair but skeptical).
---

# TASK-171E — Claim-resolution amendment (v1.3) - vague structure/function claims

## Deliverable (Nutrition D6 authoring — 2026-06-03)

**v1.3 D6-AUTHORED. Proposed status: pending Product D7 co-sign + Data engine implementation. NOT closed.**
This amendment **moves a real grade** (magnesium PoC E/34 → expected B/A), so per Hard Rule 8 it requires Product D7 co-sign before it ships. Everything stays `candidate` / `should_affect_score_now: false`.

### Authored artifacts
- **Methodology v1.3** (`01_framework/supplement_framework/methodology_v1.md`):
  - §2.1 — claim-resolution procedure replaces "vague claim → Insufficient" default; defines the moderate "plausibly maps" boundary (recognized physiological correlate + pre-authored + cited; deterministic engine = exact umbrella key-lookup).
  - §2.4 — over-promise catch confirmed (over-specific lie → Honesty claim-gap + resolves to real Weak tier; not a loophole).
  - §5 — `structure_function_umbrella` schema added (firewall membrane; `mappings[]` + `resolves_to: null` for deliberate non-mapping).
  - §13.4 — three golden fixtures specified (R1 vague/evidenced→B/A; R2 vague/snake-oil→E; R3 over-specific-false→D) + cross-fixture invariants.
  - Header → v1.3; Changelog entry; §11 decision item #12.
- **Magnesium umbrella** (`03_operations/.../evidence_dossiers/magnesium.yaml`): authored against live `literature` evidence — heart→BP **Moderate** (maps, best), bone→BMD **Weak**, muscle→sarcopenia **Weak**, nerve→**null (does NOT map)**. Resolves PoC to Moderate → expected B/A.
- **Registry** (`03_operations/.../evidence_registry/supp_evidence_registry_v1.md`): `SUPP-EV-006` added (rule + magnesium mappings; D6-authored, Product D7 PENDING).

### Open / handoff
- **Product D7 co-sign** required (gating — moves a grade; Hard Rule 8). `roadmap_impact: true` → CC close-readiness gate + `cc_reviewed` before any close.
- **Data**: implement the claim-resolution engine logic (exact umbrella key-lookup; best-mapped-tier selection; cap-1 conditional on "nothing maps") + build the 3 §13.4 golden fixtures; re-score the magnesium PoC under co-signed logic. PoC stays E/34 in the artifact until then.
- **No engine code authored here** (constraint); **no evidence invented** (every mapping cited via `literature`; nerve refusal cited too).

## Product D7 co-sign (2026-06-03, product-agent) — CO-SIGNED, no edits
Confirmed all 5 checks faithful at the moderate posture; singled out the **cited refusal to map "nerve"** as proof the umbrella has real edges (not a loophole). Candidate / no published score / no launch; Data cleared to implement. Carried-forward: bone/muscle citations stay `NEEDS-ENV-VERIFY`; the actual score-move requires `SUPP-EV-006 should_affect_score_now` flip + QA re-validation (Data+QA).

## Data implementation (2026-06-03, data-agent) — done
Implemented claim resolution in `score_engine.py` (frozen exact umbrella key-lookup; best-mapped-tier; cap-1 only when nothing maps; §2.4 over-promise → Honesty gap + real tier), `dossier_loader.py` (uncited mapping → `DossierError`), `trace_writer.py` (resolution audit block). Added `_fixture_snakeoil.yaml` (throwaway R2 active). Engine 0.1.0→0.2.0, methodology string v1.3.
**Validation: 17/17 PASS** (14 prior green + 3 new). Inverted-E intact. **Cross-fixture invariants asserted true:** R1 vague/evidenced→**B/77.3** (blend-bound, cap-1 did NOT fire), R2 snake-oil→**E/34** (cap-1, Dose N/A), R3 over-specific-lie→**D/49** (cap_3_honesty) — R3 strictly below R1 on the same active; R1 unreachable by R2.
**Magnesium PoC: E/34 → B/77.3** (heart→BP=Moderate), recorded as `claim_resolution_rescore` with original E/34 kept for before/after; stays `candidate`/`should_affect_score_now: false`.

## CLOSED 2026-06-03 — orchestrator close-readiness gate
Independently re-ran `run_golden_validation.py`: **17/17 PASS**, inverted-E PASSED, cross-fixture invariants PASSED. D6-authored (Nutrition) + D7 CO-SIGNED (Product) + implemented/validated (Data). Hard Rule 8 satisfied. All candidate/calibration-pending; nothing ships; separate tree. `cc_reviewed: true`.
**Carried-forward (not blockers):** `SUPP-EV-006 should_affect_score_now` flip + QA re-validation before the E→B move is authoritative (Data+QA); bone/muscle tier citations `NEEDS-ENV-VERIFY`.
