# P206 — TASK-327 palm-hydro severity + first-flip red-team (route: C3)
# ChatGPT challenge — advice only, never closes, never builds

**Repo:** `C:\Bari`
**Task to read:** `C:\Bari\tasks\TASK-327.md`
**Engine context:** `03_operations/bsip2/proto_v0/src/signal_extractor.py` lines ~1157-1208 (EV-097 PHVO two-tier:
`_PHVO_PARTIAL_MARKERS` → ceiling 40 / true industrial-trans; `_PHVO_GENERIC_MARKERS` → ceiling 55 /
fully-hydrogenated·interesterified·margarine).
**Evidence on file:** `research/16.08/` (FDA 2015 PHO non-GRAS; EFSA TFA opinion; Bonanome–Grundy NEJM 1988
stearic acid; Sundram 2007 interesterified fat).

## The fork (why C3 is mandatory here)
We intend, as the spine's FIRST live flip, to make `שמן דקל מוקשה` (hardened palm oil) detectable by adding it
to the **EXISTING generic PHVO tier (ceiling 55), NOT the partial/trans tier (40).** This is a
scoring-philosophy / precedent fork: it sets how Bari treats "hardened tropical fat" severity for every future
category.

## What we need from you (challenge, do not build)
1. **Severity placement.** Is routing unspecified `מוקשה`/hardened palm to the GENERIC tier (moderate, ceiling 55)
   — and requiring an explicit `חלקית`/"partial" cue for the PHO/trans tier — defensible against the cited
   evidence? Or is hardened palm severe enough (high-SFA palmitic load) to deserve more than the generic tier?
2. **First-flip choice.** Is palm-hydro on **cakes** the right lowest-risk first exercise of the spine, or is a
   different signal a cleaner smoke test? Name the risk you'd most want watched.
3. **False-positive / scope traps.** Where could `דקל מוקשה` aliasing over- or under-fire (e.g. plain palm
   `שמן דקל` with no `מוקשה`; `עמילן מוקשה` modified-starch collision; bread/butter spillover)?
4. **Blind spots** in our plan you'd flag before we flip.

## Boundaries
- Advice only. Do not edit files, do not propose closing anything. OFF-ban absolute (never cite Open Food Facts).
- Ground every claim in the cited regulators/PMIDs or say "no source."

## Return format
Prose verdict per question 1–4, each with an evidence pointer, then the return-contract JSON
(`01_framework/operations/return_contract_v1.md`). **Do not close — this is a consult; propose nothing as CLOSED.**
