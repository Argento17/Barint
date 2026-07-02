# P240 / SIE: can we broaden sources & research? (route: C3)

You are the independent outside-the-family advisor (red-team / research 2nd opinion). Evidence + reasoning only — no data production, no file edits. Be concise and concrete; name specific source types, not generalities.

## Context — Bari Supplement Intelligence Engine (SIE)
We scored the Israeli Super-Pharm supplement shelf: 118 addressable SKUs, 82 scored (69.5%), 36 unscoreable. The engine is proven (golden 17/17). We are pre-launch and considering whether to broaden coverage.

### HARD RULES (non-negotiable — any answer violating these is rejected)
- **Open Food Facts (OFF) is banned forever, every field, no exceptions.** Unknown is acceptable; OFF is not.
- **The ONLY data source is the direct product scrape** (manufacturer/brand site, e-tailer product page, or the physical label) tied to the **exact barcode/product**. Dose+unit must be explicitly stated in such a source or the SKU is unscoreable. No inference, no "typical value," no fabrication.
- **Missing-data discard rule:** if a product's data isn't found with reasonable effort, discard it. Do NOT over-source.

### The 36 unscoreable, by bucket
- **~14 Life (Super-Pharm house brand):** no brand site, no published supplement-facts panel anywhere found.
- **5 "Magnesia" sub-brands (FOCUS/WOMEN/CALM/WINTER/ACTIVE):** no published panel found.
- **~9 acquisition_miss:** a panel likely exists but WebFetch/WebSearch didn't surface it; some Israeli e-tailers are Cloudflare-walled or return 503 in our environment (e.g. vitamins4all).
- **~6 out_of_ontology:** omega-5 (punicic/pomegranate), plant-ALA (chia, clary sage) — genuinely not EPA/DHA omega-3; and decaf coffee (zero caffeine active).

### Evidence base today
Per-active evidence dossiers with claim-tier (Strong/Moderate/Weak/Insufficient) umbrella mappings, currently **cited to EFSA health-claim opinions**. 20 cap_1 E-grades remain because a real on-label claim has no EFSA-cited mapping.

## Questions (answer each briefly)
1. **Acquisition breadth:** Which of the 4 unscoreable buckets are *legitimately recoverable within the hard rules*, and via what **concrete, named source types** (e.g. importer regulatory filing, retailer PDP, JS-rendered scrape of a specific site)? Which should stay discarded per the discard rule?
2. **Research/evidence breadth:** Can the dossier evidence base be responsibly broadened **beyond EFSA** to map more real claims — which **authoritative bodies/sources** (name them), and what is the credibility/consistency risk of mixing them with EFSA tiers?
3. **Tripwires:** Name any source or method that would *violate* the OFF-ban or the direct-scrape rule that we should explicitly rule out before a scale-up.

End with a 3-line bottom-line recommendation: broaden / hold / discard, per the two axes (sources, research).
