# P264 / Partial flags → material gaps only (route: C1-CURSOR)

Repo C:\Bari, site under bari-web. TASK-424. STAGING ONLY — no commit/push/deploy. Do not git stash/checkout/reset beyond your own lane. Touch ONLY the 9 comparison JSONs that currently have partial-flagged products: bread_frontend_v3, cakes_hard_cookies_frontend_v1, cereals_frontend_v2, cheese_frontend_v4, cookies_coffee_frontend_v2, granola_frontend_v2, hard_cheeses_frontend_v4, hummus_frontend_v5, juices_frontend_v3 (all under bari-web/src/data/comparisons/). NO score/grade/number/ingredient/d4_additives changes — only the confidence label/tooltip fields.

## Owner decision (2026-07-01)
Only flag a product "partial" if a MATERIAL nutrition field is actually missing. Fiber (and any field NOT used by the score) is immaterial — a product missing only immaterial fields has a fully-determined score and must NOT show a partial badge.

MATERIAL fields (the scoring inputs) = energy, protein, fat_g, sugar, sodium (check the product's real nutrition wherever it lives — likely nested under `expansion` and/or `_scoring_trace`; find where complete products carry these and use the same path). IMMATERIAL = fiber and anything outside the material set.

## Do
For every product currently flagged partial (`confidence`=="partial" or `confidence_label_he`=="ניתוח חלקי"):
- If ALL material fields are present (the only gap is fiber/immaterial) → **UN-FLAG it**: set it to the FULL-confidence state exactly as complete products in the SAME file carry it (mirror their `confidence`, `confidence_label_he`, and `confidence_tooltip_he` values — read a verified product in that file to get the exact strings; do not invent).
- If ANY material field is missing → **KEEP it flagged** with the current honest wording (unchanged): label "ניתוח חלקי", tooltip "חלק מהנתונים התזונתיים לא היו זמינים מהסריקה הישירה; הציון מתבסס על הנתונים שנמצאו."
- Do NOT discard any product. Do NOT change scores/grades. Do NOT touch products that were already full-confidence.

## Verify + report (per file)
- partial before → after; how many UN-flagged (immaterial-only) vs KEPT (material missing); for a sample of 5 un-flagged, name which fields were present to justify it; for a sample of kept, name the missing material field.
- Confirm 0 score/grade changes (barcode-keyed vs HEAD) and that only confidence_* fields differ.

End with the return contract (01_framework/operations/return_contract_v1.md); status RETURNED, not CLOSED. Trace-derived counts + the command.
