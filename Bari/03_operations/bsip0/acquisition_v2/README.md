# BSIP0 Acquisition Infrastructure v2

Browser automation layer for Israeli retailer bread/cracker product acquisition.

## Overview

Static HTTP scraping failed for all Israeli retailers (real_bread_retail_002 audit).
This infrastructure uses Playwright headless browser to:
- Handle JavaScript-rendered SPAs (Victory/AngularJS)
- Handle cookie/consent/popup flows (Carrefour)
- Navigate category pages and capture dynamic XHR product APIs (Wolt Market)
- Retry with session persistence (Shufersal post-maintenance)

## Files

| File | Purpose |
|:-----|:--------|
| `browser_session.py` | Playwright session manager — persistent context, network capture, popup dismissal, screenshots |
| `retailer_base.py` | `RetailSource` abstract base + `RawProduct` + `RetailProbeResult` data classes |
| `shufersal_probe.py` | Shufersal OCC API (with maintenance check) |
| `victory_probe.py` | Victory AngularJS — browser render + DOM extraction + XHR capture |
| `carrefour_probe.py` | Carrefour Israel — browser session with consent flow + network capture |
| `wolt_probe.py` | Wolt Market — browser navigation through bread categories + XHR capture |
| `acquisition_audit_v2.py` | Orchestrator — runs probes, applies gate, writes 9 reports |

## Usage

```bash
# Run all probes
python acquisition_audit_v2.py

# Run specific retailers
python acquisition_audit_v2.py --retailers shufersal,victory

# Skip browser probes (static HTTP only)
python acquisition_audit_v2.py --skip-browser
```

## Acceptance Gate

Gate passes when ALL of:
- ≥20 real retailer products extracted
- ≥70% have nutrition table data
- ≥40% have ingredient text
- ≥1 real retailer source (not OFF)

**If gate fails: do NOT proceed to BSIP1/BSIP2.**

## Output (→ C:\Bari\02_products\bread_retail_002\)

| File | Contents |
|:-----|:---------|
| `bsip0_acquisition_v2_audit.md` | Full audit: gate result, per-retailer findings, products table |
| `retailer_access_matrix_v2.md` | Compact access matrix |
| `session_state_inventory.md` | Cookie/session state per retailer |
| `shufersal_probe_report.md` | Shufersal detailed report |
| `victory_probe_report.md` | Victory detailed report |
| `carrefour_probe_report.md` | Carrefour detailed report |
| `wolt_probe_report.md` | Wolt Market detailed report |
| `discovered_api_endpoints.json` | All captured XHR/API calls with response previews |
| `bsip0_source_manifest_v2.json` | Gate result + retailer summary + full product list |
| `{RUN_ID}_bsip0_raw.json` | Raw products (written only if gate passes) |

## Session Persistence

Persistent Playwright contexts are stored in `sessions/{retailer_id}/`.
If a retailer requires manual login:
1. Copy session cookies from your browser (Edit This Cookie extension works)
2. Place `cookies.json` in `sessions/{retailer_id}/`
3. Re-run the probe — it will pick up the session

## Screenshot Evidence

All failure states are captured to `screenshots/failure_states/`.
Format: `{retailer_id}_{label}_{timestamp}.png`

## Data Integrity Rules

- Every product has `source_url` and `scraped_at`
- Raw source JSON is preserved in `raw_source_json` field
- No synthetic products, no OFF as primary corpus
- Gate must pass before any BSIP1/BSIP2 run
