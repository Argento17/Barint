# Project Tom's Voice — Program Charter

**Registry:** TASK-374 · **Owner:** content-agent · **Initiated:** 2026-06-22 (owner) · **Priority:** HIGH
**Why now:** strategy is pivoting to content-first; Bari needs *excellent* native Hebrew, not the
current mediocre-but-passable. This charter recalibrates a set of external AI recommendations against
the system we actually have ([[tom_bari_voice_system]], [[content_signoff_hard_rule]],
[[bari_brand_anchor_clarity]]).

---

## 1. The diagnosis (why Hebrew is still mediocre)

We already have: a locked voice fingerprint (`2_voice_fingerprint.md` v1.0), a contrast few-shot
(`3_before_after_pairs.md`), a content blacklist (`5_banned_phrases_and_claims.md`), four NLP gates
(Nakdan / DictaBERT-morph / heBERT-HebEMO / hebrew_readability), an 8-hard-fail voice-match gate
(`7_voice_match_gate.md`), the two-gate sign-off (Content Agent + Adversarial QA), and a harvest engine
(`8_edit_feedback_log.md`). "Add a blacklist / few-shot / gates" is therefore **already done**.

**The real defect:** every existing gate catches a *gross* failure (leakage, code tokens, brand
attacks, nutrition-fact tails, agreement errors, wrong mode). **None detects translationese** —
grammatically-clean, leakage-clean Hebrew that still reads translated/stilted. It passes every gate.

Three holes:
1. **No naturalness detector.** Naturalness lives only in subjective checklist items 11–13, *self-assessed
   by the agent that wrote the copy.* Nothing independent blocks mediocre phrasing.
2. **The blacklist bans content, not syntax.** File 5 bans fear/health/leakage — not the syntactic tells
   of LLM-Hebrew (calqued word order, `אשר`-clauses, `של`-chains, nominalization stacks, redundant
   copulas, `מהווה`/`מבחינת`).
3. **Golden set is two categories deep** (cakes, cereals) — thin exactly on the strategy shelves.

---

## 2. Recalibration of the external recommendations

**Adopt:** Critic+Refiner loop (independent + a *gate*, not a suggestion) · category-specific golden +
style notes · translationese-tell taxonomy + cheap detector · systematic harvest cadence.

**Reject:**
- *"Draft in English → translate to Hebrew."* For us this is the translationese **generator**, not the
  cure — the voice is Hebrew-native idiom (`אז זהו — שלא תמיד`) that does not survive an English layer.
  Salvaged kernel (separate **fact** from **voice**) is already done structurally (Nutrition fact brief →
  Content voice rewrite); never route it through English.
- *DictaLM-2.0 / model-swap as generator.* Conflicts with the fixed lane architecture; weaker at the
  reasoning the voice needs. Demoted to an optional low-priority experiment as a *critic/scorer* only.

**Adopt-with-caution:** RAG only over **our own strongest shipped pieces**. The claim firewall +
citations discipline forbid pulling external blog/article text into generation; file 9 stays
register-calibration-only, never a source.

---

## 3. Locked scope (owner, 2026-06-22)

- **Pilot scope:** protein-bars / snacks / granola first; prove it lifts them to milk/bread level, then
  roll the gate across all live categories.
- **Critic:** an **automated independent LLM-judge Naturalness Gate** is the centerpiece — separate lane
  (not the drafting context), scores naturalness/voice 1–5, names failing lines, hard-blocks below
  threshold, feeds a refiner pass. (Human harvest, `8_edit_feedback_log.md`, continues as-is but is not
  the headline mechanism.)

---

## 4. Phases (by ROI)

- **Phase 0 — Baseline the defect.** Run ~10 owner-flagged "mediocre" lines through *all* existing gates
  to prove they pass (confirms the gap is naturalness); extract the real translationese taxonomy from the
  failures. Measure before building.
- **Phase 1 — Naturalness Gate (centerpiece), TWO-AXIS.** Independent LLM-judge scoring **two** axes
  (owner ruling 2026-06-22, file 10 §D): **F1 naturalness** (no translationese — T1–T7) AND **F2
  stance/substance** (not neutral-bland — has a clear verdict, not hedge-only). A line passes only when
  F1-clean *and* F2-clean. Output: per-axis 1–5 score, named failing lines, in-voice rewrites; below
  threshold = reject → refiner. Calibration set = the 8 owner gold examples (`phase0_owner_gold_examples.md`)
  + the 12 flagged live examples; the gate must flag every owner-flagged line and pass every owner gold
  line. Wire into the 6-stage chain (as a new gate) and into the two-gate sign-off.
- **Phase 1.5 — Fingerprint recalibration pass.** Move `2_voice_fingerprint.md` default texture from
  staccato/fragments/"(!)" to natural connected prose; demote punch moves to seasoning-when-earned; keep
  the stance/verdict commitment as the F2 guard. Target register = *opinionated substance in natural
  connected Hebrew* (the in-between, file 10 §D).
- **Phase 2 — Translationese taxonomy + cheap detector.** Extend file 5 with a syntax-tell section; a
  deterministic regex/heuristic pre-filter (cheap lane) catches mechanical tells before the LLM critic runs.
- **Phase 3 — Category golden expansion.** 5–8 perfect pieces + a one-page style note for each pilot shelf.
- **Phase 4 — Standing harvest cadence.** Every category batch auto-captures before/after; promote at 2–3 repeats.
- **Phase 5 (low-priority experiment).** Test a Hebrew-tuned/alternate lane as the *critic*, evidence-only.

---

## 5. Governance

- Trips only "starts a major program" (tripwire #3) — owner-initiated, so no escalation.
- Touches copy quality, **not scores** — no scoring tripwire. Gates are additive and reversible.
- When the Naturalness Gate changes what ships, output goes through the normal two-gate sign-off.
- Lane split: critic = independent lane (C3 fresh-eyes or a separate Sonnet context) · deterministic
  detector = C2/C0 · golden authoring = C1 per-piece · gate code = C1.
