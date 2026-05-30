# BSIP0 Framework

**Maturity:** Early / Not yet written  
**Status:** Placeholder — implementation is ahead of documentation

BSIP0 is the data extraction layer. It is responsible for acquiring raw product data from two sources:
- Web scraping (retailer product pages)
- OCR/image extraction (nutrition label photographs)

## What belongs here

Design documents that describe how BSIP0 extraction should work — independent of any specific scraper implementation:

- Product identification and barcode schema
- Retailer capability specification format
- Field extraction standards (which fields to extract, in what format, with what confidence)
- Quality assessment framework for raw OCR/scrape data
- Handoff schema to BSIP1 (what BSIP0 guarantees to deliver)

## What does NOT belong here

Scraper code, run outputs, cached responses — those live in `03_operations\bsip0\`.

## Current state

The operational implementation is ahead of the documentation:
- Web scraper for Carrefour (v0.2, frozen) and Yohananof (active) exist in `03_operations\bsip0\scrape\`
- OCR pipeline prototype exists in `03_operations\bsip0\pipeline\`
- No formal design documents have been written for BSIP0 yet

## Priority documentation to write

1. Product ID convention — stable barcode-anchored IDs across retailers
2. BSIP0 handoff schema — what a valid BSIP0 output JSON looks like
3. Retailer capability spec format — generalization of `carrefour.yaml`
4. Field confidence taxonomy — how to signal extraction quality to BSIP1
