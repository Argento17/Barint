# Orphaned comparison datasets — archived 2026-06-02

Moved out of `bari-web/src/data/comparisons/` per `category_module_contract_v1.md` §4.3
(superseded dataset versions imported by no live route must be relocated once their
successor has been LIVE for one green build). Confirmed via repo-wide grep that **no
`.ts`/`.tsx` route imports any of these files** at archive time.

| File | Superseded by (LIVE) | Notes |
|------|----------------------|-------|
| `hummus_frontend_v1.json` | `hummus_frontend_v3.json` | v1 → v2 (insight integration) → v3 (explanation layer). |
| `hummus_frontend_v2.json` | `hummus_frontend_v3.json` | intermediate insight-integrated version. |
| `yogurts_frontend_v1.json` | `yogurts_frontend_v2.json` | v1 = 13/14-product manual MVP corpus (DEC-005), retired by run_yogurt_004. |

History preserved via `git mv`. Safe to delete once no longer needed for reference.

Note: `bari-web/scripts/generate-yogurts-corpus.mjs` still writes `yogurts_frontend_v1.json`
to the live dir — it is a stale MVP generator (v1-mvp-manual) and is no longer part of the
live pipeline. Flagged, not modified (out of scope for this hygiene pass).
