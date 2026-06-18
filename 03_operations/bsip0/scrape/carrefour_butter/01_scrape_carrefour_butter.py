"""
DISABLED — Open Food Facts (OFF) acquisition removed (TASK-238 / TASK-248).

Original purpose: BSIP0 Carrefour Israel Butter scraper (TASK-191) — discovered butter
barcodes via the Carrefour search API, then acquired every nutrition panel, ingredient
list and image from Open Food Facts by barcode (OFF-only; no direct nutrition scrape).

OFF is BANNED project-wide (owner hard rule, TASK-238): never a source for nutrition,
ingredients, names, images, barcodes, or fallback — for any category, ever. "Unknown is
acceptable; OFF is not." There is no replacement source wired here; this category, if
rebuilt, must come from a direct retailer/product scrape, or stay NULL.

Re-enable only under a future explicit written owner policy.
"""
raise RuntimeError(
    "DISABLED (TASK-238/248): 01_scrape_carrefour_butter.py acquired Open Food Facts "
    "panels, which are banned project-wide. No OFF code path may run. See CLAUDE.md."
)
