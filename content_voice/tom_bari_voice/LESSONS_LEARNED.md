# Project Tom's Voice — Lessons Learned (TASK-374)

Consolidated record from the 2026-06-22 build + protein-bars proof run. Source detail
lives in `8_edit_feedback_log.md` (Harvests #5–#7), `TASK-374.md`, and memory
`project_toms_voice`. This file is the single durable summary.

---

## A. Verification & QA (the highest-value lessons)

**A1 — The two-gate is load-bearing, not ceremony.**
The LLM author repeatedly removed one calque and substituted a *sibling* calque:
`X, לא Y` closer → `עובד כ-X; פחות כ-Y` antithesis → bare one-word closer (`סביר.`/
`מהונדס.`). The deterministic Layer-1 gate said "clean" each time; only the
**independent judge** caught the swap. Rule: after every refine, the independent judge
re-confirms. A single authoring pass is never sign-off.

**A2 — Render-verify is mandatory; "0 HIGH" ≠ "page clean".**
The gate + judge both passed, yet fetching the live page showed `מזון שלם` ×19 on
screen. A gate's all-clear is only as wide as the fields it scans. Rule: before calling
any page done, fetch the real rendered DOM and check ALL consumer strings — it is the
only check that sees copy regardless of where it lives.

**A3 — Verify which file actually feeds the page.**
We rewrote `protein_bars_frontend_v1.json` first; the page actually imports
`protein_combined_frontend_v2.json`. Always trace page → component → loader → data and
confirm the real render source *before* editing copy.

**A4 — Scanner coverage must be total.**
The gate/pilot only covered `insightLine/rowVerdict/comparisonContext`. It missed
`positiveSignals[]`, some `limitingFactors[]`, and ALL hardcoded `.ts/.tsx` copy — where
translationese survived. Rule: scan every consumer string + hardcoded component/loader
copy, not a convenient subset.

**A5 — Verify the builder's claims; don't trust the summary.**
Every agent return was independently re-checked (re-ran the gate, diffed numbers). This
caught the need to confirm `1.8` (real sat-fat) and `28` (own value rounded) were not
fabrication/contamination after the agent admitted an ID-mapping wobble.

**A6 — Untracked files can't be git-diffed for integrity.**
v2 was untracked (no HEAD baseline), so numeric preservation was verified by a different
instrument: every number in a product's copy must exist in *that product's own*
structured data. Pick the verification to fit what's available.

---

## B. Content & Voice

**B1 — The defect was naturalness (translationese), not stance.**
Grammatically-clean, leakage-clean Hebrew that still reads translated passed every prior
gate. It needed a dedicated naturalness gate; grammar/leakage/tone gates do not catch it.

**B2 — Removing one calque isn't enough — enumerate the family.**
When a calque is found, add its structural siblings to the gate, or the author just
migrates to the next one.

**B3 — "Calm" is a trap.**
Told to be calm, the model over-corrects into neutral mush that says nothing. Target =
*opinionated substance in natural connected Hebrew*. Two failure modes, both fatal: F1
translationese-punch AND F2 neutral-bland.

**B4 — The closer / "finish line" is the systematic failure zone.**
Body prose improved fast; the verdicts/closers were where the calques concentrated.

**B5 — Gloss jargon; humanize technical terms (owner rules).**
"מזון שלם" → "אוכל אמיתי"/"חומרי גלם אמיתיים" (T8). Never a bare additive name — gloss it
("הממתיק מלטיטול", "תוסף המזון גליצרול") (T9).

**B6 — Owner gold beats the documented fingerprint where they conflict.**
The trained fingerprint over-rewarded "punch"; the owner's real edits were calmer and
connected. Recalibrate the system to demonstrated preference, not the doc.

---

## C. Gate Engineering

**C1 — The gate is a self-sharpening signal amplifier.**
Hardened 4× from real judge-misses (T1b, T4 promotion, META, BARE, GRADE, T4s, T8, T9).
Each gate-miss → a new detector + a new selftest line (Phase-4 cadence trigger 3).

**C2 — Calibrate on real owner-labeled examples with guards.**
Flagged lines MUST fail; gold lines MUST pass — both in the runnable selftest. Bake in
anti-over-flag guards (`אשר` is natural; an earned short fragment is fine).

---

## D. Process, Lane & Git Hygiene

**D1 — The orchestrator must not author consumer copy inline.**
Even when the owner says "just do it," route copy through the Content Agent + the
independent judge (the two-gate). The orchestrator owns tooling, system docs, and
verification — not the words a shopper reads.

**D2 — Shared-tree git hygiene.**
Always `git add <explicit files>`, never `-A`. Watch for pre-staged foreign files (a
`granola_*.json` was already in the index and rode along until caught). Isolate work on
its own branch.

**D3 — Respect in-flight cross-task files.**
v2 is an untracked in-flight bars-rework (TASK-362) file. Copy edits are fine, but
committing/shipping it must be coordinated with that task; the loader v1→v2 switch was
left to bars-rework.

**D4 — Push ≠ deploy.**
The public site is a separate, blocked migration (TASK-314). Pushing a branch shows
nothing live; local render (`npm run dev`) is how to view changes.

**D5 — Environment gotchas.**
Background-command cwd is unreliable — use absolute paths / `npm --prefix DIR`. Hebrew
through `python -c` stdout corrupts under cp1252 — write UTF-8 files or print ASCII-only.
Next.js caches JSON imports — restart the dev server before judging a render.
