# Handoff → Shelves Sweep + Clean chat — data-integrity defects found by the de-chain validation (2026-06-26)

**From:** de-chain / TASK-395 orchestrator. **Why:** an independent validation triad (C3 + Gemini + Red-Team) on the de-chain shadow surfaced concrete DATA defects that are bigger than de-chain — they affect TODAY's live scores too. Handing you the clean-relevant ones. De-chain is on hold until your sweep lands; I'll re-validate on the cleaned data.

---

## FINDING 1 (PRIORITY) — Ingredient-field pollution: ~15% of products

**What:** the scraped **ingredient field** has non-ingredient text bleeding into it — most often the **nutrition panel** appended after the real ingredient list, also disclaimers / serving-size / marketing. The parser then counts that junk as ingredients.

**Scale (measured):** 47 of 311 products with ingredient text (**15.1%**) are polluted; dominant in **cheese**. 29 products have parsed-ingredient-count vs real-count diff > 3.

**Dominant marker:** the Hebrew string `ערכים תזונתיים` (nutritional values), usually `ערכים תזונתיים ל-100 גרם` / `100 גרם` followed by kcal/grams — everything from that marker onward is NOT ingredients. Other tails to cut: serving size (`גודל מנה`, `מנה`), allergen/marketing blurbs that follow the list.

**Worst offenders (verify your fix against these barcodes):**
- `7290014758681` קוטג 1% — real label is just `חלב, מלח, תוסף תזונה: סידן (טריקלציום פוספט)` (3 items) but parses as 6 because the panel bled in. (This single artifact wrongly drove the largest score move in our whole shadow.)
- `4127077`, `4127329`, `4127336`, `41445`, `41452` (cottage cheeses), `2824183`, `2824640` (white cheeses) — same nutrition-panel-bleed pattern.

**Impact:** corrupts ingredient COUNT and likely ingredient-derived scoring for these products — on the LIVE shelves, not just our candidate. Any logic that reads the ingredient list (count, ingredient quality, NOVA, confidence) is getting garbage in for ~15%.

**What to apply:**
1. In the clean pass, **truncate the ingredient field at the first nutrition-panel marker** (`ערכים תזונתיים` / `ערך תזונתי` / `ל-100 גרם`) and strip trailing serving/disclaimer/marketing sections, BEFORE any parsing. Source fields to clean: `ingredients_text_he` then `ingredients_raw` (BSIP1 `03_operations/bsip1/.../output`, carried from the BSIP0 scrape).
2. **Flag-and-escalate, don't silently fix:** if a field is still ambiguous after cleaning (can't confidently isolate the ingredient list), raise it as an imperfect read rather than scoring it — per the owner's "raise the imperfect reads / unknown is acceptable" rule. Don't impute.
3. Acceptance: the 8 barcodes above parse to their TRUE ingredient count after cleaning (e.g. `7290014758681` → 3 items, not 6); re-scan and report the new pollution rate.

---

## FINDING 2 — Provenance leaks (reproducibility): 7 of 12 live categories can't regenerate their published scores

These break "re-score and get the same number," which blocks any trustworthy before/after.

- **Unrecorded patch:** the D4 additive patch (`BARI_D4_SCORE_V1`, commit `361748722`, 2026-06-22) was applied to LIVE files but never written into any `configs/*.json` flag block nor `rescore_all.py` `MANAGED_BARI_VARS`. Setting it on reproduces cheese+milk exactly; off over-scores them. Cookies_coffee was published WITHOUT it. **Per-category publish-time flag state is unrecorded.**
- **NULL run_id** on frontend files: bread (v2, v3), cheese_v4, snacks_v5.
- **Wrong corpus pinned:** snacks config points to `run_001` / `run_snack_bars_001`, but the live page is the later `task362` build — only 12/21 barcodes overlap.
- **Baseline pointer mismatch:** granola — config + manifest say `granola_frontend_v1.json`, but the route imports `granola_frontend_v2.json` (`bari-web/src/lib/comparisons/granola-page-data.ts`); the two differ on 20/22 products.
- **Uncovered live routes:** chocolate-bars, chocolate-tablets, protein-bars have live routes but **no** `live_manifest.json` entry and no `page_generator/configs` — zero provenance.
- Small non-D4 ~±2 pt drift on cereals / hard_cheeses / juices (suspect router commit `b3319fede`).

**What to apply:** while you sweep each shelf, persist a full **provenance record** per published file — corpus `run_id` + the COMPLETE flag vector (including patches like D4) + engine version — and reconcile each category's served file to a reproducible source (fix the granola v1↔v2 pointer, re-pin snacks to the task362 corpus, bring chocolate/protein into the manifest+configs). Goal: every published score round-trips to its committed hash.

---

## FINDING 3 — Two code bugs (likely OUT of your scope — for when de-chain resumes, but flagging in case you touch the reader)
- **`חומר משמר` (preservative, mem) ≠ `חומר שימור` (preservation, shin):** any contested/additive lexicon keyed on `חומר שימור` MISSES the common `חומר משמר` spelling → preservatives slip through. (Real case: brined cheese `2133889`.) Worth adding `חומר משמר` wherever `חומר שימור` is used.
- A no-data product in our candidate emits the string `"WITHHELD"` where the frontend contract expects a null grade — de-chain-internal, I'll fix on resume.

---

## Coordination
- **I am on hold and will not touch the shared tree** (`C:\Bari`) while you sweep — my de-chain work is isolated in git worktrees. No collision from my side.
- When you finish, please **flag done + list which files/corpus you changed** so I can re-run the reproducibility map and re-shadow on the cleaned data.
- Priority order for me: Finding 1 (pollution) is the hard blocker; Finding 2 (provenance) unblocks the 7 unreproducible categories.
