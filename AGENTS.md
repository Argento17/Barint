# Bari — Agent Instructions (repo root)

You are working in the Bari monorepo: an Agent OS / product-data workspace at the
root, plus the Next.js website under `bari-web/` (which has its own `AGENTS.md` —
follow it for any frontend work).

## Hard rules (non-negotiable)

1. **NEVER use Open Food Facts (OFF) as a data source — any field, any purpose,
   ever.** The only source for ingredients + nutrition is the direct product scrape.
   If a field isn't parsed, it is NULL — never substituted. "Unknown is acceptable;
   OFF is not."
2. **Never invent product, nutrition, or ingredient data.** No plausible fills, no
   "temporary" placeholders that look like real data.
3. **Do not change published scores or scoring logic** unless the task prompt
   explicitly instructs it. Frozen invariants (milk = run_005_headpin, snack-bar
   ceiling 70/B, bread provenance) are untouchable.
4. **Stay inside the task prompt's scope.** Execute the task body exactly; don't
   refactor, tidy, or "improve" beyond what it asks. If the spec seems wrong,
   say so in your return instead of improvising.
5. **Never close work.** End with a return block proposing RETURNED, listing every
   file you changed and what to verify (file:line). The orchestrator verifies and
   closes.

## Orientation (read on demand, don't preload)

- Repo layout: `REPO_MAP.md` · architecture: `ARCHITECTURE.md`
- Scoring/BSIP work: read `.claude/scoring.md` first
- Task registry: `tasks/` (one `TASK-NNN.md` per task; YAML `status:`)
- Return contract (your return block must end with its JSON):
  `01_framework/operations/return_contract_v1.md`
- Routing/lane law: `01_framework/operations/capability_router_v5.md` (Capability Router v5.2, canonical; implemented by `03_operations/router/dispatch.py`, `--selftest-table` asserts doc↔code parity)

## Conventions

- Python: stdlib-first, match the style of the module you're editing; pipeline code
  lives under `03_operations/` and `02_products/<category>/`.
- Run scripts from the repo root; outputs/artifacts go where the task prompt says —
  never scatter new top-level directories.
- Windows environment: PowerShell-compatible commands; paths may contain spaces.
- Hebrew consumer copy is governed — do not write or edit consumer-facing Hebrew
  text unless the task prompt explicitly assigns it and names the standard to follow.
