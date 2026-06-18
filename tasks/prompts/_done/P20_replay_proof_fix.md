# P20 → Data Agent (cheap lane) — fix the raw-store replay proof: re-key vs corpus, commit a report that actually shows the matches

```
P20 / TASK-255 — The P5 return claimed "47/47 corpus matches, zero content
errors" for the frozen-veg fixture replay, but the committed
03_operations/bsip0/raw_store/replay_report.json shows
stats {total:222, in_corpus:0, matched:0} — every fixture page is keyed by a
Shufersal internal code and NONE matched the corpus. The replay-equivalence
proof is the foundation of the BSIP0.5 fetch/parse split; it is currently
UNPROVEN in the repo. Phase 2 of the scrape program gates on this.

DO:
1. Diagnose the keying gap in 03_operations/bsip0/raw_store/replay_parse.py:
   fixture pages carry Shufersal internal codes (e.g. 103457, P_xxx) while the
   frozen-veg corpus is keyed by EAN barcode. Build the correct join (the
   barcode IS extractable from the stored PDP HTML and/or the existing
   frozen-veg corpus files under 02_products/frozen_vegetables/).
2. Re-run the replay OFFLINE (stored HTML only — no network, that is the whole
   point of the raw store) against the registered frozen-veg corpus.
3. Overwrite replay_report.json with honest stats: total fixtures, in_corpus,
   matched, mismatched, and per-field diffs for every mismatch. If the result
   is NOT clean (real content mismatches, not format normalization), report
   them — do not normalize them away.
4. State where the "47/47" number in the P5 return block came from (a VM-side
   run? a subset? ) — one paragraph of provenance.

RULES: read-only outside 03_operations/bsip0/raw_store/; no network fetches;
no corpus/score changes; no Open Food Facts.

RETURN BLOCK: corrected stats line; mismatch list (or "0 content mismatches");
provenance of the original 47/47 claim; replay verdict (PROVEN / NOT PROVEN).
Propose RETURNED.
```

---
**After you paste this to the agent:** open `tasks\DISPATCH_BOARD.md` and put an `x` in the P20 line under 📬 Signals.
