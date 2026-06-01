# BSIP1 Framework

**Maturity:** Partial — trust layer design documented in memory; implementation exists; formal design docs not yet written here  
**Status:** Placeholder — trust scoring logic is implemented; architecture docs to be migrated here

BSIP1 is the cross-retailer consolidation layer. It is responsible for:
- Merging product observations from multiple retailers into a canonical record
- Scoring observation quality (trust layer)
- Producing the canonical product JSON that BSIP2 scores

BSIP1 does NOT score nutritional quality. It consolidates and validates what BSIP0 collected.

## What belongs here

- Canonical product schema (the BSIP1 output format)
- Trust layer design: observation quality signals, weight constants, scoring formula
- Conflict resolution logic: how disagreements between retailers are resolved
- Cross-retailer deduplication strategy (barcode → canonical product identity)
- Handoff contract to BSIP2 (what fields BSIP2 can rely on)

## What does NOT belong here

Batch run scripts and outputs — those live in `03_operations\bsip1\`.

## Current implementation state

- `03_operations\bsip1\run_001\` contains the first batch run: 53 products consolidated, trust-scored
- Trust scoring uses observation quality + canonical trust score; weight constants are in `core/trust.py`
- Dataset: 53 snack bar products from Yohananof

## Priority documentation to write

1. Canonical product schema spec (field definitions, types, optionality)
2. Trust layer design document (the formula, the weight constants, the rationale)
3. Conflict resolution rules (which retailer wins for which fields under what conditions)
4. BSIP1 → BSIP2 handoff contract
