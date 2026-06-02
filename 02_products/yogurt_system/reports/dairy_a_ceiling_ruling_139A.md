# Dairy A-Ceiling Ruling — Can plain live-culture dairy reach grade A?

**Task:** TASK-139A · **Owner:** nutrition-agent · **Date:** 2026-06-01
**Type:** Scoring-philosophy ruling (governed grade-structure decision) — no engine code changed in this task.
**Engine read:** proto_v0 / 0.4.0 · **Evidence:** BSIP2 Evidence Registry v1 (EV-014, EV-015, EV-018, EV-019) + frozen milk precedent (CNO ruling 2026-05-30).
**Co-sign required:** Product (published-grade consequence).
**Gates:** TASK-139B / 139C re-score interpretation, TASK-142 (cheese scoring), TASK-143.

---

## 1. The question, stated precisely

run_yogurt_003 (88 real Shufersal SKUs, engine unmodified) produced **0 grade-A**: median 57,
ceiling 78.2/B, with 60% of SKUs read as NOVA 4 because real Israeli labels expose added sugar
(`סוכר`), modified starch (`עמילן…E-1442`), and stabilizers (`פקטין`). The reconciliation framed
this as a philosophy fork:

> *Does Bari accept that mainstream Israeli yogurt tops out at B, or should plain live-culture
> yogurt reach A?*

That framing conflates **two different ceilings** that this ruling must separate:

- **Category ceiling** — what the *best possible* product in the category can score.
- **Mainstream ceiling** — what the *typical shelf* product scores.

The ruling below answers both, and resolves which frozen precedent governs.

---

## 2. The two frozen precedents — and the decisive test

| Precedent (frozen) | Top product | Why that ceiling | Governing logic |
|---|---|---|---|
| **Milk** (CNO 2026-05-30) | whole / 4% / goat dairy = **85/A** | NOVA 1, single-ingredient, intact matrix, zero additives, zero engineering. *A is a structural-coherence claim, not a health claim.* | A is **earned** by a clean dairy matrix. |
| **Snack bar** (frozen) | snk-001 date-almond bar = **70/B** | Even the best bar carries an **intrinsic, irreducible compromise** — concentrated sugar (dates) + bar-forming processing. No reformulation removes it while staying a bar. | B is the **honest category ceiling** when the best-case product is still compromised by construction. |

**Decisive test:** *Does the best-possible plain, additive-free, live-culture yogurt carry an
intrinsic, irreducible compromise of the snack-bar kind — or is it a coherent dairy matrix of the
milk kind?*

**Answer: it is the milk kind, and it is in fact *more* complete than whole milk.** A plain,
additive-free, live-culture yogurt is a whole-milk matrix **plus a documented positive** —
fermentation (EV-015: phytase-driven mineral bioaccessibility, organic-acid glycemic dampening,
restructured protein). It has **no** snack-bar-style irreducible compromise: its sugar is intrinsic
lactose (not added), its fat is intrinsic dairy fat, and it carries live cultures milk does not.

The only thing pulling the cleanest Israeli yogurts below milk is the **milk-powder standardization
step** (`milk + אבקת חלב + culture` → read NOVA 3), which is a fortification/standardization
operation, **not** an engineering compromise. That is a ~20-pt processing/WFI cost, not a structural
disqualification.

**Conclusion: yogurt (and white cheese) inherit the MILK precedent, not the snack-bar precedent.**

---

## 3. The "0 grade-A" result is mostly an artifact, not a philosophy signal

Per the TASK-135 calibration impact audit (`yogurt_calibration_impact_audit_135.md`), the absence
of any A in run_yogurt_003 is **not a punitive ceiling** — it is the **culture-detection gap (Gap 2)**:

- The defining positive of a live yogurt — its cultures — currently scores **zero**. The enricher's
  `FERMENTATION_TERMS` match **0/88** SKUs, while the Israeli label vocabulary actually present
  (`ביפידוס` / `פרוביוטי` / `תרבית` / `BIFIDUS`) appears in **54/88 (61%)**.
- The fermentation credit is **+8.2 pts**, gated to **NOVA ≤ 3** (`FERMENTATION_DIRECT_BONUS=8` +
  WFI). That gate is correct: it credits clean plain/bio yogurts and **does not rescue** sugar-laden
  NOVA-4 flavored yogurts.
- Restoring culture detection lifts the cleanest plain/bio/lactose-free tier to **~80–86 → grade A
  organically**, producing the run's first **~2–5 earned A's** — with **no change to scoring
  philosophy and no format credit.**

So a large share of the "missing A-ceiling" was the culture-detection bug wearing a philosophy
costume. **The truthful category outcome is A-reachable; the truthful mainstream outcome is B.**

---

## 4. THE RULING — `RULING-DAIRY-A-01`

> **B is the truthful ceiling for the sweetened/stabilized mainstream (≈60% of the Israeli yogurt
> shelf). It is NOT the truthful ceiling for the category. Plain, additive-free, live-culture dairy
> — yogurt AND white cheese — MAY reach grade A, earned organically by score, in exact parallel to
> whole milk at 85/A. No category A-grant, no floor, no format credit.**

### 4.1 The exact condition under which dairy reaches A

A live-culture dairy product (sub-pools: `yogurt`, `white_cheese`) is **A-eligible** when **ALL six**
hold. If any fails, the ceiling is **B** (sweetened/stabilized mainstream) or lower.

| # | Condition | Signal / evidence | Disqualifier examples |
|---|---|---|---|
| **C1** | **No added sugar / caloric sweetener** | `added_sugar_sources_count == 0`. Fruit-prep / `פירות יער` flavoring counts as added sugar. **Must exclude the `סוכרים`→`סוכר` nutrition-text false positive** flagged in the audit. | `סוכר`, `סוכר לבן`, glucose-fructose syrup, fruit prep |
| **C2** | **No engineered additive load** | No modified starch (E-14xx), no synthetic stabilizers/thickeners, no artificial sweeteners, no flavor enhancers, no colors. Label-neutral natural set-agents are **not** disqualifying (EV-019 prebiotic-gum / neutral-gum exemption). | `עמילן מעובד E-1442`, סוכרלוז, צבעי מאכל |
| **C3** | **Live culture confirmed AND credited** | `fermentation_marker_detected == true` and the EV-015 bonus is applied. **Requires the Gap 2 Israeli culture-vocabulary fix** (`ביפידוס`/`פרוביוטי`/`תרבית`/`BIFIDUS`). The yogurt-defining positive must be present, not assumed. | "sourdough flavour"-equivalent: vinegar/acid-only with no microbial strain ⇒ no credit |
| **C4** | **Intact dairy-protein matrix** | Milk base. Milk-powder *standardization* permitted (NOVA ≤3 read). A **reconstituted / `חלב מאבקה`-primary base is NOT A-eligible** (EV-018 reconstituted-matrix downgrade). | חלב מאבקה as primary, חלב מרוכז |
| **C5** | **Correct dairy identity (routing)** | Routed `yogurt` / `white_cheese`, **not** `dessert` / `cereal` / `whole_food_fat`. Requires the Gap 1 router yogurt-anchor fix (19% misroute today). | יופלה GO→dessert, crunch→cereal, זית→WFF |
| **C6** | **Confidence = verified** | Full ingredient + nutrition coverage; no confidence ceiling applied. | INSUFFICIENT / partial |

When C1–C6 hold, the product reaches A **by score alone** — fermentation bonus (EV-015) + clean
processing + protein density — the identical mechanism to whole milk's earned 85/A. The engine is
**not** instructed to grant A by category; it is permitted to *reach* A when the matrix earns it.

### 4.2 White cheese (TASK-142/143) — same condition, one clarification

`RULING-DAIRY-A-01` applies unchanged to white cheese / quark / `קוטג'` / `גבינה לבנה`. Plain,
additive-free, live-culture white cheese is A-eligible; salted, stabilized, or flavored white cheese
is B or lower. **EV-014 (hard-cheese calcium saponification) is a fat-absorption exception, not an
A-grant** — it softens the saturated-fat penalty on *hard* cheese only and does not by itself confer
grade A. It must not be read as a back-door A for processed/spreadable cheese.

### 4.3 What this ruling explicitly does NOT do

- It does **not** validate the DEC-005 manual shelf's blanket **5×A by format credit** (88/A on
  plain תנובה 3%). That is over-generous format-credit the engine correctly disciplines.
- It does **not** rescue any sweetened, stabilized, or flavored yogurt. The NOVA-4 majority stays
  C/D — **correctly** — because they genuinely contain added sugar + modified starch + stabilizers.
- It does **not** lower the milk precedent or contradict the snack-bar precedent. Both remain frozen.

---

## 5. Published-grade consequence — flag for Product

**This ruling permits an A to appear on the replaced yogurt shelf and the new white-cheese shelf —
but only for products that earn it organically after the Gap 2 culture fix.** Product must co-sign
the following downstream consequences:

| Consequence | Today (DEC-005 manual) | After ruling + Gap 2 re-run (run_yogurt_004) |
|---|---|---|
| Grade-A count on yogurt shelf | **5** (format-credited) | **~2–5** (earned; cleanest plain/bio/lactose-free/Greek) |
| Category median | 72 | **~61–63** (truthfully lower — flavored lines carry sugar) |
| What disappears | — | The format-credited A's that were never earned |
| White-cheese shelf | n/a (not built) | A-eligible only under C1–C6; otherwise B or lower |

**Net message for the consumer:** fewer A's, a lower median, but **every A is earned**. This is
truthful disciplining, not a regression — and it is consistent with "best ≠ excellent."

### ⚠️ One unresolved calibration dependency Product/139B MUST reconcile before publishing grades

The A threshold is **inconsistent across the two authoritative reads**:

- `scoring.md` (Grades table) states **A = 85–100**.
- The frozen milk run_004 report applied **A ≥ 80** (whole milk = 85 = A; B labeled 65–79, A ≥ 80).

The cleanest yogurts project to **~80–86**. Whether **2 or 5** of them cross into A depends entirely
on whether the live A cutoff is **80 or 85**. **This must be reconciled before TASK-139B publishes
any yogurt grade**, or the A-count is undefined. Flagged to Product as a blocking pre-condition for
139B, not resolved here (resolving it would be an un-instructed scoring change).

---

## 6. Evidence registry registration

Registered as **`EV-021` — Live-Culture Dairy A-Ceiling Governance Ruling** in
`03_operations/bsip2/evidence_registry/bsip2_evidence_registry_v1.{md,json}`. It is a
**governance ruling**, not a new evidence finding — it composes existing findings:

- **EV-015** (fermentation bonus) — the positive that earns the A.
- **EV-014** (hard-cheese saponification) — explicitly *not* an A-grant.
- **EV-018** (reconstituted-matrix downgrade) — C4 disqualifier.
- **EV-019** (prebiotic/neutral-gum exemption) — C2 non-disqualifier.
- **Milk precedent** (whole/4%/goat = 85/A) — the governing analogy.

No new scoring rule, weight, or threshold is created by this ruling. It governs the *ceiling
permission* for a category; the *mechanism* is the already-registered EV-015 bonus.

---

## 7. Governance verdict (bari-bsip2-scoring-governance)

```json
{
  "proposal_id": "RULING-DAIRY-A-01 (TASK-139A dairy A-ceiling)",
  "review_date": "2026-06-01",
  "reviewer": "Claude (bari-bsip2-scoring-governance)",
  "governance_checks": {
    "evidence_registry_reference": "pass — EV-021 created; composes EV-014/015/018/019 + milk precedent",
    "label_observability": "conditional — depends on fermentation_marker_detected, currently 0% coverage due to the Gap 2 vocabulary gap; the A-condition CANNOT activate until culture-vocab coverage is restored and tracked (this is why the ruling gates 139B)",
    "category_activation_scope": "pass — scoped to dairy_protein sub-pools {yogurt, white_cheese}; not global",
    "rollback_plan": "pass — ruling is a documented decision, no code changed; if Product rejects, revert to status quo (engine B-read stands, DEC-005 manual shelf remains LIVE)",
    "rule_accumulation_check": "pass — no shadow rule; composes existing EV-014/015/018/019 rather than duplicating them"
  },
  "verdict": "approved — activation gated on (a) Product co-sign and (b) Gap 2 culture-vocab coverage restoration before 139B publishes grades",
  "blocking_reasons": [],
  "activation_preconditions": [
    "Product co-sign of the published-grade consequence (Section 5)",
    "Gap 2 culture-vocabulary fix restores fermentation_marker_detected coverage on the yogurt corpus (precondition for C3)",
    "A-threshold reconciliation (80 vs 85) resolved before 139B publishes grades"
  ],
  "revision_requests": []
}
```

---

## 8. Decision summary

1. **A is reachable by plain, additive-free, live-culture dairy (yogurt + white cheese).** Dairy
   inherits the **milk** precedent — a clean dairy matrix *plus* the fermentation positive earns A.
2. **B is the truthful ceiling for the sweetened/stabilized mainstream (~60% of the shelf)** — not
   for the category. The category ceiling is A; the mainstream ceiling is B.
3. **The run_yogurt_003 "0 A" is mostly the culture-detection bug, not a philosophy signal.** Fixing
   Gap 2 yields ~2–5 *earned* A's organically — not the manual shelf's 5×A-by-format.
4. **Exact A-condition = C1–C6** (Section 4.1). Earned by score; no grant, no floor, no format credit.
5. **Product co-signs** the published-grade consequence: fewer A's, lower median, every A earned —
   and resolves the 80-vs-85 A-threshold before 139B publishes grades.

---

## 9. State

**Proposes RETURNED pending Product co-sign** — this is a governed grade-structure decision with
published-grade consequences. Blocks/gates 139B/139C re-score interpretation, TASK-142, TASK-143.
Only the Central Controller records CLOSED.

*nutrition-agent · TASK-139A · 2026-06-01 · ruling only — no scores changed, no engine code modified · anchored to frozen milk + snack-bar precedents · evidence-registered EV-021*
</content>
</invoke>
