"""
DISABLED — Open Food Facts (OFF) acquisition removed (TASK-238 / TASK-248).

Original purpose: BSIP0 Yohananof Cheese acquisition (TASK-210 Phase B) — used the
il_prices + Open Food Facts model (same as multiretailer_cereals): il_prices catalog for
identity, then paired each barcode with an OFF panel for nutrition + ingredients
(il_prices gives identity + price only; OFF was the sole panel source).

OFF is BANNED project-wide (owner hard rule, TASK-238): never a source for nutrition,
ingredients, names, images, barcodes, or fallback — for any category, ever. "Unknown is
acceptable; OFF is not." There is no replacement source wired here; this category, if
rebuilt, must come from a direct retailer/product scrape, or stay NULL.

Re-enable only under a future explicit written owner policy.
"""
raise RuntimeError(
    "DISABLED (TASK-238/248): 01_acquire_yohananof_cheese.py paired il_prices barcodes "
    "with Open Food Facts panels, which are banned project-wide. No OFF code path may run."
)
