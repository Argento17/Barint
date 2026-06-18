"""
DISABLED — Open Food Facts (OFF) acquisition removed (TASK-238 / TASK-248).

Original purpose: BSIP0 Multi-retailer Breakfast Cereals + Granola/Muesli acquisition
(TASK-184) — used Israeli price-transparency catalogs (il_prices) as the identity layer,
then paired each barcode with an Open Food Facts panel for nutrition + ingredients
(il_prices gives identity + price only; OFF was the sole panel source).

OFF is BANNED project-wide (owner hard rule, TASK-238): never a source for nutrition,
ingredients, names, images, barcodes, or fallback — for any category, ever. "Unknown is
acceptable; OFF is not." There is no replacement source wired here; this category, if
rebuilt, must come from a direct retailer/product scrape, or stay NULL.

Re-enable only under a future explicit written owner policy.
"""
raise RuntimeError(
    "DISABLED (TASK-238/248): 01_acquire_multiretailer.py paired il_prices barcodes with "
    "Open Food Facts panels, which are banned project-wide. No OFF code path may run."
)
