# Launch-Readiness Validation Pass — 002 (final)

**Task:** TASK-130 subtask (launch-readiness validation pass)
**Owner:** data-agent
**Date:** 2026-06-01
**Tool:** `validate-corpus` (TASK-130B) — `bari-web/scripts/validate-corpus.mjs`
**Scope:** the 5 live gen1 v2 launch categories — bread, hummus, maadanim, snacks, yogurts. `vegetable-spreads` noted separately (hummus-derived shared corpus).
**Mode:** **validation only. No datasets modified.**
**Supersedes (delta against):** `validate_corpus_audit_001.md` (TASK-130C), after remediation TASK-130D (§2.5 unknowns), TASK-130E (§2.7 ordering), and the snacks NOVA-remediation pass (§2.8 framework vocab).

> Severity model: in **DEV** all 5 categories are LIVE, so failures report as WARN (exit 0) — this preserves the shipped state and is **not** a launch pass. The launch-relevant signal is **`--handoff`** (Wave-2 gate), where the same failures are blocking ERRORS. Counts below are from `--handoff` unless noted.

---

## 0. Headline

- **`--handoff` exit code: 1** — 21 error(s), 34 warning(s).
- **`--all` (DEV) exit code: 0** — 0 error(s), 55 warning(s) (all 5 LIVE pages preserved).
- **All three data-layer launch blockers from Audit-001 are RESOLVED:**
  - §2.5 unknowns: **142 → 0**
  - §2.7 ordering: **7 → 0**
  - §2.8 NOVA framework leak: **29 → 0** (purged from all consumer-facing rendered fields)
- **Every one of the 21 remaining errors is the §2.8 health-word heuristic class** (`נקי`/`כדאי`/`בריא`) — the audit's pre-classified **R4 accepted technical debt**, pending a Content/QA editorial read. **No framework vocabulary (NOVA/BSIP/score-mechanics) remains anywhere.**

---

## 1. Category readiness table

| Category | DEV (live) | HANDOFF errors | §2.5 unknowns | §2.7 order | §2.8 vocab | §2.4v2 (advisory warn) | Verdict |
|---|---|---|---|---|---|---|---|
| **snacks** | 0e / 4w ✅ | **4** | 0 | 0 | 4 (`נקי`×3, `בריא`×1) | 0 | 🟢 data-clean; 1 genuine health-word to read |
| **yogurts** | 0e / 6w ✅ | **3** | 0 | 0 | 3 (`נקי`×2, `כדאי`×1) | 3 | 🟢 data-clean; heuristic read only |
| **bread** | 0e / 26w ✅ | **2** | 0 | 0 | 2 (`כדאי`×2, one product) | 24 | 🟢 data-clean; heuristic read only |
| **hummus** | 0e / 8w ✅ | **3** | 0 | 0 | 3 (`נקי`, same phrase ×3) | 5 | 🟢 data-clean; heuristic read only |
| **maadanim** | 0e / 9w ✅ | **9** | 0 | 0 | 9 (`נקי`×4, `כדאי`×2, `בריא`×3) | 0 | 🟢 data-clean; heuristic read only |
| *vegetable-spreads* | inherits hummus | not validated | — | — | — | — | ⚪ post-filter still not validated (R3 / §6.6 MVP gap) |

Every launch category is now **data-layer clean** (0 unknowns gaps, 0 ordering errors, 0 framework vocab). The remaining red is uniformly the heuristic vocabulary backstop, which the contract itself defines as *non-authoritative* (R4).

---

## 2. Remaining ERROR findings (handoff-blocking) — all §2.8 heuristic vocab

**Total: 21**, classified by linguistic function. None are framework/score-mechanics vocabulary.

### Bucket A — compositional / comparative fact ("clean = short, additive-free ingredient list") — 12
Heuristic fires on `נקי`/`נקייה` but the usage describes *ingredient composition*, not a health or safety claim. Strongest false-positive case.
- hummus ×3 — `bsip1_7296073733324 / _7296073733331 / _3643820` · positiveSignals · *"רשימת רכיבים נקייה — ללא תוספי מזון מזוהים"*
- maadanim `5014271300429` · bottomLine · *"הרשימה הנקייה ביותר בקטגוריה …"*
- maadanim `5014271360423` · limitingFactors · *"… אפילו עם רשימה נקייה"*
- maadanim `5014271360423` · bottomLine · *"תפוז טבעי ונקי …"*
- maadanim `7290110325312` · comparisonContext · *"… הסויה הנקייה ניצחת."*
- snacks `snk-001` · bottomLine · *"… הבסיס הנקי ביותר …"*
- snacks `snk-011` · positiveSignals · *"… אחד הבסיסים הנקיים בקטגוריה"*
- snacks `snk-011` · limitingFactors · *"… למרות הרשימה הנקייה אחרת"*
- yogurts `yog-003` · bottomLine · *"… בסיס נקי"*
- yogurts `yog-007` · bottomLine · *"… לא בסיס נקי"* (negated)

### Bucket B — meta / ironic `בריא` (explicitly *about* health labeling; quoted or negated) — 3 (FALSE POSITIVES)
- maadanim `5014271360423` · insightLine · *"מעדן פרי בלי תווית בריאות"* (without a health label)
- maadanim `7290110558703` · bottomLine · *"… הפכו את ה'בריא' לעמוס יותר בתוספים …"* (quoted, critical)
- maadanim `7290107950206` · limitingFactors · *"\"דיאט\" — … לא 'מוצר בריא'"* (negated, quoted)

### Bucket C — reader-directed soft phrasing `כדאי` ("worth knowing / worth checking") — 5
Editorial register, not a product recommendation ("buy this"). Borderline; needs Content judgment.
- bread `shufersal_7290016245325` · insightLine + bottomLine (same string ×2) · *"… אבל כדאי לדעת: הסיבים כאן מגיעים מהטחינה …"*
- maadanim `7290107958035` · bottomLine · *"… כדאי לבדוק את האריזה."*
- maadanim `7290110561604` · comparisonContext · *"… כדאי לבדוק אם ההרכב שונה."*
- yogurts `yog-001` · bottomLine · *"… המוצר שממנו כדאי לצאת כשמשווים"*

### Bucket D — genuine health descriptor — 1 (HIGHEST-PRIORITY READ)
- snacks `snk-012` · positiveSignals · *"… שומן בריא ממקורות שונים"* ("healthy fat") — the one hit that reads as a direct health claim rather than a compositional fact or meta-reference. Recommend Content rephrase (e.g. to a structural descriptor) regardless of the broader R4 decision.

---

## 3. Remaining WARN findings (non-blocking)

**Total: 34** (handoff) / 55 (DEV, which also surfaces the 21 errors as warnings under live-warn policy).

- **§2.4v2** — *both* positiveSignals *and* limitingFactors present (exemption-gated): **bread 24, hummus 5, yogurts 3 = 32**. Advisory only; never blocks (`ALWAYS_WARN`). The exemption registry is still not machine-readable (R2) — hummus's limitingFactors exemption is legitimate.
- **§4.3 orphaned datasets** — `hummus_frontend_v1.json`, `hummus_frontend_v2.json` (imported by nothing). Delete or relocate; Controller-owned.

---

## 4. Confirmed launch blockers

**Data-layer: none remaining.** All three data-owned blocker classes named by Audit-001 are eliminated and verified at 0:
- §2.5 unknowns backfill — **cleared** (TASK-130D)
- §2.7 ordering — **cleared** (TASK-130E)
- §2.8 NOVA framework leak — **cleared** (snacks NOVA-remediation pass)

**The only thing keeping `--handoff` red is the §2.8 heuristic-vocab class (21 hits).** Per the Category Module Contract this rule is an explicit *heuristic backstop, not the authority* (R4), and Audit-001 §5 pre-classified it as **accepted technical debt pending a Content/QA read** — not a mechanical-removal blocker. Triage above shows ~15 of 21 are false positives (Buckets A+B) and only **1** (Bucket D, `snk-012` "healthy fat") reads as a genuine health claim.

→ **No genuine data-integrity launch blocker exists.** The residual gate is a one-pass editorial sign-off, owned by Content/QA, not Data.

---

## 5. Accepted technical debt (tracked, does not gate data readiness)

- **§2.8 health-word heuristic hits (21)** — R4. Disposition is a Content/QA editorial read (keep compositional `נקי`/meta `בריא`; rephrase the one genuine `snk-012` health claim; rule on soft `כדאי`). Not data work.
- **§2.4v2 advisory (32)** — R2; exemption registry not yet machine-readable; never blocks.
- **vegetable-spreads post-filter unvalidated** — R3 / §6.6 MVP gap; validator validates raw `hummus_frontend_v3.json`, not the rendered subset.
- **Orphaned hummus v1/v2 datasets** — §4.3; cleanup, Controller-owned.
- **Validator-side gaps** (not category debt) — §6.4 baselines, §6.5 runtime-schema-from-type, §2.9 image-resolution, §3.6 build/git handoff preconditions.

---

## 6. Recommendation — TASK-130: **KEEP OPEN (one narrow condition)**

The **data-agent scope inside TASK-130 is fully discharged**: validator built (130B), audited (130C), and every data-layer blocker remediated and re-verified at 0 (130D/130E + NOVA pass). Data-layer launch readiness = **GO**.

I recommend **KEEP OPEN** rather than CLOSE, because TASK-130 explicitly owns the *launch QA-threshold dimension* and that threshold — a green `--handoff` — is **objectively not yet met (exit 1, 21 errors)**. Closing now would retire the gate while it is still red. The single remaining close condition is tightly scoped and **not data work**:

> **Close condition:** a Content/QA §2.8 editorial read of the 21 health-word hits (triage in §2), after which either (a) the strings are adjusted and `--handoff` goes green, or (b) the R4 exemptions are recorded so the validator stops flagging legitimate compositional facts — at which point `--handoff` is green by policy.

Suggested handoff (matches Audit-001 §6):
- **Content Agent** — §2.8 read; minimum action = rephrase `snk-012` "שומן בריא" (Bucket D). New/continued task.
- **Central Controller** — §4.3 orphan cleanup + R2 exemption-registry governance (would also clear the 32 §2.4v2 warnings and the Bucket-A false positives).

If the Controller's policy is that R4 heuristic debt does **not** gate launch (consistent with Audit-001 §5), then this report is sufficient evidence to **CLOSE TASK-130** immediately and spin the §2.8 read as an independent Content task — launch is unblocked at the data layer either way.

---

*Launch-Readiness Validation 002 — TASK-130 — data-agent — 2026-06-01. Validation only; no datasets modified. `--handoff` exit 1 (21 §2.8 heuristic errors); `--all` DEV exit 0.*
