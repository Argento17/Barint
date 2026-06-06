# Supplement Intelligence Engine (SIE) — Asset & Closure Record

**Status: PROVEN ASSET — BANKED, NOT LAUNCHED.** Acquisition experiment CLOSED 2026-06-03 (owner directive).
**Object:** TASK-171 (+ sub-tasks 171A–171L). All outputs `verification_status: candidate` / `should_affect_score_now: false` — **nothing was ever shipped; no published score moved; no category launched (D10/D1 not made).** Separate tree from BSIP2 — the frozen food invariants are structurally untouched.

---

## 1. What the SIE is
A sibling scoring engine to BSIP2, for **supplements** — a different object than food. The unit of analysis is the **(active, dose, form, evidence) tuple**, not a per-100g nutrition panel. It answers **"is this product worth taking, as sold?"** across **5 dimensions**: Evidence Strength · Dose Adequacy · Form & Bioavailability · Formulation Honesty · Safety Ceiling. Methodology: `01_framework/supplement_framework/methodology_v1.md` (v1.4 as of 2026-06-06 — banked amendments A/B/C from TASK-195; D7 co-signed Nutrition + Product on v1.1; v1.4 is Nutrition self-sign pre-launch).

## 2. What was built & PROVEN
- **The engine** (`03_operations/supplement_engine/proto_v0/src/`): `score_engine.py`, `dossier_loader.py`, `supplement_label.py`, `trace_writer.py`, `constants.py`. Algorithm 0.2.0; all thresholds calibration-pending.
- **15 Evidence Dossiers** (`evidence_dossiers/*.yaml`): creatine, magnesium, vitamin D3, caffeine, omega-3, vitamin C, zinc, iron, calcium, folic acid, B12, melatonin, biotin, vitamin E, CoQ10 — each cited, tiered (Nutrition D6), with a `structure_function_umbrella` claim-map (incl. Hebrew/EFSA vocab, TASK-171K) and §5.1 lifecycle fields. Registry: `evidence_registry/supp_evidence_registry_v1.md` (SUPP-EV-001…016).
- **Proven behaviors** (golden corpus **17/17**, AND verified on REAL Israeli SKUs):
  - Distinguishes + **explains** failure modes via the *binding constraint* (not the lowest sub-score). The inverted-E pair (no-evidence `cap_1` vs unsafe `veto_safety`) is never confused.
  - **Claim-resolution (v1.3):** a vague label claim resolves to the active's cited studied endpoint via the umbrella; Insufficient→E only when nothing maps; over-promises caught by Honesty. Stance: *"punish over-promise, not compliance."*
  - Real-SKU evidence: **Altman Vitamin D-1000 → S/91.2** (clean); **Altman Magnesium 450mg oxide → E/20** (safety veto on a real over-dose); **Altman Biotin → E/34** (cosmetic Insufficient). The engine scored every real product correctly.
- **Maintenance economics VALIDATED:** ~**30–33 hrs/yr at 15 dossiers** (TASK-171F/171B), tiered sweep cadence, UL fields offloadable to NIH ODS/EFSA re-sync.
- **EDPG firewall** held throughout: the engine reads in-house dossiers/labels only; external sources calibrate (with citations), never feed the score path directly.

## 3. The acquisition experiment — why the category was NOT launched
The engine is excellent; **the wall is panel acquisition for the Israeli shelf.** Measured, not assumed:
- iHerb yields only ~2–4 SKUs (TASK-171D thin proof) — "global brand + matching Israeli-pack barcode" is a tiny intersection.
- The real shelf is **local-brand-dominated** (Altman, SupHerb, Life, Tink); their Supplement Facts panels are largely **not online in a resolvable form**.
- The MVP acquisition adapter (third-party e-tailers + Altman + resolver), run live on 118 addressable SKUs, scored **6.8% (8/118)** — vs a ~31–37% projection (TASK-171J). The feasibility probe's ~75–85% was hand-picked-optimistic.
- The only path to the local-brand shelf is a **manufacturer/importer data feed (a BD effort, not engineering)**. The structurally-hard categories (multivitamins, probiotics, herbals ≈ 20–30% of shelf, and the biggest sellers) need subsystems the MVP deliberately deferred.
**Verdict (owner, 2026-06-03):** stop investing engineering; bank the engine as a proven asset; close the acquisition experiment.

## 4. How to run it (for a future revival)
- Validate: `python run_golden_validation.py` (expect 17/17 + inverted-E + cross-fixture invariants).
- Load dossiers: `dossier_loader.load_all()` (16 files incl. the snake-oil fixture; uncited umbrella mapping hard-fails).
- Acquisition plumbing (read-only, candidate): `integrations/clients/` → `il_prices.py` (Super-Pharm catalog), `iherb_panel.py`, `il_supplement_panels.py` (IL e-tailer/brand-site), `il_panel_resolver.py`, `supplement_bridge.py`.
- Real-SKU runs / reports: `02_products/supplements/` (`real_corpus_v1`, `real_corpus_v2`, the feasibility + coverage + decision-pack docs).

## 5. Carried-forward IF revived (none active now)
- **Acquisition is the gate** — pursue a manufacturer-feed (BD), not more scraping.
- **Score-path-creating items need Product D7 + golden re-validation before any SHIP:** the v1.3 claim-resolution rule's live use, the TASK-171K tokenizer change + the 3 first-authored umbrellas (D3, creatine, omega-3), and any dossier value flagged `NEEDS-ENV-VERIFY` (all primary UL/safety numbers — confirm vs NIH ODS/EFSA primary sheets).
- **Calibration items surfaced by real SKUs:** omega-3 "Heart Healthy" → should it resolve to the contested CV endpoint or the Strong triglyceride endpoint? EFSA-divergence flags (magnesium 'nerve', zinc 'antioxidant', calcium 'muscle', biotin cosmetic).
- **A launch is a separate D10/D1 decision** + requires the EDPG candidate→promote (D3/D4) + QA freeze on real panels.

### Pending amendments on revival (TASK-195, 2026-06-06)

Three methodology amendments were authored during the banked period and are ready to activate on revival. All were applied to `methodology_v1.md` (now v1.4) and recorded in `supp_evidence_registry_v1.md` (SUPP-EV-017–019). No engine code was touched; no corpus was touched; no score was changed. These amendments require no additional D7 co-sign for the methodology text itself (Nutrition self-sign, `roadmap_impact: false`); Product per-number gate applies to any threshold that moves a published score when activated.

**Amendment A — Speciation tier: graded Form scoring for Mg, folate, B12 (SUPP-EV-017, §2.3)**
- Adds a named speciation tier sub-table to §2.3 (Form & Bioavailability).
- Magnesium: oxide = `poor` (~4% absorption), citrate = `preferred` (~25–30%), glycinate/bisglycinate = `preferred` (~31%), L-threonate = `preferred-specialized` (BBB-crossing).
- Folate: folic acid = `acceptable` (DHFR bottleneck; UMFA above ~200–400 mcg/day; MTHFR issue); 5-MTHF = `preferred` (bypasses DHFR and MTHFR entirely; no UMFA).
- B12: cyanocobalamin = `acceptable`; methylcobalamin = `preferred`; adenosylcobalamin = `preferred-specialized`.
- Implementation note: dose comparison for oxide must use elemental fraction via pubchem (§2.2 — the oxide-paradox trap). Methylcobalamin superiority at equivalent doses is contested — record as watch item, not settled `preferred` with Strong evidence.

**Amendment B — EFSA Tolerable Upper Limit as named primary Safety ceiling (SUPP-EV-018, §2.5)**
- Names EFSA TULs (Directive 2002/46/EC; EFSA NDA Panel) as the governing Safety ceiling reference. Israel has no standalone TUL table; EFSA TULs govern.
- Formalizes a three-band structure:
  - Dose > EFSA TUL → Safety VETO (hard floor, grade cap E) — existing behavior, now cited.
  - Dose 80–100% EFSA TUL → Safety FLAG (`safety_flag: approaching_tul`, annotate only, no grade cap) — new behavior (pre-launch).
  - Dose < 80% EFSA TUL → no Safety action on dose grounds.
- Engine constant to add on revival: `TUL_FLAG_FRACTION = 0.80`.
- Per-dossier governing-UL choice supersedes this general rule where NIH/IOM governs instead (Mg: SUPP-EV-002 FLAG-2; omega-3: SUPP-EV-005).
- `NEEDS-ENV-VERIFY` on primary EFSA opinion numbers per active — confirm vs primary EFSA opinion sheets before activating the FLAG band.

**Amendment C — Probiotics: strain-resolved Evidence Dossiers (SUPP-EV-019, §7 — Phase 3+ scope only)**
- Probiotic efficacy is strain-specific; pooling genus/species generates inaccurate conclusions.
- Each named strain requires its own Evidence Dossier (Phase 3+). Un-named strains or CFU-only labels → Evidence tier = Insufficient (cap-1 fires).
- CFU dose adequacy is unresolvable without end-of-shelf-life viability data.
- Does NOT affect MVP or Phase 2 scope. Probiotics remain deferred-to-hard-gate until a Phase 3 is formally authorized with a data feed covering named strains.

## 6. Bottom line
A genuinely strong, self-explaining, cheap-to-maintain supplement scoring engine — proven on real Israeli products — **parked because the shelf can't be acquired economically by scraping, not because the engine fell short.** Reviving it is a business-development question (manufacturer data), not an engineering one.
