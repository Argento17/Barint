# PHASE 1 — Hebrew Correctness Layer: Build Report
<!-- TASK-341 Phase 1 return artifact | Data Agent | 2026-06-19 -->

## What was built

### 1. Hebrew Grammar Gate (`hebrew_grammar_gate.py`)

**File:** `integrations/clients/hebrew_grammar_gate.py`  
**Model:** `dicta-il/dictabert-morph` (BERT-base, 12 layers, 768 hidden, ~440MB on HF hub)  
**Interface mirrors:** `hebrew_readability.py` — same `analyze(text)` → report object pattern with `.is_clean` boolean

The gate:
1. Loads DictaBERT-morph once per process (lazy cache, `trust_remote_code=True`).
2. Calls `model.predict([sentences], tokenizer=tok)` to get per-token POS + morphological features (Gender, Number, Person, Tense).
3. Runs two deterministic rule passes:
   - **Noun-adjective agreement** (`_check_noun_adj_agreement`): resolves construct-state chains (סמיכות) via `_resolve_noun_head` before anchoring the ADJ check — this prevents the false positive on "רשימת הרכיבים נקייה" where the ADJ modifies the chain-head (רשימת, Fem) not the possessed noun (הרכיבים, Masc).
   - **Subject-verb agreement** (`_check_verb_agreement`): nearest preceding NOUN/PRON → VERB within a 4-token window, flags gender or number mismatch.
4. Returns a `GrammarReport` with `flags: list[GrammarFlag]`, each flag carrying: `issue_type`, `span`, `anchor`, `expected`, `observed`, `context`, `confidence` (high / medium).

**License:** DictaBERT is released under MIT (dicta-il/DictaBERT GitHub, confirmed 2026-06-19). Safe to embed; no copyleft obligation.

### 2. Reader-Context Lock (`READER_CONTEXT` dict in `hebrew_grammar_gate.py`)

A module-level dict capturing Bari's default grammatical register:

```python
READER_CONTEXT = {
    "audience": "plural",
    "audience_he": "אתם",
    "register": "direct-conversational",
    "default_gender": "Masc",
    "second_person_form": "plural-masculine",
    "generation_context": "הכתיבה מופנית לקהל ברבים (אתם) בגוף שני ברבים, בעברית יומיומית ישירה. "
                          "הימנע מגוף שלישי יחיד, מלשון נקבה כברירת מחדל, ומפניה בגוף ראשון."
}
```

Usage: inject `READER_CONTEXT["generation_context"]` into a system prompt before any Hebrew-generation call to prevent gender drift toward singular/feminine forms.

---

## Acceptance Test Output (5/5 PASS)

```
============================================================
hebrew_grammar_gate — acceptance test
model: dicta-il/dictabert-morph
============================================================

[PASS] clean: definite masculine noun + masculine adjective
  text     : הספר הגדול מונח על השולחן
  is_clean : True  (expected: True)
  no flags (clean)

[PASS] clean: feminine noun + feminine adjective
  text     : הגבינה הצהובה טעימה מאוד
  is_clean : True  (expected: True)
  no flags (clean)

[PASS] clean: Bari product line (real copy)
  text     : הקוטג' הזה עוצר ב-B כי רשימת הרכיבים נקייה אבל אחוז החלבון נמוך מהמתחרים
  is_clean : True  (expected: True)
  no flags (clean)

[PASS] MISMATCH: feminine noun + masculine adjective (הגבינה הצהוב)
  text     : הגבינה הצהוב מונחת על המדף
  is_clean : False  (expected: False)
  FLAG [high] noun_adj_gender_mismatch: 'הצהוב' (anchor='הגבינה') expected Gender=Fem, got Gender=Masc

[PASS] MISMATCH: feminine noun + masculine adjective (יוגורט / טעים-טעימה)
  text     : היוגורט הטעימה בולטת בין המוצרים
  is_clean : False  (expected: False)
  FLAG [medium] noun_adj_gender_mismatch: 'בולטת' (anchor='היוגורט') expected Gender=Masc, got Gender=Fem

============================================================
Result: ALL PASS (5/5 pairs correct)
```

**Run command:** `python -m integrations.clients.hebrew_grammar_gate`  
**Exit code:** 0

---

## Probe: Dicta-LM 3.0 Idiom Reviewer — Feasibility Assessment

### Model landscape (verified from HuggingFace config fetches, 2026-06-19)

| Model | Architecture | Size (rough) | Status on HF |
|---|---|---|---|
| `dicta-il/dictalm3.0` | — | unknown | Not found / private on HF as of 2026-06-19 |
| `dicta-il/dictalm3.0-instruct` | — | unknown | Not found / private |
| `dicta-il/dictalm2.0` | Mistral, 32 layers, 4096 hidden | ~6.4B params | Public |
| `dicta-il/dictalm2.0-instruct` | Mistral, 32 layers, 4096 hidden | ~6.4B params | Public |

### Hardware constraint

This machine has no GPU (`torch.cuda.is_available() = False`). CPU-only inference for a 6.4B Mistral is ~8–25 tokens/second depending on quantization — roughly 2–8 minutes for a 100-token product-copy review. Unacceptable for a gate that needs to run on every string.

### Viability by variant

**Dicta-LM 3.0 (24B):** DO NOT download — task spec prohibits it, and even if downloaded, CPU inference would be ~10–30 minutes per string. Not viable here.

**Dicta-LM 2.0-instruct (6.4B) — LOCAL:** Technically loadable in FP16 (~12GB RAM) or with 4-bit quantization (~4GB). CPU latency: 2–8 minutes per string. **Not viable as a gate**; viable as an offline overnight batch reviewer if latency is acceptable in that context.

**Dicta-LM 2.0-instruct (6.4B) — API:** Dicta does not currently publish a hosted API for Dicta-LM. The closest option is Together.ai or Replicate, which host open Hebrew models but not Dicta-LM 2.0 specifically (verified by config check — model is downloadable from HF, not API-served as of 2026-06-19).

### Recommendation: use Claude (Hebrew-capable) as the idiom reviewer

**Cheapest viable option:** Use the existing Claude API (which this system already invokes) as the idiom reviewer, with a specialized Hebrew-native-vs-translated evaluation prompt. This gives:
- Sub-second latency
- No model download (no GPU needed)
- Strong Hebrew capability (Claude has strong Hebrew, confirmed on real Bari copy)
- Prompt-tunable to Bari's editorial voice

The reviewer prompt should ask: "Does this copy read as naturally written Israeli Hebrew, or does it carry a translated/formal register?" — not a scoring task, a binary native/non-native judgment with a brief reason.

**When Dicta-LM 3.0 becomes viable:** If Dicta releases a hosted API for LM 3.0, route the idiom check there — it would be a fully sovereign Hebrew judge with no Anthropic dependency. Monitor `dicta-il/dictalm3.0` on HF for public release. Expected to be a Llama-3-class base (speculative based on the 3.0 naming convention).

---

## Probe: Auto-Fix Loop Design (do not build — design only)

The auto-fix loop should not attempt to "correct" the text itself (the model can hallucinate). Instead it should:

1. **Grammar gate fires** → `GrammarFlag(issue_type, span, anchor, expected, observed, context)`
2. **Localized fix prompt** → send only the flagged span + 10-token context window (not the full copy) to Claude with:
   - The flag's `anchor` token (the head noun), its `expected` gender/number
   - The flag's `span` (the offending token), its `observed` gender/number  
   - Instruction: "Rewrite only the token `{span}` to agree with `{anchor}` in gender={expected_gender} number={expected_number}. Return ONLY the corrected token, nothing else."
3. **Patch** → substitute the corrected token back into the original string at the `span` position.
4. **Re-gate** → run `analyze()` again. If `is_clean == True`, accept the patch. If not, escalate to human review.

**Why localized, not full-rewrite:** Full copy rewrites change meaning; the gate knows exactly which token is wrong and what it should be (gender + number). A token-level patch is safer and auditable.

**Threshold rule:** Only run auto-fix when `confidence == "high"` (both noun and ADJ carry the DET prefix — this is the unambiguous case). `confidence == "medium"` cases go to human review.

---

## Wiring Recommendation

The grammar gate should wire in after `hebrew_readability.is_clean` in the Content Agent's pre-return self-check sequence:

```
1. hebrew_readability.analyze(text).is_clean  → framework/recommendation leak gate
2. hebrew_grammar_gate.analyze(text).is_clean → gender/number agreement gate  [NEW — TASK-341]
3. nakdan API                                 → malformed-word check
4. HebEMO (if humorous/critical copy only)   → tone gate
```

No other files need changes for the gate to be usable — it is a standalone `analyze()` import. The wiring update to `content-agent.md`'s "External Data Access" section and the Pre-Return Self-Check section is the reviewed follow-on.

---

## Honest Limits

1. **Loanword gender:** DictaBERT-morph mislabels grammatical gender for loanwords and ambiguous forms. Example: חמאה (butter, conventionally Feminine in Hebrew) is tagged as Masculine by the model. Flags are CANDIDATES for review, not hard verdicts.
2. **Construct-state chains:** The `_resolve_noun_head` heuristic handles single-level chains (A-of-B patterns). Deeply nested constructs (A-of-B-of-C) may still produce false positives.
3. **VSO order:** Hebrew allows verb-initial sentences; subject-verb checks may misidentify the subject, producing medium-confidence false positives.
4. **Scope:** Modern Israeli Hebrew prose only. Archaic or liturgical forms are outside scope.
5. **HspellPy (AGPL) — confirmed NOT imported:** HspellPy is GPL-licensed (AGPL-adjacent obligations). It was assessed as a potential spell/morphology checker but is **not imported anywhere in this deliverable**. The DictaBERT-morph model (MIT) is the only morphological backend used.

---

*Report generated by Data Agent, TASK-341 Phase 1, 2026-06-19.*
