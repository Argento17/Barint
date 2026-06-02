# validate-corpus Audit 001 — Launch-Scope Categories + Remediation Backlog

**Task:** TASK-130C
**Owner:** data-agent
**Date:** 2026-06-01
**Tool:** `validate-corpus` (TASK-130B) — `bari-web/scripts/validate-corpus.mjs`
**Scope:** the 5 live gen1 v2 categories (TASK-132 launch set): bread, hummus, maadanim, snacks, yogurts. `vegetable-spreads` noted separately (hummus-derived shared corpus).
**Mode:** audit only. **No datasets modified.**

> Severity note: in DEV mode all 5 are LIVE so failures report as WARN (exit 0) — this preserves the shipped state and is NOT a launch pass. The launch-relevant signal is `--handoff` (Wave-2 gate), where the same failures become blocking ERRORS. Counts below are from `--handoff`.

---

## 1. Category readiness table

| Category | DEV (live) | HANDOFF errors | §2.5 unknowns | §2.7 order | §2.8 vocab | §2.4v2 (advisory) | Verdict |
|---|---|---|---|---|---|---|---|
| **hummus** | 0e / 8w ✅ | **3** | 0 | 0 | 3 (`נקי` heuristic) | 5 | 🟡 closest to green — only heuristic vocab |
| **yogurts** | 0e / 19w ✅ | **16** | 13 | 0 | 3 (`נקי`/`כדאי`) | 3 | 🟠 unknowns backfill + QA read |
| **bread** | 0e / 56w ✅ | **32** | 24 | 6 | 2 (`כדאי`) | 24 | 🟠 unknowns + ordering |
| **snacks** | 0e / 52w ✅ | **52** | 18 | 1 | 33 (**29 = NOVA**) | 0 | 🔴 real framework leak + unknowns |
| **maadanim** | 0e / 96w ✅ | **96** | 87 | 0 | 9 (`נקי`/`כדאי`/`בריא`) | 0 | 🔴 largest unknowns gap |
| *vegetable-spreads* | inherits hummus | not validated | — | — | — | — | ⚪ post-filter not validated (R3) |

`hummus_v3` is the only dataset that passes §2.5 cleanly (the contract's "1 of 7 good" dataset). `vegetable-spreads` renders a deterministic filter over `hummus_frontend_v3.json`; the MVP validates the raw hummus file, not the post-filter subset (§6.6 gap / R3) — its true readiness is unverified.

---

## 2. ERROR findings (handoff-blocking, grouped by category)

- **maadanim — 96**: §2.5 unknowns ×87 (nutrition field null but `unknowns[]` empty), §2.8 ×9 (`נקי`×4, `כדאי`×2, `בריא`×3 — several meta/ironic uses).
- **snacks — 52**: §2.8 ×33 (**`NOVA`×29** real framework leak + `נקי`×3 + `בריא`×1), §2.5 unknowns ×18, §2.7 ordering ×1 (`snk-010`: 46 > 44).
- **bread — 32**: §2.5 unknowns ×24, §2.7 ordering ×6, §2.8 ×2 (`כדאי` — "כדאי לדעת").
- **yogurts — 16**: §2.5 unknowns ×13, §2.8 ×3 (`נקי`×2, `כדאי`×1).
- **hummus — 3**: §2.8 ×3 (`נקי` — "רשימת רכיבים נקייה", all the same compositional phrase).

**§2.5 total across launch scope: 142 products** (maadanim 87, bread 24, snacks 18, yogurts 13; hummus 0). Single systematic root cause: builders don't emit an `unknowns[]` entry when a nutrition field is suppressed/null.

---

## 3. WARN findings (non-blocking in dev; informational)

- **§2.4v2** (both positiveSignals *and* limitingFactors required, exemption-gated): bread 24, hummus 5, yogurts 3. Advisory only — the exemption registry is not yet machine-readable (R2). hummus's limitingFactors exemption is legitimate.
- **§4.3 orphaned datasets**: `hummus_frontend_v1.json`, `hummus_frontend_v2.json` — imported by nothing; delete or relocate.
- All ERROR findings above also surface as WARN in DEV mode (live-warn policy).

---

## 4. Recommended remediation order

| # | Item | Categories | Effort | Why this order |
|---|---|---|---|---|
| 1 | **Strip NOVA from consumer strings** (§2.8) | snacks (29 occ / 15 products) | S–M | Only *real* framework-vocabulary leak; consumer-facing reputational/governance risk; not heuristic noise. |
| 2 | **Backfill `unknowns[]` when nutrition null** (§2.5) | maadanim 87, bread 24, snacks 18, yogurts 13 | M | Highest volume (142), one systematic fix in the builders; data-integrity/disclosure rule. |
| 3 | **Re-sort products score-desc, insufficient last** (§2.7) | bread 6, snacks 1 | S | Trivial deterministic builder fix. |
| 4 | **Content/QA read of health-word hits** (§2.8 heuristic) | maadanim, hummus, yogurts, bread (`נקי`/`בריא`/`כדאי`) | M | Judgment, not mechanical (R4). Route to Content/QA; some are legitimate compositional facts, some soft-recommendations. |
| 5 | **Resolve orphaned hummus v1/v2** (§4.3) | hummus | S | Delete or relocate; removes standing warning. |
| 6 | **Declare §2.4v2 exemptions in readiness docs** (R2) | hummus (+others) | S | Governance; lets validator stop flagging legitimate single-additive exemptions. |

**Fastest path to a green `--handoff`:** hummus (only item #4 `נקי` blocks it) → then yogurts/bread (#2 + #3) → snacks/maadanim last (largest #1/#2 load).

---

## 5. What blocks launch vs accepted technical debt

### Blocks launch (must fix before `--handoff` green / Wave 2)
- **§2.5 unknowns backfill** — all categories except hummus. Disclosure rule; the gap the contract was built to catch.
- **§2.8 NOVA leak (snacks)** — true framework vocabulary in consumer-facing strings.
- **§2.7 ordering (bread, snacks)** — data-layer correctness (UI never sorts).

### Accepted technical debt (does not block; tracked, conditioned)
- **§2.8 health-word heuristic hits** (`נקי`/`בריא`/`כדאי`) — R4: heuristic backstop, not authority. Accepted pending a Content/QA read sign-off rather than mechanical removal. (snacks NOVA is excluded — that's a blocker.)
- **§2.4v2 advisory** — exemption registry doesn't exist yet (R2); never blocks today.
- **vegetable-spreads post-filter not validated** — R3 / §6.6 MVP gap. Accepted until validator gains shared-corpus awareness.
- **Validator-side gaps** (not category debt): §6.4 baselines, §6.5 runtime-schema-from-type, §3.6 build/git handoff preconditions, §2.9 image-resolution.

---

## 6. Handoff to owners (suggested)
- **Data Agent** — items #2, #3 (builder fixes: emit `unknowns[]`, re-sort). New task.
- **Content Agent** — item #1 (NOVA rewrite, snacks) + #4 (health-word read). New task.
- **Central Controller** — item #5 (orphan resolution) + #6 (exemption-registry governance, R2).

*validate-corpus Audit 001 — TASK-130C — data-agent — 2026-06-01. Audit only; no datasets modified.*
