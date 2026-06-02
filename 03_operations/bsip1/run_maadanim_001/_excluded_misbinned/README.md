# Excluded from the מעדנים (maadanim) corpus — mis-binned products

These BSIP1 records were scraped into the maadanim shelf but do not belong to the
dairy-dessert category. They are quarantined here (not deleted) to preserve provenance
and are excluded from `run_maadanim_001` BSIP2 scoring and all maadanim counts.

## bsip1_554532.json — גבינה צפתית מעודנת 5% (TASK-147)
- **What it is:** a צפתית (Tzfat) salty *cheese*, not a dairy dessert.
- **Evidence:** BSIP0 `source_url` resolves to שופרסל's *מדף הגבינות › גבינות מלוחות*
  (cheese counter › salty cheeses); BSIP0 `category_raw` = `[A0104, ..., A010407, A01]`
  (cheese taxonomy), distinct from the maadanim/קינוחים path.
- **Why it landed in maadanim:** acquired via the `עדנה` brand query — the substring
  `עדנ` inside the product name `מע·עדנ·ת` ("מעודנת") matched the עדנה anchor.
- **Why it was the lone A in the patched (0.4.1) run:** a clean high-protein, low-fat,
  low-carb cheese with a FALSE added-sugar signal. The "סוכר" sweetener marker came from
  un-sanitized nutrition-panel text bleed ("...1.5 כפיות סוכר..."), not a real ingredient;
  `sugars_g` is actually null. Removing it removes a spurious A that was never a dessert.
- **Disposition:** belongs in the cheese category. The cheese pipeline (`run_cheese_001`)
  is a separate, currently NON-AUTHORITATIVE / NO-GO run; re-insertion into a cheese
  corpus is out of scope for TASK-147 and tracked there if/when cheese goes live.
- **Live impact:** none — this product was never on the live maadanim 87-shelf.
