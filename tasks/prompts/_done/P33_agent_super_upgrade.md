# P33 / Agent-OS hardening Wave 2 — Instruments, Fixtures, Self-Gating, Challenge Duty (route: C2)

⚠️ SEQUENCING: run ONLY AFTER P32 is completed (P32 edits the same 11 files; the
files will already contain a "## Return Contract" section when you start).

ZERO-JUDGMENT MECHANICAL TASK. You create 1 config file and insert EXACT text
blocks into agent definition files. Do not rephrase, do not improve, do not
reorganize anything else. All inserts go immediately BEFORE the line
"## Autonomy Mandate" in each file (if absent, append at end of file).
Insert order when a file gets 2 blocks: per-agent block first, shared block second.

---

## STEP 1 — create: 01_framework/governance/grade_boundary_policy_v1.json
Exact content:
```json
{
  "version": 1,
  "policy": "grade_boundary",
  "boundary": "floor",
  "rationale": "An engine grade is never inflated by display rounding: 34.7 (E) must not display as 35/D. Score display may round; the grade derives from the raw trace score.",
  "scale": {"S": 90, "A": 80, "B": 65, "C": 50, "D": 35, "E": 0},
  "status": "default-binding; Nutrition ratification pending",
  "date": "2026-06-12",
  "source": "TASK-257 road move 4; Great Grains 884912126115 incident (trace 34.7/E displayed as 35/D); second instance found by gate suite: 7290014471436 (granola)"
}
```

## STEP 2 — SHARED insert into ALL 11 agent files
(.claude/agents/: cc-agent, content-agent, data-agent, design-agent,
frontend-agent, marketing-agent, nutrition-agent, product-agent, qa-agent,
red-team-agent, research-agent — all .md)

## Spec-Conflict Duty (mandatory — 2026-06-12)

If a delegation spec conflicts with your lane law, this file's hard rules, or a
standing owner ruling — flag the conflict in your return block and propose the
compliant alternative instead of silently executing. If the spec contradicts data
you can see (e.g., a display scope smaller than the scored corpus, a source the
spec misnames), say so BEFORE building. Silent faithful execution of a flawed
spec is the RC1/RC3 failure class (see
`02_products/yogurt_system/yogurt_relaunch_failure_audit_v1.md`).

## STEP 3 — per-agent inserts (exact text per file)

### 3a → qa-agent.md

## Instruments & Fixtures (mandatory — 2026-06-12)

- Primary instrument: `03_operations/page_generator/gates/run_gates.py`. Run it on
  any page JSON you are asked to verify; cite its report + exit code in the
  verdict. Never eyeball what the gate suite can check.
- You OWN the fixture library (`03_operations/page_generator/fixtures/`):
  known-bad inputs MUST keep failing (the rejected yogurts v4 is the founding
  known-bad fixture); golden inputs must keep passing. After any change to gates
  or generator, rerun fixtures. A known-bad that passes = the check is broken
  (mutation-testing rule), and that is a FAIL of the change, not of the fixture.
- Every verdict also emits machine-readable JSON (PASS/FAIL + per-gate evidence)
  alongside prose.
- Hard Rule 9 is enforced mechanically: the red-team check is a gate line (report
  exists + 0 open CRITICAL findings), never a memory item.

### 3b → data-agent.md

## Self-Gating Duty (mandatory — 2026-06-12)

- Every builder/script you deliver ENDS by running the relevant machine check on
  its own output (`run_gates.py` for page JSONs; the raw-store replay check for
  parsing work) and includes the report + exit code in the return.
- Field-coverage duty: any output carrying display fields reports per-field
  coverage N/M vs the source (images, names, nutrition) in the return contract's
  `counts`. Silent field loss is the RC2 failure class — it is yours to prevent.
- A number without a committed artifact behind it is not a result. Never report
  sums/matches you did not recompute from the artifact itself.

### 3c → content-agent.md

## Pre-Return Self-Check & Editorial Instruments (mandatory — 2026-06-12)

Before returning ANY consumer copy:
1. Run `integrations/clients/hebrew_readability.py` on every string — `is_clean`
   must be true (framework leakage = automatic not-done).
2. Standalone-value test: every line must fully inform a reader who sees ONLY
   that card. No relational framing ("כמו ה-X", "אותו עיקרון כמו", "הפרש של N
   ציונים מ-Y") unless the line still carries its own complete meaning.
3. Grade letters in prose = the badge grade exactly; sodium and fat are never
   framed as the cause of a grade.
4. Quality bar = the live milk/granola/snacks lines. If a draft reads thinner
   than those, it is not done — iterate before returning.
Right to challenge: a brief that instructs law-breaking copy (relational framing,
leakage, fabricated causes) gets flagged with a proposed compliant alternative —
executing it silently is the RC3 failure class.

### 3d → nutrition-agent.md

## Rulings as Config (mandatory — 2026-06-12)

- Scoring-presentation rulings ship as machine-readable config, not prose.
  Canonical instance: `01_framework/governance/grade_boundary_policy_v1.json`
  (boundary="floor": an engine E never displays as D; the default binds until
  your formal ratification — review and ratify or amend it).
- Any future ruling a gate or generator must obey gets a versioned config
  artifact. Prose-only rulings that machines must read are the Great-Grains
  failure class.
- Engine invariants (monotonicity: adding sugar or additives never raises a
  score; removing data never raises a score) home in your lane when the
  property-testing track opens (gap-analysis card #2, with Shadow).

### 3e → red-team-agent.md

## Mechanical Trigger (mandatory — 2026-06-12)

- Your gate is CODE: the QA gate suite checks that
  `02_products/{category}/reports/red_team_*.md` exists for the current corpus
  version with 0 open CRITICAL findings. No report = automatic go-live FAIL,
  regardless of anyone's memory.
- Auto-trigger: any corpus-version bump or pre-go-live parity run on a category
  without a current red-team report dispatches you — challenge the corpus BEFORE
  QA's final verdict, not after.
- Seeded-defect drills (on request): plant a documented defect in a COPY of a
  corpus and verify the gate suite catches it. The drill tests the testers.
  Never seed defects in real corpora; always work on copies and say so.

### 3f → frontend-agent.md

## Self-Gating Duty (mandatory — 2026-06-12)

- Any change touching page data (frontend JSONs, page-data .ts files, imports)
  ENDS with: `03_operations/page_generator/gates/run_gates.py` on the affected
  category JSON (with --baseline when a live page exists) + `next build`. Reports
  and exit codes go in the return.
- Field-coverage duty: when you produce or transform page JSON, report per-field
  coverage N/M vs source in `counts`. The P19 image-drop is the failure class
  you own.
- NEVER flip a live import without a parity-gate report attached and explicit
  owner approval (Page Parity Gate law).

### 3g → design-agent.md

## Instruments (mandatory — 2026-06-12)

- Your checks are runnable, not opinions: `npm run test:e2e` (geometry/RTL
  render), `npm run test:a11y` (axe-core WCAG gate), Playwright viewport
  screenshots for the 375px mobile-geometry checklist. Cite runs + results in
  returns.
- Screenshot-baseline duty: visual changes ship with before/after screenshots at
  375px and desktop, attached to the return.

### 3h → product-agent.md  AND  cc-agent.md (same block in both)

## Decision-Log Duty (mandatory — 2026-06-12)

- Every accept/reject/prioritization decision returns with: options considered,
  the chosen option, the single decisive reason, and the reversal condition
  ("revisit if X"). One line each — but always present.
- The Page Parity Gate report (gate 7) is the primary input for any swap or
  go-live recommendation; never recommend a swap without citing it.

(marketing-agent.md and research-agent.md receive ONLY the STEP 2 shared block —
they are parked lanes by design.)

## STEP 4 — version bumps
Bump each edited agent file's frontmatter `version:` by +0.1 (on top of P32's
bump) and add changelog entry: `Wave-2 hardening: instruments/fixtures/self-gating/challenge duty (P33).`
Match each file's existing changelog format.

RULES: touch ONLY the 12 files named (11 agents + the new config). No other
edits, no reformatting of untouched sections, preserve UTF-8.

RETURN BLOCK: list every file with action; per file state WHICH blocks were
inserted (shared / per-agent / both); confirm insert position (before
"## Autonomy Mandate"); state sha256 of the config file. End with the JSON
return contract per `01_framework/operations/return_contract_v1.md` (installed
by P32) — counts must include `files_edited: N/12`. Propose RETURNED.

---
After you send this to the agent: open tasks\DISPATCH_BOARD.md and tick the P33 line.
