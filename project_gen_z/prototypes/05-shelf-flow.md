# P1-07 — Shelf flow (prototype)

**Status:** Theoretical — defines future app infrastructure

## Intent

Category → pick on shelf → ranked list. In-store journey without barcode v1.

## Steps

1. Category grid (hashvaot)
2. Shelf picker (P1-03 cards)
3. My shelf — sorted by score
4. Drill-down → expansion

## Infrastructure contracts

- productId: stable BSIP id
- categorySlug: route + corpus key
- sort: score | name (filter only)
- card VM: P1-03 shape

## Not v1

Barcode, cross-category shelf, cart health score, accounts (localStorage ok for mock)
