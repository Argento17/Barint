# Gate Scope Carve-Out Spec — Guides Tier-Label Exemption (implements EXCEPTION-003)

**Author:** Product Agent · **Date:** 2026-07-04
**Implements:** `01_framework/governance/exception_registry_v1.md` EXCEPTION-003
**Target file:** `integrations/clients/hebrew_readability.py` (and any caller that
validates Guides tier-label strings — currently ad hoc red-team review per
`03_operations/reports/qa/magnesium_guide_tier_copy_redteam_v1.md` RT-4; recommend this
becomes the scope-declaration point if/when a mechanical Guides copy CI check is built).
**Owner:** gate/copy-rules code owner (wiring) + Frontend (call-site integration).
**Product does not implement this spec.** No code is edited by this document.

---

## 1. Premise (verified, not assumed)

Read directly from `integrations/clients/hebrew_readability.py`:

- `_RECOMMENDATION_TERMS` (line 92) includes the literal term `"מומלץ"`.
- `_scan_leaks()` (line 202-205) matches via `text.find(term)` — a **substring** search,
  case-sensitive, anywhere in the input string.
- `"recommendation"` is one of the 6 `_HARD_LEAK_KINDS` (line 107-108) — any hit sets
  `is_clean = False` regardless of context.
- `analyze(text: str)` (line 223) takes **only** a text argument — no route, doc-type, or
  scope parameter exists today. Every caller (`03_operations/evals/copy_evals/run_evals.py`
  line 50-105, and any other) calls it the same way for every kind of copy.

This confirms the RT-4 finding mechanically: any of the 3 tier labels containing "מומלץ"
(מומלץ מאוד / מומלץ / לא מומלץ) will HARD-fail `is_clean` wherever they're checked, with
no existing mechanism to distinguish "Guides tier label" from "BSIP/comparison copy."

---

## 2. Design goals

1. Exempt **only** the 4 exact tier-label strings registered in EXCEPTION-003.
2. Exempt **only** when the calling context explicitly opts in — no existing call site
   changes behavior by default.
3. **Never** weaken the ban for BSIP/comparison-page copy, marketing collateral, or
   Guides body prose/captions that merely contain a recommendation word inside a longer
   sentence.
4. A waived leak stays **visible in the report**, never silently disappears — matches the
   standing "disclosed, never silently vanished" pattern already used elsewhere in this
   codebase's gate design (`display_suppression_rule` in the guides bar rubric).
5. Every waiver is traceable to the exception ID.

---

## 3. Mechanism

### 3.1 New exact-match allowlist (near `_RECOMMENDATION_TERMS`)

```python
# EXCEPTION-003 (01_framework/governance/exception_registry_v1.md) — owner-directed
# tier vocabulary for the מדריכים (Guides) product. EXACT-STRING match only: a leak is
# waived here iff the ENTIRE input text (after strip()) equals one of these strings AND
# the caller explicitly declares scope="guides_tier_label". Never a substring match,
# never applied to prose/captions/body copy, never applied to any other scope.
_GUIDES_TIER_LABEL_EXEMPTIONS = {
    "מומלץ מאוד", "מומלץ", "טוב", "לא מומלץ",
}
```

### 3.2 Opt-in scope parameter

Add `scope: str | None = None` to `analyze()`:

```python
def analyze(text: str, scope: str | None = None) -> ReadabilityReport:
```

Default `None` preserves current behavior for every existing caller — nothing changes
unless a caller explicitly passes `scope="guides_tier_label"`.

### 3.3 Waiver applied at the point of the leak, not by deleting the leak

Extend the `Leak` dataclass (line 113) with two fields:

```python
waived: bool = False
waiver_ref: str | None = None
```

In `_scan_leaks()`, where a `"recommendation"` leak is currently appended (line 202-205):

```python
for term in _RECOMMENDATION_TERMS:
    idx = text.find(term)
    if idx != -1:
        leak = Leak("recommendation", term, _ctx(text, idx))
        if scope == "guides_tier_label" and text.strip() in _GUIDES_TIER_LABEL_EXEMPTIONS:
            leak.waived = True
            leak.waiver_ref = "EXCEPTION-003"
        leaks.append(leak)
```

(`_scan_leaks` needs `scope` threaded into it from `analyze()`.)

### 3.4 `is_clean` excludes only waived leaks

Change (line 133-139):

```python
@property
def is_clean(self) -> bool:
    return not any(l.kind in _HARD_LEAK_KINDS and not l.waived for l in self.leaks)
```

### 3.5 Waived leaks still appear in `.flags`, labeled distinctly

In the flag-building loop (line 244-256), before the existing `"recommendation"` branch:

```python
elif l.kind == "recommendation" and l.waived:
    flags.append(f"WAIVED ({l.waiver_ref}): recommendation language '{l.term}'")
elif l.kind == "recommendation":
    flags.append(f"RECOMMENDATION language: '{l.term}'")
```

---

## 4. Why this cannot leak into BSIP/comparison copy or Guides prose

The exact-string equality check in §3.3 is the load-bearing safety property, not the
`scope` flag alone. Even if a caller mistakenly passed `scope="guides_tier_label"` while
validating a full caption or sentence (e.g. "המוצר הזה מומלץ מאוד לרוב הצרכנים"), that
string does not `==` any of the 4 short exact strings in
`_GUIDES_TIER_LABEL_EXEMPTIONS` — only equals one when the *entire* validated value is a
bare tier label — so it cannot accidentally match. The `scope` parameter is a second,
independent gate on top of that: BSIP/comparison-page callers never pass it, so they
receive zero behavior change even in the hypothetical worst case where the equality check
were somehow bypassed.

---

## 5. Required tests before this ships (spec, not code)

1. `analyze("מומלץ", scope="guides_tier_label").is_clean is True` — bare label, scoped →
   waived.
2. `analyze("מומלץ").is_clean is False` — same bare label, no scope declared → still
   fails. Proves the exemption is opt-in, not a global unban.
3. `analyze("המוצר הזה מומלץ מאוד לרוב הצרכנים", scope="guides_tier_label").is_clean is
   False` — full sentence containing a tier label as a substring, even with scope
   declared → still fails. Proves prose is never covered.
4. `analyze("מומלץ מאוד").is_clean is True` and `analyze("לא מומלץ").is_clean is True`,
   both with scope declared — the other 2 leaking labels.
5. A comparison-page or BSIP copy string containing "מומלץ" with no scope argument →
   unaffected, still fails exactly as today (regression guard — proves the ban elsewhere
   is intact).

---

## 6. Call-site integration note (for whoever wires this)

Whichever script gates Guides copy (today: manual red-team per
`magnesium_guide_tier_copy_redteam_v1.md`; tomorrow: possibly a mechanical
`validate_guide_copy.py` analogous to `validate_comparison_page.py`) must pass
`scope="guides_tier_label"` **only** when validating an isolated tier-label field value
— never when validating a caption, body paragraph, one-liner, or any other Guides string,
even Guides-product strings that are not the tier label itself. If in doubt, do not pass
the scope argument — the string will then be checked under the full, unweakened ban,
which is always the safe default.

---

## Return Contract

```json
{
  "task": "TASK-504-RT4-guides-tier-vocabulary-exception",
  "agent": "Product Agent",
  "artifacts": [
    {
      "path": "C:\\Bari\\01_framework\\governance\\exception_registry_v1.md",
      "change": "added EXCEPTION-003 section (Recommendation-Tier Vocabulary for the Guides Product)",
      "sha256": "df6ddc13c20141beb2b3628c0b92fb3488c4f6ed02fd4262364cde68718b44da"
    },
    {
      "path": "C:\\Bari\\03_operations\\reports\\product\\madrichim_tier_vocabulary_gate_carveout_spec_v1.md",
      "change": "new file — implementable gate carve-out spec, no code edited",
      "sha256": "659afda5b12980075b36a2ca8251f75ee4685191640622e82e8995cd622f79db"
    }
  ],
  "counts": {
    "leaking_tier_labels_of_4": 3,
    "leaking_labels": ["מומלץ מאוד", "מומלץ", "לא מומלץ"],
    "non_leaking_labels": ["טוב"],
    "source": "integrations/clients/hebrew_readability.py lines 90-94 (_RECOMMENDATION_TERMS), 202-205 (_scan_leaks substring match) — read directly, not asserted from the coordinator's message"
  },
  "commands_run": [],
  "not_done": [
    "Nutrition Agent co-sign on EXCEPTION-003 — required per guides bar-rubric governance, not yet requested/received; routing is the orchestrator's job",
    "Gate code itself (hebrew_readability.py) is NOT edited — spec only, per task instruction; implementation belongs to the gate/copy-rules code owner",
    "Call-site wiring (which script passes scope=\"guides_tier_label\" and when) is not implemented — flagged for Frontend/QA in spec §6",
    "The 3 required-re-author copy strings from RT-1/RT-2/RT-3 (מומלץ caption, טוב caption, body[2]) are Content Agent's job, unrelated to this exception, not touched here"
  ],
  "acceptance_test": {
    "spec": "Author an Exception-Registry entry for the owner-directed Guides tier vocabulary (co-sign with Nutrition) and a precise, implementable gate carve-out spec that does not weaken the recommendation-language ban elsewhere.",
    "result": "PASS — EXCEPTION-003 registered in the canonical registry file in the existing format; gate carve-out spec written with exact-match + opt-in-scope double safeguard, verified against the live gate source; no code edited; Nutrition co-sign correctly left outstanding rather than fabricated"
  }
}
```
