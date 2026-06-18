# P207 — TASK-327 palm-hydro aliases, flag-gated default-OFF (route: C1-GEMINI)
# Data Agent build — engine detection change, reversible, score-neutral when OFF

**Repo:** `C:\Bari`
**Task to read:** `C:\Bari\tasks\TASK-327.md`
**ONLY file you may edit:** `03_operations/bsip2/proto_v0/src/signal_extractor.py`
(Do NOT touch score_engine.py, constants.py, nova_proxy.py, any `configs/*.json`, or anything under `bari-web/`.)

## Objective
Make hardened palm oil (`שמן דקל מוקשה`) detectable as a **generic** hardened fat, behind a NEW env flag so the
committed engine is **byte-identical until the flag is set**. The spine will flip the flag via env as a what-if.

## Exact change
1. Add a module-level flag next to the other `BARI_*` flags:
   `PALM_HYDRO_V1_ON = os.environ.get("BARI_PALM_HYDRO_V1", "off").lower() == "on"`
2. The EV-097 marker lists `_PHVO_PARTIAL_MARKERS` / `_PHVO_GENERIC_MARKERS` are in `extract_signals` (~line 1175).
   Do **not** mutate the base lists. Instead build an *effective* generic list at use-time:
   when `PALM_HYDRO_V1_ON`, append these palm-hardened aliases to the GENERIC tier only:
   `שמן דקל מוקשה`, `שמן דקלים מוקשה`, `שומן דקל מוקשה`.
   Leave the PARTIAL tier unchanged (hardened palm is NOT a confirmed-trans/PHO signal — it gets the generic
   ceiling 55, never the partial ceiling 40). Preserve the existing position gate (≤8).
3. Add a short evidence comment: EV-097 lineage + research/16.08 (FDA 2015 PHO non-GRAS; Bonanome–Grundy NEJM
   1988 stearic acid → fully-hydrogenated ≠ trans severity). Note this resolves the open "generic hardened-fat
   ceiling" delta conservatively.

## Hard guards
- **Flag default OFF ⇒ behaviour byte-identical to baseline.** The base `_PHVO_GENERIC_MARKERS` content and all
  other outputs must be unchanged when `BARI_PALM_HYDRO_V1` is unset/off.
- **No scoring-path edit.** You only add detection strings + a flag; you do not touch any score/constant/config.
- OFF-ban absolute: do not read or reference Open Food Facts anywhere.

## Acceptance test (run it, put the result in self_check)
Pick one cake product whose ingredient text contains `שמן דקל מוקשה` and one that does not.
- With `BARI_PALM_HYDRO_V1` unset: `has_phvo_generic` is unchanged from baseline for both.
- With `BARI_PALM_HYDRO_V1=on`: `has_phvo_generic=True` ONLY for the `שמן דקל מוקשה` product; the plain-palm
  product still does NOT fire. Show the two boolean pairs (OFF vs ON) for both products with the deriving command.
- Confirm `git diff --stat` touches ONLY `signal_extractor.py`.

## Return
RETURNED proposal + return-contract JSON (`01_framework/operations/return_contract_v1.md`).
**Do not close. Do not commit or push.** Propose RETURNED for orchestrator verification.
