# TASK-562 Return Block — Sucralose Dechlorination Research

**Returning agent:** Research Agent (claude-sonnet)  
**Date:** 2026-07-11  
**Proposed status:** RETURNED

---

## Summary of Findings

### Q1 — Israeli Authorisation in Baked Goods
**UNVERIFIED — authoritative source unreachable.** The relevant regulation is תקנות בריאות הציבור (מזון) (תוספי מזון), תשנ"ו-1996 and its amendments. The Israeli MoH website (health.gov.il) has undergone a full migration and all former additive sub-pages (and every URL pattern tried) now redirect to 404/403 pages on the new host. No alternative online source for the current Israeli permitted-additives list was accessible during this session. Label evidence from Israeli-sold products carrying sucralose (two products manufactured by Israeli companies, sold through Shufersal) is circumstantial evidence that it is not prohibited — but is not a regulatory opinion. What cannot be confirmed: whether Israel has adopted any restriction equivalent to EFSA's Feb 2026 category-extension refusal for baked goods.

### Q2 — Bearing on Scored Products
**6 corpus products carry sucralose across both categories (4/167 in cakes_hard_cookies; 2/61 in cookies_coffee).** Of these, 2 are confirmed oven-baked biscuits/cookies (barcode 311463, מן עוגיות חמאה ללת"ס; barcode 960860015432, אביבה עוגיות ללת"ס מקמח מלא) and both are **live and consumer-facing** in cookies_coffee_frontend_v2.json (scores 45.2/D and 46.0/D respectively). The remaining 4 are: 1 ambiguous dairy-dessert with a baked cookie sub-component (5431920, not published in cakes frontend), and 3 cold-formed protein bars (not baked at relevant temperatures, also not published in cakes frontend). The EFSA dechlorination finding directly applies to the 2 published cookie products.

### Q3 — D4/EV Consequence
No score change per efsa_no_scoring_exposure. An evidence registry entry (EV-109) is warranted and has been drafted in the report. The existing E955 additive explanation copy ("dose-dependent, authorised at current levels, research continues") is incomplete in light of EFSA's specific inability to confirm safety in a baked-good application. Flag routed to Nutrition Agent for copy review. No consumer-facing change from this agent.

### EFSA Citation Verification
- PMID 41710869: **VERIFIED** (PubMed direct fetch).
- DOI 10.2903/j.efsa.2026.9854: **REDIRECT CONFIRMED** (doi.org → wiley.com); full text **PAYWALLED** (HTTP 402). The specific temperature values (120–250°C) and compound names (PCDDs, PCDFs) in the full paper are UNVERIFIED-DETAIL — the mechanism and the conclusion (extension declined, chlorinated compound concern) are confirmed from the PubMed abstract.

---

## Return Contract

```json
{
  "task": "TASK-562",
  "proposed_status": "RETURNED",
  "artifacts": [
    {
      "path": "03_operations/reports/research/task562_sucralose_dechlorination_v1.md",
      "action": "created",
      "sha256": "704df3151a75f40a247f3113326ee1cb8b98704126180c44e847a2614b8430b6"
    }
  ],
  "counts": {
    "sucralose_products_cakes_corpus": "4/167 (run_cakes_001 BSIP2 traces, Python scan)",
    "sucralose_products_cookies_corpus": "2/61 (run_cookies_001 BSIP2 traces, Python scan)",
    "sucralose_products_cakes_frontend": "0/62 (cakes_hard_cookies_frontend_v1.json, Python scan — cake_2472254 hash false-positive confirmed)",
    "sucralose_products_cookies_frontend": "2/117 (cookies_coffee_frontend_v2.json, Python scan)",
    "confirmed_baked_good_sucralose_products": "2/6 (311463 + 960860015432, both cookies; corpus total = 6)",
    "ambiguous_baked_component_sucralose_products": "1/6 (5431920, baked cookie sub-component 20%; not published)",
    "cold_formed_non_baked_sucralose_products": "3/6 (protein bars: 7290018043134, 7290019766018, 7290117384572; not published in cakes frontend)",
    "live_consumer_facing_sucralose_baked_products": "2/2 (311463, 960860015432 — cookies_coffee page)"
  },
  "commands_run": [
    {
      "cmd": "python -c \"[sucralose pattern scan across run_cakes_001 167 traces]\"",
      "exit_code": 0
    },
    {
      "cmd": "python -c \"[sucralose pattern scan across run_cookies_001 61 traces]\"",
      "exit_code": 0
    },
    {
      "cmd": "python -c \"[sucralose scan in cakes_hard_cookies_frontend_v1.json]\"",
      "exit_code": 0
    },
    {
      "cmd": "python -c \"[sucralose scan in cookies_coffee_frontend_v2.json]\"",
      "exit_code": 0
    },
    {
      "cmd": "WebFetch https://pubmed.ncbi.nlm.nih.gov/41710869/",
      "exit_code": 0
    },
    {
      "cmd": "WebFetch https://pubmed.ncbi.nlm.nih.gov/32278984/",
      "exit_code": 0
    },
    {
      "cmd": "WebFetch https://doi.org/10.2903/j.efsa.2026.9854 [redirect confirmed; full text paywalled]",
      "exit_code": 1
    },
    {
      "cmd": "WebFetch health.gov.il additive pages [multiple URLs, all 404/403]",
      "exit_code": 1
    },
    {
      "cmd": "python -c \"[highest EV number scan across all Bari files]\"",
      "exit_code": 0
    },
    {
      "cmd": "python -c \"[sha256 of report file]\"",
      "exit_code": 0
    }
  ],
  "not_done": [
    "Israeli regulation status: UNVERIFIED — MoH website inaccessible. The תקנות בריאות הציבור (מזון) (תוספי מזון) 1996 and amendment text could not be retrieved online. Direct MoH contact or physical access to the Official Gazette (Reshumot) would be needed.",
    "EFSA full paper specific details (120–250°C temperature range, specific PCDD/PCDF compound names): UNVERIFIED — paywalled at Wiley (HTTP 402). Mechanism confirmed from abstract and supporting literature.",
    "Hellwig 2024 (PMID 39556422) abstract content: UNVERIFIED — PubMed blocked by CAPTCHA on fetch.",
    "EV-109 not registered — draft provided in report for Nutrition Agent decision. Registration is out of scope for Research Agent."
  ],
  "self_check": "Acceptance test: report must answer all 3 questions with source citations, confirmed vs unconfirmed split, and EV draft. Observed: Q1 answered — UNVERIFIED with full explanation of why and what regulation is relevant; Q2 answered — 6 products identified with full barcode/name/category/baking-status table, 2 confirmed baked goods in live frontend; Q3 answered — no score change recommended (efsa_no_scoring_exposure), EV-109 draft provided, Nutrition Agent escalation noted. All identifiers verified or marked UNVERIFIED. No OFF used. No scores changed. No consumer copy modified."
}
```
