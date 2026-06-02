# Maadanim Confidence Blocker — Displayed-Set Audit

**Task:** TASK-128C (Maadanim corpus confidence finalization + v2 activation gate)
**Owner:** data-agent
**Date:** 2026-06-01
**Method:** Displayed-set audit (mirrors TASK-129D Hummus). Two detectors run over the
**displayed 90** (`bari-web/src/data/comparisons/maadanim_frontend_v2.json`), not the
200-row raw corpus. Read-only — **no corpus writes, no score/label changes in this pass.**
**Script:** `02_products/maadanim/frontend/audit_maadanim_confidence_129e.py`

---

## Headline

**The maadanim confidence-LABEL blocker is INFLATED — same heuristic artifact found in
Hummus.** The re-audit's "~63 marketing-prose `verified`" was counted against the
file/corpus view, not the curated shelf. On the displayed 90, the canonical
ingredient-quality gate finds **0 genuine `verified → partial` candidates**.

The **only** genuine residual is the **3 §2.2 category-instability survivors** — and that
is a **routing** defect (P0 #3), not a confidence-prose defect (P0 #1).

---

## 1. Original vs corrected counts

| Measure | Source | Count |
|---|---|---|
| Re-audit claim: "marketing-prose `verified`" | file/corpus view | **~63** |
| Detector 1 (original promo-token heuristic), **displayed 87 verified** | this audit | **1** |
| Detector 1 (promo-token heuristic), **full 200-trace corpus** | this audit | **2** |
| Detector 2 (canonical ingredient-quality gate, hummus-shipped), **displayed** | this audit | **0** |
| Structured/real ingredient lists across 184 traces w/ ingredients | this audit | **171 (93%)** |

**The "63" does not reproduce.** Promo tokens (`מסייע`, `האריזה`, `מיחזור`, `עשיר ב…`)
appear in only **2** ingredient strings across the entire 200-product corpus, and the
single displayed hit (`גמדים לשתיה תות בננה`) tripped on `מיחזור` ("recycling") embedded
in a fully structured, genuine ingredient list (commas + percentages + parenthetical
sub-ingredients) — a textbook substring false positive, identical to the
`טרי`-in-`ציטרית` class of error that inflated the Hummus count.

---

## 2. Products genuinely requiring relabel

**Confidence-quality gate (P0 #1): 0 products.** Every displayed `verified` row carries a
real ingredient list. There is no ingredient-prose over-verification on the maadanim shelf.

**Category-instability survivors (P0 #3 / §2.2): 3 products — genuine, but routing-driven, not prose-driven.**

| id | product | score/grade | route | cat_conf | instability |
|---|---|---|---|---|---|
| `bsip1_maadanim_4584306` | סופר גמדים תות בננה מארז | 53/C | default | 0.30 | true |
| `bsip1_maadanim_7290010472307` | גמדים לשתיה תות בננה | 46/D | default | 0.30 | true |
| `bsip1_maadanim_7290119375356` | דנונה מולטי קולגן | 45/D | dessert | 0.55 | true |

These are squeezable kids' **drinks** + a **collagen drink** mis-routed onto the maadanim
shelf. They are correctly flagged for **re-route or exclude** (TASK-128C §2 / re-audit
§2.2). Their `verified` label is wrong because the *category* is unstable, **not** because
the ingredient text is marketing prose. Fixing them via confidence-relabel would mask a
routing error; the correct fix is exclusion/re-route per TASK-128C scope.

**§2.1 exclusion list — already satisfied at the display layer.** All 7 non-maadanim items
(arm-muscle meat, hamburger, lettuce, brined cheese, kid mix) and the entire probiotic-
supplement cluster are **absent from the displayed 90**. The written `excluded_products`
list still needs formalizing (so they cannot re-enter on a re-run), but they pose **no live
confidence risk** today.

---

## 3. Score impact

**None.** This pass is read-only; no JSON was modified. The downstream P0 #3 action
(exclude/re-route the 3 survivors) is a **display-set membership / routing** change, not a
scoring change — `run_maadanim_001` scores stay frozen (CLAUDE.md invariant). Confidence is
a display label; no grade or numeric score moves under any recommended action.

---

## 4. Activation recommendation: 🟡 CONDITIONAL GO

| Dimension | Verdict |
|---|---|
| **Confidence-label quality (P0 #1)** | ✅ **CLEARED — blocker not real.** 0 displayed rows over-verified; the "63" was a file-view + substring artifact, identical to Hummus (TASK-129D). This dimension does **not** block activation. |
| **Corpus finalization (P0 #3 / §2.2)** | ⚠️ **OPEN — small & bounded.** 3 instability survivors must be re-routed/excluded before flipping `MAADANIM_V2_SLICE`. This is the sole remaining gate. |
| **§2.1 exclusions** | ✅ Effectively satisfied (all absent from displayed 90); formalize the written list for re-run safety. |

**Net:** The headline confidence blocker that justified holding maadanim v2 is **inflated**
and clears with no work. The real, far smaller blocker is the **3 §2.2 survivors**. Once
those 3 are excluded/re-routed and the displayed corpus frozen with a formal
`excluded_products` list, maadanim is **GO** for `MAADANIM_V2_SLICE = true` + QA
re-baseline (mobile + `lg`).

**Recommended next action (TASK-128C owner):** exclude/re-route the 3 survivors, formalize
`excluded_products`, freeze the corrected displayed corpus (now 87), then hand to
frontend-agent for the one-line flip. No confidence-gate hardening script is needed for
maadanim — unlike the re-audit's premise, there is nothing for it to catch.

---

## 5. Freeze applied (2026-06-01)

`02_products/maadanim/frontend/freeze_maadanim_corpus_128c.py` executed. The corrected
displayed corpus is frozen to both the deployed file and the workspace mirror
(byte-identical, MD5-verified).

| | before | after |
|---|---|---|
| displayed products | 90 | **87** |
| confidence dist | verified 87 · partial 3 | **verified 84 · partial 3** |
| score/grade changes | — | **0 (asserted per surviving row)** |

- **Excluded (§2.2 instability survivors):** `bsip1_maadanim_4584306` (53/C),
  `bsip1_maadanim_7290010472307` (46/D), `bsip1_maadanim_7290119375356` (45/D).
- **Formal `excluded_products` written to `_meta`:** 3 displayed survivors + 8 non-maadanim
  + 6 supplements (re-run safety; the 14 corpus items were already absent from display).
- **Post-freeze re-audit:** Detector 1 = 0, Detector 2 = 0. The shelf is confidence-clean.
- **Idempotent:** re-running the freeze is a no-op.

### Remaining gate → GO
The TASK-128C confidence/corpus gate is now **closed**. Hand to **frontend-agent** to flip
`MAADANIM_V2_SLICE = true` (one line) + **QA** re-baseline at mobile + `lg`. Only the
Central Controller records CLOSED.
