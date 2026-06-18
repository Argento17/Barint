"""
DISABLED — Open Food Facts (OFF) acquisition removed (TASK-238 / TASK-248).

Original purpose: BSIP0 Yohananof Butter (חמאה) scraper (TASK-191) — used the Israeli
price-transparency feed (il_prices) to discover butter barcodes from the Yohananof
chain, then enriched each barcode with a nutrition panel from Open Food Facts
(il_prices gives identity + price only, never nutrition; OFF was the sole panel source).

OFF is BANNED project-wide (owner hard rule, TASK-238): never a source for nutrition,
ingredients, names, images, barcodes, or fallback — for any category, ever. "Unknown is
acceptable; OFF is not." There is no replacement source wired here; this category, if
rebuilt, must come from a direct retailer/product scrape, or stay NULL.

Re-enable only under a future explicit written owner policy.
"""
raise RuntimeError(
    "DISABLED (TASK-238/248): 01_scrape_yohananof_butter.py acquired Open Food Facts "
    "panels, which are banned project-wide. No OFF code path may run. See CLAUDE.md."
)
