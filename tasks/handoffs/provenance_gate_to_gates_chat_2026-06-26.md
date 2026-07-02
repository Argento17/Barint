# Handoff → the chat that owns gates/run_gates.py — wire the provenance gate (prevention layer)

**From:** de-chain / TASK-395 orchestrator. **Why this is a handoff, not me doing it:** `03_operations/page_generator/gates/run_gates.py` AND `generate_page.py` are both **dirty with your uncommitted work** right now (you're building baseline_verify / inversion_invariant / monotonicity_invariant in that dir). Editing them from my side would clobber you. So I placed the gate file (new, no conflict) and am handing you the two edits to your files.

## Context (the failure this prevents)
Provenance audit: 4 live pages (chocolate-bars, chocolate-tablets, protein-bars, snacks) were scored off-pipeline from corpora **never committed to git** → unauditable/unreproducible. Root cause = the canonical path RECORDS provenance but nothing ENFORCED it. (I just committed the at-risk corpora — commit `5c110fb8a` — so the data is now safe; this gate stops recurrence.)

## DONE by me (collision-safe)
- **Placed:** `03_operations/page_generator/gates/provenance_gate.py` (new file). Deterministic C0 gate, rules R1–R5, HARD (R1 run_id|config_sha256 · R4 corpus committed in git · R5 config binds served file) vs SOFT (R3 generator stamp). `--all --repo-root C:/Bari --configs-dir 03_operations/page_generator/configs` prints a PASS/FAIL table. **Verified** read-only against all 15 live served files: 3 PASS / 4 FAIL[HARD] / 8 FAIL[SOFT].
  - FAIL[HARD] = exactly chocolate_bars, chocolate_tablets, protein_bars, snacks (null run_id + untracked corpus). It flags precisely the off-spine pages and nothing it shouldn't.
- Committed the 4 at-risk corpora + the 3 untracked served frontends (5c110fb8a).

## YOURS — two edits to your dirty files + register the gate

### 1. Register provenance_gate as a blocking gate in `run_gates.py`
Add it to your gate set so it runs per category at go-live; a **HARD** fail must BLOCK publish/serve (SOFT may warn). It exposes a `run(...)`/`--all` entrypoint; call it the same way as your other gates. This is the "locked door" — after this, an off-pipeline score cannot ship.

### 2. Apply the `generate_page.py` self-stamp (closes all 8 SOFT, score-neutral)
Add to the `_meta` build (additive, **_meta only — zero score/grade change, proven byte-identical on products[]**). Apply on top of YOUR version:

```python
# --- provenance self-stamp (provenance_gate R1/R2/R3) ---
scoring_cfg = config.get("scoring", {}) or {}
scoring_flags = scoring_cfg.get("flags") if isinstance(scoring_cfg.get("flags"), dict) else None
run_id = config.get("run_id") or scoring_cfg.get("run_id")
if not run_id:
    for d in run_dirs:
        if not d: continue
        parts = [p for p in str(d).replace("\\","/").split("/") if p]
        if parts:
            run_id = parts[-2] if parts[-1].lower()=="products" and len(parts)>=2 else parts[-1]
            break
# ... then in the meta dict, add:
#   "run_id": run_id,
#   "scoring_flags": scoring_flags,
```
(`generator_version` + `config_sha256` you already stamp — keep them.)

### 3. (optional, when your gate work is committed) run the quarantine
Reversible mover for the 10 off-spine scorer scripts is authored at `…/worktrees/agent-a0c9b893b7be33704/03_operations/_quarantine_offspine_scorers/QUARANTINE_PLAN.py` (`--apply`/`--undo`, dry-run default). Run when the tree is clear; it `git mv`s tracked ones + moves untracked ones into a quarantine dir with an undo map.

## Acceptance after wiring
`run_gates.py` blocks any category whose served file FAILs[HARD]; the 8 SOFT clear after a generate_page regeneration; the 4 HARD pages clear once re-derived through the canonical pipeline (separate step — corpora are now committed so they CAN be).

## Coordination
I'm holding all further shared-tree writes. Ping when run_gates.py + generate_page.py are committed and I'll (a) re-run the gate to confirm it's enforcing, (b) run the quarantine if you haven't.
